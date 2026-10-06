const filter = document.querySelector('.classic-filter');
const cards = [...document.querySelectorAll('.classic-game')];
const list = document.querySelector('.classic-games');
const platformButtons = [...filter.querySelectorAll('[data-platform]')];
const genre = document.getElementById('game-genre');
const search = document.getElementById('game-search');
const status = document.getElementById('game-count');
const empty = document.getElementById('game-empty');
const loadStatus = document.getElementById('game-load-status');
const loadTrigger = document.getElementById('game-load-trigger');
const batchSize = 24;
const entries = cards.map((element) => ({
  element,
  platform: element.dataset.platform,
  genre: element.dataset.genre,
  search: element.textContent.normalize('NFKC').toLocaleLowerCase('ko').replace(/\s+/g, ' '),
}));
let platform = '';
let renderedCount = 0;
let matches = [];

function loadMore() {
  observer?.disconnect();
  const end = observer ? Math.min(renderedCount + batchSize, matches.length) : matches.length;
  list.append(...matches.slice(renderedCount, end).map((entry) => entry.element));
  renderedCount = end;
  loadTrigger.hidden = renderedCount === matches.length;
  loadStatus.hidden = matches.length === 0;
  if (!loadTrigger.hidden) observer?.observe(loadTrigger);
  loadStatus.textContent = renderedCount === matches.length
    ? `${renderedCount}개 게임을 모두 표시했습니다.`
    : `${renderedCount} / ${matches.length}개 게임 표시 · 아래로 스크롤하면 계속 표시됩니다.`;
}

const observer = 'IntersectionObserver' in window
  ? new IntersectionObserver((observations) => {
    if (observations.some((entry) => entry.isIntersecting) && renderedCount < matches.length) loadMore();
  }, { rootMargin: '600px 0px' })
  : null;

function applyFilter({ sync = true } = {}) {
  const terms = search.value.normalize('NFKC').toLocaleLowerCase('ko').trim().split(/\s+/).filter(Boolean);
  matches = entries.filter((entry) => (!platform || entry.platform === platform)
    && (!genre.value || entry.genre === genre.value)
    && terms.every((term) => entry.search.includes(term)));
  observer?.disconnect();
  list.replaceChildren();
  renderedCount = 0;
  // Browsers without IntersectionObserver retain the full, readable list.
  loadMore();
  for (const button of platformButtons) button.setAttribute('aria-pressed', String(button.dataset.platform === platform));
  const label = platformButtons.find((button) => button.dataset.platform === platform).dataset.label;
  status.textContent = `${label} · ${genre.value || '전체 장르'} · ${matches.length}개 게임`;
  empty.hidden = matches.length !== 0;
  if (sync) {
    const params = new URLSearchParams();
    if (platform) params.set('platform', platform);
    if (genre.value) params.set('genre', genre.value);
    if (search.value.trim()) params.set('q', search.value.trim());
    const query = params.toString();
    history.replaceState(null, '', `${location.pathname}${query ? `?${query}` : ''}${location.hash}`);
  }
}

function readLocation() {
  const params = new URLSearchParams(location.search);
  platform = platformButtons.some((button) => button.dataset.platform === params.get('platform')) ? params.get('platform') : '';
  genre.value = [...genre.options].some((option) => option.value === params.get('genre')) ? params.get('genre') : '';
  search.value = params.get('q') ?? '';
  // Old page links still open the matching list, without a paging parameter.
  applyFilter();
}

for (const button of platformButtons) button.addEventListener('click', () => {
  platform = button.dataset.platform;
  applyFilter();
});
genre.addEventListener('change', () => applyFilter());
search.addEventListener('input', () => applyFilter());
filter.addEventListener('reset', (event) => {
  event.preventDefault();
  platform = '';
  genre.value = '';
  search.value = '';
  applyFilter();
});
filter.addEventListener('submit', (event) => event.preventDefault());
window.addEventListener('popstate', readLocation);
// Bind before detaching cards so later batches retain image error handling.
for (const card of cards) {
  for (const img of card.querySelectorAll('.game-screenshot img')) {
    img.addEventListener('error', () => {
      const fallback = document.createElement('span');
      fallback.className = 'game-image-missing';
      fallback.textContent = '이미지를 표시할 수 없습니다. 원문을 확인해 주세요.';
      img.parentElement.replaceWith(fallback);
    }, { once: true });
  }
}
readLocation();
filter.hidden = false;
