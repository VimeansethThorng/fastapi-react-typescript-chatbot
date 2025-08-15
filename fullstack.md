# 🚀 FastAPI-React TypeScript Chatbot - Full Stack Architecture

## 🌟 Application Overview

This is a modern full-stack AI chatbot application built with FastAPI (backend) and React TypeScript (frontend). The application supports real-time chat, conversation management, and user authentication using SQLite for data persistence and pip for dependency management.

## ✨ Key Features

### Core Features
- 💬 **Real-time Chat** - Instant messaging with AI assistant
- 📚 **Conversation Management** - Persistent chat history
- 🔐 **User Authentication** - Secure JWT-based login system
- 📱 **Responsive Design** - Works on all devices

### Technical Features
- 🏗️ **Modern Architecture** - FastAPI + React + TypeScript
- � **Virtual Environment** - Clean Python dependency management with pip  
- 🚀 **One-command Setup** - Simple deployment
- 📊 **Rich Content** - Tables, code blocks, math equations
- 🐳 **Docker Support** - Full containerization with Docker Compose
- 🔧 **Health Monitoring** - Built-in health checks and status endpoints
- 📊 **Static File Integration** - Seamless frontend-backend integration

## 🏗️ Application Flow Diagram

```mermaid
graph TB
    %% User Interface Layer
    subgraph "Frontend (React + TypeScript)"
        UI[User Interface<br/>Rich Content Rendering]
        APP[App.tsx<br/>Main Application]
        CHATBOT[ChatBot.tsx<br/>Chat Interface] 
        COMPONENTS[Components<br/>MessageBubble, Input, etc.]
        API_CLIENT[api.ts<br/>HTTP Client]
        TYPES[types.ts<br/>TypeScript Definitions]
        MARKDOWN[React Markdown<br/>Tables, Code, Math]
        
        UI --> APP
        APP --> CHATBOT
        CHATBOT --> COMPONENTS
        CHATBOT --> API_CLIENT
        CHATBOT --> MARKDOWN
        API_CLIENT --> TYPES
    end
    
    %% Network Layer
    HTTP[HTTP/HTTPS Requests<br/>localhost:3000 → localhost:8000<br/>CORS Enabled]
    
    %% Backend Layer
    subgraph "Backend (FastAPI + pip)"
        MAIN[main_sqlite.py<br/>FastAPI App + CORS]
        MODELS[models.py<br/>Pydantic Models]
        CHAT_SERVICE[chat_service_sqlite.py<br/>OpenAI Integration]
        DB_MANAGER[database_sqlite.py<br/>SQLite Manager]
        CONFIG[config_sqlite.py<br/>Environment Config]
        REQUIREMENTS[requirements_sqlite.txt<br/>Python Dependencies]
    end
    
    %% Database Layer
    subgraph "Database (SQLite)"
        SQLITE[(chatbot.db<br/>Local Storage)]
        CONVERSATIONS[conversations table<br/>Chat Sessions]
        MESSAGES[messages table<br/>User + AI Messages]
        
        SQLITE --> CONVERSATIONS
        SQLITE --> MESSAGES
    end
    
    %% External Services
    OPENAI[OpenAI API<br/>GPT-4 Model]
    
    %% Connections
    API_CLIENT -.->|POST /chat<br/>GET /conversations<br/>DELETE /conversations| HTTP
    HTTP -.-> MAIN
    
    MAIN --> MODELS
    MAIN --> CHAT_SERVICE
    MAIN --> DB_MANAGER
    DB_MANAGER --> CONFIG
    
    CHAT_SERVICE --> DB_MANAGER
    DB_MANAGER --> SQLITE
    
    CHAT_SERVICE -.-> OPENAI
    
    %% Data Flow
    MAIN -.->|JSON Response| HTTP
    HTTP -.->|JSON Response| API_CLIENT
```

## Detailed Component Flow

```mermaid
sequenceDiagram
    participant User
    participant ChatBot as ChatBot.tsx
    participant API as api.ts
    participant FastAPI as main_sqlite.py
    participant ChatService as chat_service_sqlite.py
    participant DBManager as database_sqlite.py
    participant SQLite as chatbot.db
    participant OpenAI as OpenAI API
    
    %% Chat Flow
    User->>ChatBot: Types message
    ChatBot->>ChatBot: Add user message to UI
    ChatBot->>API: sendMessage(request)
    API->>FastAPI: POST /chat
    
    FastAPI->>DBManager: create_conversation (if new)
    DBManager->>SQLite: INSERT INTO conversations
    SQLite-->>DBManager: conversation_id
    
    FastAPI->>DBManager: save_message (user message)
    DBManager->>SQLite: INSERT INTO messages
    
    FastAPI->>DBManager: get_conversation_history
    DBManager->>SQLite: SELECT messages
    SQLite-->>DBManager: message history
    
    FastAPI->>ChatService: generate_response(query, history)
    ChatService->>OpenAI: chat_completion(prompt)
    OpenAI-->>ChatService: AI response
    ChatService-->>FastAPI: AI response
    
    FastAPI->>DBManager: save_message (assistant message)
    DBManager->>SQLite: INSERT INTO messages
    
    FastAPI-->>API: ChatResponse JSON
    API-->>ChatBot: Response data
    ChatBot->>ChatBot: Update UI with assistant message
    ChatBot->>User: Display conversation
```

## Component Architecture

