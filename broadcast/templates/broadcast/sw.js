// Service worker: makes the site installable and handles push notifications.
// Pages are always fetched fresh; the cache is only an offline fallback.

const CACHE_NAME = 'scmm-app-shell-v4';
const APP_SHELL = [
  '/viewer.html',
  '/index.html',
  '/icon-192.png',
  '/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      // Add files one by one so one missing file can't break the install.
      Promise.all(APP_SHELL.map((url) => cache.add(url).catch(() => {})))
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);
  // Only handle plain GETs for this site's own files; leave everything else to the browser.
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;
  if (url.pathname.startsWith('/api/')) return;

  event.respondWith(
    fetch(req, { cache: 'no-store' })
      .catch(() => caches.match(req).then((hit) => hit || Response.error()))
  );
});

self.addEventListener('push', (event) => {
  let data = { title: 'SCMM Live Media Center', body: 'A new announcement was just posted.' };
  try {
    if (event.data) data = event.data.json();
  } catch (e) {
    // fall back to default text above
  }

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icon-192.png',
      badge: '/icon-192.png',
      vibrate: [100, 50, 100],
      data: { url: '/viewer.html' }
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes('viewer.html') && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow('/viewer.html');
      }
    })
  );
});