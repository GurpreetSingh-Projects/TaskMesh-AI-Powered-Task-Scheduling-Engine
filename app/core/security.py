from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from .config import settings

pwd_context= CryptContext( schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/create")

def hashPassword(password: str)-> str:
    return pwd_context.hash(password)

def verifyPassowrd(passowrd: str, hashed_password: str)-> bool:
    return pwd_context.verify(passowrd, hashed_password)
