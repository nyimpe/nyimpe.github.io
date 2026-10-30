import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

const source = readFileSync(new URL('../src/post-scroll.js', import.meta.url), 'utf8')
  .replaceAll('export function', 'function');

function setup({ path = '/posts/game-feel/', search = '', hash = '', saved,
  denied = false, loading = false } = {}) {
  const window = new EventTarget();
  const document = new EventTarget();
  const location = { pathname: path, search, hash };
  const history = { scrollRestoration: 'auto' };
  const key = `nyimpe-post-scroll:${path.replace(/index\.html$/, '')}${search}`;
  const storage = new Map(saved === undefined ? [] : [[key, saved]]);
  const timers = new Map();
  const frames = [];
  let timerId = 0;
  let writes = 0;
  window.scrollY = 0;
  window.scrollTo = ({ top }) => { window.scrollY = top; };
  document.querySelector = () => ({});
  document.readyState = loading ? 'loading' : 'complete';
  document.visibilityState = 'visible';
  document.fonts = { ready: Promise.resolve() };
  const event = (target, type, fields = {}) => {
    const e = new Event(type);
    Object.assign(e, fields);
    target.dispatchEvent(e);
  };
  runInNewContext(`${source}\nrememberPostScroll();`, {
    window, document, location, history, URLSearchParams,
    localStorage: {
      getItem: (k) => { if (denied) throw Error('blocked'); return storage.get(k) ?? null; },
      setItem: (k, v) => { if (denied) throw Error('blocked'); writes++; storage.set(k, v); },
    },
    CustomEvent: class extends Event {
      constructor(type, { detail }) { super(type); this.detail = detail; }
    },
    setTimeout: (fn) => { timers.set(++timerId, fn); return timerId; },
    clearTimeout: (id) => timers.delete(id),
    requestAnimationFrame: (fn) => frames.push(fn),
  });
  return {
    window, document, location, history, storage, key, timers,
    get writes() { return writes; },
    event,
    flushTimers() { for (const fn of [...timers.values()]) fn(); },
    async loaded() {
      event(window, 'load');
      await new Promise((resolve) => setImmediate(resolve));
      for (const fn of frames.splice(0)) fn();
    },
  };
}

const tests = {
  async 'save continuously, flush on hide/leave, and remember top'() {
    const s = setup();
    s.window.scrollY = 1250;
    for (let i = 0; i < 20; i++) s.event(s.window, 'scroll');
    assert.equal(s.timers.size, 1);
    s.flushTimers();
    assert.equal(s.storage.get(s.key), '1250');
    s.window.scrollY = 1500;
    s.document.visibilityState = 'hidden';
    s.event(s.document, 'visibilitychange');
    assert.equal(s.storage.get(s.key), '1500');
    s.window.scrollY = 0;
    s.event(s.window, 'pagehide');
    assert.equal(s.storage.get(s.key), '0');
  },
  async 'wait for layout and preserve the saved value during loading'() {
    const s = setup({ saved: '4000', loading: true });
    s.event(s.window, 'scroll');
    s.event(s.window, 'pagehide');
    assert.equal(s.writes, 0);
    let revealed;
    s.window.addEventListener('post-scroll-restore', (e) => { revealed = e.detail.top; });
    await s.loaded();
    assert.equal(revealed, 4000);
    assert.equal(s.window.scrollY, 4000);
    assert.equal(s.history.scrollRestoration, 'manual');
  },
  async 'respect section links and cached history pages'() {
    const anchor = setup({ saved: '4000', hash: '#chapter-2' });
    await anchor.loaded();
    assert.equal(anchor.window.scrollY, 0); // Browser owns the anchor jump.
    assert.equal(anchor.history.scrollRestoration, 'auto');
    const cached = setup({ saved: '4000' });
    cached.window.scrollY = 8500;
    cached.event(cached.window, 'pageshow', { persisted: true });
    await cached.loaded();
    assert.equal(cached.window.scrollY, 8500);
  },
  async 'cancel pending restoration when the reader interacts'() {
    for (const type of ['wheel', 'touchstart', 'pointerdown', 'keydown', 'hashchange']) {
      const s = setup({ saved: '4000', loading: true });
      s.event(s.window, type);
      s.window.scrollY = 300;
      await s.loaded();
      assert.equal(s.window.scrollY, 300, type);
    }
  },
  async 'normalize index URLs and keep posts/filter URLs separate'() {
    const s = setup({ path: '/posts/game-feel/index.html', saved: '2300' });
    await s.loaded();
    assert.equal(s.window.scrollY, 2300);
    s.location.pathname = '/posts/designing-games/';
    s.location.search = '?q=test&platform=dos';
    s.window.scrollY = 1200;
    s.event(s.window, 'pagehide');
    assert.equal(s.storage.get('nyimpe-post-scroll:/posts/designing-games/?platform=dos&q=test'), '1200');
    assert.equal(s.storage.get(s.key), '2300');
  },
  async 'ignore non-post pages, corrupt data and blocked storage'() {
    for (const path of ['/', '/about/']) {
      const s = setup({ path, saved: '4000' });
      s.event(s.window, 'pagehide');
      await s.loaded();
      assert.equal(s.writes, 0);
      assert.equal(s.window.scrollY, 0);
    }
    for (const saved of ['NaN', 'Infinity', '-20', '{bad}', '']) {
      const s = setup({ saved });
      await s.loaded();
      assert.equal(s.window.scrollY, 0);
    }
    const s = setup({ denied: true });
    await s.loaded();
    s.event(s.window, 'scroll');
    s.flushTimers();
    s.event(s.window, 'pagehide');
  },
};

tests['replace history for section links only'] = async () => {
  let onClick;
  const replaced = [];
  runInNewContext(`${source}\nkeepSectionLinksOutOfHistory();`, {
    document: { querySelector: () => ({ addEventListener: (type, fn) => { onClick = fn; } }) },
    location: { replace: (hash) => replaced.push(hash) },
  });
  const click = (link, fields = {}) => {
    const e = { button: 0, target: { closest: () => link }, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; }, ...fields };
    onClick(e);
    return e.defaultPrevented;
  };
  assert.equal(click({ hash: '#chapter-4' }), true);
  assert.equal(click({ hash: '#chapter-4' }, { metaKey: true }), false);
  assert.equal(click({ hash: '#chapter-4' }, { button: 1 }), false);
  assert.equal(click({ hash: '' }), false);
  assert.equal(click(null), false);
  assert.deepEqual(replaced, ['#chapter-4']);
};

for (const [name, test] of Object.entries(tests)) {
  await test();
  console.log(`PASS ${name}`);
}
