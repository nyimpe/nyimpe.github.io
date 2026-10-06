// NODE_PATH must provide playwright; pass a local preview or deployed base URL.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const sites = ['playretrogames', 'playretro-io', 'retrogames-onl-snes'];

(async () => {
  const base = process.argv[2] || 'http://127.0.0.1:8080';
  const tag = base.includes('127.0.0.1') ? 'local' : 'live';
  const live = tag === 'live';
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  const results = [];
  for (const site of sites) {
    const data = JSON.parse(await fs.readFile(path.resolve(__dirname, `../public/data/${site}-games.json`), 'utf8'));
    const url = `${base}/posts/${site}/`;
    const games = data.games;
    assert.equal(new Set(games.map((g) => g.id)).size, games.length);
    assert.equal(new Set(games.map((g) => g.source)).size, games.length);
    const response = await page.goto(url, { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200);
    await page.locator('.classic-filter').waitFor({ state: 'visible' });
    const cards = page.locator('.classic-game');
    const status = page.locator('#game-count');
    assert.equal(await cards.count(), Math.min(24, games.length));
    assert.match(await status.textContent(), new RegExp(`· ${games.length}개 게임$`));
    const genres = [...new Set(games.map((g) => g.genre))];
    // Exhaustive combinations run locally. On Pages, sample both platform ends
    // and contrasting genres so UI verification does not flood its CDN.
    const platforms = live ? [...new Set(['', Object.keys(data.platforms)[0], Object.keys(data.platforms).at(-1)])] : ['', ...Object.keys(data.platforms)];
    const checkedGenres = live ? ['', ...[...new Set([genres[0], 'RPG', '퍼즐/보드'])].filter((g) => genres.includes(g))] : ['', ...genres];
    for (const platform of platforms) {
      await page.locator(`button[data-platform="${platform}"]`).click();
      assert.equal(await page.locator(`button[data-platform="${platform}"]`).getAttribute('aria-pressed'), 'true');
      for (const genre of checkedGenres) {
        if (live) await page.waitForTimeout(300);
        await page.locator('#game-genre').selectOption(genre);
        const expected = games.filter((g) => (!platform || g.platform === platform) && (!genre || g.genre === genre));
        assert.match(await status.textContent(), new RegExp(`· ${expected.length}개 게임$`));
        assert.deepEqual(await cards.evaluateAll((els) => els.map((el) => el.id)), expected.slice(0, 24).map((g) => g.id));
        assert.equal(await page.locator('#game-empty').isVisible(), expected.length === 0);
      }
    }
    await page.locator('.game-reset').click();
    await page.locator('#game-load-trigger').scrollIntoViewIfNeeded();
    await page.waitForFunction(() => document.querySelectorAll('.classic-game').length >= 48);
    const loaded = await cards.count();
    assert.deepEqual(await cards.evaluateAll((els) => els.map((el) => el.id)), games.slice(0, loaded).map((g) => g.id));
    // Filter a small group and reach its final entry to check the end-of-list state.
    const groups = [...new Set(games.map((g) => `${g.platform}|${g.genre}`))]
      .map((key) => { const [platform, genre] = key.split('|'); return { platform, genre, games: games.filter((g) => g.platform === platform && g.genre === genre) }; });
    const small = groups.find((g) => g.games.length > 24 && g.games.length <= 120) || groups.find((g) => g.games.length <= 24);
    await page.locator(`button[data-platform="${small.platform}"]`).click();
    await page.locator('#game-genre').selectOption(small.genre);
    while (await cards.count() < small.games.length) {
      const before = await cards.count();
      await page.locator('#game-load-trigger').scrollIntoViewIfNeeded();
      await page.waitForFunction((n) => document.querySelectorAll('.classic-game').length > n, before);
    }
    assert.deepEqual(await cards.evaluateAll((els) => els.map((el) => el.id)), small.games.map((g) => g.id));
    assert.ok(await page.locator('#game-load-trigger').isHidden());
    await page.locator('.game-reset').click();
    assert.equal(await cards.count(), 24);
    await page.locator('#game-search').fill('zzzz없는게임');
    assert.equal(await cards.count(), 0);
    assert.ok(await page.locator('#game-empty').isVisible());
    await page.locator('.game-reset').click();
    await page.locator('#game-search').focus();
    await page.keyboard.type('tetris');
    assert.ok(await cards.count() > 0);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('.game-reset').evaluate((el) => el === document.activeElement), true);
    await page.keyboard.press('Enter');
    assert.equal(await cards.count(), 24);
    const last = games.at(-1);
    await page.locator('#game-search').fill(last.title);
    assert.ok(await page.locator(`#${last.id}`).count(), 'last game searchable');
    const query = `?platform=${last.platform}&genre=${encodeURIComponent(last.genre)}&q=${encodeURIComponent(last.title)}`;
    await page.goto(url + query);
    await page.locator('.classic-filter').waitFor({ state: 'visible' });
    assert.equal(await page.locator('#game-search').inputValue(), last.title);
    assert.ok(await page.locator(`#${last.id}`).count());
    await page.goto(url + '?platform=invalid&genre=invalid');
    await page.locator('.classic-filter').waitFor({ state: 'visible' });
    assert.equal(await cards.count(), 24);
    const links = await page.locator('.game-source a').evaluateAll((els) => els.map((a) => [a.href, a.target, a.rel]));
    assert.ok(links.every(([href, target, rel]) => href.startsWith('https://') && target === '_blank' && rel.includes('noopener')));
    for (const width of [1280, 375, 320]) {
      await page.setViewportSize({ width, height: 1000 });
      for (const theme of ['light', 'dark']) {
        if (await page.locator('html').getAttribute('data-theme') !== theme) await page.locator('#theme-toggle').click();
        assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${site} ${width} ${theme} overflow`);
        await page.screenshot({ path: `/tmp/${site}-${tag}-${width}-${theme}.png` });
      }
    }
    // Ensure the visitor sees loaded image pixels, including after a filter changes.
    await page.setViewportSize({ width: 1280, height: 1000 });
    await cards.first().scrollIntoViewIfNeeded();
    await page.waitForFunction(() => [...document.querySelectorAll('.classic-game img')].slice(0, 2).every((i) => i.complete && i.naturalWidth > 0));
    assert.equal(await page.locator('.game-image-missing').count(), games.slice(0, await cards.count()).filter((g) => !g.image).length);
    await page.screenshot({ path: `/tmp/${site}-${tag}-cards.png` });
    const nojs = await browser.newContext({ javaScriptEnabled: false });
    const fallback = await nojs.newPage();
    await fallback.goto(url);
    assert.deepEqual(await fallback.locator('.classic-game').evaluateAll((els) => els.map((el) => el.id)), games.map((g) => g.id));
    await nojs.close();
    const noObserver = await browser.newContext();
    await noObserver.addInitScript(() => { delete window.IntersectionObserver; });
    const unsupported = await noObserver.newPage();
    await unsupported.goto(url);
    await unsupported.locator('.classic-filter').waitFor({ state: 'visible' });
    assert.equal(await unsupported.locator('.classic-game').count(), games.length);
    await noObserver.close();
    // Verify the deployed metadata is exactly the checked-in inventory.
    const remote = await context.request.get(`${base}/data/${site}-games.json`);
    assert.equal(remote.status(), 200);
    assert.deepEqual(await remote.json(), data);
    results.push({ site, games: games.length, combinations: platforms.length * checkedGenres.length, exhaustive: !live, widths: [1280, 375, 320], themes: ['light', 'dark'], scroll: true, keyboard: true, images: true, noJavaScript: true, noIntersectionObserver: true });
    console.log(JSON.stringify(results.at(-1)));
    if (live) await page.waitForTimeout(2000);
  }
  await page.goto(base);
  for (const site of sites) assert.ok(await page.locator(`.post-list a[href="/posts/${site}/"]`).isVisible());
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ base, results, consoleErrors: errors }, null, 2));
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
