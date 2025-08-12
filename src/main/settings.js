const fs = require('fs');
const path = require('path');
const { app } = require('electron');

const settingsPath = path.join(app.getPath('userData'), 'settings.json');

const defaultSettings = {
  openai_api_key: '',
  auto_execute: false,
  overlay_opacity: 0.95,
  shortcut_key: 'CommandOrControl+Shift+C',
  theme: 'dark',
  window_position: { x: 100, y: 100 },
  window_size: { width: 420, height: 600 }
};

function loadSettings() {
  try {
    if (fs.existsSync(settingsPath)) {
      const data = fs.readFileSync(settingsPath, 'utf8');
      const settings = JSON.parse(data);
      return { ...defaultSettings, ...settings };
    }
  } catch (error) {
    console.error('Error loading settings:', error);
  }
  return { ...defaultSettings };
}

function saveSettingsToFile(settings) {
  try {
    const settingsDir = path.dirname(settingsPath);
    if (!fs.existsSync(settingsDir)) {
      fs.mkdirSync(settingsDir, { recursive: true });
    }
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
    return true;
  } catch (error) {
    console.error('Error saving settings:', error);
    return false;
  }
}

let cachedSettings = null;

function getSettings() {
  if (!cachedSettings) {
    cachedSettings = loadSettings();
  }
  return cachedSettings;
}

function saveSettings(newSettings) {
  const currentSettings = getSettings();
  const updatedSettings = { ...currentSettings, ...newSettings };
  
  if (saveSettingsToFile(updatedSettings)) {
    cachedSettings = updatedSettings;
    return true;
  }
  return false;
}

module.exports = {
  getSettings,
  saveSettings
}; 