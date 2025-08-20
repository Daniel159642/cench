import React, { useState, useEffect } from 'react';

const SettingsPanel = ({ onClose }) => {
  const [settings, setSettings] = useState({
    openai_api_key: '',
    auto_execute: false,
    overlay_opacity: 0.95,
    shortcut_key: 'CommandOrControl+Shift+C',
    theme: 'dark'
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const currentSettings = await window.electronAPI.getSettings();
      setSettings(currentSettings);
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    setSaveStatus('');
    
    try {
      const success = await window.electronAPI.saveSettings(settings);
      if (success) {
        setSaveStatus('Settings saved successfully!');
        setTimeout(() => setSaveStatus(''), 3000);
      } else {
        setSaveStatus('Failed to save settings');
      }
    } catch (error) {
      setSaveStatus(`Error: ${error.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleInputChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const testDaVinciConnection = async () => {
    try {
      const result = await window.electronAPI.checkDaVinciConnection();
      alert(result.connected ? 'DaVinci Resolve connected!' : `Connection failed: ${result.message}`);
    } catch (error) {
      alert(`Connection test failed: ${error.message}`);
    }
  };

  const testAfterEffectsConnection = async () => {
    try {
      const result = await window.electronAPI.checkAfterEffectsConnection();
      alert(result.connected ? 'After Effects connected!' : `Connection failed: ${result.message}`);
    } catch (error) {
      alert(`Connection test failed: ${error.message}`);
    }
  };

  return (
    <div className="settings-overlay">
      <div className="settings-panel">
        <div className="settings-header">
          <h2>Settings</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="settings-content">
          <div className="setting-group">
            <h3>OpenAI Configuration</h3>
            <div className="setting-item">
              <label htmlFor="api-key">API Key:</label>
              <input
                id="api-key"
                type="password"
                value={settings.openai_api_key}
                onChange={(e) => handleInputChange('openai_api_key', e.target.value)}
                placeholder="sk-..."
                className="setting-input"
              />
            </div>
            <p className="setting-help">
              Get your API key from <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener">OpenAI Platform</a>
            </p>
          </div>

          <div className="setting-group">
            <h3>Behavior</h3>
            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.auto_execute}
                  onChange={(e) => handleInputChange('auto_execute', e.target.checked)}
                />
                Auto-execute safe commands
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="opacity">Overlay Opacity:</label>
              <input
                id="opacity"
                type="range"
                min="0.5"
                max="1"
                step="0.05"
                value={settings.overlay_opacity}
                onChange={(e) => handleInputChange('overlay_opacity', parseFloat(e.target.value))}
                className="setting-range"
              />
              <span className="range-value">{(settings.overlay_opacity * 100).toFixed(0)}%</span>
            </div>
          </div>

          <div className="setting-group">
            <h3>Connections</h3>
            <div className="connection-test">
              <button 
                className="test-btn"
                onClick={testDaVinciConnection}
              >
                Test DaVinci Resolve Connection
              </button>
              <p className="setting-help">
                Make sure DaVinci Resolve is running and accessible
              </p>
            </div>
            <div className="connection-test">
              <button 
                className="test-btn"
                onClick={testAfterEffectsConnection}
              >
                Test After Effects Connection
              </button>
              <p className="setting-help">
                Make sure After Effects is running and accessible
              </p>
            </div>
          </div>

          {saveStatus && (
            <div className={`save-status ${saveStatus.includes('Error') ? 'error' : 'success'}`}>
              {saveStatus}
            </div>
          )}
        </div>

        <div className="settings-footer">
          <button 
            className="save-btn"
            onClick={handleSave}
            disabled={isSaving}
          >
            {isSaving ? 'Saving...' : 'Save Settings'}
          </button>
          <button className="cancel-btn" onClick={onClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel; 