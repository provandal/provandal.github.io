/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Warm off-black / off-white. No pure #000 or #fff.
        ink: {
          950: '#14110f',  // deepest bg
          900: '#1a1714',  // bg
          800: '#241f1b',  // raised surface
          700: '#3a332d',  // border
          600: '#5a5048',  // muted text
          500: '#8a7f75',  // secondary text
          400: '#b8ac9f',  // tertiary
          300: '#d6ccbf',  // body emphasis
          200: '#e8dfd3',  // body
          100: '#f2ebe0',  // headings
          50:  '#faf5ec',  // lightest
        },
        // Single signal accent: muted terracotta.
        signal: {
          DEFAULT: '#c2583a',
          soft: '#d47a5d',
          dim:  '#8a3c27',
        },
      },
      fontFamily: {
        display: ['Fraunces', 'ui-serif', 'Georgia', 'serif'],
        sans: ['Geist', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      maxWidth: {
        prose: '68ch',
        wide: '76ch',
      },
      letterSpacing: {
        tightest: '-0.04em',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
