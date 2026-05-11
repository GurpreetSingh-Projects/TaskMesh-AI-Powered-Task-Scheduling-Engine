from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from .core.database import get_db
from .models import *
from .schemas import *
from .services import *
from .core.database import engine
from .routers import *
from .core.config import Settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
app = FastAPI(title="TODO API", version="1.0.1", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"hello":"world"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)
