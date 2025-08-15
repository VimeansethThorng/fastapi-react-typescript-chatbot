
# 🤖 FastAPI-React TypeScript AI Chatbot

A modern, full-stack AI chatbot application built with React (TypeScript) frontend ### Prerequisites

Before running the application locally, make sure you have:

- **Node.js** (v16 or higher) and **npm**
- **Python** (v3.8.1 or higher) 
- **pip** (usually comes with Python)│   ├── config_sqlite.py         # Configuration
│   ├── requirements_sqlite.txt  # Python dependencies
│   └── chatbot.db               # SQLite database (auto-created)*OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/))API backend, featuring conversation management, real-time chat, and AI-powered responses using OpenAI's GPT model.

## ✨ Features

### Core Chat Features
- 💬 **Real-time Chat Interface** - Seamless conversation with AI assistant
- 📚 **Conversation History** - All chats are saved and retrievable  
- 🗑️ **Delete Conversations** - Remove unwanted conversation history
- 🔄 **Auto-refresh** - Conversation list updates automatically every 30 seconds
- 👤 **User Avatars** - Visual distinction between user and AI messages
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Clean, professional interface with custom CSS styling
- 📊 **Rich Content Support** - Tables, code blocks, and mathematical equations

### Core Chat Features
- � **Real-time Chat Interface** - Seamless conversation with AI assistant
- 📚 **Conversation History** - All chats are saved and retrievable  
- 🗑️ **Delete Conversations** - Remove unwanted conversation history
- 🔄 **Auto-refresh** - Conversation list updates automatically every 30 seconds
- � **User Avatars** - Visual distinction between user and AI messages
- � **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Clean, professional interface with custom CSS styling
- � **Rich Content Support** - Tables, code blocks, and mathematical equations

### Technical Features
- 🚀 **One-command Setup** - Start entire stack with a single script
- � **Python Virtual Environment** - Clean dependency isolation with pip
- 🔐 **User Authentication** - JWT-based secure login system
- 🌐 **CORS Support** - Seamless frontend-backend communication
- 🐳 **Docker Support** - Full containerized deployment with Docker Compose
- 🔧 **Environment Configuration** - Easy setup with environment variables

## 🏗️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **React Markdown** with syntax highlighting
- **KaTeX** for mathematical equations
- **Custom CSS** with responsive design
- **Modern UI Components** with animations

### Backend  
- **FastAPI** (Python web framework)
- **User Authentication** with JWT tokens
- **Virtual Environment** with pip for dependency management
- **SQLite** database for conversation storage
- **OpenAI API** for AI responses
- **CORS** enabled for frontend communication
- **Pydantic** for data validation

### Development & Deployment
- **GitHub CLI** for repository management
- **Hot reload** for development
- **Environment variables** with `.env.example`
- **Comprehensive `.gitignore`**
- **Docker & Docker Compose** for containerized deployment
- **Multi-stage Docker builds** for optimized production images

## � Docker Setup

This project includes full Docker support with both development and production configurations.

### Prerequisites for Docker
- Docker (v20.10 or higher)
- Docker Compose (v2.0 or higher)

### Docker Quick Start

1. **Switch to Docker branch** (contains all Docker files):
```bash
git checkout docker
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. **Run with Docker Compose**:
```bash
# Production mode
docker-compose up -d

# Development mode (with hot reload)
docker-compose --profile dev up -d

# View logs
docker-compose logs -f
```

### Docker Services

- **Backend**: FastAPI server with SQLite database
- **Frontend**: React TypeScript application 
- **Frontend-dev** (dev profile): Development server with hot reload

### Environment Configuration

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### Docker Commands

```bash
# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# View service status  
docker-compose ps

