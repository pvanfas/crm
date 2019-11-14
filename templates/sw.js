var cacheName = 'Tutorial-v1';

var urlsToCache = [
    '/',

    '/static/css/app.css',
    '/static/css/app.min.1.css',
    '/static/css/app.min.2.css',
    '/static/css/demo.css',
];

self.addEventListener('install', function(event) {
    // Perform install steps
    console.log(cacheName + ' installing...');
    self.skipWaiting();

    event.waitUntil(
        caches.open(cacheName).then(function(cache) {
            console.log('Opened cache');
            cache.addAll(urlsToCache.map(function(urlsToCache) {
                return new Request(urlsToCache, { mode: 'no-cors' });
            })).then(function() {
                console.log('All resources have been fetched and cached.');
            });
        })
    );
});


self.addEventListener('activate', function(event) {

    var cacheWhitelist = ['Tutorial-v1',];

    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheWhitelist.indexOf(cacheName)  === -1) {
                        return caches.delete(cacheName);
                    }
                    console.log('activated');
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(async function() {
    const cache = await caches.open('mysite-dynamic');
    const cachedResponse = await cache.match(event.request);
    const networkResponsePromise = fetch(event.request);

    event.waitUntil(async function() {
      const networkResponse = await networkResponsePromise;
      await cache.put(event.request, networkResponse.clone());
    }());

    // Returned the cached response if we have one, otherwise return the network response.
    return cachedResponse || networkResponsePromise;
  }());
});


function addToHomeScreen() {  var a2hsBtn = document.querySelector(".ad2hs-prompt");  // hide our user interface that shows our A2HS button
  a2hsBtn.style.display = 'none';  // Show the prompt
  deferredPrompt.prompt();  // Wait for the user to respond to the prompt
  deferredPrompt.userChoice
    .then(function(choiceResult){

  if (choiceResult.outcome === 'accepted') {
    console.log('User accepted the A2HS prompt');
  } else {
    console.log('User dismissed the A2HS prompt');
  }

  deferredPrompt = null;

});}