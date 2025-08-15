"""
FastAPI Backend for AI Chatbot Application

This is the main backend application built with FastAPI that provides:
- RESTful API endpoints for chat functionality
- SQLite database integration for persistent conversation storage
- OpenAI GPT integration for AI responses
- CORS support for frontend communication
- Real-time message processing and conversation management

Key Features:
- Create and manage conversations
- Send messages and receive AI responses
- Retrieve conversation history
- Delete conversations
- User-based conversation organization
"""

# FastAPI framework imports for web API functionality
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import Pydantic models for request/response validation
from models import ChatRequest, ChatResponse, ConversationCreate, ConversationResponse, UserCreate, UserLogin, LoginResponse, UserResponse

# Import database manager for SQLite operations
from database_sqlite import db_manager

# Import chat service for OpenAI integration and business logic
from chat_service_sqlite import chat_service

# Import authentication service for user management
from auth_service import auth_service

# Import logging for debugging and monitoring
import logging

# LOGGING CONFIGURATION
# Logging helps debug issues, monitor performance, and track errors in production
# Configure root logger to show INFO level messages and above
logging.basicConfig(level=logging.INFO)
# Create module-specific logger for tracking messages from this file
logger = logging.getLogger(__name__)

# SECURITY CONFIGURATION
# JWT Bearer token authentication
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials containing JWT token
        
    Returns:
        UserResponse: Current authenticated user
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = credentials.credentials
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user

# FASTAPI APPLICATION INITIALIZATION
# Initialize FastAPI application with metadata for auto-generated documentation
app = FastAPI(
    title="Chatbot API", 
    version="1.0.0",
    description="Backend API for AI-powered chatbot with conversation management"
)

# CORS CONFIGURATION
# Cross-Origin Resource Sharing (CORS) middleware to allow frontend communication
# This is essential for web browsers to allow requests from React frontend to FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # React frontend URLs
    allow_credentials=True,                   # Allow cookies and authentication headers
    allow_methods=["*"],                      # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],                      # Allow all headers
)

# STATIC FILES CONFIGURATION
# Serve React build files
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
# Mount the nested static directory for CSS, JS, and media files
nested_static_dir = os.path.join(static_dir, "static")
if os.path.exists(nested_static_dir):
    app.mount("/static", StaticFiles(directory=nested_static_dir), name="static")

# APPLICATION LIFECYCLE EVENTS
# These events run when the FastAPI application starts and stops

@app.on_event("startup")
async def startup_event():
    """
    Initialize database connection when application starts
    
    This ensures the database is ready before handling any requests
    """
    logger.info("Starting up chatbot application...")
    db_manager.connect()
    logger.info("Database connection established")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up database connection when application shuts down
    
    This ensures proper cleanup and prevents database connection leaks
    """
    logger.info("Shutting down chatbot application...")
    db_manager.close()
    logger.info("Database connection closed")

# API ENDPOINTS

@app.get("/")
async def serve_react_root():
    """
    Serve React app from root path
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_file = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {
            "message": "Chatbot API is running with SQLite",
            "version": "1.0.0",
            "status": "healthy"
        }

@app.get("/favicon.ico")
async def serve_favicon():
    """
    Serve favicon.ico from static directory
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    favicon_file = os.path.join(static_dir, "favicon.ico")
    
    if os.path.exists(favicon_file):
        return FileResponse(favicon_file)
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/manifest.json")
async def serve_manifest():
    """
    Serve manifest.json from static directory
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    manifest_file = os.path.join(static_dir, "manifest.json")
    
    if os.path.exists(manifest_file):
        return FileResponse(manifest_file)
    else:
        raise HTTPException(status_code=404, detail="Manifest not found")

