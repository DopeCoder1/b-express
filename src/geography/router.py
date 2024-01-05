from fastapi import APIRouter, status

from src.geography.schemas import GeographyViewSchemas
from src.geography.service import geography_service

router = APIRouter(
    tags=["Geography"]
)


@router.get("/city", status_code=status.HTTP_200_OK, response_model=list[GeographyViewSchemas])
async def get_city():
    return await geography_service.get()
