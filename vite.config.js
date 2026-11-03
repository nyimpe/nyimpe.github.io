import { readdirSync } from "node:fs";
import { resolve } from "node:path";
import { defineConfig } from "vite";

// Every posts/<slug>/index.html is an independent page, including plain notes.
const posts = readdirSync("posts", { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => resolve("posts", entry.name, "index.html"));

const SITE_HOST = "nyimpe.github.io";

// Links to other sites always open in a new tab, on every page, without editing each post.
function externalLinksInNewTab() {
  return {
    name: "external-links-in-new-tab",
    transformIndexHtml(html) {
      return html.replace(/<a\b[^>]*>/gi, (tag) => {
        const href = tag.match(/\shref\s*=\s*(["'])(.*?)\1/i)?.[2];
        if (!href || !/^(https?:)?\/\//i.test(href)) return tag;
        if (new URL(href, `https://${SITE_HOST}`).host === SITE_HOST) return tag;
        const rel = new Set((tag.match(/\srel\s*=\s*(["'])(.*?)\1/i)?.[2] ?? "").split(/\s+/).filter(Boolean));
        rel.add("noopener").add("noreferrer");
        const rest = tag.replace(/\s(?:target|rel)\s*=\s*(["']).*?\1/gi, "").replace(/\s*>$/, "");
        return `${rest} target="_blank" rel="${[...rel].join(" ")}">`;
      });
    },
  };
}

export default defineConfig({
  plugins: [externalLinksInNewTab()],
  build: {
    rollupOptions: {
      input: [resolve("index.html"), resolve("about/index.html"), ...posts],
      output: { manualChunks: { phaser: ["phaser"] } },
    },
  },
});
