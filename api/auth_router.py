from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from models import User, get_db
from core.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    get_current_admin_user
)
from core.logging_config import get_logger
from datetime import datetime

logger = get_logger("auth_router")

router = APIRouter(prefix="/auth", tags=["认证"])


# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# 注册接口
@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        logger.warning(f"注册失败: 用户名已存在 - {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        logger.warning(f"注册失败: 邮箱已存在 - {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    
    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"用户注册成功: username={new_user.username}, email={new_user.email}")
    return new_user


# 登录接口
@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 查找用户
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user:
        logger.warning(f"登录失败: 用户不存在 - {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.hashed_password):
        logger.warning(f"登录失败: 密码错误 - username={login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 检查用户是否激活
    if not user.is_active:
        logger.warning(f"登录失败: 用户已被禁用 - username={login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被禁用",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 创建 JWT Token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    logger.info(f"用户登录成功: username={user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# 获取当前用户信息
@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    logger.info(f"获取用户信息: username={current_user.username}")
    return current_user


# 创建管理员用户（仅管理员可调用）
@router.post("/create-admin", response_model=UserResponse, summary="创建管理员用户")
async def create_admin(
    user_data: UserCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建管理员用户（仅管理员可调用）"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建管理员用户
    hashed_password = get_password_hash(user_data.password)
    new_admin = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=True
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    logger.info(f"管理员创建用户成功: admin={current_admin.username}, new_admin={new_admin.username}")
    return new_admin


# 初始化默认管理员
@router.post("/init-admin", summary="初始化默认管理员")
async def init_admin(db: Session = Depends(get_db)):
    """初始化默认管理员（仅在无用户时可用）"""
    # 检查是否已有用户
    existing_users = db.query(User).count()
    if existing_users > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="系统已有用户，无法初始化"
        )
    
    # 创建默认管理员
    hashed_password = get_password_hash("admin123")
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hashed_password,
        is_active=True,
        is_admin=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    logger.info(f"初始化默认管理员成功: username=admin")
    return {"message": "默认管理员创建成功", "username": "admin", "password": "admin123"}