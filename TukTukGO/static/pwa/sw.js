// static/pwa/sw.js
const PWA_CACHE = "pwa-v0.0.1";
const PWA_URLS = [
  "/",
  "/static/css/styles.css",
  "/static/js/app.js",
  "/static/img/Screenshot_2024-08-14-13-26-38-876_com.android.chrome.png",
  "/static/img/Screenshot_2024-08-14-13-25-55-716_com.android.chrome.png",
  "/static/img/pwa.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(PWA_CACHE)
      .then((cache) => {
        console.log("Caching resources...");
        return cache.addAll(PWA_URLS);
      })
      .catch((error) => {
        console.error("Failed to cache resources:", error);
      }),
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
      .catch((error) => {
        console.error("Fetch failed:", error);
      }),
  );
});
