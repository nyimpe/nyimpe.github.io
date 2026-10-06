// NODE_PATH must provide playwright. Pass a local or deployed URL.
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const assert = require('node:assert/strict');
const path = require('node:path');
(async () => {
  const base = process.argv[2] || 'http://127.0.0.1:8080';
  const jjang = process.argv[3] === 'jjang';
  const live = base.startsWith('https://');
  const slug = jjang ? 'jjang-games' : 'classic-games';
  const dataset = jjang ? 'jjang-games' : 'tooli-games';
  const postTitle = jjang ? '짱게임 2D·오락실 게임 도감' : 'tooli의 고전게임 정리';
  const root = path.resolve(__dirname, '..');
  const data = JSON.parse(await fs.readFile(path.join(root, `public/data/${dataset}.json`), 'utf8'));
  const secondPlatform = jjang ? 'old' : 'lounge';
  const finalPlatform = jjang ? 'old' : 'md';
  const finalGenre = jjang ? '퀴즈' : '';
  const finalGames = data.games.filter((game) => game.platform === finalPlatform && (!finalGenre || game.genre === finalGenre));
  assert.ok(finalGames.length > 24 && finalGames.length <= 48, 'Last batch fixture');
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') errors.push(`${message.text()} ${message.location().url}`.trim()); });
  await page.goto(`${base}/posts/${slug}/`, { waitUntil: 'networkidle' });
  const visible = () => page.locator('.classic-game:visible');
  const status = () => page.locator('#game-count').textContent();
  assert.equal(await page.locator('.classic-game').count(), 24);
  assert.equal(await page.locator('#game-pagination, #game-previous, #game-next').count(), 0);
  assert.ok(await page.locator('.classic-game img').evaluateAll((imgs) => imgs.every((img) => img.loading === 'lazy')));
  assert.equal(await visible().count(), 24);
  assert.match(await status(), new RegExp(`${data.games.length}개 게임`));
  const genres = [...new Set(data.games.map((game) => game.genre))];
  for (const platform of ['', ...Object.keys(data.platforms)]) {
    await page.locator(`[data-platform="${platform}"][type="button"]`).click();
    for (const genre of ['', ...genres]) {
      if (live) await page.waitForTimeout(150);
      await page.locator('#game-genre').selectOption(genre);
      const expected = data.games.filter((game) => (!platform || game.platform === platform) && (!genre || game.genre === genre)).length;
      assert.match(await status(), new RegExp(`· ${expected}개 게임$`));
      assert.equal(await visible().count(), Math.min(24, expected));
      assert.equal(await page.locator('#game-empty').isVisible(), expected === 0);
      if (expected) assert.ok((await visible().evaluateAll((cards) => cards.map((card) => [card.dataset.platform, card.dataset.genre]))).every(([p, g]) => (!platform || p === platform) && (!genre || g === genre)));
    }
  }
  await page.locator('.game-reset').click();
  const firstIds = await visible().evaluateAll((cards) => cards.map((card) => card.id));
  await page.locator('#game-load-trigger').scrollIntoViewIfNeeded();
  await page.waitForFunction(() => document.querySelectorAll('.classic-game').length >= 48);
  const loadedIds = await visible().evaluateAll((cards) => cards.map((card) => card.id));
  assert.deepEqual(loadedIds.slice(0, 24), firstIds);
  assert.deepEqual(loadedIds, data.games.slice(0, loadedIds.length).map((game) => game.id));
  // Keep scrolling through the complete catalog: no duplicate or missing games.
  while (await visible().count() < data.games.length) {
    // Avoid turning a catalog UI check into a burst of thousands of CDN requests.
    if (live) await page.waitForTimeout(1300);
    const count = await visible().count();
    await page.locator('#game-load-trigger').scrollIntoViewIfNeeded();
    await page.waitForFunction((count) => document.querySelectorAll('.classic-game').length > count, count);
  }
  assert.deepEqual(await visible().evaluateAll((cards) => cards.map((card) => card.id)), data.games.map((game) => game.id));
  assert.ok(await page.locator('#game-load-trigger').isHidden());
  // Filtering after loading another batch removes stale games and resets the list.
  await page.locator(`[data-platform="${secondPlatform}"][type="button"]`).click();
  assert.equal(await visible().count(), 24);
  assert.ok((await visible().evaluateAll((cards) => cards.map((card) => card.dataset.platform))).every((platform) => platform === secondPlatform));
  await page.locator(`[data-platform="${finalPlatform}"][type="button"]`).click();
  await page.locator('#game-genre').selectOption(finalGenre);
  await page.locator('#game-load-trigger').scrollIntoViewIfNeeded();
  await page.waitForFunction((count) => document.querySelectorAll('.classic-game').length === count, finalGames.length);
  assert.ok(await page.locator('#game-load-trigger').isHidden());
  assert.match(await page.locator('#game-load-status').textContent(), new RegExp(`${finalGames.length}개 게임을 모두`));
  const finalIds = await visible().evaluateAll((cards) => cards.map((card) => card.id));
  assert.deepEqual(finalIds, finalGames.map((game) => game.id));
  await page.locator('.game-reset').click();
  assert.equal(await visible().count(), 24);
  for (const query of jjang ? ['마리오', 'Sonic', '철권', '1945', '라이덴'] : ['마리오', 'Sonic', '역전재판', '스테판 울프']) {
    await page.locator('#game-search').fill(query);
    assert.ok(await visible().count() > 0, query);
  }
  await page.locator('#game-search').fill('없는게임zzzzz');
  assert.equal(await visible().count(), 0);
  assert.ok(await page.locator('#game-empty').isVisible());
  await page.locator('.game-reset').click();
  assert.match(await status(), new RegExp(`${data.games.length}개 게임`));
  const savedQuery = jjang ? '철권' : 'Sonic';
  await page.goto(`${base}/posts/${slug}/?platform=${finalPlatform}&genre=${encodeURIComponent(jjang ? '격투' : '액션/아케이드')}&q=${encodeURIComponent(savedQuery)}&page=999`);
  assert.equal(await page.locator('#game-search').inputValue(), savedQuery);
  assert.ok(!(new URL(page.url())).searchParams.has('page'));
  assert.ok(await visible().count() > 0);
  await page.goto(`${base}/posts/${slug}/?platform=invalid&genre=invalid&page=-1`);
  assert.equal(await visible().count(), 24);
  // Browser keyboard input through the same controls a visitor uses.
  await page.locator('#game-search').focus();
  await page.keyboard.type(jjang ? '1945' : 'tetris');
  assert.ok(await visible().count() > 0);
  await page.keyboard.press('Tab');
  assert.equal(await page.locator('.game-reset').evaluate((el) => el === document.activeElement), true);
  await page.keyboard.press('Enter');
  assert.equal(await visible().count(), 24);
  const external = page.locator('.game-source a').first();
  assert.equal(await external.getAttribute('target'), '_blank');
  assert.match(await external.getAttribute('rel'), /noopener/);
  for (const width of [1280, 375, 320]) {
    await page.setViewportSize({ width, height: 900 });
    await page.locator(`[data-platform="${finalPlatform}"][type="button"]`).click();
    await page.locator('#game-genre').selectOption(finalGenre);
    await page.locator('#game-load-trigger').scrollIntoViewIfNeeded();
    await page.waitForFunction((count) => document.querySelectorAll('.classic-game').length === count, finalGames.length);
    await page.locator('.game-reset').click();
    for (const theme of ['light', 'dark']) {
      if (await page.locator('html').getAttribute('data-theme') !== theme) await page.locator('#theme-toggle').click();
      assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow ${width} ${theme}`);
      await page.screenshot({ path: `/tmp/${slug}-${base.includes('127.0.0.1') ? 'local' : 'live'}-${width}-${theme}.png`, fullPage: false });
    }
  }
  const broken = await page.locator('.classic-game:visible img').evaluateAll((imgs) => imgs.filter((img) => img.complete && img.naturalWidth === 0).map((img) => img.src));
  assert.deepEqual(broken, []);
  assert.deepEqual(errors, []);
  const nojs = await browser.newContext({ javaScriptEnabled: false });
  const fallback = await nojs.newPage();
  await fallback.goto(`${base}/posts/${slug}/`);
  assert.equal(await fallback.locator('.classic-game:visible').count(), data.games.length);
  await nojs.close();
  const noObserver = await browser.newContext();
  await noObserver.addInitScript(() => { delete window.IntersectionObserver; });
  const unsupported = await noObserver.newPage();
  await unsupported.goto(`${base}/posts/${slug}/`);
  await unsupported.waitForFunction(() => !document.querySelector('.classic-filter').hidden);
  assert.equal(await unsupported.locator('.classic-game').count(), data.games.length);
  await unsupported.locator(`[data-platform="${finalPlatform}"][type="button"]`).click();
  await unsupported.locator('#game-genre').selectOption(finalGenre);
  assert.equal(await unsupported.locator('.classic-game').count(), finalGames.length);
  await noObserver.close();
  await page.goto(base);
  assert.ok(await page.getByRole('link', { name: postTitle, exact: true }).isVisible());
  console.log(JSON.stringify({ url: base, post: slug, games: data.games.length, combinations: (Object.keys(data.platforms).length + 1) * (genres.length + 1), widths: [1280, 375, 320], themes: ['light', 'dark'], infiniteScroll: true, filterResetsLoadedGames: true, noIntersectionObserver: true, search: true, keyboard: true, noJavaScript: true, consoleErrors: errors }, null, 2));
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
