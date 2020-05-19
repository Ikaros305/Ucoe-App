const CACHE_NAME = "static-cache-v4";
const dynamicCacheName = "site-dynamic-v4";
const FILES_TO_CACHE = [
  "/offline",
  "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
  "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css",
  "/static/assets/css/all.min.css",
  "/static/assets/css/bootstrap.min.css",
  "/static/assets/css/bootstrap.min.css.map",
  "/static/assets/css/chosen.min.css",
  "/static/assets/css/demo.css",
  "/static/assets/css/depart.css",
  "/static/assets/css/feed.css",
  "/static/assets/css/font-awesome.min.css",
  "/static/assets/css/jquery.mCustomScrollbar.min.css",
  "/static/assets/css/main.css",
  "/static/assets/css/main2.css",
  "/static/assets/css/man.css",
  "/static/assets/css/poppins.css",
  "/static/assets/css/regular.min.css",
  "/static/assets/css/style.css",
  "/static/assets/css/style.css.map",
  "/static/assets/css/style1.css",
  "/static/assets/css/swiper.min.css",
  "/static/assets/js/jquery.min.js",
  "/static/assets/js/jquery.nicescroll.js",
  "/static/assets/js/skel.min.js",
  "/static/assets/js/util.js",
  "/static/assets/js/main.js",
  "/static/assets/js/state.js",
  "/static/assets/js/jquery-3.3.1.min.js",
  "/static/assets/js/aos.js",
  "/static/assets/js/res.js",
  "/static/assets/js/swiper.min.js",
  "/static/assets/js/select.js",
];

const limitCacheSize = (name, size) => {
  caches.open(name).then((cache) => {
    cache.keys().then((keys) => {
      if (keys.length > size) {
        cache.delete(keys[0]).then(limitCacheSize(name, size));
      }
    });
  });
};

self.addEventListener("install", (evt) => {
  console.log("ServiceWorker Install");
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[ServiceWorker] Pre-caching offline page");
      return cache.addAll(FILES_TO_CACHE);
    }),
  );
  self.skipWaiting();
  console.log("Skipped Waiting");
});
self.addEventListener("activate", (evt) => {
  console.log("ServiceWorker Activate");
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("[ServiceWorker] Removing old cache", key);
            return caches.delete(key);
          }
        }),
      );
    }),
  );
  self.clients.claim();
});
// fetch event
self.addEventListener("fetch", (evt) => {
  //console.log('fetch event', evt);
  evt.respondWith(
    caches
      .match(evt.request)
      .then((cacheRes) => {
        return (
          cacheRes ||
          fetch(evt.request).then((fetchRes) => {
            return caches.open(dynamicCacheName).then((cache) => {
              cache.put(evt.request.url, fetchRes.clone());
              // check cached items size
              limitCacheSize(dynamicCacheName, 15);
              return fetchRes;
            });
          })
        );
      })
      .catch(() => {
        if (evt.request.url.indexOf(".html") > -1) {
          return caches.match("/offline");
        }
      }),
  );
});
