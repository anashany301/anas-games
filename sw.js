const CACHE_NAME = 'flamingo-games-v2';

// الملفات الأساسية للتطبيق
const STATIC_ASSETS = [
    './',
    './index.html',
    './room.html',
    './manifest.json'
];

// 1. عند تثبيت الـ Service Worker، بنحفظ الملفات الأساسية
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('📦 جاري حفظ الملفات الأساسية أوفلاين...');
            return cache.addAll(STATIC_ASSETS);
        })
    );
    self.skipWaiting();
});

// 2. تنظيف أي كاش قديم عند التحديث
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

// 3. طريقة جلب الملفات: لو النت قطع، هات من الكاش فوراً
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(event.request).then((networkResponse) => {
                // تخزين أي ملف يتفتح جديد في الذاكرة تلقائياً
                if (event.request.method === 'GET' && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return networkResponse;
            });
        }).catch(() => {
            // لو مفيش نت والملف مش في الكاش
            return caches.match('./index.html');
        })
    );
});

// 4. الاستماع لأوامر تنزيل الألعاب الجديدة في الخلفية
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'CACHE_NEW_GAME') {
        const gameUrl = event.data.url;
        const gameName = event.data.name;

        caches.open(CACHE_NAME).then((cache) => {
            cache.add(gameUrl).then(() => {
                console.log(`✅ تم تنزيل وحفظ اللعبة: ${gameName}`);
                // إرسال تنبيه للصفحة الرئيسية بأن اللعبة نزلت
                self.clients.matchAll().then((clients) => {
                    clients.forEach((client) => {
                        client.postMessage({
                            type: 'NEW_GAME_DOWNLOADED',
                            gameName: gameName
                        });
                    });
                });
            });
        });
    }
});
