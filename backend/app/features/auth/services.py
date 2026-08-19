from uuid import UUID
from fastapi import  HTTPException
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.users.services import UserService
from app.features.users.schemas import UserCreateRequestSchema, UserLoginRequestSchema
from app.features.users.models import Users
from app.features.users.enums import UserRoles
from app.core.utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from datetime import datetime, timezone, timedelta
from app.config import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db= db
        self.user_service= UserService(db)

    async def get_current_user(self, token: str):
        payload = decode_token(token)
        if not payload or not payload.sub:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = await self.user_service.get_user_details(user_id= UUID(payload.sub))
        return user

    async def create_user(self, user_details: UserCreateRequestSchema):
        
        query= insert(Users).values(
            email= user_details.email, 
            hashed_pswd= hash_password(user_details.password), 
            role= UserRoles.USER,
            profile_img= None,
            is_deleted= False,
            deleted_at= None
        )

        query = query.on_conflict_do_nothing(
            index_elements=[Users.email],
        ).returning(Users)

        try:
            result= (await self.db.execute(query)).scalar_one_or_none()
            
            if result is None:
                await self.db.rollback()
                raise HTTPException(status_code = 409, detail= "User with this email already exists")

            await self.db.commit()
            access_token = create_access_token(result.user_id)
            refresh_token = create_refresh_token(result.user_id)

            return {
                "message": "User created successfully",
                "user": result,
                "access_token": access_token,
                "access_token_expires_at": datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                "refresh_token": refresh_token,
                  "user_settings": "",
                "refresh_token_expires_at": datetime.now(timezone.utc) + timedelta(days= settings.REFRESH_TOKEN_EXPIRE_DAYS),
                "token_type": "bearer"
            }

        except Exception:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail= "Something went wrong while creating the user")

    async def login_user(self, user_details: UserLoginRequestSchema):
        user = await self.user_service.get_user_details(user_details.email)

        if not user.is_deleted and not verify_password(user_details.password, user.hashed_pswd):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "message": "User logged in successfully",
            "user": user,
            "user_settings": "",
            "access_token": create_access_token(user.user_id),
            "access_token_expires_at": datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "refresh_token": create_refresh_token(user.user_id),
            "refresh_token_expires_at": datetime.now(timezone.utc) + timedelta(days= settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "token_type": "bearer"
        }

    async def refresh_token(self, refresh_token: str):
        result = decode_token(refresh_token)
        print(f"Decoded token: {result, type(result)}")  # Debugging line
        if result.sub is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = await self.user_service.get_user_details(user_id=UUID(result.sub))
        return {
            "message": "User token refreshed successfully",
            "user": user,
            "user_settings": "",
            "access_token": create_access_token(user.user_id),
            "access_token_expires_at": datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "refresh_token": refresh_token,
            "refresh_token_expires_at": datetime.now(timezone.utc) + timedelta(days= settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "token_type": "bearer"
        }

    async def reactivate_user(self, user_id: UUID):
        reactivate_query= (
            update(Users)
            .where(
                Users.user_id == user_id
            )
            .values(
                is_deleted= False,
                deleted_at= None,
                updated_by= user_id
            )
            .returning(Users)
        )

        try:
            response = (await self.db.execute(reactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating task: {str(e)}")

        await self.db.commit()
        return