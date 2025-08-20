const { contextBridge, ipcRenderer } = require('electron');

// Expose secure API to renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // Window controls
  minimizeWindow: () => ipcRenderer.invoke('window:minimize'),
  closeWindow: () => ipcRenderer.invoke('window:close'),
  showWindow: () => ipcRenderer.invoke('window:show'),
  maximizeWindow: () => ipcRenderer.invoke('window:maximize'),
  
  // Settings
  getSettings: () => ipcRenderer.invoke('settings:get'),
  saveSettings: (settings) => ipcRenderer.invoke('settings:save', settings),
  
  // DaVinci Resolve integration
  executeDaVinciCommand: (code) => ipcRenderer.invoke('davinci:execute', code),
  checkDaVinciConnection: () => ipcRenderer.invoke('davinci:check'),
  
  // After Effects integration
  executeAfterEffectsCommand: (code) => ipcRenderer.invoke('aftereffects:execute', code),
  checkAfterEffectsConnection: () => ipcRenderer.invoke('aftereffects:check'),
  
  // Database operations
  queryCommands: (query, params) => ipcRenderer.invoke('db:query', query, params),
  
  // OpenAI integration
  processMessage: (message, context) => ipcRenderer.invoke('openai:process', message, context),
  
  // Event listeners
  onOpenSettings: (callback) => {
    ipcRenderer.on('open-settings', callback);
    return () => ipcRenderer.removeListener('open-settings', callback);
  }
}); 