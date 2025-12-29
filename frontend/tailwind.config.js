/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './pages/**/*.{js,ts,jsx,tsx,mdx}',
        './components/**/*.{js,ts,jsx,tsx,mdx}',
        './app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            colors: {
                background: '#0a0a0f',
                foreground: '#ffffff',
                card: '#12121a',
                'card-hover': '#1a1a25',
                primary: '#06b6d4',
                'primary-hover': '#0891b2',
                secondary: '#a855f7',
                accent: '#ec4899',
                success: '#10b981',
            },
            keyframes: {
                'shimmer-text': {
                    '0%, 100%': { backgroundPosition: '200% center' },
                    '50%': { backgroundPosition: '0% center' },
                },
            },
            animation: {
                'shimmer-text': 'shimmer-text 3s ease-in-out infinite',
            },
        },
    },
    plugins: [],
};
