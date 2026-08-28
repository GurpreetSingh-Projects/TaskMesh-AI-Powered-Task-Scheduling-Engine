from passlib.context import CryptContext
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from app.config import settings

pwd_context = CryptContext( schemes=["Ärgon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/create")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db= db

    def hash_password(password: str)-> str:
        return pwd_context.hash(password)

    def verify_password(password: str, hashed_password: str)-> bool:
        return pwd_context.verify(password, hashed_password)

    def create_access_token(data: dict):
        toEncode = data
        tokenExpiry = datetime.now(timezone.utc) + timedelta( minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        toEncode.update({"exp": tokenExpiry})
        encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)
        return encodedJwt

    def create_refresh_token(data: dict):
        toEncode = data
        tokenExpiry = datetime.now(timezone.utc) + timedelta( minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        toEncode.update({"exp": tokenExpiry})
        encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)
        return encodedJwt

    def decode_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms= settings.ALGORITHM)
            return payload
        except JWTError:
            print("Invalid or expired token!!")

        return None