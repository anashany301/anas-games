const CACHE_NAME = 'flingo-cache-v41'; // غير الرقم ده (v42, v43...) مع كل تحديث كبير ترفعه

// تثبيت وفحص النسخة الجديدة
self.addEventListener('install', (event) => {
    self.skipWaiting(); // اجبار الخدمة الجديدة على العمل فوراً
});

// تنظيف الكاش القديم تماماً
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache); // مسح أي كاش قديم
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// جلب الملفات المحدثة
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
