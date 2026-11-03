import { categoryLabels, requestedCategory } from "./categories.js";

const category = requestedCategory();
const label = category ? categoryLabels[category] : "Recent Posts";

// Entries without a category are notes.
for (const entry of document.querySelectorAll(".post-list > li")) {
  entry.hidden = category !== null && (entry.dataset.category ?? "note") !== category;
}

document.getElementById("posts-title").textContent = label;
document.title = `${category ? label : "Home"} · nyimpe`;
