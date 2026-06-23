from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500, detail: str = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail


async def error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.error(f"Error: {exc.message} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": exc.detail}
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error(f"HTTP Error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "服务器内部错误", "detail": str(exc)}
    )


class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.task_id_counter = 1

    def create_task(self, title: str, description: str = None) -> dict:
        task_id = self.task_id_counter
        self.task_id_counter += 1
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": "pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> dict:
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> list:
        return list(self.tasks.values())

    def update_task(self, task_id: int, **kwargs) -> dict:
        task = self.tasks.get(task_id)
        if task:
            task.update(kwargs)
            task["updated_at"] = datetime.now()
        return task

    def delete_task(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


task_manager = TaskManager()
