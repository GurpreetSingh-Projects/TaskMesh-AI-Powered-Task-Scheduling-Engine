from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from app.features.auth.routers import router as auth_router
# from app.features.users.routers import router as user_router
from app.database import Base
from app import features

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(Base.metadata.tables.keys())
    yield

app = FastAPI(title='TaskMesh Api v2', version='2.0.0', lifespan=lifespan)

@app.get("/")
def read_root():
    return "TaskMesh - AI Powered Task Scheduling Engine"

app.include_router(auth_router)
# app.include_router(user_router)