from fastapi import FastAPI

from src.clients.sendgrid import mail_client
from src.common.models import SendEmail
from src.orders.router import router as router_orders
from src.users.router import router as router_users

app = FastAPI(debug=True)

app.include_router(router_users)
app.include_router(router_orders)


@app.post("/api/v1/send-email", tags=["email"])
async def send_email(send_email: SendEmail):
    return mail_client.send(send_email)
