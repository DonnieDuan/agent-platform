from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas import ProjectCreateRequest, ProjectResponse
from models import Project, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectResponse], summary="获取所有项目")
def get_projects(db: Session = Depends(get_db)):
    try:
        projects = db.query(Project).all()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse, summary="获取单个项目")
def get_project(project_id: int, db: Session = Depends(get_db)):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ProjectResponse, summary="创建项目")
def create_project(request: ProjectCreateRequest, db: Session = Depends(get_db)):
    try:
        project = Project(name=request.name, description=request.description)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{project_id}", response_model=ProjectResponse, summary="更新项目")
def update_project(project_id: int, request: ProjectCreateRequest, db: Session = Depends(get_db)):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        project.name = request.name
        project.description = request.description
        db.commit()
        db.refresh(project)
        return project
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}", summary="删除项目")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        db.delete(project)
        db.commit()
        return {"message": "项目删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
