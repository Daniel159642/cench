import React from 'react';

const StatusIndicator = ({ daVinciConnected, openAIConfigured }) => {
  return (
    <div className="status-indicator">
      <div className="status-item">
        <div className={`status-dot ${daVinciConnected ? 'connected' : 'disconnected'}`} />
        <span className="status-label">DaVinci</span>
      </div>
      <div className="status-item">
        <div className={`status-dot ${openAIConfigured ? 'connected' : 'disconnected'}`} />
        <span className="status-label">OpenAI</span>
      </div>
    </div>
  );
};

export default StatusIndicator; 