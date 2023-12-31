import random

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.clients.sendgrid import mail_client
from src.common.models import SendEmail
from src.config import settings
from src.dao.base import BaseDao
from src.database import async_session
from src.exceptions import NotUnique
from src.geography.models import City
from src.geography.schemas import CityOut
from src.users.auth import (create_access_token, get_password_hash,
                            verify_password)
from src.users.exceptions import EmailNotFound, EmailTaken, InvalidCredentials
from src.users.models import (EmailCode, Group, Permission, Users,
                              auth_group_permission)
from src.users.schemas import (AuthGroupPermissionCreateSchemas,
                               GroupCreateSchemas, GroupViewSchemas,
                               PermissionCreateSchemas, Token,
                               UserConfirmationEmailSchemas, UserCreateSchemas,
                               UserSchemas, UserViewSchemas)


class EmailCodeService(BaseDao):
    class_name = EmailCode

    def code_generator(self):
        code = random.randint(1000, 9999)
        return code

    async def create_code(self, user_id: int, email: str):
        return await self.add({
            "email": email,
            "user_id": user_id,
            "code": str(self.code_generator())
        })


class GroupService(BaseDao):
    class_name = Group

    async def create(self, paylaod: GroupCreateSchemas) -> dict:
        return await GroupService.add({"name": paylaod.name})

    async def get(slef) -> list[dict]:
        return await GroupService.get()


class PermissionService(BaseDao):
    class_name = Permission

    async def create(self, payload: PermissionCreateSchemas) -> dict:
        return await PermissionService.add({"name": payload.name, "codename": payload.codename})

    async def get(self) -> list[dict]:
        return await PermissionService.all()


class AuthGroupPermissionService(BaseDao):
    class_name = auth_group_permission

    async def create(self, paylaod: AuthGroupPermissionCreateSchemas) -> dict:
        async with async_session() as session:
            try:
                query = auth_group_permission.insert().values(
                    group_id=paylaod.group_id, codename=paylaod.codename).returning(
                        auth_group_permission.c.id,
                        auth_group_permission.c.group_id,
                        auth_group_permission.c.codename
                )
                data = await session.execute(query)
                inserted_data = data.first()
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise NotUnique()
            return inserted_data

    async def get(self) -> list[dict]:
        async with async_session() as session:
            query = select(auth_group_permission)
            result = await session.execute(query)
            return result


class UserService(BaseDao):
    class_name = Users

    def password_generator(self) -> str:
        password = ''.join((random.choice(
            '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8)))
        return password

    async def create_user(self, payload: UserCreateSchemas, creator: UserViewSchemas):
        user = await UserService.find_one_or_none({"email": payload.email})
        if user:
            raise EmailTaken()
        password = self.password_generator()
        hashed_password = await get_password_hash(password=password)
        session = async_session()
        group = await session.execute(select(Group).where(Group.id == payload.group_id))
        city = await session.execute(select(City).where(City.id == payload.city_id))
        user = Users(email=payload.email, hashed_password=hashed_password,
                     city=city.scalars().first().id, group_id=group.scalars().first().id)
        session.add(user)
        await session.commit()
        url = f"{settings.FRONTEND_URL}"
        send_mail = SendEmail(
            email=payload.email,
            subject="Войдите в аккаунт B-Express",
            message=f"Ваш пароль: {password} \n Ссылка для входа: {url}"
        )
        mail_client.send(send_mail)
        user_view = UserViewSchemas(id=user.id, email=user.email, is_active=user.is_active,
                                    is_superuser=user.is_superuser, is_delete=user.is_delete, group_id=user.group_id, city_id=user.city, creator=creator.id)
        if settings.ENVIRONMENT.is_debug:
            user_view.confirmation_link = password
        return user_view

    async def me(self, user: UserViewSchemas) -> UserViewSchemas:
        user_db: Users = await UserService.find_one_or_none({"id": user.id})
        group = await group_service.find_one_or_none({"id": user_db.group_id})
        user.group = GroupViewSchemas(id=group.id, name=group.name)
        if user.city:
            async with async_session() as session:
                group = await session.execute(select(City).where(City.id == user_db.city))
                city = group.scalars().first()
                user.city = CityOut(id=city.id, name=city.name)
        return user

    async def get_users(self) -> list[UserViewSchemas]:
        users = await UserService.all()
        users_view = []
        for user in users:
            group = await group_service.find_one_or_none({"id": user.group_id})
            user_view = UserViewSchemas(
                id=user.id, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser, is_delete=user.is_delete, group_id=user.group_id)
            user_view.group = GroupViewSchemas(id=group.id, name=group.name)
            users_view.append(user_view)
        return users_view

    async def login_admin(self, payload: UserSchemas) -> dict:
        user = await UserService.find_one_or_none({"email": payload.email})
        if not user:
            raise EmailNotFound()
        if not await verify_password(plain_password=payload.password, hashed_password=user.hashed_password):
            raise InvalidCredentials()
        access_token = await create_access_token({"user_id": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")

    async def create_superuser(self, email: str, password: str):
        hashed_password = await get_password_hash(password=password)
        user = await UserService.find_one_or_none({"email": email})
        if user:
            print("Email already exists")
            raise EmailTaken()
        group = await group_service.find_one_or_none({"name": "SUPER_ADMIN"})
        return await UserService.add({"email": email, "hashed_password": hashed_password, "is_superuser": True, "group_id": group.id})

    async def confirm_email(self, payload: UserConfirmationEmailSchemas) -> Token:
        code: EmailCode = await email_service.find_one_or_none({"code": payload.code, "user_id": payload.user_id})
        if not code:
            raise EmailNotFound()
        user: Users = await UserService.find_one_or_none({"id": payload.user_id})
        if not user:
            raise EmailNotFound()
        user.is_active = True
        hashed_password = await get_password_hash(password=payload.password)
        user.hashed_password = hashed_password
        access_token = await create_access_token({"user_id": str(user.id)})
        await UserService.update(id=user.id, data=user.to_dict())
        return Token(access_token=access_token, token_type="bearer")


user_service = UserService()
group_service = GroupService()
permission_service = PermissionService()
email_service = EmailCodeService()
group_permission = AuthGroupPermissionService()
