from fastapi import  HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from app.config import settings
from app.features.users.services import UserService
from app.features.users.schemas import UserCreateRequestSchema
from app.features.users.models import Users

pwd_context = CryptContext( schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/create")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db= db

    def hash_password(self, password: str)-> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str)-> bool:
        return pwd_context.verify(password, hashed_password)

    def create_access_token(self,  data: dict):
        toEncode = data
        tokenExpiry = datetime.now(timezone.utc) + timedelta( minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        toEncode.update({"exp": tokenExpiry})
        encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)
        return encodedJwt

    def create_refresh_token(self, data: dict):
        toEncode = data
        tokenExpiry = datetime.now(timezone.utc) + timedelta( minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        toEncode.update({"exp": tokenExpiry})
        encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)
        return encodedJwt

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms= settings.ALGORITHM)
            return payload
        except JWTError:
            print("Invalid or expired token!!")

        return None

    def refresh_access_token(self, token: str):
        payload = self.decode_token(token)

        if payload is None:
            raise HTTPException(status_code= 401, detail= "Invalid or expired token!!"  )

        
    async def create_user(self, user_details: UserCreateRequestSchema):
        query= insert(Users).values(
            email= user_details.email, 
            hashed_pswd= self.hash_password(user_details.password), 
            role= user_details.role,
            profile_img= None,
            is_deleted= False,
            deleted_at= None
        )

        query = query.on_conflict_do_update(
            index_elements=[Users.email],
            set_={
                "is_deleted": False,
                "deleted_at": None
            },
            where= (Users.email == user_details.email) & (Users.is_deleted.is_(True))
        ).returning(Users)

        try:
            result= (await self.db.execute(query)).scalar_one_or_none()

            if result is None:
                await self.db.rollback()
                raise HTTPException(status_code = 409, detail= "User with this email already exists") 

            await self.db.commit()
            return result

        except Exception as e:
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail= "Something went wrong while creating the user")   


    async def login_user(self, email: str, db: AsyncSession):
        user = await UserService.get_user_details(email, db)
        return {
            "message": "User logged in successfully",
            "user": user,
            "access_token": self.create_access_token({"sub": str(user.user_id)}),
            "refresh_token": self.create_refresh_token({"sub": str(user.user_id)}),
            "token_type": "bearer"
        }