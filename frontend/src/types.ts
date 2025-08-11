export interface Message {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
  conversation_id?: number;
  created_at?: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number;
  user_id?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: number;
}

export interface Conversation {
  id: number;
  user_id: string;
  created_at: string;
}

export interface ConversationSummary {
  id: number;
  user_id: string;
  created_at: string;
  message_count: number;
  last_message_at: string | null;
  preview: string;
}

export interface FullConversation {
  conversation: {
    id: number;
    user_id: string;
    created_at: string;
  };
  messages: Message[];
}
