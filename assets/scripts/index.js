import PostApp from './App';
import React from 'react';
import * as ReactDOMClient from 'react-dom/client';

// import HTMX and inject it into the window scope
window.htmx = require('htmx.org');


window.addEventListener('DOMContentLoaded', () => {
    // Get all posts container
    const post_container = document.getElementById('all-posts');
    // Get new post button an rerender PostApp
    const postBtn = document.getElementById('post-btn');

});
