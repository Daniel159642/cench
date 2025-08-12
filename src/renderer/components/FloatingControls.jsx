import React from 'react';

const FloatingControls = ({ onOpenSettings }) => {
  const handleMinimize = () => {
    window.electronAPI.minimizeWindow();
  };

  const handleClose = () => {
    window.electronAPI.closeWindow();
  };

  return (
    <div className="floating-controls">
      <button 
        className="control-btn settings-btn"
        onClick={onOpenSettings}
        title="Settings"
      >
        ⚙️
      </button>
      <button 
        className="control-btn minimize-btn"
        onClick={handleMinimize}
        title="Minimize to Dock"
      >
        −
      </button>
      <button 
        className="control-btn close-btn"
        onClick={handleClose}
        title="Close to Tray"
      >
        ×
      </button>
    </div>
  );
};

export default FloatingControls; 