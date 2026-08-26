const CACHE_NAME = 'anas-games-full-v1';

// الملفات الأساسية اللي لازم تنزل فوراً
const coreAssets = [
    './',
    './index.html',
    './room.html'
];

// تثبيت الخدمة وتحميل الأساسيات أولاً
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(coreAssets);
        })
    );
    self.skipWaiting();
});

// تفعيل النسخة الجديدة وحذف القديمة لتوفير المساحة
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// جلب الملفات: المحاولة من الذاكرة أولاً (أوفلاين)، والتحديث من السيرفر في الخلفية لو فيه نت
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            // لو الملف موجود في الذاكرة، هاته فوراً وبسرعة البرق
            if (cachedResponse) {
                // وفي الخلفية، لو فيه نت، حدث الكاش بنسخة السيرفر بصمت
                fetch(event.request).then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse);
                        });
                    }
                }).catch(() => {});
                
                return cachedResponse;
            }

            // لو الملف مش موجود، هاته من النت واحضنه في الكاش للمرة القادمة
            return fetch(event.request).then((networkResponse) => {
                if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                    return networkResponse;
                }
                const responseToCache = networkResponse.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseToCache);
                });
                return networkResponse;
            }).catch(() => {
                // لو النت مقطوع والملف مش موجود نهائي
            });
        })
    );
});
