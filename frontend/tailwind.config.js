/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        void: '#05070d',
        panel: '#0b0f1a',
        card: '#101625',
        btc: '#f7931a',
        cyber: '#22d3ee',
        nostri: '#a78bfa',
      },
      fontFamily: { display: ['Space Grotesk', 'Inter', 'system-ui', 'sans-serif'] },
    },
  },
  plugins: [],
}
