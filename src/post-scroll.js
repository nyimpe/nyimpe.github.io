// Table-of-contents jumps replace the current entry so Back (or a mobile swipe) leaves the post.
export function keepSectionLinksOutOfHistory() {
  document.querySelector('main')?.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0
      || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest?.('a[href^="#"]');
    if (!link || link.hash.length < 2) return;
    event.preventDefault();
    // A replaced fragment navigation still scrolls, opens <details> and updates :target natively.
    location.replace(link.hash);
  });
}

// Keep reading positions on this browser, independently for each post/filter URL.
export function rememberPostScroll() {
  if (!/^\/posts\/[^/]+\/(?:index\.html)?$/.test(location.pathname)
    || !document.querySelector('main article')) return;

  const storageKey = () => {
    const params = new URLSearchParams(location.search);
    params.sort();
    const query = params.toString(); // URLSearchParams.size is missing on older mobile Safari.
    return `nyimpe-post-scroll:${location.pathname.replace(/index\.html$/, '')}${query ? `?${query}` : ''}`;
  };
  let saved;
  try {
    const value = localStorage.getItem(storageKey());
    if (value !== null && value.trim() !== '') {
      const position = Number(value);
      if (Number.isFinite(position) && position >= 0) saved = position;
    }
  } catch {
    // Reading still works when persistent storage is blocked.
  }

  // Explicit section links keep the browser's normal anchor navigation.
  let ready = saved === undefined || Boolean(location.hash);
  let timer;
  const save = () => {
    clearTimeout(timer);
    timer = undefined;
    if (!ready) return;
    try {
      localStorage.setItem(storageKey(), String(Math.max(0, window.scrollY)));
    } catch {
      // Storage denial or a full quota must not interrupt reading.
    }
  };

  window.addEventListener('scroll', () => {
    if (ready && timer === undefined) timer = setTimeout(save, 200);
  }, { passive: true });
  window.addEventListener('pagehide', save);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') save();
  });
  window.addEventListener('pageshow', (event) => {
    // A cached history page already has its exact position and expanded content.
    if (event.persisted) ready = true;
  });

  if (ready) return;
  history.scrollRestoration = 'manual';
  const cancelRestore = () => { ready = true; };
  const inputs = ['wheel', 'touchstart', 'pointerdown', 'keydown', 'hashchange'];
  for (const type of inputs) window.addEventListener(type, cancelRestore, { passive: true });

  const loaded = document.readyState === 'complete'
    ? Promise.resolve()
    : new Promise((resolve) => window.addEventListener('load', resolve, { once: true }));
  Promise.all([loaded, document.fonts?.ready]).then(() => {
    requestAnimationFrame(() => {
      if (!ready && !location.hash) {
        // Incremental catalogs reveal enough entries before applying the position.
        window.dispatchEvent(new CustomEvent('post-scroll-restore', { detail: { top: saved } }));
        window.scrollTo({ top: saved, behavior: 'instant' });
      }
      ready = true;
      for (const type of inputs) window.removeEventListener(type, cancelRestore);
    });
  });
}
