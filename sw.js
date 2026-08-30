const CACHE_NAME = 'infinite-games-engine-v10';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './engine.json',
  './manifest.json'
];

// تثبيت التخزين المؤقت وتنزيل الملفات مرة واحدة بالكامل للملفات الأوفلاين
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] جاري تنزيل ملفات المحرك و الـ JSON للألعاب أوفلاين...');
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => {
      return self.skipWaiting();
    })
  );
});

// تفعيل الخدمة والتحكم الفوري بالمتصفح
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] حذف النسخ القديمة:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// اعتراض الطلبات وقراءتها من الذاكرة المحلية (Cache First) لضمان العمل بدون إنترنت نهائياً
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      }).catch(() => {
        // في حالة انقطاع الإنترنت تماماً وعدم وجود الطلب في الكاش
        if (event.request.destination === 'document') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
