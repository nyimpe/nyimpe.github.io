const filter = document.querySelector('.classic-filter');
const cards = [...document.querySelectorAll('.classic-game')];
const platformButtons = [...filter.querySelectorAll('[data-platform]')];
const genre = document.getElementById('game-genre');
const search = document.getElementById('game-search');
const status = document.getElementById('game-count');
const empty = document.getElementById('game-empty');
const pagination = document.getElementById('game-pagination');
const previous = document.getElementById('game-previous');
const next = document.getElementById('game-next');
const pageStatus = document.getElementById('game-page-status');
const pageSize = 24;
const entries = cards.map((element) => ({
  element,
  platform: element.dataset.platform,
  genre: element.dataset.genre,
  search: element.textContent.normalize('NFKC').toLocaleLowerCase('ko').replace(/\s+/g, ' '),
}));
let platform = '';
let page = 1;
let matches = [];

function applyFilter({ sync = true, scroll = false } = {}) {
  const terms = search.value.normalize('NFKC').toLocaleLowerCase('ko').trim().split(/\s+/).filter(Boolean);
  matches = entries.filter((entry) => (!platform || entry.platform === platform)
    && (!genre.value || entry.genre === genre.value)
    && terms.every((term) => entry.search.includes(term)));
  const pages = Math.max(1, Math.ceil(matches.length / pageSize));
  page = Math.min(Math.max(1, page), pages);
  const visible = new Set(matches.slice((page - 1) * pageSize, page * pageSize));
  for (const entry of entries) entry.element.hidden = !visible.has(entry);
  for (const button of platformButtons) button.setAttribute('aria-pressed', String(button.dataset.platform === platform));
  const label = platformButtons.find((button) => button.dataset.platform === platform).dataset.label;
  status.textContent = `${label} · ${genre.value || '전체 장르'} · ${matches.length}개 게임`;
  empty.hidden = matches.length !== 0;
  pagination.hidden = matches.length <= pageSize;
  previous.disabled = page === 1;
  next.disabled = page === pages;
  pageStatus.textContent = `${page} / ${pages} 페이지 · ${(page - 1) * pageSize + 1}–${Math.min(page * pageSize, matches.length)}번째`;
  if (sync) {
    const params = new URLSearchParams();
    if (platform) params.set('platform', platform);
    if (genre.value) params.set('genre', genre.value);
    if (search.value.trim()) params.set('q', search.value.trim());
    if (page > 1) params.set('page', page);
    const query = params.toString();
    history.replaceState(null, '', `${location.pathname}${query ? `?${query}` : ''}${location.hash}`);
  }
  if (scroll) status.scrollIntoView({ block: 'start' });
}

function readLocation() {
  const params = new URLSearchParams(location.search);
  platform = platformButtons.some((button) => button.dataset.platform === params.get('platform')) ? params.get('platform') : '';
  genre.value = [...genre.options].some((option) => option.value === params.get('genre')) ? params.get('genre') : '';
  search.value = params.get('q') ?? '';
  page = Math.max(1, Number.parseInt(params.get('page'), 10) || 1);
  applyFilter({ sync: false });
}

for (const button of platformButtons) button.addEventListener('click', () => {
  platform = button.dataset.platform;
  page = 1;
  applyFilter();
});
genre.addEventListener('change', () => { page = 1; applyFilter(); });
search.addEventListener('input', () => { page = 1; applyFilter(); });
filter.addEventListener('reset', (event) => {
  event.preventDefault();
  platform = '';
  genre.value = '';
  search.value = '';
  page = 1;
  applyFilter();
});
filter.addEventListener('submit', (event) => event.preventDefault());
previous.addEventListener('click', () => { page -= 1; applyFilter({ scroll: true }); });
next.addEventListener('click', () => { page += 1; applyFilter({ scroll: true }); });
window.addEventListener('popstate', readLocation);
readLocation();
filter.hidden = false;
// Keep a readable fallback if a saved image is ever unavailable.
for (const img of document.querySelectorAll('.game-screenshot img')) {
  img.addEventListener('error', () => {
    const fallback = document.createElement('span');
    fallback.className = 'game-image-missing';
    fallback.textContent = '이미지를 표시할 수 없습니다. 원문을 확인해 주세요.';
    img.parentElement.replaceWith(fallback);
  }, { once: true });
}
