/**
 * api.ts
 *
 * This module provides a typed API client for interacting with the FastAPI backend.
 * It defines all HTTP requests used by the frontend to manage chat conversations,
 * send/receive messages, and perform CRUD operations on conversations.
 *
 * Key Features:
 * - Centralized API endpoint management
 * - TypeScript type safety for all request/response payloads
 * - Consistent error handling for failed requests
 * - Easy to extend for new endpoints
 *
 * API Methods:
 * - sendMessage: Send a chat message and receive a response
 * - getConversationMessages: Fetch all messages for a conversation
 * - createConversation: Start a new conversation for a user
 * - getUserConversations: List all conversations for a user
 * - getFullConversation: Fetch a conversation with all messages and metadata
 * - deleteConversation: Remove a conversation and all its messages
 *
 * Usage:
 *   import { chatAPI } from './api';
 *   const response = await chatAPI.sendMessage({ ... });
 *
 * All methods return Promises and throw errors on network or server failure.
 */

import { ChatRequest, ChatResponse, Message, ConversationSummary, FullConversation } from './types';

const API_BASE_URL = 'http://localhost:8000'; // backend

export const chatAPI = {
  /**
   * Sends a chat message to the backend API and returns the response.
   *
   * @param request - The chat request payload containing the message and any additional metadata required by the backend.
   * @returns A promise that resolves to a {@link ChatResponse} object containing the response from the backend.
   * @throws {Error} Throws an error if the network request fails or the response status is not OK.
   *
   * @remarks
   * This method sends a POST request to the `/chat` endpoint of the API, serializing the request object as JSON.
   * It expects the backend to return a JSON response conforming to the {@link ChatResponse} type.
   * Ensure that the {@link API_BASE_URL} is correctly configured and accessible from the frontend environment.
   */
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

  /**
   * Retrieves all messages for a given conversation by its ID.
   *
   * @param conversationId - The unique identifier of the conversation to fetch messages from.
   * @returns A promise that resolves to an array of `Message` objects belonging to the specified conversation.
   * @throws Will throw an error if the network request fails or the response is not OK.
   */
  async getConversationMessages(conversationId: number): Promise<Message[]> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch messages');
    }

    return response.json();
  },

  /**
   * Creates a new conversation for the specified user.
   *
   * Sends a POST request to the backend API to create a conversation associated with the given user ID.
   *
   * @param userId - The unique identifier of the user for whom the conversation is being created.
   * @returns A promise that resolves to an object containing the conversation's `id` and the associated `user_id`.
   * @throws Will throw an error if the conversation creation fails (i.e., the response is not OK).
   */
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

  /**
   * Retrieves the full conversation details for a given conversation ID.
   *
   * @param conversationId - The unique identifier of the conversation to fetch.
   * @returns A promise that resolves to a {@link FullConversation} object containing the complete conversation data.
   * @throws {Error} If the request fails or the response is not OK.
   */
  async getFullConversation(conversationId: number): Promise<FullConversation> {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/full`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch full conversation');
    }

    return response.json();
  },

  /**
   * Deletes a conversation and all its messages by conversation ID.
   *
   * @param conversationId - The unique identifier of the conversation to delete.
   * @returns A promise that resolves to an object containing a confirmation message and the deleted conversation's ID.
   * @throws {Error} If the network request fails or the response is not OK.
   *
   * @remarks
   * This method sends a DELETE request to the `/conversations/{conversationId}` endpoint.
   * The backend is expected to return a JSON object with a message and the conversation ID.
   */
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
