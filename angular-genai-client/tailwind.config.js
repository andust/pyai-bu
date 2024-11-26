/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      container: {
        center: true
      },
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        red: "red",
        green: "green",
      },
    },
  },
  plugins: [],
}