# 🚀 FastAPI Chatbot Backend

This is the backend service for the FastAPI-React TypeScript chatbot application, featuring modern Python dependency management with Poetry and OpenAI integration.

## ✨ Features

- 🤖 **OpenAI Integration**: GPT-4 powered responses
- 📦 **Poetry Management**: Modern Python dependency handling
- 🗄️ **SQLite Database**: Lightweight, file-based storage
- 🔒 **Environment Variables**: Secure configuration management
- 📚 **API Documentation**: Auto-generated with FastAPI
- 🌐 **CORS Support**: Seamless frontend integration

## 🚀 Quick Start

### Using the Root Script (Recommended)
```bash
# From the project root
./start.sh
```

### Manual Setup

#### Using Poetry (Recommended)

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. Run the server:
   ```bash
   poetry run uvicorn main_sqlite:app --reload
   ```

### Using pip (Alternative)

If you prefer to use pip:
```bash
pip install -r requirements_sqlite.txt
uvicorn main_sqlite:app --reload
```

## API Documentation

Once the server is running, you can access:
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file in this directory with your configuration:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Database

The application uses SQLite with the database file `chatbot.db`.