```mermaid
graph LR
    subgraph "React Components"
        A[App.tsx] --> B[ChatBot.tsx]
        B --> C[MessageBubble.tsx]
        B --> D[MessageInput.tsx]
        B --> E[TypingIndicator.tsx]
        B --> F[AllConversations.tsx]
        B --> G[LoadingDots.tsx]
        B --> H[ConfirmDialog.tsx]
    end
    
    subgraph "API Layer"
        H[api.ts]
        I[types.ts]
    end
    
    subgraph "Backend Services"
        J[main_sqlite.py]
        K[chat_service_sqlite.py]
        L[database_sqlite.py]
        M[models.py]
        N[config_sqlite.py]
    end
    
    B --> H
    H --> I
    H --> J
    J --> K
    J --> L
    J --> M
    L --> N
```

## Database Schema

```mermaid
erDiagram
    CONVERSATIONS {
        int id PK
        string user_id
        timestamp created_at
    }
    
    MESSAGES {
        int id PK
        int conversation_id FK
        string role
        string content
        timestamp created_at
    }
    
    CONVERSATIONS ||--o{ MESSAGES : contains
```

## Project Structure

```
FastAPI-React/
├── backend/
│   ├── main_sqlite.py       # FastAPI application entry point
│   ├── models.py           # Pydantic models for request/response
│   ├── database_sqlite.py  # SQLite database manager
│   ├── chat_service_sqlite.py  # Chat service logic
│   ├── config_sqlite.py    # Configuration settings
│   └── requirements_sqlite.txt # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.tsx         # Main React component
    │   ├── api.ts          # API client functions
    │   ├── types.ts        # TypeScript type definitions
    │   └── components/     # React components
    │       ├── ChatBot.tsx
    │       ├── MessageBubble.tsx
    │       ├── MessageInput.tsx
    │       ├── TypingIndicator.tsx
    │       ├── AllConversations.tsx
    │       └── LoadingDots.tsx
    └── package.json        # Node.js dependencies
```

## Key Components

### Backend (FastAPI)

1. **main_sqlite.py**: The main FastAPI application with CORS middleware and API endpoints
2. **database_sqlite.py**: SQLite database connection and CRUD operations
3. **chat_service_sqlite.py**: Business logic for chat functionality
4. **models.py**: Pydantic models for data validation

### Frontend (React + TypeScript)

1. **App.tsx**: Main application component
2. **api.ts**: HTTP client for backend communication
3. **ChatBot.tsx**: Main chat interface component
4. **MessageBubble.tsx**: Individual message display
5. **MessageInput.tsx**: User input component

## Data Flow

1. User types message in React frontend
2. Frontend sends HTTP POST request to FastAPI backend
3. Backend processes message and stores in SQLite database
4. Backend returns response to frontend
5. Frontend displays the conversation

## API Endpoints

- `POST /chat`: Send a message and get response
- `GET /conversations/user/{user_id}`: Get user's conversations
- `POST /conversations`: Create new conversation
- `GET /conversations/{conversation_id}/messages`: Get conversation messages

## 🐳 Docker Deployment Architecture

### Deployment Modes

#### Production Mode
```mermaid
graph TB
    subgraph "Docker Container (Port 8000)"
        FASTAPI[FastAPI Server]
        STATIC[Static Files<br/>React Build]
        API[API Endpoints]
        DB[(SQLite Database)]
        
        FASTAPI --> STATIC
        FASTAPI --> API
        FASTAPI --> DB
    end
    
    CLIENT[Web Browser] --> FASTAPI
```

#### Development Mode
```mermaid
graph TB
    subgraph "Frontend Container (Port 3000)"
        REACT_DEV[React Dev Server<br/>Hot Reload]
        FRONTEND_SRC[Source Code<br/>Volume Mount]
        REACT_DEV --> FRONTEND_SRC
    end
    
    subgraph "Backend Container (Port 8000)"
        FASTAPI_DEV[FastAPI Server]
        API_ENDPOINTS[API Endpoints]
        HEALTH[Health Check]
        DB_DEV[(SQLite Database)]
        
        FASTAPI_DEV --> API_ENDPOINTS
        FASTAPI_DEV --> HEALTH
        FASTAPI_DEV --> DB_DEV
    end
    
    CLIENT[Web Browser] --> REACT_DEV
    REACT_DEV --> FASTAPI_DEV
```

### Docker Services Configuration

```yaml
# compose.yml
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend-dev:
    build:
      context: .
      target: frontend-dev
    ports:
      - "3000:3000"
    profiles:
      - dev
    volumes:
      - "./frontend/src:/app/src"
```

### Container Health Monitoring

- **Backend Health**: `/health` endpoint with database connectivity check
- **Frontend Health**: Development server status and compilation success
- **Docker Health Checks**: Built-in container monitoring with automatic restarts

## Technology Stack

- **Frontend**: React, TypeScript, CSS
- **Backend**: FastAPI, Python, Pydantic
- **Database**: SQLite
- **Communication**: HTTP/REST API with JSON
- **Development**: Node.js (frontend), Python (backend)
- **Containerization**: Docker, Docker Compose
- **Health Monitoring**: Built-in health checks and status endpoints
- **Deployment**: Multi-stage builds with development and production profiles

## Quick Start

### Docker Deployment (Recommended)
```bash
# Production mode
git checkout docker
docker-compose up -d

# Development mode  
docker-compose --profile dev up -d

# Access application
open http://localhost:8000  # Production
open http://localhost:3000  # Development
```

### Local Development
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_sqlite.txt
uvicorn main_sqlite:app --reload

# Frontend  
cd frontend
npm install
npm start
```
