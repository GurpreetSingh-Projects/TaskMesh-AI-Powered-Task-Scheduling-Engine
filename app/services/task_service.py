from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.tasks import *
from ..schemas import *
from .user_service import *

async def createTask(task_details: TaskCreate, db: AsyncSession):
    user = await getUser(task_details.user_id, db)
    
    new_task = Task(
        user_id= user.user_id,
        task_name= task_details.task_name,
        task_description= task_details.task_description,
        task_status= task_details.task_status,
    )
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task
    
async def getTask(task_id: int, db: AsyncSession):
    task = await db.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

async def getAllTasksByUser(user_id: int, db: AsyncSession):
    user = await getUser(user_id, db)
    
    tasks= (await db.execute(select(Task).where(Task.user_id == user_id))).scalars().all()
    return tasks

async def editTask(task_id, task_details: TaskUpdate, db: AsyncSession):
    task = await getTask(task_id, db)
    
    if task_details.task_name:
        task.task_name= task_details.task_name
    
    if task_details.task_description:
        task.task_description= task_details.task_description
    
    if task_details.task_status:
        task.task_status= task_details.task_status
        
    await db.commit()
    await db.refresh(task)
    return task
    
async def deleteTask(task_id: int, db: AsyncSession):
    task = await getTask(task_id, db)
    
    await db.delete(task)
    await db.commit()
    return

async def getAllTasks(db: AsyncSession):
    tasks= await db.execute(select(Task))
    return tasks.scalars().all()