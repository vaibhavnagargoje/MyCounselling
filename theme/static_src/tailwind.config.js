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
                primary: '#6366F1', // Changed to indigo (purple)
                secondary: '#2563eb', // Blue for some buttons as requested
                accent: '#0D9488', // Teal as accent color
                dark: '#1e293b',
                // Theme-specific colors for consistent usage
                success: '#10b981', 
                warning: '#f59e0b',
                danger: '#ef4444',
                info: '#3b82f6',
                light: '#f3f4f6'
            },
            animation: {
                'fade-in-up': 'fadeInUp 0.8s ease-out',
                'fade-in-left': 'fadeInLeft 0.8s ease-out',
                'fade-in-right': 'fadeInRight 0.8s ease-out',
                'bounce-slow': 'bounce 2s infinite',
                'pulse-slow': 'pulse 3s infinite',
                'slide': 'slide 20s infinite linear',
                'slideshow': 'slideshow 15s infinite',
                'zoom-in': 'zoomIn 0.6s ease-out',
                'rotate': 'rotate 20s linear infinite',
                'float': 'float 4s ease-in-out infinite',
                'fade-in-up': 'fadeInUp 0.8s ease-out',
                'fade-in-left': 'fadeInLeft 0.8s ease-out',
                'fade-in-right': 'fadeInRight 0.8s ease-out',
                'bounce-slow': 'bounce 2s infinite',
                'pulse-slow': 'pulse 3s infinite',
                'slide-down': 'slideDown 0.3s ease-out',
                'slide-up': 'slideUp 0.3s ease-out'
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
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
