// Compare the deployed HTML, metadata, hashed bundles and every screenshot to this build.
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const base = process.argv[2] || 'https://nyimpe.github.io';
const jjang = process.argv[3] === 'jjang';
const slug = jjang ? 'jjang-games' : 'classic-games';
const dataset = jjang ? 'jjang-games' : 'tooli-games';
const hash = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
(async () => {
  const metadata = JSON.parse(await fs.readFile(path.join(root, `public/data/${dataset}.json`), 'utf8'));
  const html = await fs.readFile(path.join(root, `dist/posts/${slug}/index.html`), 'utf8');
  const urls = [...new Set([`/posts/${slug}/index.html`, `/data/${dataset}.json`,
    ...[...html.matchAll(/(?:src|href)="(\/assets\/[^"\s]+)"/g)].map((m) => m[1]),
    ...metadata.games.filter((game) => game.image).map((game) => game.image.src)])];
  let next = 0;
  let verified = 0;
  let resumeAt = 0;
  async function readRemote(url) {
    for (let attempt = 0; attempt < 5; attempt += 1) {
      if (resumeAt > Date.now()) await sleep(resumeAt - Date.now());
      const response = await fetch(base + url, { signal: AbortSignal.timeout(30000), cache: 'no-store' });
      if ([429, 502, 503, 504].includes(response.status)) {
        await response.arrayBuffer();
        const backoff = response.status === 429 ? 30000 * 2 ** attempt : 1000 * (attempt + 1);
        const retryAfter = response.headers.get('retry-after') || '0';
        const retryMs = /^\d+$/.test(retryAfter) ? Number(retryAfter) * 1000 : Math.max(0, Date.parse(retryAfter) - Date.now());
        resumeAt = Math.max(resumeAt, Date.now() + Math.max(backoff, retryMs || 0));
        console.log(`HTTP ${response.status}; waiting before retry ${attempt + 1}/5`);
        continue;
      }
      assert.equal(response.status, 200, url);
      return Buffer.from(await response.arrayBuffer());
    }
    throw new Error(`Server still unavailable after retries: ${url}`);
  }
  async function worker() {
    while (next < urls.length) {
      const url = urls[next++];
      const remote = await readRemote(url);
      const local = await fs.readFile(path.join(root, 'dist', new URL(url, base).pathname));
      assert.equal(hash(remote), hash(local), `deployed content mismatch: ${url}`);
      verified += 1;
      if (verified % 200 === 0) console.log(`Verified ${verified}/${urls.length} deployed files`);
      await sleep(250);
    }
  }
  await Promise.all(Array.from({ length: 2 }, worker));
  console.log(JSON.stringify({ base, verifiedFiles: verified, screenshots: metadata.games.filter((game) => game.image).length, htmlAndHashedAssets: true, allContentHashesMatch: true }, null, 2));
})().catch((error) => { console.error(error); process.exit(1); });
