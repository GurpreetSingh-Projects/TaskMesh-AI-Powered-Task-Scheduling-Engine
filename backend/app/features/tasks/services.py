from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, insert, func, update
import math
from datetime import datetime, timezone
from app.features.users.models import Users
from app.features.tasks.models import Tasks, SubTasks
from app.features.tasks.schemas import TaskCreateRequestSchema, TaskUpdateRequestSchema, TaskReadResponseItemSchema, TaskReadResponseSchema, SubtaskReadResponseItemSchema, SubtaskReadResponseSchema, SubtaskCreateRequestSchema, SubtaskUpdateRequestSchema

class TaskService:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create_task(self, user: Users, task_data: TaskCreateRequestSchema):
        insert_query= (
            insert(Tasks)
            .values(
                user_id= user.user_id,
                title= task_data.title,
                description= task_data.description,
                image_url= task_data.image_url,
                status= task_data.status,
                completed_at= task_data.completed_at,
                due_at= task_data.due_at,
                priority= task_data.priority,
                updated_by= user.user_id,
                created_by= user.user_id,
            )
            .returning(Tasks)
        )
        try:
            response = (await self.db.execute(insert_query)).scalar_one_or_none()
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while adding task: {str(e)}")
        await self.db.commit()
        return response

    async def get_tasks(self, user: Users, limit: int= 1, offset: int= 0):
        query= (
            select(Tasks)
            .where(
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
            .order_by(
                Tasks.created_at.desc(),
                Tasks.updated_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        tasks = (await self.db.execute(query)).scalars().all()

        count_query = (
            select(func.count(Tasks.task_id))
            .where(
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
        )

        total_tasks_count = (await self.db.execute(count_query)).scalar_one_or_none()

        has_more = offset + len(tasks) < total_tasks_count
        page = (offset // limit) + 1
        total_pages = (math.ceil(total_tasks_count/ limit))
        
        return {
            "items": tasks,
            "limit": limit,
            "offset": offset,
            "has_more": has_more,
            "total_tasks": total_tasks_count,
            "page": page,
            "total_pages": total_pages
        }

    async def update_task(self, user: Users, task_id: UUID, task_data: TaskUpdateRequestSchema):
        task_data = task_data.model_dump(exclude_unset= True)

        if not task_data:
            raise HTTPException(status_code= 400, detail= "Invalid question data provided")

        task_data["updated_by"]= user.user_id

        update_query= (
            update(Tasks)
            .where(
                Tasks.task_id == task_id, 
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
            .values(**task_data)
            .returning(Tasks)
        )

        try:
            response = (await self.db.execute(update_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating task: {str(e)}")

        await self.db.commit()
        return response

    async def deactivate_task(self, user: UUID, task_id: UUID):
        deactivate_query= (
            update(Tasks)
            .where(
                Tasks.task_id == task_id, 
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
            .values(
                is_deleted= True,
                deleted_at= datetime.now(timezone.utc),
                updated_by= user.user_id
            )
            .returning(Tasks)
        )

        try:
            response = (await self.db.execute(deactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating task: {str(e)}")
        
        await self.db.commit()
        return

    async def create_subtask(self, user: Users, subtask_data: TaskCreateRequestSchema):
         insert_query= (
             insert(SubTasks)
             .values(
                 task_id= subtask_data.task_id,
                 user_id= user.user_id,
                 title= subtask_data.title,
                 description= subtask_data.description,
                 image_url= subtask_data.image_url,
                 status= subtask_data.status,
                 completed_at= subtask_data.completed_at,
                 due_at= subtask_data.due_at,
                 priority= subtask_data.priority,
                 updated_by= user.user_id,
                 created_by= user.user_id,
             )
             .returning(SubTasks)
         )
         try:
             response = (await self.db.execute(insert_query)).scalar_one_or_none()
         except HTTPException:
             await self.db.rollback()
             raise
         except Exception as e:
             raise HTTPException(status_code=500, detail=f"An error occurred while adding subtask: {str(e)}")
         await self.db.commit()
         return response
 
    async def get_SubTasks(self, user: Users, limit: int= 1, offset: int= 0):
        query= (
            select(SubTasks)
            .where(
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
            .order_by(
                Tasks.created_at.desc(),
                Tasks.updated_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        tasks = (await self.db.execute(query)).scalars().all()

        count_query = (
            select(func.count(Tasks.task_id))
            .where(
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
        )

        total_tasks_count = (await self.db.execute(count_query)).scalar_one_or_none()

        has_more = offset + len(tasks) < total_tasks_count
        page = (offset // limit) + 1
        total_pages = (math.ceil(total_tasks_count/ limit))
        
        return {
            "items": tasks,
            "limit": limit,
            "offset": offset,
            "has_more": has_more,
            "total_tasks": total_tasks_count,
            "page": page,
            "total_pages": total_pages
        }

    async def update_subtask(self, user: Users, task_id: UUID, task_data: TaskUpdateRequestSchema):
        task_data = task_data.model_dump(exclude_unset= True)

        if not task_data:
            raise HTTPException(status_code= 400, detail= "Invalid question data provided")

        task_data["updated_by"]= user.user_id

        update_query= (
            update(Tasks)
            .where(
                Tasks.task_id == task_id, 
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
            .values(**task_data)
            .returning(Tasks)
        )

        try:
            response = (await self.db.execute(update_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating task: {str(e)}")

        await self.db.commit()
        return response

    async def deactivate_task(self, user: UUID, task_id: UUID):
        deactivate_query= (
            update(Tasks)
            .where(
                Tasks.task_id == task_id, 
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False)
            )
            .values(
                is_deleted= True,
                deleted_at= datetime.now(timezone.utc),
                updated_by= user.user_id
            )
            .returning(Tasks)
        )

        try:
            response = (await self.db.execute(deactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating task: {str(e)}")
        
        await self.db.commit()
        return
