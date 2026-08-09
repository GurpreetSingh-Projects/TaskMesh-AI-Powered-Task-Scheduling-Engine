from uuid import UUID
from fastapi import  HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.features.users.services import UserService
from app.features.users.schemas import UserCreateRequestSchema, UserLoginRequestSchema
from app.features.users.models import Users
from app.features.users.enums import UserRoles
from app.core.utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/create")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db= db
        self.user_service= UserService(db)
        
    async def create_user(self, user_details: UserCreateRequestSchema):
        query= insert(Users).values(
            email= user_details.email, 
            hashed_pswd= hash_password(user_details.password), 
            role= UserRoles.USER,
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
            access_token = create_access_token(result.user_id)
            refresh_token = create_refresh_token(result.user_id)

            return {
                "message": "User created successfully",
                "user": result,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

        except Exception as e:
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
            "access_token": create_access_token(user.user_id),
            "refresh_token": create_refresh_token(user.user_id),
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
            "access_token": create_access_token(user.user_id),
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }