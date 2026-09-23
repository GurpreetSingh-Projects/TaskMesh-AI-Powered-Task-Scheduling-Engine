from uuid import UUID
from fastapi import  HTTPException, UploadFile
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.users.services import UserService
from app.features.storage.services import StorageService
from app.features.users.schemas import UserLoginRequestSchema, UserEditRequestSchema
from app.features.users.models import Users
from app.features.users.enums import UserRoles
from app.core.utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from datetime import datetime, timezone, timedelta
from app.config import settings
from app.features.storage.enums import FileStorageEntity

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db= db
        self.user_service= UserService(db)
        self.storage_service= StorageService(db)

    async def create_user(self, email: EmailStr, password: str, profile_img: UploadFile | None):
        user = await self.user_service.get_user_details(email= email, silent_mode= True)

        if user:
            if not user.is_deleted and user.deleted_at is None:
                raise HTTPException(status_code = 409, detail= "User with this email already exists, please try logging in")
            raise HTTPException(status_code = 410, detail= "This user was deleted, please try reactivating your account")

        insert_query= insert(Users).values(
            email= email, 
            hashed_pswd= hash_password(password), 
            role= UserRoles.USER,
            profile_img= None,
            is_deleted= False,
            deleted_at= None
        )

        insert_query = insert_query.on_conflict_do_nothing(
            index_elements=[Users.email],
        ).returning(Users)

        try:
            user= (await self.db.execute(insert_query)).scalar_one_or_none()
            
            if user is None:
                await self.db.rollback()
                raise HTTPException(status_code = 409, detail= "User with this email already exists")

            await self.db.commit()

            if profile_img:
                file_record = await self.storage_service.upload_file(
                    user=user,
                    file=profile_img,
                    entity_type=FileStorageEntity.PROFILE_IMG,
                    entity_id=str(user.user_id),
                )

                await self.user_service.edit_user(user= user, user_data= UserEditRequestSchema(profile_img=str(file_record["item"].file_storage_id)))

            access_token = create_access_token(user.user_id)
            refresh_token = create_refresh_token(user.user_id)
            user.profile_img= await self.storage_service.get_signed_asset_url(file_record["item"].storage_key)

            return {
                "message": "User created successfully",
                "user": user,
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


    async def get_current_user(self, token: str):
        payload = decode_token(token)
        if not payload or not payload.sub:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = await self.user_service.get_user_details(user_id= UUID(payload.sub))
        return user

    async def login_user(self, user_details: UserLoginRequestSchema):
        user = await self.user_service.get_user_details(user_details.email)

        if user.is_deleted and user.deleted_at is not None:
            raise HTTPException(status_code = 410, detail= "This user was deleted, please try reactivating your account")
        
        
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

    async def reactivate_user(self, user_details: UserLoginRequestSchema):
        user = await self.user_service.get_user_details(user_details.email, silent_mode= True)

        if not user:
            raise HTTPException(status_code=404, detail="User not found, please create a new account")
        
        if not user.is_deleted and user.deleted_at is None:
            raise HTTPException(status_code=409, detail="Existing user, please try logging in ")

        reactivate_query= (
            update(Users)
            .where(
                Users.user_id == user.user_id
            )
            .values(
                is_deleted= False,
                deleted_at= None,
                updated_by= user.user_id
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