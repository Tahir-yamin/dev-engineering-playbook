import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#00f0ff",
                secondary: "#f0a500",
            },
            fontFamily: {
                mono: ['var(--font-mono)', 'monospace'],
                display: ['var(--font-rajdhani)', 'sans-serif'],
            },
            boxShadow: {
                'neon': '0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3)',
                'neon-amber': '0 0 10px rgba(240, 165, 0, 0.5), 0 0 20px rgba(240, 165, 0, 0.3)',
                'inset-neon': 'inset 0 0 15px rgba(0, 240, 255, 0.2)',
                'glow-cyan': '0 0 10px #00f0ff, 0 0 5px #00f0ff inset',
                'glow-orange': '0 0 10px #ffae00, 0 0 5px #ffae00 inset',
            },
            animation: {
                'pulse-glow': 'pulse-glow 3s ease-in-out infinite',
                'scan': 'scan 8s linear infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                'pulse-glow': {
                    '0%, 100%': { opacity: '0.8', boxShadow: '0 0 20px rgba(0,255,249,0.5)' },
                    '50%': { opacity: '1', boxShadow: '0 0 40px rgba(0,255,249,0.8)' },
                },
                'scan': {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(100vh)' },
                },
                'float': {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
            },
            backgroundImage: {
                'grid-pattern': 'linear-gradient(to right, rgba(0,255,249,0.1) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,255,249,0.1) 1px, transparent 1px)',
            },
            backgroundSize: {
                'grid': '40px 40px',
            },
        },
    },
    plugins: [],
};

export default config;
