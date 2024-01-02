import json

from fastapi import FastAPI

from src.orders.router import router as router_orders
from src.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_orders)
