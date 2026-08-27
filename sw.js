const CACHE_NAME = 'flaming-game-v1';
const assetsToCache = [
  'index.html',
  'room.html',
  'manifest.json'
];

// تثبيت وتخزين الملفات
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(assetsToCache);
    })
  );
});

// تشغيل الملفات من الذاكرة لو مفيش نت
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
