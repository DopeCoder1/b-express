from fastapi import APIRouter, Depends, status

from src.users.auth import JWTBearer
from src.users.models import Users
from src.users.schemas import (AuthGroupPermissionCreateSchemas,
                               AuthGroupPermissionViewSchemas,
                               GroupCreateSchemas, GroupViewSchemas,
                               PermissionCreateSchemas, PermissionViewSchemas,
                               Token, UserConfirmationEmailSchemas,
                               UserCreateSchemas, UserSchemas, UserViewSchemas)
from src.users.service import (group_permission, group_service,
                               permission_service, user_service)
from src.users.utils import func_user_has_permissions

router = APIRouter(
    tags=["User"]
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(payload: UserSchemas):
    return await user_service.login_admin(payload)


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=UserViewSchemas, status_code=status.HTTP_200_OK)
async def me(user: str = Depends(JWTBearer())):
    return await user_service.me(user)


@router.post("/superusers", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_superuser(email: str, password: str):
    return await user_service.create_superuser(email, password)


@router.get("/users", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, response_model=list[UserViewSchemas])
async def get_users():
    return await user_service.get_users()


@router.post("/users", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, response_model=UserCreateSchemas)
async def create_user(payload: UserCreateSchemas, user: str = Depends(JWTBearer())):
    return await user_service.create_user(payload, user)


@router.post("/users/email-confirmation", status_code=status.HTTP_201_CREATED, response_model=Token)
async def confirm_email(payload: UserConfirmationEmailSchemas):
    return await user_service.confirm_email(payload)


@router.get("/groups", status_code=status.HTTP_200_OK, response_model=list[GroupViewSchemas])
async def get_groups():
    return await group_service.all()


@router.post("/groups", status_code=status.HTTP_201_CREATED, response_model=GroupViewSchemas)
async def create_group(payload: GroupCreateSchemas):
    return await group_service.create(payload)


@router.get("/permissions", status_code=status.HTTP_200_OK, response_model=list[PermissionViewSchemas])
async def get_permissions():
    return await permission_service.get()


@router.post("/permissions", status_code=status.HTTP_201_CREATED, response_model=PermissionViewSchemas)
async def create_permission(payload: PermissionCreateSchemas):
    return await permission_service.create(payload)


@router.post("/group_permissions", status_code=status.HTTP_201_CREATED, response_model=AuthGroupPermissionViewSchemas)
async def create_group_permission(paylaod: AuthGroupPermissionCreateSchemas):
    return await group_permission.create(paylaod)


@router.get("/group_permissions", status_code=status.HTTP_200_OK, response_model=list[AuthGroupPermissionViewSchemas])
async def get_group_permissions():
    return await group_permission.get()


@router.get("/check")
async def check(user: Users = Depends(func_user_has_permissions(['string2']))):
    return {"detail": "OK"}
