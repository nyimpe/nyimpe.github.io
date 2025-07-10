import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const phasermsg = () => {
  return {
    name: "phasermsg",
    buildStart() {
      process.stdout.write(`build start...\n`);
    },
    buildEnd() {
      const line = "---------------------------------------------------------";
      const msg = `build end`;
      process.stdout.write(`${line}\n${msg}\n${line}\n`);

      process.stdout.write(`✨ Done ✨\n`);
    },
  };
};

export default defineConfig({
  base: "./",
  plugins: [react(), phasermsg()],
  logLevel: "warning",
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          phaser: ["phaser"],
        },
      },
    },
    minify: "terser",
    terserOptions: {
      compress: {
        passes: 2,
      },
      mangle: true,
      format: {
        comments: false,
      },
    },
  },
});
