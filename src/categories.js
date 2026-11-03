// The home page filter, its menu links and the post list share these category names.
export const categoryLabels = { game: "Game", design: "Game Design", note: "Note" };

// The category from the query string, or null when it is missing or unknown.
export function requestedCategory() {
  const category = new URLSearchParams(window.location.search).get("category");
  return Object.hasOwn(categoryLabels, category) ? category : null;
}
