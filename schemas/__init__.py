from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class AgentTaskRequest(BaseModel):
    task: str = Field(..., description="任务描述")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")


class AgentResponse(BaseModel):
    agent: str = Field(..., description="Agent 名称")
    task: str = Field(..., description="任务描述")
    result: str = Field(..., description="执行结果")
    status: str = Field(..., description="状态: completed 或 failed")


class TaskCreateRequest(BaseModel):
    title: str = Field(..., description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")


class TaskResponse(BaseModel):
    id: int = Field(..., description="任务 ID")
    title: str = Field(..., description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    status: str = Field(..., description="任务状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")


class ProjectResponse(BaseModel):
    id: int = Field(..., description="项目 ID")
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")
    created_at: datetime = Field(..., description="创建时间")


class MemorySaveRequest(BaseModel):
    text: str = Field(..., description="记忆内容")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class MemorySearchRequest(BaseModel):
    query: str = Field(..., description="查询内容")
    limit: int = Field(5, description="返回数量")


class MemoryResponse(BaseModel):
    text: str = Field(..., description="记忆内容")
    score: float = Field(..., description="匹配分数")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    detail: Optional[str] = Field(None, description="详细信息")


class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="服务状态")
    database: str = Field(..., description="数据库连接状态")
    redis: str = Field(..., description="Redis 连接状态")
    qdrant: str = Field(..., description="Qdrant 连接状态")
    llm: str = Field(..., description="LLM 服务状态")
