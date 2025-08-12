# Cench AI - DaVinci Resolve Assistant

An AI-powered desktop assistant that helps you edit videos in DaVinci Resolve using natural language commands. Cench AI runs as a floating overlay application, similar to how Cluely works with other software.

## Features

- 🤖 **AI-Powered Editing**: Use natural language to control DaVinci Resolve
- 🖥️ **Floating Overlay**: Always-on-top chat interface that stays out of your way
- 🔧 **System Tray Integration**: Runs in the background with quick access
- ⌨️ **Global Shortcuts**: Toggle overlay with Ctrl+Shift+C (customizable)
- 🛡️ **Safe Execution**: Code safety checks before executing commands
- 📚 **Command Database**: Local SQLite database with DaVinci commands
- ⚙️ **Customizable Settings**: Configure OpenAI API, auto-execute, and more

## Prerequisites

Before installing Cench AI, make sure you have:

- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Python 3.8+** - [Download here](https://python.org/)
- **DaVinci Resolve 18+** - [Download here](https://www.blackmagicdesign.com/products/davinciresolve)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## Installation

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/cench-ai-desktop.git
   cd cench-ai-desktop
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install DaVinciResolveScript
   ```

4. **Start in development mode**
   ```bash
   npm run dev
   ```

### Production Build

1. **Build the application**
   ```bash
   npm run build
   npm run dist
   ```

2. **Install the generated application**
   - **macOS**: Open the `.dmg` file in `dist/`
   - **Windows**: Run the `.exe` installer in `dist/`
   - **Linux**: Extract the `.AppImage` in `dist/`

## First Time Setup

1. **Launch Cench AI**
   - The application will start in your system tray
   - Use `Ctrl+Shift+C` to open the overlay

2. **Configure OpenAI API**
   - Click the settings gear icon (⚙️)
   - Enter your OpenAI API key
   - Click "Save Settings"

3. **Test DaVinci Connection**
   - In settings, click "Test DaVinci Resolve Connection"
   - Make sure DaVinci Resolve is running

4. **Start Editing!**
   - Type natural language commands like:
     - "Add a new video track"
     - "Speed up this clip to 2x"
     - "Add a cross dissolve transition"

## Usage Examples

### Basic Editing Commands
```
"Add a new video track"
"Create a new timeline called Main Edit"
"Import the video files from my desktop"
"Add a title that says Opening Scene"
```

### Timeline Operations
```
"Delete the selected clips"
"Add a cross dissolve between these clips"
"Make this clip play at half speed"
"Create a new audio track"
```

### Effects and Transitions
```
"Add a fade to black transition"
"Apply a color correction preset"
"Add a blur effect to this clip"
"Create a picture-in-picture effect"
```

## Configuration

### Settings Options

- **OpenAI API Key**: Your OpenAI API key for AI processing
- **Auto-execute**: Automatically run safe commands without confirmation
- **Overlay Opacity**: Adjust the transparency of the overlay window
- **Global Shortcut**: Customize the keyboard shortcut (default: Ctrl+Shift+C)

### Safety Features

- **Code Validation**: All generated code is checked for safety
- **Sandboxed Execution**: Python code runs in a restricted environment
- **Confirmation Required**: Dangerous operations require user approval

## Architecture

### Project Structure
```
cench-desktop-mvp/
├── src/
│   ├── main/           # Electron main process
│   ├── renderer/       # React frontend
│   ├── database/       # SQLite database & schema
│   └── python-scripts/ # DaVinci Resolve integration
├── assets/             # Icons and resources
└── dist/              # Built application
```

### Key Components

- **Main Process** (`src/main/`): Electron app lifecycle, IPC handlers
- **Renderer Process** (`src/renderer/`): React UI components
- **Python Integration** (`src/python-scripts/`): DaVinci Resolve API wrapper
- **Database** (`src/database/`): Command storage and chat history

## Troubleshooting

### Common Issues

**"DaVinci Resolve not connected"**
- Make sure DaVinci Resolve is running
- Check if you have the correct version installed
- Verify Python DaVinciResolveScript is installed

**"OpenAI API error"**
- Verify your API key is correct
- Check your OpenAI account has credits
- Ensure you're using a valid API key format

**"Application won't start"**
- Check Node.js version (requires 18+)
- Verify all dependencies are installed
- Check system requirements

### Logs and Debugging

- **Development**: Check browser console for errors
- **Production**: Check application logs in AppData folder
- **Python Scripts**: Check terminal output for Python errors

## Development

### Adding New Commands

1. **Add to database** (`src/database/seed-data.sql`)
2. **Update Python wrapper** (`src/python-scripts/davinci_execute.py`)
3. **Test with natural language**

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/your-username/cench-ai-desktop/issues)
- **Documentation**: [Wiki](https://github.com/your-username/cench-ai-desktop/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/cench-ai-desktop/discussions)

## Roadmap

- [ ] **Voice Commands**: Support for voice input
- [ ] **Custom Presets**: Save and reuse command sequences
- [ ] **Batch Processing**: Multiple clips at once
- [ ] **Project Templates**: Quick project setup
- [ ] **Collaboration**: Share commands with team
- [ ] **Cloud Sync**: Settings and history sync

---

**Made with ❤️ for video editors everywhere** 