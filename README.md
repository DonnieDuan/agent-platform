# 智能研发 Agent 协作平台

基于 FastAPI + DeepSeek LLM 构建的智能研发协作平台。

> **项目状态**: 当前为单机版原型，支持后续扩展 RBAC 权限模型、分布式部署和多 Agent 协同。

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
- **前端**: Alpine.js + TailwindCSS（轻量级响应式框架）

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

## LLM 接入说明

### DeepSeek-LLM 接入方式

本项目通过 **API 方式**接入 DeepSeek LLM，使用 LangChain 框架进行封装。

#### 配置要求

1. **API Key**：需在 [DeepSeek 平台](https://platform.deepseek.com/) 注册获取 API Key
2. **模型选择**：支持 `deepseek-chat`（对话模型）和 `deepseek-code`（代码模型）
3. **API 基础地址**：`https://api.deepseek.com/v1`

#### 配置示例（.env 文件）

```bash
# LLM 配置
LLM_MODEL_NAME=deepseek-chat
LLM_API_KEY=your_api_key_here
LLM_API_BASE=https://api.deepseek.com/v1
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.7
```

#### 本地部署说明（可选）

若需本地部署 DeepSeek 模型，硬件要求如下：

| 模型 | 显存要求 | 推荐配置 |
|------|---------|---------|
| DeepSeek-R1.5-8B | ≥ 24GB | RTX 4090 / A10 |
| DeepSeek-R1.5-70B | ≥ 128GB | A100 80GB x 2 |
| DeepSeek-V3-Coder | ≥ 48GB | RTX A6000 / H100 |

> 本地部署需修改 `agents/` 目录下的 Agent 实现，改用 HuggingFace Transformers 加载模型。

## 项目状态与扩展方向

### 当前状态

- ✅ 单机版原型，核心功能完整
- ✅ Agent 能力：代码生成、审查、文档编写
- ✅ 任务/项目管理模块
- ✅ 前端已升级为 Alpine.js + TailwindCSS
- ⚠️ 无用户认证体系（当前为公开访问）

### 扩展方向

1. **安全与权限**
   - 集成 OAuth2 / JWT 认证
   - 实现 RBAC 角色权限模型（管理员/开发者/访客）

2. **前端升级** ✅ 已完成
   - 已采用 Alpine.js + TailwindCSS 轻量方案
   - 支持响应式数据绑定和组件化
   - 可进一步升级为 Vue 3 + Pinia 或 React + TypeScript

3. **性能与可观测性** ✅ 部分完成
   - ✅ 已集成 logging 日志记录
   - 接入 Prometheus + Grafana 监控
   - 实现 Agent 超时重试机制

4. **分布式部署**
   - 使用 Celery 实现异步任务队列
   - 支持多节点部署和负载均衡

## 目录结构

```
agent-platform/
├── main.py                 # 应用入口（FastAPI 启动）
├── LICENSE                 # MIT 开源协议
├── pytest.ini              # pytest 测试配置
├── config/
│   └── settings.py         # 全局配置管理（Pydantic Settings）
├── core/
│   ├── __init__.py         # 核心模块（错误处理、任务管理）
│   └── logging_config.py   # 日志配置（文件+控制台输出）
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
├── tests/
│   ├── test_agents.py      # Agent 单元测试
│   └── test_api.py         # API 集成测试
├── frontend/
│   └── index.html          # 前端主页面（Alpine.js + TailwindCSS）
├── screenshots/
│   ├── agent-features.png  # Agent 功能截图
│   ├── task-management.png # 任务管理截图
│   ├── project-management.png # 项目管理截图
│   └── system-status.png   # 系统状态截图
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI 配置
└── .gitignore              # Git 忽略配置
```
