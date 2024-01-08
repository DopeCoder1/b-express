from fastapi import FastAPI
from sqlalchemy import select
from starlette.middleware.cors import CORSMiddleware

from src.clients.sendgrid import mail_client
from src.common.models import SendEmail
from src.config import settings
from src.database import async_session
from src.directions.router import router as directions_router
from src.geography.router import router as router_geography
from src.geography.utils import init_data
from src.orders.models import OrderStatus
from src.orders.router import router as router_orders
from src.users.models import Group, Permission
from src.users.router import router as router_users
from src.users.schemas import PERMISSIONS_MAP
from src.warehouse.router import router as router_warehouse

app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users)
app.include_router(router_orders)
app.include_router(router_geography)
app.include_router(router_warehouse)
app.include_router(directions_router)


@app.on_event('startup')
async def startup_event_setup():
    await init_data()


@app.post("/api/v1/send-email", tags=["email"])
async def send_email(send_email: SendEmail):
    return mail_client.send(send_email)


@app.get("/api/v1/statuses", tags=["health"])
async def get_statuses():
    return [status.value for status in OrderStatus]


@app.on_event("startup")
async def create_groups_and_permissions() -> None:
    print("Creating groups and permissions")
    session = async_session()
    for group in PERMISSIONS_MAP:
        if (await session.execute(select(Group).where(Group.name == group["group_name"]))).scalar_one_or_none():
            continue
        group_name = group["group_name"]
        permissions = group["permissions"]
        group = Group(name=group_name)
        session.add(group)
        for permission in permissions:
            if (await session.execute(
                    select(Permission).where(Permission.codename == permission["codename"]))).scalar_one_or_none():
                continue
            permission = Permission(name=permission["name"], codename=permission["codename"],
                                    group_id=group.id)
            session.add(permission)
    await session.commit()
