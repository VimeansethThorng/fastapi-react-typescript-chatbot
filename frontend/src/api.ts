import { ChatRequest, ChatResponse, Message, ConversationSummary, FullConversation } from './types';

const API_BASE_URL = 'http://localhost:8000';

export const chatAPI = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return response.json();
  },

  async getConversationMessages(conversationId: number): Promise<Message[]> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch messages');
    }

    return response.json();
  },

  async createConversation(userId: string): Promise<{ id: number; user_id: string }> {
    const response = await fetch(`${API_BASE_URL}/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId }),
    });

    if (!response.ok) {
      throw new Error('Failed to create conversation');
    }

    return response.json();
  },

  async getUserConversations(userId: string): Promise<ConversationSummary[]> {
    const response = await fetch(`${API_BASE_URL}/conversations/user/${userId}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch user conversations');
    }

    return response.json();
  },

  async getFullConversation(conversationId: number): Promise<FullConversation> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/full`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch full conversation');
    }

    return response.json();
  },

  async deleteConversation(conversationId: number): Promise<{ message: string; conversation_id: number }> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete conversation');
    }

    return response.json();
  },
};
