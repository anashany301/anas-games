const CACHE_NAME = 'flamingo-games-auto-sync-v3';

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

// دالة فحص وجلب الألعاب الجديدة في الخلفية وصمت تام
async function backgroundSyncNewGames() {
    try {
        const cache = await caches.open(CACHE_NAME);
        const response = await fetch(`https://api.github.com/repos/${username}/${repo}/contents/`);
        if (!response.ok) return;
        
        const files = await response.json();
        
        for (const file of files) {
            if (file.name.endsWith('.html') && !excludedFiles.includes(file.name)) {
                const gameUrl = `./${file.name}`;
                const cachedMatch = await cache.match(gameUrl);
                
                if (!cachedMatch) {
                    const gameResponse = await fetch(gameUrl);
                    if (gameResponse.status === 200) {
                        await cache.put(gameUrl, gameResponse);
                        
                        // إرسال إشعار للموقع لو مفتوح
                        const clients = await self.clients.matchAll();
                        clients.forEach(client => {
                            client.postMessage({
                                type: 'NEW_GAME_DOWNLOADED',
                                gameName: file.name
                            });
                        });
                    }
                }
            }
        }
    } catch (error) {}
}

// 1. التثبيت السريع
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

// 2. التفعيل ومسح أي كاش قديم فوري
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(async (cacheNames) => {
            await Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName); // مسح النسخ القديمة بالكامل
                    }
                })
            );
            backgroundSyncNewGames();
        })
    );
    self.clients.claim();
});

// 3. استراتيجية Stale-While-Revalidate (عرض القديم بسرعة، وجلب الجديد وتحديثه في الخلفية لمرة قادمة)
self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('api.github.com')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            // جلب التحديث من النت في الخلفية بصمت وتحديث الكاش لو فيه تغيير
            const fetchPromise = fetch(event.request).then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return networkResponse;
            }).catch(() => {});

            // لو الملف موجود في الكاش رجعه فوراً بسرعة الصاروخ، ولو مش موجود استنى النت
            return cachedResponse || fetchPromise;
        })
    );
});
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => {
    e.waitUntil(caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k)))));
    self.clients.claim();
});
