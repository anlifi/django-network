import PostApp from './App';
import React from 'react';
import * as ReactDOMClient from 'react-dom/client';

// import HTMX and inject it into the window scope
window.htmx = require('htmx.org');


// Render PostApp
const container = document.getElementById('all-posts');
const root = ReactDOMClient.createRoot(container);
root.render(<PostApp />);