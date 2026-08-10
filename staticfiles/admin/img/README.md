# SCMM Media Center - Real Streaming Setup

This replaces the fake "Start Streaming" simulation with a real relay:

**Browser (camera+mic) → WebSocket → Node server → ffmpeg → RTMP → Facebook + YouTube (simultaneously)**

## What's real now vs. still simulated

- **Real:** the video/audio captured from your camera and mic is actually transcoded
  and pushed live to Facebook and YouTube via RTMP when you click Start Streaming.
- **Real:** login is checked server-side with a hashed password and a session cookie,
  not a hardcoded string in the JavaScript.
- **Still simulated:** the "FB Viewers" / "YT Viewers" numbers and the on-screen VU
  meter animation. Real viewer counts require polling the YouTube Data API and
  Facebook Graph API with OAuth tokens tied to the live broadcast — a separate,
  optional add-on if you want it later.

## 1. Prerequisites on the server/machine that will run this

- Node.js 18+
- **ffmpeg** installed and on your PATH. Check with `ffmpeg -version`.
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: install from ffmpeg.org and add to PATH

This server needs to run continuously with a decent upload connection while you're
live (it's re-encoding and uploading video). A small VPS (DigitalOcean, Railway,
a Linux box at the church) works well. It does not need to be the same machine as
the camera if you access the dashboard over the network — but your best bet for a
church setup is usually running it locally on the media booth computer.

## 2. Install dependencies

```bash
cd scmm-stream
npm install
```

## 3. Configure `.env`

```bash
cp .env.example .env
```

Then edit `.env`:

- `SESSION_SECRET` — generate one:
  ```bash
  node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
  ```
- `ADMIN_USERNAME` — whatever login username you want.
- `ADMIN_PASSWORD_HASH` — generate a hash of your chosen password:
  ```bash
  node -e "console.log(require('bcryptjs').hashSync('yourpassword', 10))"
  ```
  Paste the output (starts with `$2a$...`) as the value. Never put the plain
  password itself in `.env`.

### Getting your YouTube stream key
1. Go to YouTube Studio → **Go Live** → **Stream**.
2. Copy the **Stream URL** and **Stream key** shown there.
3. Put the URL in `YT_STREAM_URL` and the key in `YT_STREAM_KEY`.

### Getting your Facebook stream key
1. Go to Facebook **Live Producer** (facebook.com/live/producer) → **Use Stream Key**.
2. Copy the **Server URL** and **Stream Key**.
3. Put them in `FB_STREAM_URL` and `FB_STREAM_KEY`.

Stream keys are secrets — anyone with your key can broadcast to your channel/page.
Never commit `.env` to git (it's already in `.gitignore`).

## 4. Run it

```bash
npm start
```

Visit `http://localhost:3000` (or your server's address). Log in, allow camera/mic
access, and hit **Start Streaming**. Check YouTube Studio and Facebook Live Producer
— both should show an incoming stream within a few seconds.

## 5. Notes / troubleshooting

- If the stream doesn't show up on one platform, check the server console —
  ffmpeg's stderr output is logged there and will show connection errors
  (bad stream key, network issues, etc.).
- If you only want to test one platform first, just leave the other's
  `_STREAM_KEY` blank in `.env` — the relay will only push to whichever
  platform(s) have a key configured.
- For production use behind a domain with HTTPS, put this behind a reverse
  proxy (nginx/Caddy) that terminates TLS and forwards to this Node app —
  the WebSocket upgrade will work fine through either of those.
