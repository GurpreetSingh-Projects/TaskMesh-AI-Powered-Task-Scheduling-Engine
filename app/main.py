from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from .core.database import get_db
from .models import *
from .schemas import *
from .services import *
from .core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
app = FastAPI(title="TODO API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"hello":"world"}

@app.get("/users/get/{user_id}", response_model=UserRead, tags=["user"])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    users = await getUser(user_id, db)
    return users

@app.get("/users/get/all", response_model=list[UserRead], tags=["user"])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await getAllUsers(db)
    return users

@app.post("/users/create/", response_model=UserRead, tags=["user"])
async def create_user(user_details: UserCreate, db: AsyncSession= Depends(get_db)):
        new_user = await createUser(user_details, db)
        return new_user

# @app.post("users/edit/{user_id}", response_model=UserRead, tags=["user"])
# async def create_user(user: UserCreate, db: AsyncSession= Depends(get_db)):
#         new_user = await createUser(db, user_data=user)
#         return {
#             "user_id": new_user.user_id,
#             "email": new_user.email,
#         }
