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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import Pydantic models for request/response validation
from models import ChatRequest, ChatResponse, ConversationCreate, ConversationResponse

# Import database manager for SQLite operations
from database_sqlite import db_manager

# Import chat service for OpenAI integration and business logic
from chat_service_sqlite import chat_service

# Import logging for debugging and monitoring
import logging

# LOGGING CONFIGURATION
# Logging helps debug issues, monitor performance, and track errors in production
# Configure root logger to show INFO level messages and above
logging.basicConfig(level=logging.INFO)
# Create module-specific logger for tracking messages from this file
logger = logging.getLogger(__name__)

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
    allow_origins=["http://localhost:3000"],  # React frontend URL - restrict in production
    allow_credentials=True,                   # Allow cookies and authentication headers
    allow_methods=["*"],                      # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],                      # Allow all headers
)

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
async def root():
    """
    Health check endpoint
    
    Returns basic API information and status
    Useful for monitoring and confirming the API is running
    
    Returns:
        dict: API status message and version information
    """
    return {
        "message": "Chatbot API is running with SQLite",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
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
        
    Returns:
        ChatResponse: Contains AI response text and conversation_id
        
    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        logger.info(f"Received chat request from user {request.user_id}")
        
        # Handle conversation creation for new chats
        if not request.conversation_id:
            logger.info("Creating new conversation")
            conversation_id = db_manager.create_conversation(request.user_id)
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

# Create a new conversation for a user
@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationCreate):
    try:
        conversation_id = db_manager.create_conversation(request.user_id)
        if not conversation_id:
            raise HTTPException(status_code=500, detail="Failed to create conversation")
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

# Get all conversations for a specific user
@app.get("/conversations/user/{user_id}")
async def get_user_conversations(user_id: str):
    try:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
