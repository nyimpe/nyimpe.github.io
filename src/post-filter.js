const requestedCategory = new URLSearchParams(window.location.search).get("category");
const category = requestedCategory === "game" || requestedCategory === "design" || requestedCategory === "note"
  ? requestedCategory
  : "all";
const labels = { all: "Recent Posts", game: "Game", design: "Game Design", note: "Note" };

for (const entry of document.querySelectorAll(".post-list > li")) {
  const entryCategory = entry.dataset.category ?? "note";
  entry.hidden = category !== "all" && entryCategory !== category;
}

const heading = document.getElementById("posts-title");
heading.textContent = labels[category];
document.title = `${category === "all" ? "Home" : labels[category]} · nyimpe`;
