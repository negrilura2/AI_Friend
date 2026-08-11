# AI Friend

面向 **AI 角色陪伴与多轮对话** 的全栈应用：支持角色创建与广场浏览、好友会话、**SSE 流式对话**、**ASR / TTS**、基于 **LanceDB** 的向量检索（RAG）以及周期性 **长期记忆摘要**。
访问地址：https://app8026.acapp.acwing.com.cn/
## 功能概览

| 模块 | 说明 |
|------|------|
| 账号 | 注册 / 登录 / 登出、JWT（Access + Refresh Cookie）、静默刷新 |
| 用户 | 资料与头像更新 |
| 角色 | 创建 / 编辑 / 删除、预设音色列表、首页分页与关键词搜索 |
| 好友 | 列表、添加（或创建会话）、移除 |
| 对话 | LangGraph Agent（工具调用）、流式文本 + 流式 TTS 音频（SSE） |
| 语音 | 音频上传 ASR 转写（WebSocket） |
| 记忆 | 每累计一定轮次触发记忆子图，更新好友维度长期记忆 |
| 知识库 | LanceDB 向量存储 + 相似度检索（需预先构建索引） |

## 技术栈

- **后端**：Python · Django · Django REST Framework · SQLite · LangGraph · LangChain · LanceDB · SimpleJWT  
- **前端**：Vue 3 · Vite · Pinia · Vue Router · Tailwind CSS · DaisyUI · `@microsoft/fetch-event-source`

## 仓库结构

```
AI_Friend/
├── backend/                 # Django 项目
│   ├── backend/             # 设置与入口（settings / urls / wsgi）
│   ├── web/                 # 业务应用（models / views / documents）
│   └── manage.py
├── frontend/                # Vue 3 SPA（开发独立运行；构建产物输出到 Django static）
└── README.md
```

生产构建时，前端 `vite build` 默认输出到 `backend/static/frontend`，由 Django 托管静态资源。

## 环境要求

- **Python** 3.11+（建议与 Django 6.x 兼容的版本）
- **Node.js** `^20.19.0` 或 `>=22.12.0`（见 `frontend/package.json`）

## 环境变量（后端）

在 `backend/` 下创建 `.env`（项目已使用 `python-dotenv` 加载），示例：

```env
# 大模型与向量（OpenAI 兼容接口）
API_KEY=your_api_key
API_BASE=https://api.example.com/v1

# 语音：ASR / TTS 使用的 WebSocket 网关（与现有代码一致）
WSS_URL=wss://your-gateway/...

# 自定义音色相关 HTTP 接口（若使用自定义音色 API）
VOICE_URL=https://your-voice-api/...
```

> **说明**：嵌入模型在代码中配置为 `text-embedding-v4`（见 `custom_embeddings.py`），对话模型为 `deepseek-v4-pro`（见 `graph.py` / `memory/graph.py`）。部署时请按实际供应商调整模型名与 URL。

## 本地开发

### 1. 后端

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate   # Linux / macOS

pip install django djangorestframework djangorestframework-simplejwt django-cors-headers python-dotenv pillow
pip install langchain-core langchain-openai langchain-community langgraph langchain-text-splitters
pip install lancedb openai websockets

python manage.py migrate
python manage.py createsuperuser   # 可选，用于 Django Admin
python manage.py runserver 0.0.0.0:8000
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

将 `frontend/src/js/config/config.js` 中 `platform` 设为 `'vue'`，使接口指向 `http://127.0.0.1:8000`，与本地后端一致。

### 3. 知识库索引（可选）

若需启用 RAG 工具 `search_knowledge_base`，请：

1. 将语料保存为 `backend/web/documents/data.txt`。  
2. 在 `backend` 目录下进入 Django Shell 执行入库：

```bash
cd backend
python manage.py shell
```

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

成功后会在 `web/documents/lancedb_storage` 生成 LanceDB 数据（需已配置 `API_KEY` / `API_BASE` 用于 Embedding）。

## API 约定要点

- 除登录、注册、首页等接口外，多数业务接口需 **Bearer Token**（`Authorization: Bearer <access>`）。
- 对话接口返回 **`text/event-stream`（SSE）**，前端通过 `streamApi` 处理流及 **401 刷新重试**。
- 媒体文件开发环境下由 Django `MEDIA_URL` / `MEDIA_ROOT` 提供；生产环境请修改 `settings.py` 中 `ALLOWED_HOSTS`、`MEDIA_URL` 与 HTTPS Cookie 策略。
