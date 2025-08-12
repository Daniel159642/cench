import { useState, useEffect, useCallback } from 'react';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [daVinciConnected, setDaVinciConnected] = useState(false);
  const [openAIConfigured, setOpenAIConfigured] = useState(false);

  // Check connections on mount
  useEffect(() => {
    checkConnections();
  }, []);

  const checkConnections = async () => {
    try {
      const daVinciStatus = await window.electronAPI.checkDaVinciConnection();
      setDaVinciConnected(daVinciStatus.connected);
    } catch (error) {
      console.error('DaVinci connection check failed:', error);
      setDaVinciConnected(false);
    }
    
    // For testing purposes, always set OpenAI as configured since we're using mock responses
    setOpenAIConfigured(true);
  };

  const sendMessage = useCallback(async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Mock response for testing UI without OpenAI API
      const mockResponses = [
        "I understand you want to test the chat interface. This is a mock response to help you see how the UI behaves when messages are sent and received.",
        "Great! The chat UI is working perfectly. You can see how messages appear above the input and the positioning changes from center to bottom.",
        "This mock response system allows you to test all the UI features without needing an OpenAI API key. Try sending more messages to see the behavior!",
        "The floating chat input should now be at the bottom of the window, with your conversation history displayed above it.",
        "You can continue chatting to test the message flow, auto-scrolling, and overall user experience of the interface."
      ];
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Get a mock response (cycle through them)
      const mockIndex = messages.length % mockResponses.length;
      const mockResponse = mockResponses[mockIndex];

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: mockResponse,
        code: null, // No code for mock responses
        timestamp: new Date(),
        executed: false
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 2,
        type: 'error',
        content: `Error: ${error.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  const executeCode = async (messageId, code) => {
    try {
      const result = await window.electronAPI.executeDaVinciCommand(code);
      
      setMessages(prev => prev.map(msg => 
        msg.id === messageId 
          ? { ...msg, executed: true, executionResult: result }
          : msg
      ));
    } catch (error) {
      setMessages(prev => prev.map(msg =>
        msg.id === messageId
          ? { ...msg, executed: false, executionError: error.message }
          : msg
      ));
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return {
    messages,
    isLoading,
    sendMessage,
    executeCode,
    clearMessages,
    daVinciConnected,
    openAIConfigured,
    checkConnections,
    setMessages,
    setIsLoading
  };
}; 