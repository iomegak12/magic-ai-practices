/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
      colors: {
        panel: 'rgba(255,255,255,0.72)',
        card: 'rgba(255,255,255,0.85)',
        'text-primary': '#1a1a2e',
        'text-secondary': '#6b7280',
        'text-muted': '#9ca3af',
        'send-btn': '#1a1a2e',
      },
      backdropBlur: {
        panel: '16px',
        bg: '40px',
      },
      borderRadius: {
        panel: '20px',
        card: '14px',
        input: '16px',
        pill: '999px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
