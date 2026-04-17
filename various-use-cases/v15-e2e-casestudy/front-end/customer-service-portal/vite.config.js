import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 9090,
    proxy: {
      '/health': {
        target: 'http://localhost:9080',
        changeOrigin: true,
      },
      '/chat': {
        target: 'http://localhost:9080',
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          http:   ['axios'],
        },
      },
    },
  },
})
