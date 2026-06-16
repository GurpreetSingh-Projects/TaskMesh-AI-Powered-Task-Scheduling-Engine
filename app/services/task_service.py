from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID
from ..models import User, Task, TaskStatus, UserRoles
from ..schemas import TaskFilters, TaskUpdate
from .user_service import get_user_by_id
import math

async def create_task(
    task_name: str,
    task_status: TaskStatus,
    db: AsyncSession,
    current_user: User,
    user_id: Optional[UUID] = None,
    task_description: Optional[str] = None
):
    if current_user.role != UserRoles.ADMIN and user_id is not None:
        raise HTTPException(status_code=403, detail="Forbidden Action!!")

    if current_user.role == UserRoles.ADMIN and user_id is not None:
        await get_user_by_id(user_id, db)

        new_task = Task(
            user_id=user_id,
            task_name=task_name,
            task_description=task_description,
            task_status=task_status,
            created_by=user_id,
            updated_by=user_id
        )
    else:
        new_task = Task(
            user_id=current_user.user_id,
            task_name=task_name,
            task_description=task_description,
            task_status=task_status,
            created_by=current_user.user_id,
            updated_by=current_user.user_id
        )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def get_task(task_id: UUID, db: AsyncSession, user: User):
    if user.role == UserRoles.USER:
        task = (
            await db.execute(
                select(Task).where(
                    (Task.task_id == task_id)
                    & (Task.user_id == user.user_id)
                    & (not Task.is_deleted)
                )
            )
        ).scalar_one_or_none()
    else:
        task = (
            await db.execute(
                select(Task).where(
                    (Task.task_id == task_id)
                    & (not Task.is_deleted)
                )
            )
        ).scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="No task found!!")

    return task


async def get_all_tasks_by_user(
    filters: TaskFilters,
    user_id: UUID,
    page: int,
    page_size: int,
    db: AsyncSession
):
    await get_user_by_id(user_id, db)

    total_pages = 0
    total_tasks = 0
    
    query = (Task.user_id == user_id) & (Task.is_deleted.is_(False))

    if filters.status:
        query = query & (Task.task_status == filters.status)
        
    if filters.priority:
        query = query & (Task.priority == filters.priority)
        
    if filters.search and filters.search.strip():
        search_term = f"%{filters.search}%"
        query = query & (
            or_(
                Task.task_name.ilike(search_term), 
                Task.task_description.ilike(search_term))
            )
        
    print("created query", query)
   
    total_tasks = (
        await db.execute(select(func.count(Task.task_id)))).scalar()
             
    items = (
        await db.execute(
            select(Task)
            .where(query)
            .order_by(Task.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    if total_tasks is not None and total_tasks > 0 and page_size > 0:
        total_pages = math.ceil(total_tasks / page_size)
    
    return {
        "items": items,
        "total": total_tasks,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
    

async def edit_task(
    task_id: UUID,
    task_details: TaskUpdate,
    db: AsyncSession,
    user: User
):
    task = await get_task(task_id, db, user)

    updated_task_details = task_details.model_dump(exclude_unset=True)

    if not updated_task_details:
        raise HTTPException(
            status_code=404,
            detail="Please enter valid details for edit task!!"
        )

    for key, value in updated_task_details.items():
        setattr(task, key, value)

    task.updated_by = user.user_id

    await db.commit()
    await db.refresh(task)
    return task


async def deactivate_task(task_id: UUID, db: AsyncSession, user: User):
    task = await get_task(task_id, db, user)

    task.is_deleted = True
    task.deleted_at = datetime.now(timezone.utc)

    await db.commit()
    return


async def delete_task(task_id: UUID, db: AsyncSession, user: User):
    task = await get_task(task_id, db, user)

    await db.delete(task)
    await db.commit()
    return