from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from .core.database import get_db
from .models import *
from .schemas import *
from .services import *
from .core.database import engine
from typing import Optional
from pydantic import EmailStr

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

@app.patch("/users/edit/{user_id}", response_model=UserRead, tags=["user"])
async def edit_user(user_id:int, email: Optional[EmailStr]= None, password: Optional[str]= None, db: AsyncSession= Depends(get_db)):
        edit_user = await editUser(user_id, email, password, db)
        return edit_user

@app.delete("/users/delete/{user_id}", tags=["user"])
async def delete(user_id:int, db: AsyncSession= Depends(get_db)):
        delete_user = await deleteUser(user_id, db)
        return {"detail": "User deleted successfully"}
