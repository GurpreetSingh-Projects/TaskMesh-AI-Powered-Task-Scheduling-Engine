from fastapi import HTTPException
from sqlachemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.features.users.schemas import UserCreate
from app.features.users.models import Users
from app.features.auth.security import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_details: UserCreate):
        query= insert(Users).values(
            email= user_details.email, 
            hashed_pswd= hash_password(user_details.password), 
            role= user_details.role
            profile_img= None
            is_deleted= False
            deleted_at= None
        )

        query = query.on_conflict_do_update(
            index_elements=[Users.email],
            set_={
                "is_deleted": False,
                "deleted_at": None
            }
            where= (Users.email == user_details.email) & (Users.is_deleted.is_(True))
            .returning(Users)
        )

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

    async def get_user_details(self, user_details: UserCreate):
        query = select(Users).where(Users.email == user_details.email, Users.is_deleted.is_(False))
        user = (await self.db.execute(query)).scalar_one_or_none()
        return user

    # only for reference

    # async def verify_user(email: EmailStr, password: str, db: AsyncSession):
    #     user = await get_user_by_email(email, db)

    #     if not user:
    #         raise HTTPException(status_code=401, detail="Invalid Credentials!!")

    #     password_matched = verify_password(password, user.hashed_pswd)

    #     if not password_matched:
    #         raise HTTPException(status_code=401, detail="Invalid Credentials!!")

    #     return user


    # async def get_all_users(page: int, page_size: int, db: AsyncSession):
    #     total_pages = 0

    #     total_users = (
    #         await db.execute(
    #             select(func.count(User.user_id))
    #             .where(User.is_deleted.is_(False))
    #         )
    #     ).scalar()

    #     items = (
    #         await db.execute(
    #             select(User)
    #             .where(User.is_deleted.is_(False))
    #             .order_by(User.created_at)
    #             .offset((page - 1) * page_size)
    #             .limit(page_size)
    #         )
    #     ).scalars().all()

    #     if total_users is not None and total_users > 0 and page_size > 0:
    #         total_pages = math.ceil(total_users / page_size)

    #     return {
    #         "items": items,
    #         "total": total_users,
    #         "page": page,
    #         "page_size": page_size,
    #         "total_pages": total_pages
    #     }
        

    #     async def edit_user(
    #         user_id: UUID,
    #         email: EmailStr | None,
    #         password: str | None,
    #         db: AsyncSession
    #     ):
    #         user = await get_user_by_id(user_id, db)

    #         if email:
    #             user.email = email

    #         if password:
    #             user.hashed_pswd = hash_password(password)

    #         user.updated_by = user.user_id

    #         await db.commit()
    #         await db.refresh(user)
    #         return user


    #     async def deactivate_user(user_id: UUID, db: AsyncSession):
    #         user = await get_user_by_id(user_id, db)

    #         user.is_deleted = True
    #         user.deleted_at = datetime.now(timezone.utc)

    #         await db.commit()
    #         return


    #     async def delete_user(user_id: UUID, db: AsyncSession):
    #         user = await get_user_by_id(user_id, db)

    #         await db.delete(user)
    #         await db.commit()
    #         return
