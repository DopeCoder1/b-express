from fastapi import APIRouter, HTTPException, status, Depends
from src.users.schemas import UserSchemas, Token, UserViewSchemas
from src.users.models import Users
from src.users.service import user_service
from src.users.auth import JWTBearer
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src.users.service import UserService

router = APIRouter(
    tags=["User"]
)

@router.post("/register/admin",status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def register(payload: UserSchemas):
    return await user_service.register_admin(payload)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(payload: UserSchemas):
    return await user_service.login_admin(payload)

@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=UserViewSchemas, status_code=status.HTTP_200_OK)
async def me(user: str = Depends(JWTBearer())):
    return user

@router.post("/create/superuser", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_superuser(email:str, password:str):
    return await user_service.create_superuser(email, password)

@router.post("/create/group", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
