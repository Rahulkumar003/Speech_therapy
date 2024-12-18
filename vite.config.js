import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env.GEMINI_API_KEY': JSON.stringify(env.VITE_GEMINI_API_KEY) // Use VITE_ prefix
    },
    plugins: [react()],
    resolve: {
      alias: {
        src: path.resolve(__dirname, './src'), // Alias for src directory
      },
    },
  };
});
