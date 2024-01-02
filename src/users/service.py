from src.clients.sendgrid import mail_client
from src.common.models import SendEmail
from src.config import settings
from src.dao.base import BaseDao
from src.email.service import email_service
from src.users.auth import (create_access_token, get_password_hash,
                            verify_password)
from src.users.exceptions import EmailNotFound, EmailTaken, InvalidCredentials
from src.users.models import EmailCode, Users
from src.users.schemas import (Token, UserConfirmationEmailSchemas,
                               UserCreateSchemas, UserSchemas, UserViewSchemas)


class UserService(BaseDao):
    class_name = Users

    async def register_admin(self, payload: UserSchemas) -> dict:
        user = await UserService.find_one_or_none({"email": payload.email})
        if user:
            raise EmailTaken()
        hashed_password = await get_password_hash(password=payload.password)
        return await self.add({"email": payload.email, "hashed_password": hashed_password})

    async def create_user(self, payload: UserCreateSchemas):
        user = await UserService.find_one_or_none({"email": payload.email})
        if user:
            raise EmailTaken()
        user: Users = await self.add({"email": payload.email})
        code: EmailCode = await email_service.create_code(user_id=user.id, email=payload.email)
        url = f"{settings.FRONTEND_URL}/users/confirm?code={code.code}&user_id={user.id}"
        send_mail = SendEmail(email=payload.email, subject="Подтверждение почты",
                              message=f"Перейдите по ссылке для подтверждения почты: {url}")
        mail_client.send(send_mail)
        user_view = UserViewSchemas(
            id=user.id, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser, is_delete=user.is_delete, group_id=user.group_id)
        if settings.ENVIRONMENT.is_debug:
            user_view.confirmation_link = url
        return user_view

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
        return await UserService.add({"email": email, "hashed_password": hashed_password, "is_superuser": True})

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
