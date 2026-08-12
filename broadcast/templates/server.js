const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());

// server.js lives in broadcast/templates/
// The HTML pages actually live one folder deeper, in broadcast/templates/broadcast/
const PAGES_DIR = path.join(__dirname, 'broadcast');

// Serve static assets (CSS, JS, images) from that same folder
app.use(express.static(PAGES_DIR));

// Admin credentials - set these in Render's Environment Variables, NOT hardcoded here,
// so they never sit in your GitHub repo either. Fallback values below are just for local testing.
const ADMIN_USER = process.env.ADMIN_USER || "SCMM";
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "scmm2026admin";

// Login check happens here on the server, never exposed in browser-visible code.
app.post('/api/login', (req, res) => {
    const { username, password } = req.body || {};
    if (username === ADMIN_USER && password === ADMIN_PASSWORD) {
        res.json({ success: true });
    } else {
        res.status(401).json({ success: false });
    }
});

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
    // logout.html sits next to server.js, not inside the broadcast/ pages folder
    res.sendFile(path.join(__dirname, 'logout.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
});