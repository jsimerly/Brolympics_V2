/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  mode: "jit",
  theme: {
    extend: {
      colors: {
        primary: "#4F86C6",
        primaryLight: "#e4eaf6",
        secondary: "#FAF3C5", 
        secondaryLight: '#ffffff',
      },
      fontFamily: {
        roboto : ['Roboto', 'serif'],
        londrina: ['Londrina Solid', 'sans-serif']
      },
    },
    screens: {
      xs: "480px",
      ss: "620px",
      sm: "768px",
      ms: "840px",
      md: "1060px",
      lg: "1280px",
      xl: "1700px",
    },
  },
  plugins: [],
};

