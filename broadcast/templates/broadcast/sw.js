// Minimal service worker — just enough to make the site installable as an app.
// Does not cache posts/comments (those must always be fetched fresh from the cloud).

const CACHE_NAME = 'scmm-app-shell-v3';
const APP_SHELL = [
  '/viewer.html',
  '/index.html',
  '/icon-192.png',
  '/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
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
  // Network-first: always try to get the freshest page/data, fall back to cache if offline.
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});

// Show a system notification when the server pushes a new post alert.
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

// Tapping the notification opens (or focuses) the viewer page.
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