# FastAPI-React Chatbot Application

## Application Architecture

This is a full-stack chatbot application built with FastAPI (backend) and React (frontend) using SQLite as the database.

## Application Flow Diagram

```mermaid
graph TB
    %% User Interface Layer
    subgraph "Frontend (React + TypeScript)"
        UI[User Interface]
        APP[App.tsx]
        CHATBOT[ChatBot.tsx]
        COMPONENTS[Components]
        API_CLIENT[api.ts]
        TYPES[types.ts]
        
        UI --> APP
        APP --> CHATBOT
        CHATBOT --> COMPONENTS
        CHATBOT --> API_CLIENT
        API_CLIENT --> TYPES
    end
    
    %% Network Layer
    HTTP[HTTP Requests<br/>localhost:3000 → localhost:8000]
    
    %% Backend Layer
    subgraph "Backend (FastAPI)"
        MAIN[main_sqlite.py<br/>FastAPI App + CORS]
        MODELS[models.py<br/>Pydantic Models]
        CHAT_SERVICE[chat_service_sqlite.py<br/>Business Logic]
        DB_MANAGER[database_sqlite.py<br/>Database Manager]
        CONFIG[config_sqlite.py<br/>Configuration]
    end
    
    %% Database Layer
    subgraph "Database (SQLite)"
        SQLITE[(chatbot.db)]
        CONVERSATIONS[conversations table]
        MESSAGES[messages table]
        
        SQLITE --> CONVERSATIONS
        SQLITE --> MESSAGES
    end
    
    %% Connections
    API_CLIENT -.->|POST /chat<br/>GET /conversations| HTTP
    HTTP -.-> MAIN
    
    MAIN --> MODELS
    MAIN --> CHAT_SERVICE
    MAIN --> DB_MANAGER
    DB_MANAGER --> CONFIG
    
    CHAT_SERVICE --> DB_MANAGER
    DB_MANAGER --> SQLITE
    
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
    
    FastAPI->>ChatService: generate_response
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

## Technology Stack

- **Frontend**: React, TypeScript, CSS
- **Backend**: FastAPI, Python, Pydantic
- **Database**: SQLite
- **Communication**: HTTP/REST API with JSON
- **Development**: Node.js (frontend), Python (backend)
