from src.database import async_session_maker
from sqlalchemy import select,insert
from fastapi import status, HTTPException
from typing import Any, Type

class BaseDao:
    class_name = None
    
    @classmethod
    async def find_by_id(cls, id:int):
        async with async_session_maker() as session:
            query = select(cls.class_name).filter_by(id=id)
            data = await session.execute(query)
            resp = data.scalar_one_or_none()
            return resp
    
    @classmethod
    async def find_one_or_none(cls, filter):
        async with async_session_maker() as session:
            query = select(cls.class_name).filter_by(**filter)
            data = await session.execute(query)
            resp = data.scalar_one_or_none()
            return resp
        
    @classmethod
    async def find_all(cls, filter):
        async with async_session_maker() as session:
            query = select(cls.class_name).filter_by(**filter)
            data = await session.execute(query)
            resp = data.scalars().all()
            return resp
            
    @classmethod
    async def add(cls, data: Any):
        async with async_session_maker() as session:
            data = cls.class_name(**data)
            session.add(data)
            await session.commit()
            await session.refresh(data)
            return data
        

    @classmethod
    async def delete(cls, filter):
        async with async_session_maker() as session:
            query = select(cls.class_name).filter_by(**filter)
            data = await session.execute(query)
            resp = data.scalar_one_or_none()
            if not resp:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.class_name.__name__} not found")
            await session.delete(resp)
            await session.commit()





    