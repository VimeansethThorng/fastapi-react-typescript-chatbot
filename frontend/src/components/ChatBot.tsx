import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import AllConversations from './AllConversations';
import { Message, FullConversation } from '../types';
import { chatAPI } from '../api';

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isTyping, setIsTyping] = useState(false);
  const [userId] = useState('user-123'); // In a real app, this would come from authentication
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSelectConversation = (fullConversation: FullConversation) => {
    setConversationId(fullConversation.conversation.id);
    setMessages(fullConversation.messages);
  };

  const handleDeleteConversation = (deletedConversationId: number) => {
    // If the deleted conversation is the current one, clear the chat
    if (conversationId === deletedConversationId) {
      setMessages([]);
      setConversationId(null);
    }
  };

  const handleSendMessage = async (messageContent: string) => {
    if (!messageContent.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      role: 'user',
      content: messageContent,
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setIsTyping(true);

    const isNewConversation = !conversationId;

    try {
      const response = await chatAPI.sendMessage({
        message: messageContent,
        conversation_id: conversationId || undefined,
        user_id: userId,
      });

      // Update conversation ID if this is the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
        // Trigger refresh of conversation list for new conversation with a small delay
        setTimeout(() => {
          setRefreshTrigger(prev => prev + 1);
        }, 500);
      }

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        conversation_id: response.conversation_id,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="app-container">
      {/* Left Sidebar - Conversations */}
      <div className="conversations-sidebar">
        <div className="sidebar-header">
          <h3>💬 Conversations</h3>
          <button
            onClick={handleNewConversation}
            className="new-chat-button-sidebar"
            title="Start a new conversation"
          >
            ➕ New
          </button>
        </div>
        <div className="conversations-list-container">
          <AllConversations
            userId={userId}
            onSelectConversation={handleSelectConversation}
            onDeleteConversation={handleDeleteConversation}
            currentConversationId={conversationId || undefined}
            refreshTrigger={refreshTrigger}
          />
        </div>
      </div>

      {/* Right Main Chat Area */}
      <div className="chat-container">
        {/* Header */}
        <div className="chat-header">
          <h1 className="chat-title">✨ AI Assistant</h1>
        </div>

        {/* Messages Container */}
        <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <div className="welcome-content">
              <h2>
                Welcome to AI Assistant
              </h2>
              <p>
                I'm here to help you with questions, creative writing, problem-solving, and much more. 
                Start a conversation by typing a message below!
              </p>
              <p className="welcome-note">
                💡 All your conversations are automatically saved. Use the conversation history in the left sidebar to revisit previous chats.
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <MessageBubble key={index} message={message} />
            ))}
            <TypingIndicator isVisible={isTyping} />
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-area">
        <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
    </div>
  );
};

export default ChatBot;
