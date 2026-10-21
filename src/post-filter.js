const requestedCategory = new URLSearchParams(window.location.search).get("category");
const category = requestedCategory === "game" || requestedCategory === "writing"
  ? requestedCategory
  : "all";
const labels = { all: "Recent Posts", game: "Game", writing: "글쓰기" };

for (const entry of document.querySelectorAll(".post-list > li")) {
  const entryCategory = entry.dataset.category ?? "writing";
  entry.hidden = category !== "all" && entryCategory !== category;
}

const heading = document.getElementById("posts-title");
heading.textContent = labels[category];
heading.lang = category === "writing" ? "ko" : "en";
document.title = `${category === "all" ? "Home" : labels[category]} · nyimpe`;
