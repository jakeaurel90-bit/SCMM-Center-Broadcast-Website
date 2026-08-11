const express = require('express');
const path = require('path');
const app = express();

// server.js lives in broadcast/templates/
// The HTML pages actually live one folder deeper, in broadcast/templates/broadcast/
const PAGES_DIR = path.join(__dirname, 'broadcast');

// Serve static assets (CSS, JS, images) from that same folder
app.use(express.static(PAGES_DIR));

// Route handlers
app.get(['/', '/viewer', '/live', '/LIVE', '/viewer.html'], (req, res) => {
    res.sendFile(path.join(PAGES_DIR, 'viewer.html'));
});

app.get(['/login', '/login.html'], (req, res) => {
    res.sendFile(path.join(PAGES_DIR, 'login.html'));
});

app.get(['/index', '/index.html', '/admin'], (req, res) => {
    res.sendFile(path.join(PAGES_DIR, 'index.html'));
});

app.get(['/logout', '/logout.html'], (req, res) => {
    res.sendFile(path.join(PAGES_DIR, 'logout.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
});