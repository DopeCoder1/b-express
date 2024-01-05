from fastapi import APIRouter, Depends, status

from src.directions.schemas import DirectionCreateSchemas, DirectionViewSchemas
from src.directions.service import direction_service
from src.users.auth import JWTBearer

router = APIRouter(
    tags=["Directions"]
)


@router.post("/directions", status_code=status.HTTP_201_CREATED, response_model=DirectionViewSchemas)
async def create_direction(payload: DirectionCreateSchemas, user: str = Depends(JWTBearer())):
    return await direction_service.create_direction(payload, user)


@router.get("/directions", dependencies=[Depends(JWTBearer())], response_model=list[DirectionViewSchemas], status_code=status.HTTP_200_OK)
async def get_directions(user: str = Depends(JWTBearer())):
    return await direction_service.get_directions(user=user)


@router.get("/directions/{id}", dependencies=[Depends(JWTBearer())], response_model=DirectionViewSchemas, status_code=status.HTTP_200_OK)
async def get_direction(id: int, user: str = Depends(JWTBearer())):
    return await direction_service.get_direction(id, user)
