import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#1a0d14',
          panel: '#2a1520',
          border: '#3a1c2b',
        },
        accent: {
          DEFAULT: '#e8447a',
          muted: '#c9a9b4',
        },
      },
    },
  },
  plugins: [],
};

export default config;
