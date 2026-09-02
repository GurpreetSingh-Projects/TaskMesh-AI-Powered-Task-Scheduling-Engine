from sqlalchemy.ext.asyncio import AsyncSession

class TaskService:
    def __init__(self, db:AsyncSession):
        self.db = db