const express = require('express');
const path = require('path');
const app = express();

// Serve all files (HTML, CSS, JS) from the current directory
app.use(express.static(__dirname));

// Specifically handle the routes to map to your HTML files
app.get(['/', '/viewer', '/live', '/LIVE', '/viewer.html'], (req, res) => {
    res.sendFile(path.join(__dirname, 'viewer.html'));
});

app.get(['/login', '/login.html'], (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.get(['/index', '/index.html', '/admin'], (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
});