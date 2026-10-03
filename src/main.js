const themeKey = "nyimpe-theme";
const preferredTheme = window.matchMedia("(prefers-color-scheme: dark)");
const toggle = document.getElementById("theme-toggle");
let savedTheme;

try {
  const value = localStorage.getItem(themeKey);
  if (value === "light" || value === "dark") savedTheme = value;
} catch {
  // The toggle also works when the browser does not allow persistent storage.
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const isDark = theme === "dark";
  toggle.textContent = isDark ? "☀" : "☾";
  toggle.setAttribute("aria-pressed", String(isDark));
  toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
  toggle.title = toggle.getAttribute("aria-label");
}

applyTheme(savedTheme ?? (preferredTheme.matches ? "dark" : "light"));
toggle.hidden = false;

toggle.addEventListener("click", () => {
  savedTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(savedTheme);
  try {
    localStorage.setItem(themeKey, savedTheme);
  } catch {
    // Keep the current page usable even if the preference cannot be saved.
  }
});

preferredTheme.addEventListener("change", () => {
  if (!savedTheme) applyTheme(preferredTheme.matches ? "dark" : "light");
});
