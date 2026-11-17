from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, update, func
from uuid import UUID
from datetime import datetime, timezone
from loguru import logger
from app.features.users.models import Users

class UserActivityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    