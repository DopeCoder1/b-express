from fastapi import Depends, HTTPException
from src.users.models import Users, auth_group_permission
from typing import Callable, List
from src.users.auth import JWTBearer
from sqlalchemy import select
from src.database import async_session_maker


def func_user_has_permissions(need_permissions: List[str] = None) -> Callable:
    """
    Dependency for generating authority authentication
    """

    async def user_has_permission(user: Users = Depends(JWTBearer())) -> Users:
        """
                 Is there a permission
        """
        if user.is_superuser:
            return user
        if not need_permissions:
            return user
        async with async_session_maker() as session:
            for need_permission in need_permissions:
                query = select([auth_group_permission]).where(auth_group_permission.c.group_id == user.group_id).where(
                    auth_group_permission.c.codename == need_permission)
                res = await session.fetch_all(query)
                if not res:
                    raise HTTPException(status_code=403, detail="Permission denied")
            return user

    return user_has_permission