from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from loguru import logger

from app import features
from app.core.logging import setup_logging
from app.core.redis import redis_client
from app.core.schedulers import end_scheduler, start_scheduler
from app.database import Base, engine
from app.features.activity.routers import router as actiivty_router
from app.features.auth.routers import router as auth_router
from app.features.labels.routers import router as label_router
from app.features.onboarding.routers import router as onboarding_router
from app.features.storage.routers import router as storage_router
from app.features.tasks.routers import router as task_router
from app.features.users.routers import user_router, user_settings_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    start_scheduler()
    yield
    end_scheduler()
    await redis_client.aclose()


app = FastAPI(
    title="TaskMesh Api v2",
    version="2.1.1",
    lifespan=lifespan,
    description="TaskMesh is an AI-powered task scheduling engine that helps users capture tasks, set priorities and due dates, and automatically plan their day around them. This Swagger based openapi docs provides endpoints for authentication, user profiles, onboarding, task management, scheduling, and file storage.",
    contact={
        "name": "Maintained by Gurpreet Singh, checkout my Personal Portfolio here",
        "url": "https://gurpreet-singh-chadha.vercel.app/",
    },
)

health_router = APIRouter(tags=["Health"])


@health_router.api_route(
    "/awake",
    summary="Health endpoint for checking api availability and server status",
    methods=["GET", "HEAD"],
)
def awake():
    return {"messsage": "TaskMesh - AI Powered Task Scheduling Engine is online"}


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(user_settings_router)
app.include_router(onboarding_router)
app.include_router(label_router)
app.include_router(task_router)
app.include_router(actiivty_router)
app.include_router(storage_router)
