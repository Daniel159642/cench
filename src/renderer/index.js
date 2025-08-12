import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles/overlay.css';

const container = document.getElementById('root');

if (!container) {
  throw new Error('Root container not found');
}

const root = createRoot(container);

try {
  root.render(React.createElement(App));
} catch (error) {
  console.error('Error rendering app:', error);
} 