from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.features.auth.schemas import TokenSchema

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(user_id: UUID):
    toEncode = {"sub": str(user_id)}
    tokenExpiry = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    toEncode.update({"exp": tokenExpiry})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJwt


def create_refresh_token(user_id: UUID):
    toEncode = {"sub": str(user_id)}
    tokenExpiry = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    toEncode.update({"exp": tokenExpiry})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return TokenSchema.model_validate(payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token!!")