# Check logs for specific service
docker-compose logs backend
docker-compose logs frontend-dev
```

## 🚀 Local Development Setup

### Prerequisites

Before running the application, make sure you have:

- **Node.js** (v16 or higher) and **npm**
- **Python** (v3.8.1 or higher) 
- **OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/))

### Using the Start Script

The easiest way to run the application locally is using the provided start script:

```bash
./start.sh
```

This script will:
- 🔧 Set up Python virtual environment if not already created
- 📦 Install all backend dependencies using pip
- 📦 Install all frontend dependencies using npm
- 🚀 Start both backend and frontend servers
- 🔄 Provide graceful shutdown with Ctrl+C

### Manual Local Setup

If you prefer to set up each part manually:
```

This script will:
- 🔧 Set up Python virtual environment if not already created
- 📦 Install all backend dependencies using pip
- 📦 Install all frontend dependencies using npm
- 🚀 Start both backend and frontend servers
- 🔄 Provide graceful shutdown with Ctrl+C

### Manual Local Setup

If you prefer to set up each part manually:

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd FastAPI-React-TypeSciript-chatbot
```

### 2. Backend Setup

#### Option A: Using pip (Recommended)
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv .venv
```

#### Activate Virtual Environment
```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### Install Python Dependencies
```bash
pip install -r requirements_sqlite.txt
```

#### Set Up Environment Variables
Create a `.env` file in the `backend` directory:
```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd ../frontend
```

#### Install Node.js Dependencies
```bash
npm install
```

## 🏃‍♂️ Running the Application

You need to run both the backend and frontend servers simultaneously.

### 1. Start the Backend Server

Open a terminal, navigate to the backend directory, and run:

```bash
cd backend
source .venv/bin/activate  # Activate virtual environment
python main_sqlite.py
```

The backend server will start on: **http://localhost:8000**

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:database_sqlite:Successfully connected to SQLite database: chatbot.db
INFO:database_sqlite:SQLite tables created successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. Start the Frontend Server

Open a **new terminal**, navigate to the frontend directory, and run:

```bash
cd frontend
npm start
```

The frontend application will start on: **http://localhost:3000**

You should see output like:
```
Compiled successfully!

You can now view frontend in the browser.
  Local:            http://localhost:3000
  On Your Network:  http://10.x.x.x:3000
```

### 3. Access the Application

Open your web browser and go to: **http://localhost:3000**

## 📖 Usage

1. **Start Chatting**: Type your message in the input field and press Enter or click Send
2. **View History**: All conversations appear in the left sidebar
3. **Switch Conversations**: Click on any conversation in the sidebar to resume it
4. **Delete Conversations**: Hover over a conversation and click the delete button (🗑️)
5. **New Conversation**: Click the "➕ New" button to start a fresh conversation
6. **Auto-refresh**: The conversation list automatically updates every 30 seconds

## 🔧 API Endpoints

The backend provides the following REST API endpoints:

- `GET /` - Health check
- `POST /chat` - Send a message to the AI
- `POST /conversations` - Create a new conversation
- `GET /conversations/user/{user_id}` - Get all conversations for a user
- `GET /conversations/{conversation_id}/messages` - Get messages for a conversation
- `GET /conversations/{conversation_id}/full` - Get full conversation with messages
- `DELETE /conversations/{conversation_id}` - Delete a conversation

## 📁 Project Structure

```
FastAPI-React-TypeScript-Chatbot/
├── 🐳 Docker Configuration (docker branch)
│   ├── Dockerfile               # Multi-stage build for production
│   ├── compose.yml              # Docker Compose configuration
│   ├── .dockerignore           # Docker ignore patterns
│   ├── .env.example            # Environment template
│   └── DOCKER.md               # Docker documentation
├── backend/
│   ├── .env                    # Environment variables
│   ├── main_sqlite.py          # FastAPI application with static file serving
│   ├── database_sqlite.py      # Database operations
│   ├── chat_service_sqlite.py  # OpenAI service
│   ├── auth_service.py         # Authentication service
│   ├── models.py               # Pydantic models
│   ├── config_sqlite.py        # Configuration
│   ├── requirements_sqlite.txt # Python dependencies  
│   └── chatbot.db              # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ChatBot.tsx     # Main chat interface
│   │   │   ├── MessageBubble.tsx # Individual messages
│   │   │   ├── MessageInput.tsx  # Input component
│   │   │   ├── TypingIndicator.tsx # Typing animation
│   │   │   ├── AllConversations.tsx # Sidebar history
│   │   │   ├── Login.tsx       # Authentication component
│   │   │   └── ConfirmDialog.tsx # Deletion confirmation
│   │   ├── types.ts            # TypeScript types
│   │   ├── api.ts              # API service
│   │   └── styles/             # CSS stylesheets
│   ├── public/
│   ├── package.json            # Node dependencies
│   └── build/                  # Production build (auto-generated)
├── start.sh                    # Local development start script
├── readme.md                   # Main documentation
├── backend.md                  # Backend documentation
├── frontend.md                 # Frontend documentation
├── fullstack.md               # Architecture overview
└── git.md                     # Git commands reference
│   │   │   ├── TypingIndicator.tsx # Typing animation
│   │   │   └── AllConversations.tsx # Sidebar history
│   │   ├── types.ts             # TypeScript types
│   │   ├── api.ts               # API service
│   │   └── index.css            # Styles
```

## 🛠️ Development

### Docker Development
- **Production mode**: Serves optimized React build from FastAPI static files
- **Development mode**: Separate frontend container with hot reload on port 3000
- **Health checks**: Built-in container health monitoring
- **Volume mounting**: Source code mounted for live development

### Backend Development
- The backend uses **SQLite** for local development
- Database tables are created automatically on first run
- All conversation data is stored locally in `chatbot.db`
- FastAPI provides automatic API documentation at `http://localhost:8000/docs`
- Static file serving for React production builds

