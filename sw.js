const CACHE_NAME = 'flamingo-games-auto-sync-v1';

const username = "anashany301"; 
const repo = "anas-games"; 

const excludedFiles = [
    'index.html', 
    'room.html',
    'sw.js',
    'manifest.json',
    'icon.png',
    'multiplayer-helper.html', 
    'injector.py', 
    'vercel.json', 
    'package.json', 
    'server.js',
    'README.md'
];

// دالة الفحص السريع والتحميل الفوري وتتم في أقل من ثانية
async function backgroundSyncNewGames() {
    try {
        const cache = await caches.open(CACHE_NAME);
        
        // جلب قائمة الألعاب من جيت هب
        const response = await fetch(`https://api.github.com/repos/${username}/${repo}/contents/`);
        if (!response.ok) return;
        
        const files = await response.json();
        
        for (const file of files) {
            if (file.name.endsWith('.html') && !excludedFiles.includes(file.name)) {
                const gameUrl = `./${file.name}`;
                
                // هل اللعبة موجودة مسبقاً في الكاش؟
                const cachedMatch = await cache.match(gameUrl);
                
                // لو مش موجودة (يعني لعبة جديدة نازلة)، نزلها فوراً واقفل العملية
                if (!cachedMatch) {
                    const gameResponse = await fetch(gameUrl);
                    if (gameResponse.status === 200) {
                        await cache.put(gameUrl, gameResponse);
                        console.log(`تم تنزيل اللعبة الجديدة بنجاح: ${file.name}`);
                    }
                }
            }
        }
    } catch (error) {
        // لو مفيش نت، اخرج فوراً بدون أي أخطاء
    }
}

// 1. التثبيت الأولي للملفات الأساسية
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll([
                './',
                './index.html',
                './room.html',
                './manifest.json',
                './icon.png'
            ]);
        })
    );
    self.skipWaiting();
});

// 2. التفعيل وبدء الفحص والتحميل السريع في نفس الثانية أول ما يفتح
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(async (cacheNames) => {
            await Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
            // تشغيل الفحص السريع واغلاق العملية
            backgroundSyncNewGames();
        })
    );
    self.clients.claim();
});

// 3. التشغيل أوفلاين وسحب أي ملفات جديدة فوراً عند الطلب
self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('api.github.com')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                // تحديث صامت في الخلفية لو النت شغال
                fetch(event.request).then((networkResponse) => {
                    if (networkResponse.status === 200) {
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse);
                        });
                    }
                }).catch(() => {});
                
                return cachedResponse;
            }

            return fetch(event.request).then((networkResponse) => {
                const responseClone = networkResponse.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    if (event.request.method === 'GET' && networkResponse.status === 200) {
                        cache.put(event.request, responseClone);
                    }
                });
                return networkResponse;
            }).catch(() => {
                if (event.request.headers.get('accept').includes('text/html')) {
                    return caches.match('./index.html');
                }
            });
        })
    );
});
