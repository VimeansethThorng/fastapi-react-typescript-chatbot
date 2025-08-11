# 🚀 FastAPI Backend Documentation

## Overview

This is a FastAPI-based backend for an AI chatbot application that uses SQLite for data persistence and OpenAI's GPT API for chat responses. The backend provides a comprehensive RESTful API for managing conversations and processing chat messages with modern Python dependency management using Poetry.

## ✨ Key Features

- 🤖 **AI Chat Responses** - OpenAI GPT integration
- 🔐 **User Authentication** - JWT-based secure authentication
- 📚 **Conversation Management** - Persistent chat history
- 🗄️ **SQLite Database** - Lightweight, file-based storage
- 📦 **Poetry** - Modern Python dependency management

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "FastAPI Backend Architecture"
        API[FastAPI Application<br/>main_sqlite.py]
        MODELS[Pydantic Models<br/>models.py]
        AUTH[Authentication Service<br/>auth_service.py]
        CHAT_SERVICE[Chat Service<br/>chat_service_sqlite.py]
        DB[Database Manager<br/>database_sqlite.py]
        CONFIG[Configuration<br/>config_sqlite.py]
        SQLITE[(SQLite Database<br/>chatbot.db)]
        
        API --> MODELS
        API --> AUTH
        API --> CHAT_SERVICE
        API --> DB
        CHAT_SERVICE --> CONFIG
        DB --> SQLITE
        CHAT_SERVICE --> |OpenAI API| OPENAI[OpenAI GPT-4]
    end
```

## 📦 Dependencies & Setup

### Poetry Configuration
The backend uses Poetry for modern Python dependency management:

```toml
[tool.poetry.dependencies]
python = ">=3.9,<4.0"
fastapi = "^0.104.1"
uvicorn = "^0.24.0"
openai = "^1.3.7"
python-dotenv = "^1.0.0"
pydantic = "^2.9.2"
python-multipart = "^0.0.6"
passlib = "^1.7.4"
python-jose = "^3.3.0"
bcrypt = "^4.0.1"
requests = "^2.32.4"
```

### Environment Variables
Create a `.env` file based on `.env.example`:
```bash
# OpenAI API Key for chat completions
OPENAI_API_KEY=your_openai_api_key_here

# JWT Secret Key for authentication
JWT_SECRET_KEY=your_secure_random_string_here

# Database configuration
DATABASE_URL=sqlite:///chatbot.db
```

## Core Components

### 1. FastAPI Application (`main_sqlite.py`)

The main application entry point that defines all API endpoints and handles HTTP requests.

#### Key Features:
- **CORS Middleware**: Allows requests from React frontend (localhost:3000)
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **Logging**: Structured logging for debugging and monitoring
- **Lifecycle Events**: Database connection management on startup/shutdown

#### API Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check endpoint |
| `POST` | `/chat` | Send message and get AI response |
| `POST` | `/conversations` | Create new conversation |
| `GET` | `/conversations/{id}/messages` | Get conversation messages |
| `GET` | `/conversations/user/{user_id}` | Get user's conversations |
| `GET` | `/conversations/{id}/full` | Get conversation with messages |
| `DELETE` | `/conversations/{id}` | Delete conversation |

#### Request/Response Flow:
```mermaid
sequenceDiagram
    participant Client
    participant FastAPI as main_sqlite.py
    participant DB as database_sqlite.py
    participant Chat as chat_service_sqlite.py
    participant OpenAI
    
    Client->>FastAPI: POST /chat
    FastAPI->>DB: create_conversation (if new)
    FastAPI->>DB: save_message (user)
    FastAPI->>DB: get_conversation_history
    FastAPI->>Chat: generate_response
    Chat->>OpenAI: API call
    OpenAI-->>Chat: AI response
    Chat-->>FastAPI: formatted response
    FastAPI->>DB: save_message (assistant)
    FastAPI-->>Client: ChatResponse
```

### 2. Data Models (`models.py`)

Pydantic models that define the data structure and validation for API requests and responses.

#### Models:

```python
# Request Models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    user_id: str = "default_user"

class ConversationCreate(BaseModel):
    user_id: str

# Response Models
class ChatResponse(BaseModel):
    response: str
    conversation_id: int

class ConversationResponse(BaseModel):
    id: int
    user_id: str
