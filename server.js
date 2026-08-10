const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname)));

// Fallback to index or viewer if requested files are missing
app.get('*', (req, res, next) => {
    const filePath = path.join(__dirname, req.path === '/' ? '/viewer.html' : req.path);
    res.sendFile(filePath, (err) => {
        if (err) {
            // If file doesn't exist, send viewer.html as default fallback
            res.sendFile(path.join(__dirname, 'viewer.html'), (innerErr) => {
                if (innerErr) {
                    res.status(404).send('Error: Could not locate web pages in repository root directory.');
                }
            });
        }
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
});