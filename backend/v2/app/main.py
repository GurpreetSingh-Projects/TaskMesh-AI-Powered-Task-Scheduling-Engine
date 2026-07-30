from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        pass
    yield

app = FastAPI(title='TaskMesh Api v2', version='2.0.0', lifespan=lifespan)

@app.get("/")
def read_root():
    return "TaskMesh - AI Powered Task Scheduling Engine"