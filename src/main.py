import json

from fastapi import FastAPI

from src.orders.router import router as router_orders
from src.users.models import Permissions, Users
from src.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_orders)


@app.on_event("startup")
async def create_warehouses():

    from src.database import SessionLocal
    from src.warehouse.models import Warehouse
    with open('geography/cities.json') as f:
        cities = json.load(f)
    session = SessionLocal()
    for city in cities:
        session.add(Warehouse(address=city['address'], name=city['name'], city=city['city']))
    session.commit()
    session.close()
  



@app.on_event("startup")
async def create_permissions():
    from src.database import SessionLocal
    from src.users.models import Permissions
    session = SessionLocal()
    with open('users/permissions.json') as f:
        users = json.load(f)
    session = SessionLocal()
    for user in users:
        session.add(Permissions(code=user['code']))
    session.close()
