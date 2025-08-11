import React, { useState, useEffect } from 'react';
import { ConversationSummary, FullConversation } from '../types';
import { chatAPI } from '../api';
import ConfirmDialog from './ConfirmDialog';

interface AllConversationsProps {
  userId: string;
  onSelectConversation: (conversation: FullConversation) => void;
  onDeleteConversation?: (conversationId: number) => void;
  currentConversationId?: number;
  refreshTrigger?: number;
}

const AllConversations: React.FC<AllConversationsProps> = ({
  userId,
  onSelectConversation,
  onDeleteConversation,
  currentConversationId,
  refreshTrigger
}) => {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isAutoRefreshing, setIsAutoRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [conversationToDelete, setConversationToDelete] = useState<number | null>(null);

  useEffect(() => {
    loadConversations();
  }, [userId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Refresh when new conversation is created
  useEffect(() => {
    if (refreshTrigger && refreshTrigger > 0) {
      loadConversations();
    }
  }, [refreshTrigger]); // eslint-disable-line react-hooks/exhaustive-deps

  // Auto-refresh conversations every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      loadConversations(true); // Pass true for auto-refresh
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [userId]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadConversations = async (isAutoRefresh = false) => {
    if (isAutoRefresh) {
      setIsAutoRefreshing(true);
    } else {
      setIsLoading(true);
    }
    setError(null);
    try {
      const conversationList = await chatAPI.getUserConversations(userId);
      setConversations(conversationList);
    } catch (error) {
      console.error('Error loading conversations:', error);
      if (!isAutoRefresh) {
        setError('Failed to load conversations');
      }
    } finally {
      if (isAutoRefresh) {
        setIsAutoRefreshing(false);
      } else {
        setIsLoading(false);
      }
    }
  };

  const handleConversationClick = async (conversationId: number) => {
    try {
      const fullConversation = await chatAPI.getFullConversation(conversationId);
      onSelectConversation(fullConversation);
    } catch (error) {
      console.error('Error loading conversation:', error);
      setError('Failed to load conversation');
    }
  };

  const handleDeleteConversation = (conversationId: number, event: React.MouseEvent) => {
    event.stopPropagation(); // Prevent triggering the conversation click
    setConversationToDelete(conversationId);
    setShowDeleteConfirm(true);
  };

  const confirmDeleteConversation = async () => {
    if (!conversationToDelete) return;

    try {
      await chatAPI.deleteConversation(conversationToDelete);
      // Remove the conversation from the local state
      setConversations(prev => prev.filter(conv => conv.id !== conversationToDelete));
      
      // If the deleted conversation was the current one, clear it
      if (currentConversationId === conversationToDelete) {
        onDeleteConversation?.(conversationToDelete);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      setError('Failed to delete conversation');
    } finally {
      setShowDeleteConfirm(false);
      setConversationToDelete(null);
    }
  };

  const cancelDeleteConversation = () => {
    setShowDeleteConfirm(false);
    setConversationToDelete(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return 'Today';
    } else if (diffDays === 2) {
      return 'Yesterday';
    } else if (diffDays <= 7) {
      return `${diffDays - 1} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  return (
    <div className="conversations-sidebar-panel">
      {isAutoRefreshing && (
        <div className="auto-refresh-indicator">
          <div className="auto-refresh-dot"></div>
        </div>
      )}
      
      {isLoading && (
        <div className="conversations-loading">
          <div className="loading-spinner">Loading...</div>
        </div>
      )}

      {error && (
        <div className="conversations-error">
          <p>{error}</p>
          <button onClick={() => loadConversations()} className="retry-button">
            Try Again
          </button>
        </div>
      )}

      {!isLoading && !error && conversations.length === 0 && (
        <div className="no-conversations">
          <p>No conversations yet</p>
        </div>
      )}

      {!isLoading && !error && conversations.length > 0 && (
        <div className="conversations-list">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={`conversation-item ${
                currentConversationId === conversation.id ? 'active' : ''
              }`}
              onClick={() => handleConversationClick(conversation.id)}
            >
              <div className="conversation-preview">
                <div className="conversation-text">
                  {conversation.preview}
                </div>
                <div className="conversation-meta">
                  <span className="message-count">
                    💬 {conversation.message_count}
                  </span>
                  <span className="conversation-date">
                    {formatDate(conversation.last_message_at || conversation.created_at)}
                  </span>
                </div>
              </div>
              <button
                className="delete-conversation-btn"
                onClick={(e) => handleDeleteConversation(conversation.id, e)}
                title="Delete conversation"
              >
                🗑️
              </button>
            </div>
          ))}
        </div>
      )}
      
      <ConfirmDialog
        isOpen={showDeleteConfirm}
        title="Delete Conversation"
        message="Are you sure you want to delete this conversation? This action cannot be undone and all messages will be permanently lost."
        confirmText="Delete"
        cancelText="Cancel"
        variant="danger"
        onConfirm={confirmDeleteConversation}
        onCancel={cancelDeleteConversation}
      />
    </div>
  );
};

export default AllConversations;
