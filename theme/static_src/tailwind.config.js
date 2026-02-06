module.exports = {
    content: [   
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            fontFamily: {
                'inter': ['Inter', 'sans-serif'],
            },
            colors: {
                primary: '#4f46e5',
                'primary-light': '#6366f1',
                'primary-dark': '#3730a3',
                secondary: '#f59e0b',
                'secondary-light': '#fbbf24',
                accent: '#06b6d4',
                dark: '#1e1b4b',
                success: '#10b981', 
                warning: '#f59e0b',
                danger: '#ef4444',
                info: '#3b82f6',
                light: '#f5f3ff',
                'warm-white': '#fefbf6',
                'cool-slate': '#f8fafc',
            },
            animation: {
                'fade-in-up': 'fadeInUp 0.8s ease-out',
                'fade-in-left': 'fadeInLeft 0.8s ease-out',
                'fade-in-right': 'fadeInRight 0.8s ease-out',
                'bounce-slow': 'bounce 2s infinite',
                'pulse-slow': 'pulse 3s infinite',
                'slide-down': 'slideDown 0.3s ease-out',
                'slide-up': 'slideUp 0.3s ease-out',
                'float': 'float 4s ease-in-out infinite',
            },
            keyframes: {
                fadeInUp: {
                    'from': { opacity: '0', transform: 'translateY(50px)' },
                    'to': { opacity: '1', transform: 'translateY(0)' }
                },
                fadeInLeft: {
                    'from': { opacity: '0', transform: 'translateX(-50px)' },
                    'to': { opacity: '1', transform: 'translateX(0)' }
                },
                fadeInRight: {
                    'from': { opacity: '0', transform: 'translateX(50px)' },
                    'to': { opacity: '1', transform: 'translateX(0)' }
                },
                slide: {
                    '0%': { transform: 'translateX(100%)' },
                    '100%': { transform: 'translateX(-100%)' }
                },
                slideshow: {
                    '0%, 20%': { opacity: '1', transform: 'scale(1)' },
                    '25%, 95%': { opacity: '0', transform: 'scale(1.1)' },
                    '100%': { opacity: '1', transform: 'scale(1)' }
                },
                zoomIn: {
                    'from': { opacity: '0', transform: 'scale(0.8)' },
                    'to': { opacity: '1', transform: 'scale(1)' }
                },
                rotate: {
                    'from': { transform: 'rotate(0deg)' },
                    'to': { transform: 'rotate(360deg)' }
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-25px)' }
                },
                slideDown: {
                    'from': { opacity: '0', transform: 'translateY(-10px)' },
                    'to': { opacity: '1', transform: 'translateY(0)' }
                },
                slideUp: {
                    'from': { opacity: '0', transform: 'translateY(10px)' },
                    'to': { opacity: '1', transform: 'translateY(0)' }
                }
            },
            backgroundImage: {
                'gradient-hero': 'linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%)',
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
