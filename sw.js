const CACHE_NAME = 'flamingo-games-v5'; // رقم إصدار جديد لضمان التحديث الفوري

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

// 3. طريقة جلب الملفات: لو النت موجود هات الأحدث، لو قطع هات من الكاش فوراً
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            // لو الملف موجود في الكاش بنرجعه، وفي الخلفية بنحدثه لو فيه نت
            const fetchPromise = fetch(event.request).then((networkResponse) => {
                if (event.request.method === 'GET' && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return networkResponse;
            }).catch(() => {
                // لو النت فصل، نتجاهل الخطأ ونعتمد على الكاش
            });

            return cachedResponse || fetchPromise;
        }).catch(() => {
            return caches.match('./index.html');
        })
    );
});

// 4. الاستماع لأوامر تجهيز الألعاب الجديدة في الخلفية (مع الإشعار المخصص)
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'CACHE_NEW_GAME') {
        const gameUrl = event.data.url;
        const gameName = event.data.name;

        caches.open(CACHE_NAME).then((cache) => {
            cache.add(gameUrl).then(() => {
                console.log(`✅ تم تجهيز اللعبة للعب أوفلاين: ${gameName}`);
                // إرسال التنبيه للصفحة الرئيسية بالصيغة الذكية اللي طلبناها
                self.clients.matchAll().then((clients) => {
                    clients.forEach((client) => {
                        client.postMessage({
                            type: 'NEW_GAME_DOWNLOADED',
                            gameName: gameName
                        });
                    });
                });
            }).catch(err => {
                console.log('خطأ أثناء تخزين اللعبة:', err);
            });
        });
    }
});
