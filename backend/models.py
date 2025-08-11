from pydantic import BaseModel
from typing import List, Optional

class MessageCreate(BaseModel):
    content: str
    conversation_id: Optional[int] = None

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    conversation_id: int

class ConversationCreate(BaseModel):
    user_id: str

class ConversationResponse(BaseModel):
    id: int
    user_id: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
