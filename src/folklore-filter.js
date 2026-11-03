const filter = document.querySelector(".creature-filter");
const buttons = [...filter.querySelectorAll("button[data-initial]")];
const status = filter.querySelector(".creature-filter-status");
// Group doubled consonants under the 14 basic initials.
const initials = "ㄱㄱㄴㄷㄷㄹㅁㅂㅂㅅㅅㅇㅈㅈㅊㅋㅌㅍㅎ";
const entries = [...document.querySelectorAll(".creature-entry")].map((element) => {
  const name = element.querySelector("h2").textContent.trim().normalize("NFC")
    .replace(/^\(항목외\)\s*/, "");
  const syllable = name.charCodeAt(0) - 0xac00;
  return { element, initial: initials[Math.floor(syllable / 588)] };
});

function applyFilter(initial) {
  let count = 0;
  for (const entry of entries) {
    entry.element.hidden = initial !== "" && entry.initial !== initial;
    if (!entry.element.hidden) count += 1;
  }
  for (const button of buttons) {
    button.setAttribute("aria-pressed", String(button.dataset.initial === initial));
  }
  status.textContent = `${initial || "전체"} · ${count}항목`;
  if (count === 0) status.textContent += " — 해당 초성의 항목이 없습니다.";
}

for (const button of buttons) {
  button.addEventListener("click", () => applyFilter(button.dataset.initial));
}
applyFilter("");
filter.hidden = false;
