// NODE_PATH must provide playwright. Pass a local or deployed URL.
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const assert = require('node:assert/strict');
const path = require('node:path');
(async () => {
  const base = process.argv[2] || 'http://127.0.0.1:8080';
  const root = path.resolve(__dirname, '..');
  const data = JSON.parse(await fs.readFile(path.join(root, 'public/data/tooli-games.json'), 'utf8'));
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
  await page.goto(`${base}/posts/classic-games/`, { waitUntil: 'networkidle' });
  const visible = () => page.locator('.classic-game:visible');
  const status = () => page.locator('#game-count').textContent();
  assert.equal(await page.locator('.classic-game').count(), data.games.length);
  assert.equal(await visible().count(), 24);
  assert.match(await status(), new RegExp(`${data.games.length}개 게임`));
  const genres = [...new Set(data.games.map((game) => game.genre))];
  for (const platform of ['', ...Object.keys(data.platforms)]) {
    await page.locator(`[data-platform="${platform}"][type="button"]`).click();
    for (const genre of ['', ...genres]) {
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
  await page.locator('#game-next').click();
  assert.equal(await visible().count(), 24);
  assert.match(await page.locator('#game-page-status').textContent(), /^2 \/ /);
  assert.equal(await visible().first().getAttribute('id'), data.games[24].id);
  await page.locator('#game-previous').click();
  assert.deepEqual(await visible().evaluateAll((cards) => cards.map((card) => card.id)), firstIds);
  for (const query of ['마리오', 'Sonic', '역전재판', '스테판 울프']) {
    await page.locator('#game-search').fill(query);
    assert.ok(await visible().count() > 0, query);
  }
  await page.locator('#game-search').fill('없는게임zzzzz');
  assert.equal(await visible().count(), 0);
  assert.ok(await page.locator('#game-empty').isVisible());
  await page.locator('.game-reset').click();
  assert.match(await status(), new RegExp(`${data.games.length}개 게임`));
  await page.goto(`${base}/posts/classic-games/?platform=md&genre=${encodeURIComponent('액션/아케이드')}&q=Sonic&page=999`);
  assert.equal(await page.locator('#game-search').inputValue(), 'Sonic');
  assert.ok(await visible().count() > 0);
  await page.goto(`${base}/posts/classic-games/?platform=invalid&genre=invalid&page=-1`);
  assert.equal(await visible().count(), 24);
  // Browser keyboard input through the same controls a visitor uses.
  await page.locator('#game-search').focus();
  await page.keyboard.type('tetris');
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
    for (const theme of ['light', 'dark']) {
      if (await page.locator('html').getAttribute('data-theme') !== theme) await page.locator('#theme-toggle').click();
      assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow ${width} ${theme}`);
      await page.screenshot({ path: `/tmp/classic-games-${base.includes('127.0.0.1') ? 'local' : 'live'}-${width}-${theme}.png`, fullPage: false });
    }
  }
  const broken = await page.locator('.classic-game:visible img').evaluateAll((imgs) => imgs.filter((img) => img.complete && img.naturalWidth === 0).map((img) => img.src));
  assert.deepEqual(broken, []);
  assert.deepEqual(errors, []);
  const nojs = await browser.newContext({ javaScriptEnabled: false });
  const fallback = await nojs.newPage();
  await fallback.goto(`${base}/posts/classic-games/`);
  assert.equal(await fallback.locator('.classic-game:visible').count(), data.games.length);
  await nojs.close();
  await page.goto(base);
  assert.ok(await page.getByRole('link', { name: '고전게임 도감', exact: true }).isVisible());
  console.log(JSON.stringify({ url: base, games: data.games.length, combinations: 8 * (genres.length + 1), widths: [1280, 375, 320], themes: ['light', 'dark'], pagination: true, search: true, keyboard: true, noJavaScript: true, consoleErrors: errors }, null, 2));
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
