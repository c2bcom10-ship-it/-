/* 끝말 배틀: 한 번 열면 인터넷이 약해도 빨리 열리도록 파일을 저장해 둬요.
   (온라인 대결과 랭킹은 인터넷이 있어야 해요)
   게임을 고치면 아래 CACHE 이름의 숫자를 올려 주세요. */
const CACHE = 'kkeut-v1';
const FILES = ['./', './index.html', './words.txt', './supabase.js', './manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('kkeut-') && k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;   // Supabase 요청은 건드리지 않아요
  e.respondWith(
    fetch(e.request)
      .then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return res; })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
