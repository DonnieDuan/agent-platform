# 智能研发 Agent 协作平台

基于 FastAPI + DeepSeek LLM 构建的智能研发协作平台。

## 功能特性

- 🤖 **代码生成 Agent** - 基于 DeepSeek LLM 自动生成代码
- 🔍 **代码审查 Agent** - 自动化代码审查和质量评估
- 📝 **文档编写 Agent** - 自动生成项目文档
- 📋 **任务管理** - 完整的任务 CRUD 操作
- 📁 **项目管理** - 多项目并行管理
- 🧠 **分层记忆架构** - Qdrant 向量数据库 + Redis 缓存

## 界面预览

### 🤖 Agent 功能
![Agent 功能](screenshots/agent-features.png)

### 📋 任务管理
![任务管理](screenshots/task-management.png)

### 📁 项目管理
![项目管理](screenshots/project-management.png)

### 📊 系统状态
![系统状态](screenshots/system-status.png)

## 技术栈

- **后端框架**: FastAPI
- **大语言模型**: DeepSeek LLM、LangChain
- **数据库**: SQLite / MySQL
- **向量数据库**: Qdrant
- **缓存**: Redis
- **前端**: HTML5 + CSS3 + JavaScript

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python main.py
```

### 访问地址

- 前端页面: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API 接口

| 接口 | 方法 | 路径 |
|------|------|------|
| 代码生成 | POST | /agent/code/generate |
| 代码审查 | POST | /agent/code/review |
| 文档编写 | POST | /agent/document/write |
| 获取任务列表 | GET | /tasks/ |
| 创建任务 | POST | /tasks/ |
| 获取项目列表 | GET | /projects/ |
| 创建项目 | POST | /projects/ |

## 目录结构

```
agent-platform/
├── main.py                 # 应用入口（FastAPI 启动）
├── config/
│   └── settings.py         # 全局配置管理（Pydantic Settings）
├── models/
│   └── __init__.py         # 数据库模型（SQLAlchemy ORM）
├── api/
│   ├── __init__.py         # API 路由聚合
│   ├── agent_router.py     # Agent 相关接口
│   ├── task_router.py      # 任务管理接口
│   └── project_router.py   # 项目管理接口
├── schemas/
│   └── __init__.py         # 数据校验模型（Pydantic）
├── agents/
│   ├── base.py             # Agent 抽象基类
│   ├── code_generator.py   # 代码生成 Agent
│   ├── code_reviewer.py    # 代码审查 Agent
│   └── document_writer.py  # 文档编写 Agent
├── memory/
│   ├── memory_manager.py   # 记忆管理器
│   ├── vector_store.py     # 向量数据库（Qdrant）
│   └── redis_store.py      # 缓存（Redis）
├── tools/
│   └── __init__.py         # 工具模块（Git/Docker/CI/CD）
├── frontend/
│   ├── index.html          # 前端主页面
│   ├── css/
│   │   └── style.css       # 样式文件
│   └── js/
│       └── app.js          # 前端逻辑
├── screenshots/
│   ├── agent-features.png  # Agent 功能截图
│   ├── task-management.png # 任务管理截图
│   ├── project-management.png # 项目管理截图
│   └── system-status.png   # 系统状态截图
└── .gitignore              # Git 忽略配置
```
