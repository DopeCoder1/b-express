from src.dao.base import BaseDao
from src.geography.models import City
from src.geography.schemas import GeographyCreateSchemas


class GeographyService(BaseDao):
    class_name = City

    async def create(self, payload: GeographyCreateSchemas) -> dict:
        return await GeographyService.add({"name": payload.name})

    async def create_with_list(self, payload: list):
        return await GeographyService.add_all(payload)

    async def get(self):
        return await GeographyService.all()


geography_service = GeographyService()
