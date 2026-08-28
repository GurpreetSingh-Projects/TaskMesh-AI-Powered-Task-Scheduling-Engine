from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from app.features.auth.routers import router as auth_router
from app.core.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title='TaskMesh Api v2', version='2.0.0', lifespan=lifespan)

@app.get("/")
def read_root():
    return "TaskMesh - AI Powered Task Scheduling Engine"

app.include_router(auth_router)