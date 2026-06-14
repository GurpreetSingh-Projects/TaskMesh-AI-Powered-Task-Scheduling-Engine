from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from fastapi import HTTPException
from datetime import datetime, timezone
from ..schemas.user_schemas import *
from ..models.users import *
from ..core.security import hash_password, verify_password
import logging
import math

logger = logging.getLogger(__name__)


async def create_user(user_data: UserCreate, db: AsyncSession):
    query = insert(User).values(
        email=user_data.email,
        hashed_pswd=hash_password(user_data.password),
        role=UserRoles.USER,
        is_deleted=False
    )

    query = query.on_conflict_do_update(
        index_elements=[User.email],
        set_={
            User.is_deleted: False,
            User.hashed_pswd: user_data.password
        },
        where=((User.is_deleted == True) & (User.hashed_pswd == user_data.password))
    ).returning(User)

    try:
        result = (await db.execute(query)).scalar_one_or_none()
        await db.commit()
        return result

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User already exists!! please login with your current account"
        )

    except Exception:
        await db.rollback()
        logger.exception("Unexpected error occurred during Create User")


async def get_user_by_email(email: EmailStr | None, db: AsyncSession):
    user = (
        await db.execute(
            select(User).where(
                (User.email == email) & (User.is_deleted == False)
            )
        )
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_user_by_id(user_id: UUID | None, db: AsyncSession):
    user = (
        await db.execute(
            select(User).where(
                (User.user_id == user_id) & (User.is_deleted == False)
            )
        )
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def verify_user(email: EmailStr, password: str, db: AsyncSession):
    user = await get_user_by_email(email, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials!!")

    password_matched = verify_password(password, user.hashed_pswd)

    if not password_matched:
        raise HTTPException(status_code=401, detail="Invalid Credentials!!")

    return user


async def get_all_users(page: int, page_size: int, db: AsyncSession):
    total_pages = 0

    total_users = (
        await db.execute(
            select(func.count(User.user_id))
            .where(User.is_deleted == False)
        )
    ).scalar()

    items = (
        await db.execute(
            select(User)
            .where(User.is_deleted == False)
            .order_by(User.created_at)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    if total_users is not None and total_users > 0 and page_size > 0:
        total_pages = math.ceil(total_users / page_size)

    return {
        "items": items,
        "total": total_users,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


async def edit_user(
    user_id: UUID,
    email: EmailStr | None,
    password: str | None,
    db: AsyncSession
):
    user = await get_user_by_id(user_id, db)

    if email:
        user.email = email

    if password:
        user.hashed_pswd = hash_password(password)

    user.updated_by = user.user_id

    await db.commit()
    await db.refresh(user)
    return user


async def deactivate_user(user_id: UUID, db: AsyncSession):
    user = await get_user_by_id(user_id, db)

    user.is_deleted = True
    user.deleted_at = datetime.now(timezone.utc)

    await db.commit()
    return


async def delete_user(user_id: UUID, db: AsyncSession):
    user = await get_user_by_id(user_id, db)

    await db.delete(user)
    await db.commit()
    return