```

#### Benefits:
- **Type Safety**: Automatic validation and type checking
- **Documentation**: Auto-generated API documentation
- **Serialization**: Automatic JSON serialization/deserialization

### 3. Database Manager (`database_sqlite.py`)

Handles all database operations with SQLite, providing a clean abstraction layer.

#### Database Schema:

```sql
-- Conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

#### Key Methods:

| Method | Purpose |
|--------|---------|
| `connect()` | Establish database connection and create tables |
| `create_conversation()` | Create new conversation for user |
| `save_message()` | Store user or assistant message |
| `get_conversation_history()` | Retrieve message history |
| `get_all_conversations()` | Get user's conversation list with metadata |
| `delete_conversation()` | Remove conversation and all messages |

#### Features:
- **Connection Management**: Proper connection lifecycle
- **Error Handling**: Graceful error handling with logging
- **Data Integrity**: Foreign key constraints and data validation
- **Optimized Queries**: Efficient SQL with proper indexing

### 4. Chat Service (`chat_service_sqlite.py`)

Handles AI response generation using OpenAI's GPT-3.5-turbo model.

#### Features:
- **OpenAI Integration**: Direct API calls to GPT-3.5-turbo
- **Message Formatting**: Converts database format to OpenAI format
- **Error Handling**: Fallback responses for API failures
- **Configurable Parameters**: Model settings (temperature, max_tokens)

#### Message Flow:
```python
# Input: SQLite tuples [(role, content), ...]
messages = [("user", "Hello"), ("assistant", "Hi there!")]

# Formatted for OpenAI API
formatted = [
    {"role": "system", "content": "You are a helpful assistant chatbot."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
]
```

### 5. Configuration (`config_sqlite.py`)

Manages environment variables and application settings.

#### Settings:
- **OpenAI API Key**: Loaded from `.env` file
- **Database URL**: SQLite database path
- **Environment Variables**: Secure configuration management

## Data Flow

### 1. User Sends Message
```
Frontend → POST /chat → FastAPI → Database (save user message)
```

### 2. AI Response Generation
```
FastAPI → Database (get history) → Chat Service → OpenAI API → AI Response
```

### 3. Response Storage and Return
```
AI Response → Database (save assistant message) → FastAPI → Frontend
```

## Error Handling

### HTTP Status Codes:
- **200**: Success
- **404**: Conversation not found
- **500**: Internal server error

### Error Response Format:
```json
{
    "detail": "Error description"
}
```

### Logging Levels:
- **INFO**: Normal operations, connections
- **ERROR**: Exceptions, API failures
- **WARNING**: Non-critical issues

## Security Features

### 1. CORS Configuration
```python
allow_origins=["http://localhost:3000"]  # Restrict to frontend
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### 2. Environment Variables
- API keys stored in `.env` file (not committed to git)
- Database path configurable
- Secure credential management

### 3. SQL Injection Prevention
- Parameterized queries
- SQLite driver built-in protection
- Input validation through Pydantic

## Performance Considerations

### Database Optimizations:
- **Indexes**: Primary keys for fast lookups
- **Connection Reuse**: Single connection with thread safety
- **Efficient Queries**: Optimized SQL with proper joins

### API Optimizations:
- **Async Support**: FastAPI async capabilities
- **Response Models**: Efficient JSON serialization
- **Error Caching**: Graceful degradation

## Development Setup

### 1. Environment Variables (`.env`):
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=chatbot.db
```

### 2. Dependencies (`requirements_sqlite.txt`):
```
fastapi
uvicorn
openai
python-dotenv
pydantic
```

### 3. Running the Server:
```bash
# Development
uvicorn main_sqlite:app --reload --port 8000

# Production
python main_sqlite.py
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Database Management

### Initial Setup:
- Tables created automatically on first connection
- No manual database setup required

### Data Persistence:
- All data stored in `chatbot.db` file
- Conversation history preserved between sessions
- User data linked by `user_id`

## Monitoring and Debugging

### Logging:
```python
# Log levels and format
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Health Check:
```bash
curl http://localhost:8000/
# Response: {"message": "Chatbot API is running with SQLite"}
```

## Scalability Considerations

### Current Limitations:
- SQLite single-writer limitation
- In-memory OpenAI client
- Local file storage

### Future Improvements:
- PostgreSQL for better concurrency
- Redis for caching
- Load balancing for multiple instances
- Message queues for async processing

## Testing

### Unit Tests:
- Database operations
- API endpoints
- Error handling
- Model validation

### Integration Tests:
- End-to-end conversation flow
- Database consistency
- OpenAI API integration
