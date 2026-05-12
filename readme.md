# FastAPI + React TypeScript Chatbot

A modern, full-stack AI chatbot with user authentication, persistent conversations, and Retrieval-Augmented Generation (RAG) — upload PDFs, TXT files, or paste any web URL to give the AI private context.

## Features

### Chat
- Real-time chat with Claude (Anthropic) AI
- Persistent conversation history per user
- Create, switch, and delete conversations
- Rich content rendering: tables, code blocks, math equations (KaTeX)
- Typing indicator and auto-scroll

### RAG (Knowledge Base)
- Upload **PDF** or **TXT** files into ChromaDB
- Ingest any **website URL** — the page is fetched, stripped, and embedded automatically
- Personal documents (per-user) or Global documents (visible to all users)
- Semantic search via OpenAI `text-embedding-3-small`
- Relevant context injected into every chat message automatically

### Authentication
- JWT-based register/login
- All conversations and documents are scoped to the authenticated user

### Infrastructure
- Docker + docker-compose for one-command deployment
- Full pytest test suite (49 tests) covering auth, chat, conversations, and RAG

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Custom CSS |
| Backend | FastAPI, Python 3.10 |
| Database | SQLite |
| Vector DB | ChromaDB |
| Embeddings | OpenAI `text-embedding-3-small` |
| AI | Anthropic Claude (via `anthropic` SDK) |
| Auth | JWT (python-jose + passlib) |
| Deps | Poetry (backend), npm (frontend) |

## Prerequisites

- Node.js 16+
- Python 3.10+ (or Docker)
- API keys: `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`

## Quick Start

### Option A — Docker (recommended)

```bash
cp backend/.env.example backend/.env
# Fill in your API keys in backend/.env
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Option B — Manual

**Backend**
```bash
cd backend
pip install -r requirements_sqlite.txt
# or: poetry install
uvicorn main_sqlite:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

### Environment Variables

Create `backend/.env`:
```env
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
SECRET_KEY=any_random_string
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

### Auth
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login, returns JWT |
| `GET` | `/auth/me` | Current user info |

### Chat
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat` | Send message, get AI response |

### Conversations
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/conversations` | List user conversations |
| `GET` | `/conversations/{id}/full` | Full conversation + messages |
| `DELETE` | `/conversations/{id}` | Delete conversation |

### Documents (RAG)
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/documents/upload` | Upload PDF or TXT file |
| `POST` | `/documents/upload-url` | Ingest a web page by URL |
| `GET` | `/documents` | List accessible documents |
| `DELETE` | `/documents/{id}` | Delete document + embeddings |

## Project Structure

```
fastapi-react-typescript-chatbot/
├── backend/
│   ├── main_sqlite.py        # FastAPI app, all endpoints
│   ├── models.py             # Pydantic request/response models
│   ├── database_sqlite.py    # SQLite CRUD layer
│   ├── auth_service.py       # JWT auth logic
│   ├── chat_service_sqlite.py# Claude API integration
│   ├── rag_service.py        # ChromaDB + OpenAI embeddings + URL fetch
│   ├── config_sqlite.py      # Settings from env
│   ├── requirements_sqlite.txt
│   └── pyproject.toml        # Poetry config
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── ChatBot.tsx
│       │   ├── DocumentPanel.tsx  # File & URL RAG panel
│       │   ├── MessageBubble.tsx
│       │   ├── MessageInput.tsx
│       │   ├── AllConversations.tsx
│       │   ├── TypingIndicator.tsx
│       │   ├── LoadingDots.tsx
│       │   └── ConfirmDialog.tsx
│       ├── api.ts
│       ├── types.ts
│       └── App.tsx
├── test/
│   ├── conftest.py           # Shared fixtures, mocked ChromaDB
│   ├── test_auth.py
│   ├── test_chat.py
│   ├── test_conversations.py
│   └── test_rag.py
├── pytest.ini
└── docker-compose.yml
```

## Running Tests

```bash
pip install -r backend/requirements_sqlite.txt pytest beautifulsoup4 httpx
pytest test/ -v
```

## API Docs

FastAPI auto-generates interactive docs when the backend is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
