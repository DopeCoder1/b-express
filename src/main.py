from fastapi import BackgroundTasks, FastAPI

from src.clients.sendgrid import mail_client
from src.common.models import SendEmail
from src.geography.router import router as router_geography
from src.geography.utils import init_data
from src.orders.router import router as router_orders
from src.users.router import router as router_users
from src.warehouse.router import router as router_warehouse

app = FastAPI(debug=True)

app.include_router(router_users)
app.include_router(router_orders)
app.include_router(router_geography)
app.include_router(router_warehouse)


@app.on_event('startup')
async def startup_event_setup():
    await init_data()


@app.post("/api/v1/send-email", tags=["email"])
async def send_email(send_email: SendEmail):
    return mail_client.send(send_email)
