import random

from src.dao.base import BaseDao
from src.users.models import EmailCode


class EmailCodeService(BaseDao):
    class_name = EmailCode

    def code_generator(self):
        code = random.randint(1000, 9999)
        return code
    
    async def create_code(self, user_id: int, email: str):
        return await self.add({
            "email": email,
            "user_id": user_id,
            "code": str(self.code_generator())
        })


email_service = EmailCodeService()
