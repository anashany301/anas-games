const CACHE_NAME = 'flamingo-games-auto-sync-v2';

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

// دالة الفحص والتحميل مع إرسال إشعار للموقع عند تنزيل لعبة جديدة
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
                        
                        // إرسال إشعار للمتصفح والموقع
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
    } catch (error) {
        // خطأ صامت في حالة عدم وجود إنترنت
    }
}

// تثبيت الملفات الأساسية
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

// تفعيل وتشغيل الفحص السريع
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
            backgroundSyncNewGames();
        })
    );
    self.clients.claim();
});

// التشغيل الذكي أوفلاين
self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('api.github.com')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
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
