/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom color palette
        'pure-white': 'rgb(255, 255, 255)',
        'electric-blue': 'rgb(0, 118, 219)',
        'jet-black': 'rgb(33, 33, 33)',
        'bold-red': 'rgb(203, 25, 35)',
        'cool-gray': 'rgb(186, 190, 193)',
        'soft-mint': 'rgb(142, 207, 139)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}