@app.get("/logo192.png")
async def serve_logo192():
    """
    Serve logo192.png from static directory
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    logo_file = os.path.join(static_dir, "logo192.png")
    
    if os.path.exists(logo_file):
        return FileResponse(logo_file)
    else:
        raise HTTPException(status_code=404, detail="Logo not found")

# API status endpoint moved to /api
@app.get("/api")
async def api_status():
    """
    API status endpoint
    
    Returns basic API information and status
    """
    return {
        "message": "Chatbot API is running with SQLite",
        "version": "1.0.0",
        "status": "healthy"
    }

# AUTHENTICATION ENDPOINTS

@app.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    Register a new user account
    
    Creates a new user with hashed password and returns user information
    without sensitive data like password hash.
    
    Args:
        user_data (UserCreate): User registration data including username, email, password
        
    Returns:
        UserResponse: Created user information without password
        
    Raises:
        HTTPException: 400 if username/email already exists, 500 for server errors
    """
    try:
        logger.info(f"Attempting to register user: {user_data.username}")
        
        user = auth_service.register_user(user_data)
        if not user:
            logger.warning(f"Registration failed for username: {user_data.username}")
            raise HTTPException(
                status_code=400, 
                detail="Username or email already exists"
            )
        
        logger.info(f"User registered successfully: {user.username}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/auth/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    """
    Authenticate user and return access token
    
    Validates user credentials and returns JWT access token for subsequent
    authenticated requests.
    
    Args:
        login_data (UserLogin): User login credentials (username and password)
        
    Returns:
        LoginResponse: Access token and user information
        
    Raises:
        HTTPException: 401 for invalid credentials, 500 for server errors
    """
    try:
        logger.info(f"Login attempt for username: {login_data.username}")
        
        login_response = auth_service.authenticate_user(login_data)
        if not login_response:
            logger.warning(f"Login failed for username: {login_data.username}")
            raise HTTPException(
                status_code=401, 
                detail="Invalid username or password"
            )
        
        logger.info(f"User logged in successfully: {login_data.username}")
        return login_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Returns information about the currently authenticated user based on
    the JWT token provided in the Authorization header.
    
    Args:
        current_user: Authenticated user (injected by dependency)
        
    Returns:
        UserResponse: Current user information
    """
    return current_user

# CHAT ENDPOINTS

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: UserResponse = Depends(get_current_user)):
    """
    Main chat endpoint - processes user messages and returns AI responses
    
    This is the core functionality of the chatbot API. It:
    1. Creates a new conversation if none exists
    2. Saves the user's message to database
    3. Gets AI response from OpenAI via chat service
    4. Saves AI response to database
    5. Returns the response to frontend
    
    Args:
        request (ChatRequest): Contains message, optional conversation_id, and user_id
        current_user: Authenticated user (injected by dependency)
        
    Returns:
        ChatResponse: Contains AI response text and conversation_id
        
    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        # Use authenticated user's ID instead of request user_id
        user_id = str(current_user.id)
        logger.info(f"Received chat request from authenticated user {user_id}")
        
        # Handle conversation creation for new chats
        if not request.conversation_id:
            logger.info("Creating new conversation")
            conversation_id = db_manager.create_conversation(user_id)
            if not conversation_id:
                logger.error("Failed to create new conversation")
                raise HTTPException(status_code=500, detail="Failed to create conversation")
        else:
            # Use existing conversation
            logger.info(f"Using existing conversation {request.conversation_id}")
            conversation_id = request.conversation_id
            
                    
        # Save user message to database for conversation history
        logger.info(f"Saving user message to conversation {conversation_id}")
        db_manager.save_message(conversation_id, "user", request.message)
        
        # Get conversation history for AI context
        logger.info(f"Retrieving conversation history for context")
        history = db_manager.get_conversation_history(conversation_id)
        
        # Generate AI response using chat service (integrates with OpenAI)
        logger.info("Generating AI response")
        ai_response = await chat_service.generate_response(history)
        
        # Save AI response to database
        logger.info("Saving AI response to database")
        db_manager.save_message(conversation_id, "assistant", ai_response)
        
        logger.info(f"Chat request completed successfully for conversation {conversation_id}")
        return ChatResponse(response=ai_response, conversation_id=conversation_id)
        
    except Exception as e:
        # Log the error for debugging and return user-friendly message
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationCreate):
    """
    Create a new conversation for a user
    
    This endpoint allows explicitly creating a new conversation
    without sending a message first. Useful for UI that wants to
    show empty conversations or prepare conversation containers.
    
    Args:
        request (ConversationCreate): Contains user_id for the new conversation
        
    Returns:
        ConversationResponse: Contains the new conversation_id and user_id
        
    Raises:
        HTTPException: 500 if conversation creation fails
    """
    try:
        logger.info(f"Creating new conversation for user {request.user_id}")
        conversation_id = db_manager.create_conversation(request.user_id)
        if not conversation_id:
            logger.error("Database failed to create conversation")
            raise HTTPException(status_code=500, detail="Failed to create conversation")
            
        logger.info(f"Successfully created conversation {conversation_id}")
        return ConversationResponse(id=conversation_id, user_id=request.user_id)
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get all messages for a specific conversation
@app.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: int):
    try:
        messages = db_manager.get_conversation_history(conversation_id)
        return [{"role": row[0], "content": row[1]} for row in messages]
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get all conversations for the authenticated user
@app.get("/conversations")
async def get_user_conversations(current_user: UserResponse = Depends(get_current_user)):
    """
    Get all conversations for the authenticated user
    
    Args:
        current_user: Authenticated user (injected by dependency)
        
    Returns:
        list: List of conversations with metadata for the current user
    """
    try:
        user_id = str(current_user.id)
        conversations = db_manager.get_all_conversations(user_id)
        return [
            {
                "id": row[0],
                "user_id": row[1],
                "created_at": row[2],
                "message_count": row[3],
                "last_message_at": row[4],
                "preview": row[5] or "No messages yet"
            }
            for row in conversations
        ]
    except Exception as e:
        logger.error(f"Error fetching user conversations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get conversation with all its messages
@app.get("/conversations/{conversation_id}/full")
async def get_full_conversation(conversation_id: int):
    try:
        conversation_data = db_manager.get_conversation_with_messages(conversation_id)
        if not conversation_data:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation_data
    except Exception as e:
        logger.error(f"Error fetching full conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Delete a conversation and all its messages
@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    try:
        success = db_manager.delete_conversation(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"message": "Conversation deleted successfully", "conversation_id": conversation_id}
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check endpoint for Docker
@app.get("/health")
async def health_check():
    """
    Health check endpoint for Docker monitoring
    
    Returns:
        dict: Simple health status
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
