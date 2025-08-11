from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse, ConversationCreate, ConversationResponse
from database_sqlite import db_manager
from chat_service_sqlite import chat_service
import logging

# Logging helps debug issues, monitor performance, and track errors in production
# Configure root logger to show INFO level messages and above
logging.basicConfig(level=logging.INFO)
# Create module-specific logger for tracking messages from this file
logger = logging.getLogger(__name__)

app = FastAPI(title="Chatbot API", version="1.0.0")

# Enable CORS for React frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection lifecycle
# Connect to database when application starts
@app.on_event("startup")
async def startup_event():
    db_manager.connect()

# Close database connection when application shuts down
@app.on_event("shutdown")
async def shutdown_event():
    db_manager.close()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Chatbot API is running with SQLite"}

# Send message and get AI response
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Create new conversation if none provided
        if not request.conversation_id:
            conversation_id = db_manager.create_conversation(request.user_id)
            if not conversation_id:
                raise HTTPException(status_code=500, detail="Failed to create conversation")
        else:
            conversation_id = request.conversation_id
            
        # Save user message
        db_manager.save_message(conversation_id, "user", request.message)
        
        # Get conversation history
        history = db_manager.get_conversation_history(conversation_id)
        
        # Generate AI response
        ai_response = await chat_service.generate_response(history)
        
        # Save AI response
        db_manager.save_message(conversation_id, "assistant", ai_response)
        
        return ChatResponse(response=ai_response, conversation_id=conversation_id)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
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
