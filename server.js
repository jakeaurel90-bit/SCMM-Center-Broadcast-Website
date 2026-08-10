require('dotenv').config();

const express = require('express');
const http = require('http');
const path = require('path');
const { spawn } = require('child_process');
const bcrypt = require('bcryptjs');
const session = require('express-session');
const cookie = require('cookie');
const signature = require('cookie-signature');
const WebSocket = require('ws');

const PORT = process.env.PORT || 3000;
const SESSION_SECRET = process.env.SESSION_SECRET;
const SESSION_COOKIE_NAME = 'scmm.sid';

if (!SESSION_SECRET) {
  console.error('FATAL: SESSION_SECRET is not set in .env. Refusing to start.');
  process.exit(1);
}
if (!process.env.ADMIN_USERNAME || !process.env.ADMIN_PASSWORD_HASH) {
  console.error('FATAL: ADMIN_USERNAME / ADMIN_PASSWORD_HASH not set in .env. Refusing to start.');
  console.error('Generate a hash with: node -e "console.log(require(\'bcryptjs\').hashSync(\'yourpassword\', 10))"');
  process.exit(1);
}

const app = express();
const server = http.createServer(app);

app.use(express.json());

// In-memory session store - fine for a single-instance internal tool.
const sessionStore = new session.MemoryStore();
const sessionMiddleware = session({
  name: SESSION_COOKIE_NAME,
  secret: SESSION_SECRET,
  store: sessionStore,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 1000 * 60 * 60 * 8 // 8 hours
  }
});
app.use(sessionMiddleware);
app.use(express.static(path.join(__dirname, 'public')));

// ---------- Auth routes ----------

app.post('/api/login', async (req, res) => {
  const { username, password } = req.body || {};
  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'Missing credentials' });
  }
  if (username !== process.env.ADMIN_USERNAME) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  const ok = await bcrypt.compare(password, process.env.ADMIN_PASSWORD_HASH);
  if (!ok) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  req.session.authenticated = true;
  res.json({ ok: true });
});

app.post('/api/logout', (req, res) => {
  req.session.destroy(() => res.json({ ok: true }));
});

app.get('/api/session', (req, res) => {
  res.json({ authenticated: !!(req.session && req.session.authenticated) });
});

function requireAuth(req, res, next) {
  if (req.session && req.session.authenticated) return next();
  res.status(401).json({ error: 'Not authenticated' });
}

app.get('/api/stream-status', requireAuth, (req, res) => {
  res.json({ live: !!ffmpegProcess });
});

// ---------- ffmpeg relay ----------

let ffmpegProcess = null;
let liveClient = null;

function buildTeeTarget() {
  const targets = [];
  if (process.env.YT_STREAM_URL && process.env.YT_STREAM_KEY) {
    targets.push(`[f=flv]${process.env.YT_STREAM_URL}/${process.env.YT_STREAM_KEY}`);
  }
  if (process.env.FB_STREAM_URL && process.env.FB_STREAM_KEY) {
    targets.push(`[f=flv]${process.env.FB_STREAM_URL}/${process.env.FB_STREAM_KEY}`);
  }
  return targets.join('|');
}

function startFfmpeg() {
  const teeTarget = buildTeeTarget();
  if (!teeTarget) {
    throw new Error('No stream targets configured. Set YT_STREAM_KEY and/or FB_STREAM_KEY in .env');
  }

  const args = [
    '-re',
    '-i', 'pipe:0',
    '-c:v', 'libx264',
    '-preset', 'veryfast',
    '-tune', 'zerolatency',
    '-b:v', '2500k',
    '-maxrate', '2500k',
    '-bufsize', '5000k',
    '-pix_fmt', 'yuv420p',
    '-g', '60',
    '-c:a', 'aac',
    '-ar', '44100',
    '-b:a', '128k',
    '-f', 'tee',
    teeTarget
  ];

  console.log('[ffmpeg] starting with args:', args.join(' ').replace(/rtmp[^ ]+/g, '<redacted-target>'));

  const proc = spawn('ffmpeg', args, { stdio: ['pipe', 'pipe', 'pipe'] });

  proc.stderr.on('data', (d) => {
    // ffmpeg logs progress/errors to stderr - useful for debugging connection issues.
    console.log('[ffmpeg]', d.toString().trim());
  });

  proc.on('error', (err) => {
    console.error('[ffmpeg] failed to start:', err.message);
    console.error('Is ffmpeg installed? Try: ffmpeg -version');
  });

  proc.on('close', (code) => {
    console.log('[ffmpeg] exited with code', code);
    ffmpegProcess = null;
    if (liveClient && liveClient.readyState === WebSocket.OPEN) {
      liveClient.send(JSON.stringify({ type: 'stopped', code }));
    }
    liveClient = null;
  });

  return proc;
}

function stopFfmpeg() {
  if (ffmpegProcess) {
    try {
      ffmpegProcess.stdin.end();
      ffmpegProcess.kill('SIGINT');
    } catch (e) {
      console.log('Error stopping ffmpeg:', e.message);
    }
    ffmpegProcess = null;
  }
}

// ---------- WebSocket ingest (auth-gated via session cookie) ----------

const wss = new WebSocket.Server({ noServer: true });

server.on('upgrade', (req, socket, head) => {
  if (!req.url.startsWith('/stream')) {
    socket.destroy();
    return;
  }

  const cookies = cookie.parse(req.headers.cookie || '');
  const raw = cookies[SESSION_COOKIE_NAME];
  if (!raw || !raw.startsWith('s:')) {
    socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
    socket.destroy();
    return;
  }
  const sid = signature.unsign(raw.slice(2), SESSION_SECRET);
  if (!sid) {
    socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
    socket.destroy();
    return;
  }

  sessionStore.get(sid, (err, sess) => {
    if (err || !sess || !sess.authenticated) {
      socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
      socket.destroy();
      return;
    }
    wss.handleUpgrade(req, socket, head, (ws) => {
      wss.emit('connection', ws, req);
    });
  });
});

wss.on('connection', (ws) => {
  ws.on('message', (msg, isBinary) => {
    if (!isBinary) {
      let data;
      try {
        data = JSON.parse(msg.toString());
      } catch (e) {
        return;
      }

      if (data.type === 'start') {
        if (ffmpegProcess) {
          ws.send(JSON.stringify({ type: 'error', message: 'Stream already running' }));
          return;
        }
        try {
          ffmpegProcess = startFfmpeg();
          liveClient = ws;
          ws.send(JSON.stringify({ type: 'started' }));
        } catch (e) {
          ws.send(JSON.stringify({ type: 'error', message: e.message }));
        }
      } else if (data.type === 'stop') {
        stopFfmpeg();
        ws.send(JSON.stringify({ type: 'stopped' }));
      }
      return;
    }

    // Binary message = a chunk of video/audio from MediaRecorder
    if (ffmpegProcess && ffmpegProcess.stdin.writable) {
      ffmpegProcess.stdin.write(msg);
    }
  });

  ws.on('close', () => {
    if (liveClient === ws) {
      stopFfmpeg();
    }
  });
});

server.listen(PORT, () => {
  console.log(`SCMM stream relay listening on port ${PORT}`);
});
