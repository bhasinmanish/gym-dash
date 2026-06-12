const CACHE = 'gym-dash-v1';
const PRECACHE = [
  '.',
  'index.html',
  'manifest.json',
  'icon.svg',
  'tips.json',
  'config.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.allSettled(PRECACHE.map(u => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  if (new URL(e.request.url).pathname.startsWith('/api/')) return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      const live = fetch(e.request).then(resp => {
        if (resp.ok) {
          const url = e.request.url;
          // don't cache CDN resources or data files (they change)
          if (!url.includes('cdn.') && !url.includes('/data/')) {
            caches.open(CACHE).then(c => c.put(e.request, resp.clone()));
          }
        }
        return resp;
      }).catch(() => null);
      return cached || live;
    })
  );
});
