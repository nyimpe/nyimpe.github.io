// Compare the deployed HTML, metadata, hashed bundles and every screenshot to this build.
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const base = process.argv[2] || 'https://nyimpe.github.io';
const hash = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
(async () => {
  const metadata = JSON.parse(await fs.readFile(path.join(root, 'public/data/tooli-games.json'), 'utf8'));
  const html = await fs.readFile(path.join(root, 'dist/posts/classic-games/index.html'), 'utf8');
  const urls = [...new Set(['/posts/classic-games/index.html', '/data/tooli-games.json',
    ...[...html.matchAll(/(?:src|href)="(\/assets\/[^"\s]+)"/g)].map((m) => m[1]),
    ...metadata.games.filter((game) => game.image).map((game) => game.image.src)])];
  let next = 0;
  let verified = 0;
  async function worker() {
    while (next < urls.length) {
      const url = urls[next++];
      const response = await fetch(base + url, { signal: AbortSignal.timeout(30000), cache: 'no-store' });
      assert.equal(response.status, 200, url);
      const remote = Buffer.from(await response.arrayBuffer());
      const local = await fs.readFile(path.join(root, 'dist', url));
      assert.equal(hash(remote), hash(local), `deployed content mismatch: ${url}`);
      verified += 1;
      if (verified % 200 === 0) console.log(`Verified ${verified}/${urls.length} deployed files`);
    }
  }
  await Promise.all(Array.from({ length: 8 }, worker));
  console.log(JSON.stringify({ base, verifiedFiles: verified, screenshots: metadata.games.filter((game) => game.image).length, htmlAndHashedAssets: true, allContentHashesMatch: true }, null, 2));
})().catch((error) => { console.error(error); process.exit(1); });
