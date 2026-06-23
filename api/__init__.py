from fastapi import APIRouter
from api.agent_router import router as agent_router
from api.task_router import router as task_router
from api.project_router import router as project_router
from api.auth_router import router as auth_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(agent_router)
router.include_router(task_router)
router.include_router(project_router)
