from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks & Subtasks"])

@router.get("/")
async def get_tasks():
    pass