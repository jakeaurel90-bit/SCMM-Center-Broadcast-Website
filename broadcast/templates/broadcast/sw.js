// Minimal service worker — just enough to make the site installable as an app.
// Does not cache posts/comments (those must always be fetched fresh from the cloud).

const CACHE_NAME = 'scmm-app-shell-v1';
const APP_SHELL = [
  '/viewer.html',
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