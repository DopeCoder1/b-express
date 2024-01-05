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


@router.post("/register/admin", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def register(payload: UserSchemas):
    return await user_service.register_admin(payload)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(payload: UserSchemas):
    return await user_service.login_admin(payload)


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=UserViewSchemas, status_code=status.HTTP_200_OK)
async def me(user: str = Depends(JWTBearer())):
    return await user_service.me(user)


@router.post("/create/superuser", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_superuser(email: str, password: str):
    return await user_service.create_superuser(email, password)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_user(payload: UserCreateSchemas):
    return await user_service.create_user(payload)


@router.post("/create/users/deliver", status_code=status.HTTP_201_CREATED, response_model=UserViewSchemas)
async def create_user(payload: UserSchemas):
    return await user_service.register_deliver(payload)


@router.post("/users/email-confirmation", status_code=status.HTTP_201_CREATED, response_model=Token)
async def confirm_email(payload: UserConfirmationEmailSchemas):
    return await user_service.confirm_email(payload)


@router.get("/get/group", status_code=status.HTTP_200_OK, response_model=list[GroupViewSchemas])
async def get_group():
    return await group_service.all()


@router.post("/create/group", status_code=status.HTTP_201_CREATED, response_model=GroupViewSchemas)
async def create_group(payload: GroupCreateSchemas):
    return await group_service.create(payload)


@router.get("/get/permission", status_code=status.HTTP_200_OK, response_model=list[PermissionViewSchemas])
async def get_permission():
    return await permission_service.get()


@router.post("/create/permission", status_code=status.HTTP_201_CREATED, response_model=PermissionViewSchemas)
async def create_permission(payload: PermissionCreateSchemas):
    return await permission_service.create(payload)


@router.post("/create/group_permission", status_code=status.HTTP_201_CREATED, response_model=AuthGroupPermissionViewSchemas)
async def create_group_permission(paylaod: AuthGroupPermissionCreateSchemas):
    return await group_permission.create(paylaod)


@router.get("/get/group_permission", status_code=status.HTTP_200_OK, response_model=list[AuthGroupPermissionViewSchemas])
async def get_group_permission():
    return await group_permission.get()


@router.get("/check")
async def check(user: Users = Depends(func_user_has_permissions(['string2']))):
    return {"detail": "OK"}
