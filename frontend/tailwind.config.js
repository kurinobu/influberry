module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'influberry-pink': '#FF6B9D',
        'influberry-pink-light': '#FFB5C1',
        'influberry-lavender': '#B794F6',
        'influberry-lavender-light': '#E0C3FC',
        'influberry-mint': '#81E6D9',
        'influberry-mint-light': '#B2F5EA',
        'influberry-beige': '#F7E6A3',
        'influberry-beige-light': '#FFF3C4',
        },
      fontFamily: {
        'sans': ['Poppins', 'Noto Sans Rounded', 'Inter', 'sans-serif'],
        'poppins': ['Poppins', 'sans-serif'],
        'noto': ['Noto Sans Rounded', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
