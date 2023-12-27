from src.dao.base import BaseDao
from src.users.auth import (create_access_token, get_password_hash,
                            verify_password)
from src.users.exceptions import EmailNotFound, EmailTaken, InvalidCredentials
from src.users.models import Users
from src.users.schemas import (Token, UserCreateSchemas, UserSchemas,
                               UserViewSchemas)


class UserService(BaseDao):
    class_name = Users
    
    async def register_admin(self, payload: UserSchemas)-> dict:
        user = await UserService.find_one_or_none({"email": payload.email})
        if user:
            raise EmailTaken()
        hashed_password = await get_password_hash(password=payload.password)
        return await UserService.add({"email":payload.email, "hashed_password": hashed_password})
    
    async def create_user(self, payload: UserCreateSchemas)-> dict:
        user = await UserService.find_one_or_none({"email": payload.email})
        if user:
            raise EmailTaken()
        # send email
        
        return await UserService.add({"email":payload.email})
    
    async def login_admin(self, payload: UserSchemas)-> dict:
        user = await UserService.find_one_or_none({"email": payload.email})
        if not user:
            raise EmailNotFound()
        if not await verify_password(plain_password=payload.password, hashed_password=user.hashed_password):
            raise InvalidCredentials()
        access_token = await create_access_token({"user_id": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")

    async def create_superuser(self, email:str, password:str):
        hashed_password = await get_password_hash(password=password)
        user = await UserService.find_one_or_none({"email": email})
        if user:
            print("Email already exists")
            raise EmailTaken()
        return await UserService.add({"email": email, "hashed_password": hashed_password, "is_superuser": True})

user_service = UserService()