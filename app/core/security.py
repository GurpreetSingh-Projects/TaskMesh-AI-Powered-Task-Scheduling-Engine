from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from .config import settings

pwd_context= CryptContext( schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/create")

def hashPassword(password: str)-> str:
    return pwd_context.hash(password)

def verifyPassword(passowrd: str, hashed_password: str)-> bool:
    return pwd_context.verify(passowrd, hashed_password)

def createAccessToken(data: dict):
    toEncode = data
    tokenExpiry = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": tokenExpiry})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJwt

def createRefreshToken(data: dict):
    toEncode = data
    tokenExpiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    toEncode.update({"exp": tokenExpiry})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJwt

def decodeToken(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms= settings.ALGORITHM)
        return payload
    except JWTError:
        print("Invalid or expired token!!")
    
    return None 