#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 Testing Cench AI Desktop MVP Setup...\n');

// Test file structure
const requiredFiles = [
  'package.json',
  'vite.config.js',
  'index.html',
  'src/main/main.js',
  'src/main/preload.js',
  'src/main/settings.js',
  'src/renderer/index.js',
  'src/renderer/App.jsx',
  'src/renderer/components/ChatOverlay.jsx',
  'src/renderer/components/MessageBubble.jsx',
  'src/renderer/components/SettingsPanel.jsx',
  'src/renderer/components/StatusIndicator.jsx',
  'src/renderer/components/FloatingControls.jsx',
  'src/renderer/hooks/useChat.js',
  'src/renderer/styles/overlay.css',
  'src/database/database-manager.js',
  'src/database/schema.sql',
  'src/database/seed-data.sql',
  'src/python-scripts/davinci_execute.py',
  'README.md'
];

console.log('📁 Checking file structure...');
let allFilesExist = true;

requiredFiles.forEach(file => {
  const exists = fs.existsSync(file);
  console.log(`${exists ? '✅' : '❌'} ${file}`);
  if (!exists) allFilesExist = false;
});

// Test package.json dependencies
console.log('\n📦 Checking package.json...');
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  const requiredDeps = ['electron', 'react', 'react-dom', 'sqlite3'];
  const requiredDevDeps = ['@vitejs/plugin-react', 'vite', 'electron-builder'];
  
  console.log('✅ package.json is valid JSON');
  
  requiredDeps.forEach(dep => {
    const exists = packageJson.dependencies && packageJson.dependencies[dep];
    console.log(`${exists ? '✅' : '❌'} ${dep} dependency`);
  });
  
  requiredDevDeps.forEach(dep => {
    const exists = packageJson.devDependencies && packageJson.devDependencies[dep];
    console.log(`${exists ? '✅' : '❌'} ${dep} dev dependency`);
  });
  
} catch (error) {
  console.log('❌ package.json is invalid JSON');
  allFilesExist = false;
}

// Test build output
console.log('\n🔨 Checking build output...');
const distExists = fs.existsSync('dist');
console.log(`${distExists ? '✅' : '❌'} dist/ directory exists`);

if (distExists) {
  const distFiles = fs.readdirSync('dist');
  const hasIndex = distFiles.includes('index.html');
  const hasAssets = distFiles.includes('assets');
  console.log(`${hasIndex ? '✅' : '❌'} dist/index.html exists`);
  console.log(`${hasAssets ? '✅' : '❌'} dist/assets/ directory exists`);
}

// Test database schema
console.log('\n🗄️ Checking database schema...');
try {
  const schema = fs.readFileSync('src/database/schema.sql', 'utf8');
  const hasCommandsTable = schema.includes('CREATE TABLE') && schema.includes('davinci_commands');
  const hasChatHistory = schema.includes('CREATE TABLE') && schema.includes('chat_history');
  console.log(`${hasCommandsTable ? '✅' : '❌'} davinci_commands table defined`);
  console.log(`${hasChatHistory ? '✅' : '❌'} chat_history table defined`);
} catch (error) {
  console.log('❌ Could not read schema.sql');
  allFilesExist = false;
}

// Test Python script
console.log('\n🐍 Checking Python integration...');
try {
  const pythonScript = fs.readFileSync('src/python-scripts/davinci_execute.py', 'utf8');
  const hasDaVinciImport = pythonScript.includes('DaVinciResolveScript');
  const hasConnectionCheck = pythonScript.includes('check_connection');
  const hasSafetyCheck = pythonScript.includes('is_safe_code');
  console.log(`${hasDaVinciImport ? '✅' : '❌'} DaVinciResolveScript import`);
  console.log(`${hasConnectionCheck ? '✅' : '❌'} Connection check function`);
  console.log(`${hasSafetyCheck ? '✅' : '❌'} Safety check function`);
} catch (error) {
  console.log('❌ Could not read davinci_execute.py');
  allFilesExist = false;
}

// Test React components
console.log('\n⚛️ Checking React components...');
try {
  const appComponent = fs.readFileSync('src/renderer/App.jsx', 'utf8');
  const chatOverlay = fs.readFileSync('src/renderer/components/ChatOverlay.jsx', 'utf8');
  const hasReactImport = appComponent.includes('import React');
  const hasChatHook = chatOverlay.includes('useChat');
  console.log(`${hasReactImport ? '✅' : '❌'} React imports`);
  console.log(`${hasChatHook ? '✅' : '❌'} useChat hook usage`);
} catch (error) {
  console.log('❌ Could not read React components');
  allFilesExist = false;
}

// Test CSS
console.log('\n🎨 Checking CSS styling...');
try {
  const css = fs.readFileSync('src/renderer/styles/overlay.css', 'utf8');
  const hasChatOverlay = css.includes('.chat-overlay');
  const hasDarkTheme = css.includes('rgba(10, 10, 15');
  console.log(`${hasChatOverlay ? '✅' : '❌'} Chat overlay styles`);
  console.log(`${hasDarkTheme ? '✅' : '❌'} Dark theme colors`);
} catch (error) {
  console.log('❌ Could not read CSS file');
  allFilesExist = false;
}

// Summary
console.log('\n📊 Setup Summary:');
if (allFilesExist && distExists) {
  console.log('✅ Cench AI Desktop MVP is properly set up!');
  console.log('\n🚀 Next steps:');
  console.log('1. Install Python dependencies: pip install DaVinciResolveScript');
  console.log('2. Get OpenAI API key from https://platform.openai.com/api-keys');
  console.log('3. Run: npm run dev');
  console.log('4. Configure settings in the app');
  console.log('5. Test with DaVinci Resolve running');
} else {
  console.log('❌ Some issues found. Please check the errors above.');
}

console.log('\n📚 For more information, see README.md'); 