import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: "#0a1628",
          800: "#0f1f3d",
          700: "#152a4e",
          600: "#1c3660",
          500: "#234272",
        },
        accent: {
          blue: "#3b82f6",
          orange: "#f59e0b",
        },
      },
    },
  },
  plugins: [],
};

export default config;
