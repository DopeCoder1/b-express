import json
import os

from src.geography.exceptions import JsonNotFound
from src.geography.models import City
from src.geography.service import GeographyService, geography_service


async def init_data():
    file_path = "src/geography/cities.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            cities_data = json.load(file)
        data = await geography_service.get()
        existing_city_names = set([city.name.lower() for city in data])
        unique_cities = set([city_data["city"]
                             for city_data in cities_data])
        new_cities_to_create = []

        for city_data in unique_cities:
            city_name = city_data
            if city_name.lower() not in existing_city_names:
                new_cities_to_create.append(City(name=city_name))

        if new_cities_to_create:
            await geography_service.create_with_list(new_cities_to_create)
    else:
        print("File not found")
        raise JsonNotFound()
