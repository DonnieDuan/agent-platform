from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from config.settings import settings
from api import router
from pathlib import Path
from core.logging_config import logger

database_available = False
db_error_message = ""

try:
    from models import engine, Base
    Base.metadata.create_all(bind=engine)
    database_available = True
    logger.info("✅ 数据库连接成功")
    
    from models import SessionLocal
    from models import User
    from core.auth import get_password_hash
    
    db = SessionLocal()
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if not existing_admin:
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
        logger.info("✅ 默认管理员创建成功: admin / admin123")
    db.close()
except Exception as e:
    database_available = False
    db_error_message = str(e)
    logger.warning(f"⚠️ 数据库连接失败: {e}")
    logger.warning("   注意: 数据库相关功能将不可用，但 Agent 功能仍可使用")

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# 静态文件目录
frontend_dir = Path(__file__).parent / "frontend"
static_dir = frontend_dir / "static"

# 创建静态文件目录
static_dir.mkdir(parents=True, exist_ok=True)

# CSS 和 JS 目录
css_dir = static_dir / "css"
js_dir = static_dir / "js"
css_dir.mkdir(parents=True, exist_ok=True)
js_dir.mkdir(parents=True, exist_ok=True)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 前端页面路由
@app.get("/")
def root():
    return FileResponse(str(frontend_dir / "index.html"))

# API 路由
app.include_router(router)

# 健康检查
@app.get("/health")
def health_check():
    redis_status = "unavailable"
    qdrant_status = "unavailable"
    llm_status = "unavailable"
    
    try:
        from memory.redis_store import RedisStore
        redis = RedisStore()
        redis.client.ping()
        redis_status = "available"
    except Exception:
        pass
    
    try:
        from memory.vector_store import VectorStore
        qdrant = VectorStore()
        qdrant.get_collection_info()
        qdrant_status = "available"
    except Exception:
        pass
    
    try:
        from agents.code_generator import CodeGeneratorAgent
        agent = CodeGeneratorAgent()
        llm_status = "available"
    except Exception:
        pass

    return {
        "status": "running",
        "database": "available" if database_available else f"unavailable ({db_error_message})",
        "redis": redis_status,
        "qdrant": qdrant_status,
        "llm": llm_status
    }


@app.middleware("http")
async def db_availability_middleware(request: Request, call_next):
    if not database_available and request.url.path.startswith("/tasks"):
        return JSONResponse(
            status_code=503,
            content={"error": "数据库服务不可用", "detail": db_error_message}
        )
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)