### Frontend Development
- Built with **Create React App** and TypeScript
- Uses custom CSS with modern design patterns
- Responsive design works on all screen sizes
- Hot reload enabled for development (both Docker and local)

## 🔒 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Frontend
No additional environment variables needed - the frontend connects to the backend at `http://localhost:8000` by default.

## 🐛 Troubleshooting

### Docker Issues

1. **Containers won't start**
   - Ensure Docker and Docker Compose are running
   - Check if ports 3000 and 8000 are available: `lsof -ti:3000,8000`
   - Verify environment variables in `.env` file
   - Try rebuilding: `docker-compose up -d --build`

2. **Frontend container not accessible**
   - Check if frontend-dev service is running: `docker-compose ps`
   - View logs: `docker-compose logs frontend-dev`
   - Ensure development profile is active: `docker-compose --profile dev up -d`

3. **Backend API errors in Docker**
   - Check backend logs: `docker-compose logs backend`
   - Verify OpenAI API key in `.env` file
   - Ensure backend container is healthy: `docker-compose ps`

### Local Development Issues

1. **Backend won't start**
   - Make sure virtual environment is activated: `source .venv/bin/activate`
   - Check if OpenAI API key is set in `.env` file
   - Verify all dependencies are installed: `pip install -r requirements_sqlite.txt`
   - Ensure port 8000 is not in use: `lsof -ti:8000`

2. **Frontend can't connect to backend**
   - Ensure backend is running on port 8000
   - Check CORS settings in FastAPI (should allow localhost:3000)
   - Verify backend health: visit `http://localhost:8000` in browser

3. **OpenAI API errors**
   - Verify your API key is valid and has credits
   - Check OpenAI API status at https://status.openai.com/
   - Ensure you have access to GPT models

4. **Virtual environment issues**
   - Make sure you're in the backend directory
   - Try recreating the virtual environment:
     ```bash
     rm -rf .venv
     python -m venv .venv
     source .venv/bin/activate
     pip install -r requirements_sqlite.txt
     ```

### Port Conflicts
If you need to change the default ports:

**Backend**: Edit `main_sqlite.py` and change the port in `uvicorn.run(app, host="0.0.0.0", port=8000)`
**Frontend**: Set `PORT=3001` environment variable before running `npm start`

### Database Issues
- SQLite database is created automatically in the backend directory
- If you encounter database errors, delete `chatbot.db` and restart the backend
- Check file permissions on the backend directory