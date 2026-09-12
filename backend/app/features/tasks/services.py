from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.features.users.models import Users
from app.features.tasks.models import Tasks
from app.features.tasks.schemas import TaskCreateRequestSchema, TaskUpdateRequestSchema, TaskReadResponseSchema


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
            raise HTTPException(status_code=500, detail=f"An error occurred while adding onboarding questions: {str(e)}")
        return response

    # async def get_task(self, user: Users, task_id: UUID): 
    #     pass

    # async def list_tasks(self, user: Users, limit: int, offset: int): 
    #     pass

    # async def update_task(self, user: Users, task_id: UUID, task_data: TaskUpdateSchema): 
    #     pass

    # async def delete_task(self, user: Users, task_id: UUID): 
    #     pass
