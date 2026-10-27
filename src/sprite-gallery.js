const gallery = document.querySelector(".sprite-gallery");
const motionButton = document.querySelector("#sprite-motion");
const status = document.querySelector("#sprite-count");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
let paused = reducedMotion.matches;

function updateImage(card) {
  const image = card.querySelector(".sprite-preview");
  const choice = card.querySelector("select")?.selectedOptions[0];
  if (choice) {
    image.dataset.gif = choice.dataset.gif;
    image.dataset.still = choice.dataset.still;
    image.alt = `${choice.textContent} · ${card.dataset.directions}방향 ${card.dataset.motion} 미리보기`;
    const link = card.querySelector(".gif-download");
    link.href = choice.dataset.gif;
  }
  image.src = paused ? image.dataset.still : image.dataset.gif;
}

function updateMotion() {
  for (const card of gallery.children) updateImage(card);
  motionButton.textContent = paused ? "GIF 모두 재생" : "GIF 모두 정지";
  motionButton.setAttribute("aria-pressed", String(paused));
}

motionButton.hidden = false;
motionButton.addEventListener("click", () => {
  paused = !paused;
  updateMotion();
});
reducedMotion.addEventListener("change", (event) => {
  paused = event.matches;
  updateMotion();
});
for (const card of gallery.children) {
  card.querySelector("select")?.addEventListener("change", () => updateImage(card));
}
function applyFilter(filter) {
  let visible = 0;
  for (const card of gallery.children) {
    card.hidden = filter !== "all" && card.dataset.directions !== filter;
    if (!card.hidden) visible += 1;
  }
  for (const button of document.querySelectorAll("[data-sprite-filter]")) {
    button.setAttribute("aria-pressed", String(button.dataset.spriteFilter === filter));
  }
  status.textContent = `${visible}개 팩 표시`;
}

for (const button of document.querySelectorAll("[data-sprite-filter]")) {
  button.hidden = false;
  button.addEventListener("click", () => applyFilter(button.dataset.spriteFilter));
}
for (const link of document.querySelectorAll(".sprite-index a")) {
  link.addEventListener("click", () => {
    if (document.querySelector(link.hash)?.hidden) applyFilter("all");
  });
}
updateMotion();
