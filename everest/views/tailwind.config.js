const match_any_child = "**/*.{html,js,ts,jsx,tsx}"
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [`./app/${match_any_child}`, `./auth/${match_any_child}`, `./components/${match_any_child}`],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["forest"],
    base: true,
    styled: true,
    utils: true,
    logs: true,
    themeRoot: ":root"
  }
};
