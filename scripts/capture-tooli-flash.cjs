#!/usr/bin/env node
// Tooling only: npm install playwright sharp @ruffle-rs/ruffle in a temporary directory.
// Use NODE_PATH=<temporary>/node_modules. No Flash runtime ships to the website.
const { chromium } = require('playwright');
const sharp = require('sharp');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const cache = '/tmp/nyimpe-tooli-cache';
const root = path.resolve(__dirname, '..');
const ruffleDir = path.dirname(require.resolve('@ruffle-rs/ruffle'));

(async () => {
  const rows = JSON.parse(await fs.readFile(`${cache}/raw.json`, 'utf8'))
    .filter((row) => row.platform === 'flash' && !row.notice && row.embeds.some((url) => /\.swf(?:$|\?)/i.test(url)));
  const output = {};
  const failures = [];
  const movies = new Map();
  const refresh = new Set(process.argv.slice(2));
  const wrapper = `<!doctype html><html><head><style>html,body{margin:0;background:#101215}ruffle-player{display:block;width:700px;height:500px}</style></head><body><div id="game"></div><script>window.RufflePlayer={config:{autoplay:'on',frameRate:120,unmuteOverlay:'hidden',allowScriptAccess:false,showSwfDownload:false,contextMenu:'off',logLevel:'error'}};</script><script src="/ruffle/ruffle.js"></script><script>window.addEventListener('DOMContentLoaded',async()=>{try{let p=window.RufflePlayer.newest().createPlayer();document.getElementById('game').appendChild(p);await p.ruffle().load({url:new URLSearchParams(location.search).get('swf'),allowScriptAccess:false});window.loaded=true;}catch(e){window.loadError=String(e)}})</script></body></html>`;
  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://localhost');
      if (url.pathname === '/') { res.setHeader('Content-Type', 'text/html'); return res.end(wrapper); }
      if (movies.has(url.pathname)) { res.setHeader('Content-Type', 'application/x-shockwave-flash'); return res.end(movies.get(url.pathname)); }
      if (url.pathname.startsWith('/ruffle/')) {
        const filename = path.basename(url.pathname);
        res.setHeader('Content-Type', filename.endsWith('.wasm') ? 'application/wasm' : 'text/javascript');
        return res.end(await fs.readFile(path.join(ruffleDir, filename)));
      }
      res.statusCode = 404; res.end();
    } catch { res.statusCode = 500; res.end(); }
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const context = await browser.newContext({ viewport: { width: 700, height: 500 } });
  await context.route('**/*', (route) => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
  const imageDir = path.join(root, 'public/images/classic-games');
  await fs.mkdir(imageDir, { recursive: true });
  const saved = JSON.parse(await fs.readFile(`${cache}/flash-images.json`, 'utf8').catch(() => '{}'));
  let index = 0;
  async function worker() {
    while (index < rows.length) {
      const row = rows[index++];
      const filename = path.join(imageDir, `${row.id}.webp`);
      if (saved[row.id] && !refresh.has(row.id) && await fs.stat(filename).catch(() => false)) { output[row.id] = saved[row.id]; continue; }
      const sourceUrl = row.embeds.find((url) => /\.swf(?:$|\?)/i.test(url));
      const url = sourceUrl.replace(/^http:/, 'https:');
      let page;
      try {
        if (!['file.tooli.co.kr', 'www.tooli.co.kr', 'cache.armorgames.com', 'games.armorgames.com', 'www.miniclip.com', 'www.fasco-cs.com'].includes(new URL(url).hostname)) throw new Error('External SWF skipped');
        const movieFile = `${cache}/${row.id}.swf`;
        let bytes = await fs.readFile(movieFile).catch(() => null);
        if (!bytes) {
          const response = await fetch(url, { headers: { Referer: row.source }, signal: AbortSignal.timeout(30000) });
          if (!response.ok) throw new Error(`SWF HTTP ${response.status}`);
          bytes = Buffer.from(await response.arrayBuffer());
          if (!['FWS', 'CWS', 'ZWS'].includes(bytes.subarray(0, 3).toString())) throw new Error('Not a Flash movie');
          await fs.writeFile(movieFile, bytes);
        }
        const moviePath = `/movies/${row.id}.swf`;
        movies.set(moviePath, bytes);
        page = await context.newPage();
        await page.goto(`${origin}/?swf=${encodeURIComponent(moviePath)}`);
        await page.waitForFunction(() => window.loaded || window.loadError, { timeout: 30000 });
        const error = await page.evaluate(() => window.loadError);
        if (error) throw new Error(error);
        await page.waitForTimeout(6000);
        let screenshot = await page.screenshot();
        let stats = await sharp(screenshot).stats();
        if (stats.entropy < .15) {
          await page.waitForTimeout(7000);
          screenshot = await page.screenshot();
          stats = await sharp(screenshot).stats();
        }
        if (stats.entropy < .15) throw new Error('Blank movie frame');
        if (await page.getByText(/Ruffle has encountered|Something went wrong/i).count()) throw new Error('Ruffle render error');
        const savedImage = await sharp(screenshot).resize({ width: 320, height: 240, fit: 'inside', withoutEnlargement: true }).webp({ quality: 55, effort: 6 }).toFile(filename);
        output[row.id] = { src: `/images/classic-games/${row.id}.webp`, width: savedImage.width, height: savedImage.height, source: sourceUrl, kind: 'flash-capture' };
        movies.delete(moviePath);
      } catch (error) {
        console.log(`${row.id}: ${error.message}`);
        failures.push({ id: row.id, title: row.title, source: row.source, movie: url, reason: error.message });
      } finally { if (page) await page.close(); }
      if ((Object.keys(output).length + failures.length) % 10 === 0) {
        console.log(`Flash: ${Object.keys(output).length} captured, ${failures.length} failed / ${rows.length}`);
        await fs.writeFile(`${cache}/flash-images.json`, JSON.stringify(output, null, 2));
      }
    }
  }
  await Promise.all([worker(), worker()]);
  await fs.writeFile(`${cache}/flash-images.json`, JSON.stringify(output, null, 2));
  await fs.writeFile(`${cache}/flash-failures.json`, JSON.stringify(failures, null, 2));
  console.log(`Flash complete: ${Object.keys(output).length} captured, ${failures.length} failed.`);
  await browser.close();
  server.close();
})().catch((error) => { console.error(error); process.exitCode = 1; });
