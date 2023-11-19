import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  assetsInclude: ["**/*.md"],
  base: import.meta.env.MODE === "production" ? "/nyimpe.github.io/" : "/",
});
