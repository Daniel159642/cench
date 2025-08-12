import React, { useState, useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import MessageBubble from './MessageBubble';
import FloatingControls from './FloatingControls';
import StatusIndicator from './StatusIndicator';

const ChatOverlay = ({ onOpenSettings, onClose }) => {
  const {
    messages,
    isLoading,
    sendMessage,
    executeCode,
    daVinciConnected,
    openAIConfigured,
    setMessages,
    setIsLoading
  } = useChat();
  
  const [input, setInput] = useState('');
  const [editingMessageId, setEditingMessageId] = useState(null);
  const messagesEndRef = useRef(null);
  const hasMessages = messages.length > 0;

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      await sendMessage(input.trim());
      setInput('');
    }
  };

  const handleRestore = (messageId) => {
    console.log('handleRestore called with messageId:', messageId);
    // Find the index of the user message
    const userMessageIndex = messages.findIndex(msg => msg.id === messageId);
    console.log('userMessageIndex:', userMessageIndex);
    if (userMessageIndex !== -1) {
      // Remove all messages after this user message (including the AI response)
      const newMessages = messages.slice(0, userMessageIndex + 1);
      console.log('newMessages after slice:', newMessages);
      
      // Replace the original message with an editable input
      newMessages[userMessageIndex] = {
        ...newMessages[userMessageIndex],
        isEditable: true,
        originalContent: newMessages[userMessageIndex].content, // Store original content
        content: '' // Clear content to show empty input
      };
      
      // Update the messages state to restore to this point
      setMessages(newMessages);
      setEditingMessageId(messageId); // Set editing to the original message
      console.log('Original message replaced with editable input, editingMessageId set to:', messageId);
    }
  };

  const handleEdit = (messageId) => {
    // If AI is thinking, stop the loading
    if (isLoading) {
      setIsLoading(false);
    }
    
    // Replace the original message with an editable input
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, isEditable: true, originalContent: msg.content, content: '' }
        : msg
    ));
    setEditingMessageId(messageId);
  };

  const handleSaveEdit = async (messageId, newText) => {
    if (!newText.trim()) return;
    
    // Update the original message content and make it non-editable
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, content: newText.trim(), isEditable: false }
        : msg
    ));
    
    // Exit edit mode
    setEditingMessageId(null);
    
    // Don't resend - just update the existing message
    // The message is already in the conversation, just updated
  };

  const handleCancelEdit = (messageId) => {
    // Restore the original content when canceling
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, content: msg.originalContent || msg.content, isEditable: false }
        : msg
    ));
    setEditingMessageId(null);
  };

  return (
    <div className={`chat-overlay ${hasMessages ? 'has-messages' : ''}`}>
      {/* Custom Title Bar */}
      <div className="custom-title-bar">
        <div className="title-bar-left">
          <div className="window-controls">
            <button className="window-control close" onClick={() => window.electronAPI.closeWindow()}>
              <span>×</span>
            </button>
            <button className="window-control minimize" onClick={() => window.electronAPI.minimizeWindow()}>
              <span>−</span>
            </button>
            <button className="window-control maximize" onClick={() => window.electronAPI.maximizeWindow()}>
              <span>□</span>
            </button>
          </div>
        </div>
        <div className="title-bar-center">
          <span className="window-title">Cench AI</span>
        </div>
        <div className="title-bar-right">
          <button className="settings-button" onClick={onOpenSettings}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
          </button>
        </div>
      </div>
      
      {/* Small Header Bar */}
      <div className="header-bar">
        <div className="header-left">
          <span className={`header-status ${isLoading ? 'thinking' : ''}`}>
            {isLoading ? 'Thinking...' : 'Ready'}
          </span>
        </div>
        <div className="header-center">
          <span className="header-subtitle"></span>
        </div>
        <div className="header-right">
          <span className="header-version">v1.0</span>
          <button className="header-close-btn" onClick={onClose} title="Close Chat">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
      
      {/* Floating "New Chat" Tag - only show when no messages */}
      {!hasMessages && (
        <div className="floating-tag">New Chat</div>
      )}
      
      {/* Messages Container - show above input when there are messages */}
      {hasMessages && (
        <div className="messages-container">
          {messages.map((msg, index) => (
            <MessageBubble 
              key={msg.id || index}
              message={msg}
              isUser={msg.type === 'user'}
              onExecute={executeCode}
              onRestore={handleRestore}
              onEdit={handleEdit}
              isLoading={isLoading}
              isEditing={editingMessageId === msg.id}
              onSaveEdit={handleSaveEdit}
              onCancelEdit={handleCancelEdit}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
      
      {/* Loading Animation - show when waiting for response */}
      {isLoading && (
        <div className="loading-animation">
          <div className="loading-dots">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        </div>
      )}
      
      {/* Main Chat Container */}
      <div className={`main-chat-container ${hasMessages ? 'bottom-positioned' : 'center-positioned'}`}>
        {/* First Row */}
        <div className="first-row">
          <span className="at-symbol">@</span>
          <div className="cench-label">Cench 1.0</div>
        </div>
        
        {/* Text Input Area */}
        <div className="text-input-area">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Plan, overlay, trim, create anyting"
            disabled={isLoading}
            className="main-text-input"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
        </div>
        
        {/* Bottom Row */}
        <div className="bottom-row">
          <div className="agent-info">
            <span className="agent-tilde">~agent</span>
            <span className="agent-auto">Auto</span>
          </div>
          <div className="input-actions">
            <button className="image-upload-btn" title="Upload Image">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21,15 16,10 5,21"/>
              </svg>
            </button>
            <button 
              className="send-button" 
              onClick={handleSubmit}
              disabled={isLoading || !input.trim()}
              title="Send Message"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="19" x2="12" y2="5"/>
                <polyline points="5,12 12,5 19,12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      
    </div>
  );
};

export default ChatOverlay; 