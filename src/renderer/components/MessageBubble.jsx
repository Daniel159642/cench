import React, { useState } from 'react';

const MessageBubble = ({ message, isUser, onExecute, onRestore, onEdit, isLoading, isEditing, onSaveEdit, onCancelEdit }) => {
  const [showCode, setShowCode] = useState(false);
  const [editText, setEditText] = useState(message.content);

  const handleExecute = () => {
    if (message.code && onExecute) {
      onExecute(message.id, message.code);
    }
  };

  const getMessageClass = () => {
    switch (message.type) {
      case 'user':
        return 'user';
      case 'assistant':
        return 'assistant';
      case 'error':
        return 'error';
      default:
        return 'assistant';
    }
  };

  const getStatusIcon = () => {
    if (message.executed === true) {
      return '✅';
    } else if (message.executed === false) {
      return '❌';
    }
    return null;
  };

  return (
    <div className={`message-bubble ${getMessageClass()}`}>
              <div className="message-content">
          {message.isEditable ? (
            /* Show editable input when message is editable */
            <div className="edit-mode">
              <textarea
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                className="edit-textarea"
                placeholder="Type your message..."
                rows={3}
                autoFocus
              />
            </div>
          ) : (
            /* Show original message content when not editing */
            <div className="message-text">
              {message.content}
              {getStatusIcon() && (
                <span className="execution-status">
                  {getStatusIcon()}
                </span>
              )}
            </div>
          )}
        
        {/* Action buttons for user messages */}
        {isUser && (onRestore || onEdit) && (
          <div className="message-actions">
            {isLoading ? (
              /* Stop button while AI is thinking */
              <button 
                className="stop-button"
                onClick={() => onEdit(message.id)}
                title="Stop AI and edit message"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="6" y="6" width="12" height="12"/>
                </svg>
                Stop
              </button>
            ) : (isEditing || message.isEditable) ? (
              /* Send button when editing */
              <button 
                className="send-button"
                onClick={() => onSaveEdit(message.id, editText)}
                title="Send edited message"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22,2 15,22 11,13 2,9"/>
                </svg>
                Send
              </button>
            ) : (
              /* Restore button when not loading */
              <button 
                className="restore-button"
                onClick={() => {
                  console.log('Restore button clicked for message:', message.id);
                  onRestore(message.id);
                }}
                title="Restore conversation to this point"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                  <path d="M21 3v5h-5"/>
                  <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                  <path d="M3 21v-5h5"/>
                </svg>
                Restore
              </button>
            )}
          </div>
        )}
        

        
        {message.code && (
          <div className="code-section">
            <div className="code-header">
              <button 
                className="toggle-code-btn"
                onClick={() => setShowCode(!showCode)}
              >
                {showCode ? 'Hide' : 'Show'} Code
              </button>
              {!message.executed && (
                <button 
                  className="execute-button"
                  onClick={handleExecute}
                  disabled={message.executing}
                >
                  {message.executing ? 'Executing...' : 'Execute'}
                </button>
              )}
            </div>
            
            {showCode && (
              <div className="code-block">
                <pre><code>{message.code}</code></pre>
              </div>
            )}
          </div>
        )}
        
        {message.executionError && (
          <div className="error-message">
            <strong>Execution Error:</strong> {message.executionError}
          </div>
        )}
        
        {message.executionResult && message.executionResult.success && (
          <div className="success-message">
            <strong>Success:</strong> {message.executionResult.message}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble; 