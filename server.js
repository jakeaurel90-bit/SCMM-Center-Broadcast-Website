const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname)));

app.get(['/', '/viewer.html', '/live', '/LIVE'], (req, res) => {
    res.sendFile(path.join(__dirname, 'viewer.html'));
});

app.get(['/login.html', '/login'], (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.get(['/logout.html', '/logout'], (req, res) => {
    res.sendFile(path.join(__dirname, 'logout.html'));
});

app.get(['/index.html', '/admin'], (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
});