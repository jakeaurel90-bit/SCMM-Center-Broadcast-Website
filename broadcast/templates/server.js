const express = require('express');
const path = require('path');
const webpush = require('web-push');
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

// ======================================================================
// PUSH NOTIFICATIONS
// Set these in Render's Environment Variables (not hardcoded, keeps your
// private key out of GitHub):
//   VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_CONTACT_EMAIL, FIREBASE_DB_URL
// FIREBASE_DB_URL points to the same Firebase Realtime Database your
// dashboard and viewer page use, storing who has notifications turned on.
// ======================================================================
const VAPID_PUBLIC_KEY = process.env.VAPID_PUBLIC_KEY || "BFwZRLbTkfdcScWrMdg_IKDUNTe8D702g1niyvtB11IEEKxvaxqzpPq0BKH0i_RZkVHsQyjkreGONPykxiK2SAk";
const VAPID_PRIVATE_KEY = process.env.VAPID_PRIVATE_KEY || "3RcSyhYecw8ndOqL2RMXHTA0g0JanRlT9bf03ilVlyQ";
const VAPID_CONTACT_EMAIL = process.env.VAPID_CONTACT_EMAIL || "mailto:jakeaurel90@gmail.com";

const FIREBASE_DB_URL = process.env.FIREBASE_DB_URL || "https://scmm-broadcast-default-rtdb.asia-southeast1.firebasedatabase.app";

webpush.setVapidDetails(VAPID_CONTACT_EMAIL, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY);

app.get('/api/vapid-public-key', (req, res) => {
    res.json({ publicKey: VAPID_PUBLIC_KEY });
});

async function getSubscriptions() {
    const r = await fetch(FIREBASE_DB_URL + "/pushSubscriptions.json?t=" + Date.now(), {
        cache: "no-store"
    });
    if (!r.ok) return [];
    const data = await r.json();
    return Array.isArray(data) ? data.filter(s => s && s.endpoint) : [];
}

async function saveSubscriptions(subs) {
    await fetch(FIREBASE_DB_URL + "/pushSubscriptions.json", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(subs)
    });
}

// Called by viewer.html once the person allows notifications.
app.post('/api/subscribe', async (req, res) => {
    try {
        const subscription = req.body;
        if (!subscription || !subscription.endpoint) {
            return res.status(400).json({ success: false });
        }
        const subs = await getSubscriptions();
        const alreadyExists = subs.some(s => s.endpoint === subscription.endpoint);
        if (!alreadyExists) {
            subs.push(subscription);
            await saveSubscriptions(subs);
        }
        res.json({ success: true });
    } catch (e) {
        console.error("Subscribe failed:", e);
        res.status(500).json({ success: false });
    }
});

// Called by index.html right after a new post is published.
app.post('/api/notify', async (req, res) => {
    try {
        const { title, body } = req.body || {};
        const subs = await getSubscriptions();
        const payload = JSON.stringify({
            title: title || 'SCMM Live Media Center',
            body: body || 'A new announcement was just posted.'
        });

        const stillValid = [];
        for (const sub of subs) {
            try {
                await webpush.sendNotification(sub, payload);
                stillValid.push(sub);
            } catch (err) {
                // 404/410 means that device unsubscribed or uninstalled - drop it quietly.
                if (err.statusCode !== 404 && err.statusCode !== 410) {
                    stillValid.push(sub);
                }
            }
        }

        if (stillValid.length !== subs.length) {
            await saveSubscriptions(stillValid);
        }

        res.json({ success: true, sent: stillValid.length });
    } catch (e) {
        console.error("Notify failed:", e);
        res.status(500).json({ success: false });
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