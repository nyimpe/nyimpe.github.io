import { readdirSync } from "node:fs";
import { resolve } from "node:path";
import { defineConfig } from "vite";

// Every posts/<slug>/index.html is an independent page, including plain notes.
const posts = readdirSync("posts", { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => resolve("posts", entry.name, "index.html"));

export default defineConfig({
  build: {
    rollupOptions: {
      input: [resolve("index.html"), resolve("about/index.html"), ...posts],
      output: { manualChunks: { phaser: ["phaser"] } },
    },
  },
});
