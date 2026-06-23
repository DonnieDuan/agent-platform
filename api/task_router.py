from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas import TaskCreateRequest, TaskResponse
from models import Task, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskResponse], summary="获取所有任务")
def get_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse, summary="获取单个任务")
def get_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=TaskResponse, summary="创建任务")
def create_task(request: TaskCreateRequest, db: Session = Depends(get_db)):
    try:
        task = Task(title=request.title, description=request.description)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse, summary="更新任务")
def update_task(task_id: int, request: TaskCreateRequest, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        task.title = request.title
        task.description = request.description
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}", summary="删除任务")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        db.delete(task)
        db.commit()
        return {"message": "任务删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
