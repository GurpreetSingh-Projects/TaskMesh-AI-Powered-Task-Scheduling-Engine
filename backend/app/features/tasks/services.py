from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import uuid4, UUID
from sqlalchemy import select, insert, func, update, and_, case, String, cast, Date
import math
from datetime import date, datetime, timezone
from loguru import logger
from app.features.users.models import Users
from app.features.tasks.models import Tasks, SubTasks
from app.features.tasks.schemas import TaskCreateRequestSchema, TaskUpdateRequestSchema, TaskReadResponseItemSchema, TaskReadResponseSchema, SubtaskReadResponseItemSchema, SubtaskReadResponseSchema, SubtaskCreateRequestSchema, SubtaskUpdateRequestSchema
from app.features.storage.models import FileStorage
from app.features.storage.enums import FileStorageEntity
from app.features.storage.services import StorageService
from app.features.tasks.enums import TaskPriority, TaskStatus, RankStatus, RankPriority
from app.features.activity.enums import UserActivityType, ActivityEntityType
from app.features.activity.services import ActivityService
from app.features.activity.schemas import UserActivityCreateRequestSchema

class TaskService:
    def __init__(self, db:AsyncSession):
        self.db = db
        self.storage_service= StorageService(db)
        self.activity_service= ActivityService(db)

    async def create_task(self, user: Users, task_data: TaskCreateRequestSchema, task_img: UploadFile | None):
        file_record= None
        task_id: UUID= uuid4()
        
        if task_data is not None: 
            task_data= task_data.model_dump(exclude_unset= True, exclude_none= True)

        task_data["user_id"]= user.user_id
        task_data["created_by"]= user.user_id
        task_data["updated_by"]= user.user_id

        if task_img is not None:
            file_record = await self.storage_service.upload_file(
                user=user,
                file=task_img,
                entity_type=FileStorageEntity.TASK,
                entity_id=str(task_id),
            )
            task_data["file_storage_id"]=str(file_record["item"].file_storage_id)
        
        insert_query= (
            insert(Tasks)
            .values(
                task_id= task_id,
                **task_data
            )
            .returning(Tasks)
        )

        try:
            response = (await self.db.execute(insert_query)).scalar_one()
            await self.activity_service.record_activity(
                    activity_data= UserActivityCreateRequestSchema(
                    activity_type= UserActivityType.TASK_CREATED,
                    entity_type= ActivityEntityType.TASKS,
                    entity_id= task_id,
                ),
                user= user
            )
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.warning("Integrity error on task create | task_id={}, user_id={}, error={}", task_id, user.user_id, e.orig)
            raise HTTPException(status_code = 409, detail=f"Duplicate task detected, addition cancelled!")
        except Exception as e:
            await self.db.rollback()
            logger.exception("Task create failed | user_id={}", user.user_id)
            raise HTTPException(status_code=500, detail="An error occurred while adding task")
        self.db.expunge(response)
        if response.file_storage_id:
            file_details= await self.storage_service.get_file_details(file_storage_id=response.file_storage_id, entity_type=FileStorageEntity.TASK)
            response.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
        else:
            response.image_url= None

        await self.db.commit()
        logger.info("Task created | task_id={} user_id={}", response.task_id, user.user_id)
        return response

    async def get_tasks_summary(self, start_date: date, end_date: date, user: Users,limit: int= 5):
        status_priority= case(RankStatus, value= cast(Tasks.status, String), else_=0)
        rank_priority= case(RankPriority, value= cast(Tasks.priority, String), else_=0)
        top_tasks_query= (
            select(Tasks)
            .where(
                Tasks.user_id == user.user_id,
                Tasks.created_at >= start_date,
                Tasks.created_at < end_date,
                Tasks.is_deleted.is_(False),
            )
            .order_by(
                status_priority.asc(),
                rank_priority.desc(),
                Tasks.created_at.desc()
            )
            .limit(limit)
        )

        progress_query= (
            select(
                func.count().filter(
                    Tasks.created_at >= start_date,
                    Tasks.created_at < end_date,
                )
                .label("created"),

                func.count().filter(
                    Tasks.created_at >= start_date,
                    Tasks.created_at < end_date,
                    Tasks.status == TaskStatus.PENDING
                )
                .label("pending"),

                func.count().filter(
                    Tasks.created_at >= start_date,
                    Tasks.created_at < end_date,
                    Tasks.status == TaskStatus.IN_PROGRESS
                )
                .label("in_progress"),

                func.count().filter(
                    Tasks.created_at >= start_date,
                    cast(Tasks.completed_at, Date) < end_date,
                    Tasks.status == TaskStatus.COMPLETED
                )
                .label("completed"),

                func.count().filter(
                    Tasks.status == TaskStatus.OVERDUE,
                    Tasks.completed_at.is_(None)
                )
                .label("overdue")
            )      
            .where(
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False),
            )
        )

        top_tasks = (await self.db.execute(top_tasks_query)).scalars().all()

        progress_stats = (await self.db.execute(progress_query)).one()

        for task in top_tasks:
            if task.file_storage_id:
                file_details= await self.storage_service.get_file_details(file_storage_id=task.file_storage_id, entity_type=FileStorageEntity.TASK)
                task.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
            else:
                task.image_url= None

            self.db.expunge(task)

        return {
            "top_tasks": top_tasks,
            "progress_stats": progress_stats._asdict(),
            "recently_completed": [],
        }

    async def get_tasks(self, status: TaskStatus, start_date: datetime, end_date: datetime | None,  user: Users, limit: int= 1, offset: int= 0):
        if end_date is None:
            end_date= datetime.now(timezone.utc)

        if start_date and end_date and start_date >= end_date:
            raise HTTPException(422, "start_date must be before end_date")

        if status is None:
            status= TaskStatus.PENDING

        rank_priority= case(RankPriority, value= cast(Tasks.priority, String), else_=0)
        
        query= (
            select(Tasks)
            .where(
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False),
                Tasks.status == status,
                Tasks.created_at >= start_date,
                Tasks.created_at < end_date,
            )
            .order_by(
                rank_priority.desc(),
                Tasks.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        tasks = (await self.db.execute(query)).scalars().all()

        for task in tasks:
            if task.file_storage_id:
                file_details= await self.storage_service.get_file_details(file_storage_id=task.file_storage_id, entity_type=FileStorageEntity.TASK)
                task.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
            else:
                task.image_url= None

            self.db.expunge(task)

        count_query = (
            select(func.count(Tasks.task_id))
                .where(
                    Tasks.user_id == user.user_id,
                    Tasks.is_deleted.is_(False),
                    Tasks.status == status,
                    Tasks.created_at >= start_date,
                    Tasks.created_at < end_date,
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

    async def update_task(self, user: Users, task_id: UUID, task_data: TaskUpdateRequestSchema,
    task_img: UploadFile | None = None):
        if task_data is not None: 
            task_data= task_data.model_dump(exclude_unset= True, exclude_none= True)
        
        if not task_data and not task_img:
            raise HTTPException(status_code= 400, detail= "Invalid update task data provided")

        if task_img is not None:
            file_record = await self.storage_service.upload_file(
                user=user,
                file=task_img,
                entity_type=FileStorageEntity.TASK,
                entity_id=str(task_id),
            )
            task_data["file_storage_id"]=str(file_record["item"].file_storage_id)

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
            response = (await self.db.execute(update_query)).scalar_one()
            
            if response is None:
                raise HTTPException(status_code= 404, detail= "No task found with the given id")

            await self.activity_service.record_activity(
                    activity_data= UserActivityCreateRequestSchema(
                    activity_type= UserActivityType.TASK_UPDATED,
                    entity_type= ActivityEntityType.TASKS,
                    entity_id= task_id,
                ),
                user= user
            )
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.warning("Integrity error on task update | task_id={}, user_id={}, error={}", task_id, user.user_id, e.orig)
            raise HTTPException(status_code = 409, detail="An error occurred while updating user")
        except Exception as e:
            await self.db.rollback()
            logger.warning("Exception on task update | task_id={}, user_id={}, error={}", task_id, user.user_id, e)
            raise HTTPException(status_code=500, detail="An error occurred while updating task")

        await self.db.commit()

        self.db.expunge(response)

        if response.file_storage_id:
            file_details= await self.storage_service.get_file_details(file_storage_id=response.file_storage_id, entity_type=FileStorageEntity.TASK)
            response.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
        else:
            response.image_url= None
        logger.info("Task updated | task_id={} user_id={}", response.task_id, user.user_id)
        return response

    async def deactivate_task(self, user: Users, task_id: UUID):
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
            response = (await self.db.execute(deactivate_query)).scalar_one()
            await self.activity_service.record_activity(
                    activity_data= UserActivityCreateRequestSchema(
                    activity_type= UserActivityType.TASK_DELETED,
                    entity_type= ActivityEntityType.TASKS,
                    entity_id= task_id,
                ),
                user= user
            )
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            logger.exception("Task deactivation failed | task_id={}, user_id={}", task_id, user.user_id)
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred while updating task")
        
        await self.db.commit()
        logger.info("Task Deactivated | task_id={}, user_id={}", response.task_id, user.user_id)
        return

    async def create_subtask(self, user: Users, subtask_data: SubtaskCreateRequestSchema, subtask_img: UploadFile | None):
        file_record= None
        subtask_id: UUID= uuid4()
        
        if subtask_data is not None: 
            subtask_data= subtask_data.model_dump(exclude_unset= True, exclude_none= True)

        if subtask_img is not None:
            file_record = await self.storage_service.upload_file(
                user=user,
                file=subtask_img,
                entity_type=FileStorageEntity.SUBTASK,
                entity_id=str(subtask_id),
            )
            subtask_data["file_storage_id"]=str(file_record["item"].file_storage_id)

        subtask_data["created_by"]= user.user_id
        subtask_data["updated_by"]= user.user_id
        
        insert_query= (
             insert(SubTasks)
             .values(
                 subtask_id= subtask_id,
                 **subtask_data
             )
             .returning(SubTasks)
         )
        
        try:
            response = (await self.db.execute(insert_query)).scalar_one()
            await self.activity_service.record_activity(
                    activity_data= UserActivityCreateRequestSchema(
                    activity_type= UserActivityType.SUBTASK_CREATED,
                    entity_type= ActivityEntityType.SUBTASKS,
                    entity_id= subtask_id,
                ),
                user= user
            )
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.warning("Integrity error on subtask create | subtask_id={}, user_id={}, error={}", subtask_id, user.user_id, e.orig)
            raise HTTPException(status_code = 409, detail=f"Duplicate subtask detected, addition cancelled!")
        except Exception as e:
            await self.db.rollback()
            logger.exception("Subtask create failed | user_id={}", user.user_id)
            raise HTTPException(status_code=500, detail="An error occurred while adding subtask")

        self.db.expunge(response)
        if response.file_storage_id:
            file_details= await self.storage_service.get_file_details(file_storage_id=response.file_storage_id, entity_type=FileStorageEntity.TASK)
            response.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
        else:
            response.image_url= None

        await self.db.commit()
        logger.info("Subtask created | subtask_id={} user_id={}", response.task_id, user.user_id)
        return response
 
    async def get_subtasks(self, user: Users, task_id: UUID, limit: int= 1, offset: int= 0):
        query= (
            select(SubTasks)
            .join(
                Tasks,
                Tasks.task_id == SubTasks.task_id
            )
            .where(
                SubTasks.task_id == task_id,
                SubTasks.is_deleted.is_(False),
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False),
            )
            .order_by(
                SubTasks.created_at.desc(),
                SubTasks.updated_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        subtasks = (await self.db.execute(query)).scalars().all()

        for subtask in subtasks:
            if subtask.file_storage_id:
                file_details= await self.storage_service.get_file_details(file_storage_id=subtask.file_storage_id, entity_type=FileStorageEntity.SUBTASK)
                subtask.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
            else:
                subtask.image_url= None

            self.db.expunge(subtask)

        count_query = (
            select(func.count(SubTasks.subtask_id))
            .join(
                Tasks,
                and_(Tasks.task_id == SubTasks.task_id)
            )
            .where(
                SubTasks.task_id == task_id,
                SubTasks.is_deleted.is_(False),
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False),
            )
        )


        total_subtasks_count = (await self.db.execute(count_query)).scalar_one()

        has_more = offset + len(subtasks) < total_subtasks_count
        page = (offset // limit) + 1
        total_pages = (math.ceil(total_subtasks_count/ limit))
        
        return {
            "items": subtasks,
            "limit": limit,
            "offset": offset,
            "has_more": has_more,
            "total_subtasks": total_subtasks_count,
            "page": page,
            "total_pages": total_pages
        }

    async def update_subtask(
        self,
        user: Users,
        task_id: UUID,
        subtask_id: UUID,
        subtask_img: UploadFile,
        subtask_data: SubtaskUpdateRequestSchema,
    ):
        if subtask_data is not None: 
            subtask_data= subtask_data.model_dump(exclude_unset= True, exclude_none= True)
        
        if not subtask_data and not subtask_img:
            raise HTTPException(status_code= 400, detail= "Invalid update subtask data provided")

        if subtask_img is not None:
            file_record = await self.storage_service.upload_file(
                user=user,
                file=subtask_img,
                entity_type=FileStorageEntity.SUBTASK,
                entity_id=str(subtask_id),
            )
            subtask_data["file_storage_id"]=str(file_record["item"].file_storage_id)

        subtask_data["updated_by"]= user.user_id

        update_query = (
            update(SubTasks)
            .where(
                SubTasks.task_id == task_id,
                SubTasks.subtask_id == subtask_id,
                Tasks.task_id == SubTasks.task_id,
                Tasks.user_id == user.user_id,
                Tasks.is_deleted.is_(False),
                SubTasks.is_deleted.is_(False),
            )
            .values(**subtask_data)
            .returning(SubTasks)
        )

        try:
            response = (await self.db.execute(update_query)).scalar_one_or_none()

            if response is None:
                raise HTTPException(status_code= 404, detail= "No subtask found with the given id")

            await self.activity_service.record_activity(
                    activity_data= UserActivityCreateRequestSchema(
                    activity_type= UserActivityType.SUBTASK_UPDATED,
                    entity_type= ActivityEntityType.SUBTASKS,
                    entity_id= subtask_id,
                ),
                user= user
            )
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.warning("Integrity error on subtask update | subtask_id={}, user_id={}, error={}", subtask_id, user.user_id, e.orig)
            raise HTTPException(status_code = 409, detail="An error occurred while updating subtask")
        except Exception as e:
            await self.db.rollback()
            logger.exception("Exception on subtask update | task_id= {}, subtask_id={}, user_id={}, error={}", task_id, subtask_id, user.user_id, e)
            raise HTTPException(status_code=500, detail="An error occurred while updating subtask")

        await self.db.commit()
    
        self.db.expunge(response)
        if response.file_storage_id:
            file_details= await self.storage_service.get_file_details(file_storage_id=response.file_storage_id, entity_type=FileStorageEntity.SUBTASK)
            response.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
        else:
            response.image_url= None

        logger.info("Subtask updated | subtask_id={}, user_id={}", response.subtask_id, user.user_id)
        return response

    async def deactivate_subtask(self, user: UUID, subtask_id: UUID):
        deactivate_query= (
            update(SubTasks)
            .where(
                SubTasks.subtask_id == subtask_id, 
                SubTasks.task_id.in_(
                    select(Tasks.task_id)
                    .where(
                        Tasks.user_id == user.user_id,
                        Tasks.is_deleted.is_(False)
                    )
                ),
            )
            .values(
                is_deleted= True,
                deleted_at= datetime.now(timezone.utc),
                updated_by= user.user_id
            )
            .returning(SubTasks)
        )

        try:
            response = (await self.db.execute(deactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")

            await self.activity_service.record_activity(
                    activity_data= UserActivityCreateRequestSchema(
                    activity_type= UserActivityType.SUBTASK_DELETED,
                    entity_type= ActivityEntityType.SUBTASKS,
                    entity_id= subtask_id,
                ),
                user= user
            )
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.exception("Subtask deactivation failed | subtask_id={}, user_id={}", subtask_id, user.user_id)
            raise HTTPException(status_code=500, detail="An error occurred while updating task")
        
        await self.db.commit()
        logger.info("Subtask Deactivated | task_id={}, user_id={}", response.subtask_id, user.user_id)
        return