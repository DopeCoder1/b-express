from fastapi import APIRouter, Depends, status

from src.users.auth import JWTBearer
from src.users.schemas import (Token, UserConfirmationEmailSchemas,
                               UserCreateSchemas, UserSchemas, UserViewSchemas)
from src.users.service import user_service

router = APIRouter(
    tags=["User"]
)


@router.post("/register/admin", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def register(payload: UserSchemas):
    return await user_service.register_admin(payload)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(payload: UserSchemas):
    return await user_service.login_admin(payload)


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=UserViewSchemas, status_code=status.HTTP_200_OK)
async def me(user: str = Depends(JWTBearer())):
    return user


@router.post("/create/superuser", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_superuser(email: str, password: str):
    return await user_service.create_superuser(email, password)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_user(payload: UserCreateSchemas):
    return await user_service.create_user(payload)

@router.post("/users/email-confirmation", status_code=status.HTTP_201_CREATED, response_model=Token)
async def confirm_email(payload: UserConfirmationEmailSchemas):
    return await user_service.confirm_email(payload)
