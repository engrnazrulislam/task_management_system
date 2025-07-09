/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //template at root
    "./**/templates/**/*.html" //template at app level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

