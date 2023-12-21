from fastapi import FastAPI

from src.users.router import router as router_users
from src.orders.router import router as router_orders
app = FastAPI()

app.include_router(router_users)
app.include_router(router_orders)
