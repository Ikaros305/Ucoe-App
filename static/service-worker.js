const staticCacheName = "site-static-v9";
const dynamicCacheName = "site-dynamic-v9";
const assets = [
  "/",
  "/offline",
  "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
  "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css",
  "/static/assets/css/all.min.css",
  "/static/assets/css/asa.css",
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

// cache size limit function
const limitCacheSize = (name, size) => {
  caches.open(name).then((cache) => {
    cache.keys().then((keys) => {
      if (keys.length > size) {
        cache.delete(keys[0]).then(limitCacheSize(name, size));
      }
    });
  });
};

// install event
self.addEventListener("install", (evt) => {
  //console.log('service worker installed');
  evt.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      console.log("caching shell assets");
      cache.addAll(assets);
    }),
  );
  self.skipWaiting();
});

// activate event
self.addEventListener("activate", (evt) => {
  //console.log('service worker activated');
  evt.waitUntil(
    caches.keys().then((keys) => {
      //console.log(keys);
      return Promise.all(
        keys
          .filter((key) => key !== staticCacheName && key !== dynamicCacheName)
          .map((key) => caches.delete(key)),
      );
    }),
  );

  self.clients.claim();
});

// fetch event
self.addEventListener("fetch", (evt) => {
  if (evt.request.url.indexOf("firestore.googleapis.com") === -1) {
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
                limitCacheSize(dynamicCacheName, 20);
                return fetchRes;
              });
            })
          );
        })
        .catch(() => {
          return caches.match("/offline");
        }),
    );
  }
});
