from fastapi import FastAPI
from contextlib import asynccontextmanager
from .models import Base
from .dependencies.database import engine
from .routers import auth_router, user_router, task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    
app = FastAPI(title="TaskMesh API", version="1.0.3", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"hello":"world"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)