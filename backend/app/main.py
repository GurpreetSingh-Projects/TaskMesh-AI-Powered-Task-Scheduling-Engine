from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.features.auth.routers import router as auth_router
from app.features.users.routers import router as user_router
from app.features.onboarding.routers import router as onboarding_router
from app.features.tasks.routers import router as task_router
from app.database import Base
from app import features

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title='TaskMesh Api v2', version='2.0.0', lifespan=lifespan)

@app.get("/health", summary="Health for checking api availability and server status")
def read_root():
    return {
        "messsage": "TaskMesh - AI Powered Task Scheduling Engine is online"
    }

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(onboarding_router)
app.include_router(task_router)