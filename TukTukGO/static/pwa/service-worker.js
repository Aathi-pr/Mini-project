// service-worker.js
const CACHE_NAME = "tuktukgo-cache-v1";
const urlsToCache = [
  "/",
  "/static/css/nav.css",
  "/static/css/styles.css",
  "/static/css/bookingPage.css",
  "https://unpkg.com/leaflet/dist/leaflet.css",
  "https://unpkg.com/leaflet/dist/leaflet.js",
  "/static/img/icons8-location-marker-24.png",
  "/static/img/icons8-destination-48.png",
  "/static/img/icons8-auto-ricksaw-64.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache)),
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => response || fetch(event.request)),
  );
});
