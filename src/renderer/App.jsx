import React, { useState, useEffect } from 'react';
import ChatOverlay from './components/ChatOverlay';
import SettingsPanel from './components/SettingsPanel';
import logoImage from '../logo.png';
import fileIcon from '../file-icon.png';

const App = () => {
  const [showSettings, setShowSettings] = useState(false);
  const [showChat, setShowChat] = useState(true);

  useEffect(() => {
    // Listen for settings open event from main process
    const removeListener = window.electronAPI.onOpenSettings(() => {
      setShowSettings(true);
    });

    return removeListener;
  }, []);

  if (showSettings) {
    return (
      <SettingsPanel 
        onClose={() => setShowSettings(false)}
      />
    );
  }

  if (!showChat) {
    return (
      <div className="original-page">
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
            <button className="settings-button" onClick={() => setShowSettings(true)}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </button>
          </div>
        </div>

        <img src={logoImage} alt="Cench AI Logo" className="welcome-logo" />
        <div className="welcome-actions">
          <div className="action-container">
            <div className="action-icon">
              <img src={fileIcon} alt="File" className="file-icon-img" />
            </div>
            <h3>Open Project</h3>
          </div>
          <div className="action-container" onClick={() => setShowChat(true)}>
            <div className="action-icon">+</div>
            <h3>New Chat</h3>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ChatOverlay 
      onOpenSettings={() => setShowSettings(true)}
      onClose={() => setShowChat(false)}
    />
  );
};

export default App; 