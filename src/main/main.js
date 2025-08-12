const { app, BrowserWindow, Tray, Menu, globalShortcut, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const DatabaseManager = require('../database/database-manager');
const { getSettings, saveSettings } = require('./settings');
const { nativeImage } = require('electron');

let overlayWindow = null;
let tray = null;
let databaseManager = null;

// Initialize database
async function initializeDatabase() {
  try {
    const dbPath = path.join(app.getPath('userData'), 'cench-ai.db');
    databaseManager = new DatabaseManager(dbPath);
    await databaseManager.initialize();
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Database initialization failed:', error.message);
    console.log('Continuing without database functionality');
    databaseManager = null;
  }
}

function createOverlayWindow() {
  overlayWindow = new BrowserWindow({
    width: 420,
    height: 600,
    alwaysOnTop: false, // Changed to false for normal window
    frame: false, // Changed to false for custom title bar
    titleBarStyle: 'hiddenInset', // Custom title bar style
    transparent: false, // Changed to false for solid background
    skipTaskbar: false, // Show in dock/taskbar
    resizable: true,
    movable: true,
    minimizable: true, // Allow normal minimize
    maximizable: false,
    show: false, // Start hidden
    title: 'Cench AI', // Set window title
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../../assets/icons/icon.png')
  });

  // Load React app
  const isDev = process.env.NODE_ENV === 'development' || process.env.ELECTRON_IS_DEV;
  if (isDev) {
    overlayWindow.loadURL('http://localhost:3000');
    overlayWindow.webContents.openDevTools();
  } else {
    overlayWindow.loadFile(path.join(__dirname, '../../dist/index.html'));
  }

  // Show window in development mode
  if (isDev) {
    overlayWindow.show();
    overlayWindow.focus();
  }

  // Handle window events
  overlayWindow.on('close', (event) => {
    if (!app.isQuiting) {
      event.preventDefault();
      overlayWindow.hide();
    }
  });

  // Don't override minimize behavior - let it work normally
  // overlayWindow.on('minimize', (event) => {
  //   event.preventDefault();
  //   overlayWindow.hide();
  // });

  overlayWindow.on('hide', () => {
    // Update tray context menu when hidden
    if (tray) {
      const contextMenu = Menu.buildFromTemplate([
        { 
          label: 'Show Cench AI', 
          click: () => {
            overlayWindow.show();
            overlayWindow.focus();
          }
        },
        { 
          label: 'Settings', 
          click: () => {
            overlayWindow.show();
            overlayWindow.focus();
            overlayWindow.webContents.send('open-settings');
          }
        },
        { type: 'separator' },
        { 
          label: 'Quit', 
          click: () => {
            app.isQuiting = true;
            app.quit();
          }
        }
      ]);
      tray.setContextMenu(contextMenu);
    }
  });

  overlayWindow.on('show', () => {
    // Update tray context menu when visible
    if (tray) {
      const contextMenu = Menu.buildFromTemplate([
        { 
          label: 'Hide Cench AI', 
          click: () => {
            overlayWindow.hide();
          }
        },
        { 
          label: 'Settings', 
          click: () => {
            overlayWindow.webContents.send('open-settings');
          }
        },
        { type: 'separator' },
        { 
          label: 'Quit', 
          click: () => {
            app.isQuiting = true;
            app.quit();
          }
        }
      ]);
      tray.setContextMenu(contextMenu);
    }
  });

  return overlayWindow;
}

function createTray() {
  let iconPath;
  try {
    iconPath = path.join(__dirname, '../../assets/icons/tray-icon.png');
    // Check if icon exists, use default if not
    if (!fs.existsSync(iconPath)) {
      console.log('Tray icon not found, using default');
      iconPath = path.join(__dirname, '../../assets/icons/icon.png');
      if (!fs.existsSync(iconPath)) {
        // Create a simple default icon or use system default
        iconPath = null;
      }
    }
  } catch (error) {
    console.log('Error loading tray icon:', error.message);
    iconPath = null;
  }
  
  try {
    tray = new Tray(iconPath || nativeImage.createEmpty());
  } catch (error) {
    console.log('Failed to create tray, continuing without tray:', error.message);
    return null;
  }
  
  const contextMenu = Menu.buildFromTemplate([
    { 
      label: 'Show Cench AI', 
      click: () => {
        if (overlayWindow) {
          overlayWindow.show();
          overlayWindow.focus();
        }
      }
    },
    { 
      label: 'Settings', 
      click: () => {
        if (overlayWindow) {
          overlayWindow.webContents.send('open-settings');
        }
      }
    },
    { type: 'separator' },
    { 
      label: 'Quit', 
      click: () => {
        app.isQuiting = true;
        app.quit();
      }
    }
  ]);
  
  tray.setContextMenu(contextMenu);
  tray.setToolTip('Cench AI - DaVinci Resolve Assistant');
  
  tray.on('double-click', () => {
    if (overlayWindow && overlayWindow.isVisible()) {
      overlayWindow.hide();
    } else if (overlayWindow) {
      overlayWindow.show();
      overlayWindow.focus();
    }
  });
  
  return tray;
}

function registerShortcuts() {
  const settings = getSettings();
  const shortcutKey = settings.shortcut_key || 'CommandOrControl+Shift+C';
  
  globalShortcut.register(shortcutKey, () => {
    if (overlayWindow.isVisible()) {
      overlayWindow.hide();
    } else {
      overlayWindow.show();
      overlayWindow.focus();
    }
  });
}

// IPC Handlers
ipcMain.handle('window:minimize', () => {
  overlayWindow.minimize(); // Use normal minimize instead of hide
});

ipcMain.handle('window:close', () => {
  overlayWindow.hide();
});

ipcMain.handle('window:maximize', () => {
  if (overlayWindow.isMaximized()) {
    overlayWindow.unmaximize();
  } else {
    overlayWindow.maximize();
  }
});

ipcMain.handle('window:show', () => {
  overlayWindow.show();
  overlayWindow.focus();
});

ipcMain.handle('settings:get', () => {
  return getSettings();
});

ipcMain.handle('settings:save', async (event, settings) => {
  return saveSettings(settings);
});

ipcMain.handle('davinci:check', async () => {
  try {
    const pythonScript = path.join(__dirname, '../python-scripts/davinci_execute.py');
    const result = await executePythonScript(pythonScript, ['--check']);
    return { connected: result.success, message: result.message };
  } catch (error) {
    return { connected: false, message: error.message };
  }
});

ipcMain.handle('davinci:execute', async (event, code) => {
  try {
    const pythonScript = path.join(__dirname, '../python-scripts/davinci_execute.py');
    const result = await executePythonScript(pythonScript, [code]);
    return result;
  } catch (error) {
    return { success: false, message: error.message };
  }
});

ipcMain.handle('db:query', async (event, query, params = []) => {
  try {
    const results = await databaseManager.query(query, params);
    return results;
  } catch (error) {
    throw new Error(`Database error: ${error.message}`);
  }
});

ipcMain.handle('openai:process', async (event, message, context) => {
  try {
    const settings = getSettings();
    if (!settings.openai_api_key) {
      throw new Error('OpenAI API key not configured');
    }

    // Build prompt with context
    const prompt = buildPrompt(message, context);
    const response = await callOpenAI(prompt, settings.openai_api_key);
    
    return {
      explanation: response.explanation,
      code: response.code,
      safe: response.safe
    };
  } catch (error) {
    throw new Error(`OpenAI processing error: ${error.message}`);
  }
});

function buildPrompt(message, context) {
  const systemPrompt = `You are Cench AI, an assistant that helps with DaVinci Resolve video editing. 
  
Available DaVinci Resolve API methods:
- resolve.GetProjectManager().GetCurrentProject()
- project.GetMediaPool()
- project.GetCurrentTimeline()
- timeline.AddTrack("video" | "audio")
- timeline.DeleteClips(clips)
- timeline.AddTransition("Cross Dissolve" | "Fade to Color" | etc.)
- timeline_item.SetClipSpeed(speed_percentage)
- mediaPool.ImportMedia(file_paths)
- project.LoadRenderPreset(preset_name)

Generate valid Python code for DaVinci Resolve. Always include error handling and safety checks.`;

  const contextText = context.messages ? 
    context.messages.map(msg => `${msg.type}: ${msg.content}`).join('\n') : '';

  return `${systemPrompt}

Previous conversation:
${contextText}

User request: ${message}

Generate a response with:
1. A clear explanation of what you'll do
2. Safe Python code for DaVinci Resolve
3. Safety assessment (safe/unsafe)`;
}

async function callOpenAI(prompt, apiKey) {
  const fetch = (await import('node-fetch')).default;
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a helpful assistant that generates DaVinci Resolve Python code.' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 1000,
      temperature: 0.3
    })
  });

  if (!response.ok) {
    throw new Error(`OpenAI API error: ${response.statusText}`);
  }

  const data = await response.json();
  const content = data.choices[0].message.content;

  // Parse the response to extract explanation and code
  const explanationMatch = content.match(/(.*?)(?=```python|$)/s);
  const codeMatch = content.match(/```python\s*([\s\S]*?)\s*```/);

  return {
    explanation: explanationMatch ? explanationMatch[1].trim() : content,
    code: codeMatch ? codeMatch[1].trim() : null,
    safe: true // We'll implement safety checks later
  };
}

async function executePythonScript(scriptPath, args = []) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', [scriptPath, ...args]);
    
    let stdout = '';
    let stderr = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (error) {
          resolve({ success: true, message: stdout });
        }
      } else {
        reject(new Error(stderr || `Python script failed with code ${code}`));
      }
    });
    
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to execute Python script: ${error.message}`));
    });
  });
}

app.whenReady().then(async () => {
  await initializeDatabase();
  createOverlayWindow();
  createTray();
  registerShortcuts();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createOverlayWindow();
  }
});

app.on('before-quit', () => {
  app.isQuiting = true;
}); 