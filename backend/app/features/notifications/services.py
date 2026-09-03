from sqlalchemy.ext.asyncio import AsyncSession

class NotificationService:
    def __init__(self, db:AsyncSession):
        self.db = db