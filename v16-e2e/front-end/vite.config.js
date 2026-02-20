import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  server: {
    port: 3000,
    open: false,
    proxy: {
      // Proxy all /api calls to FastAPI backend
      '/api': {
        target: 'http://localhost:9080',
        changeOrigin: true,
        secure: false,
      },
      // Proxy health check endpoints
      '/health': {
        target: 'http://localhost:9080',
        changeOrigin: true,
        secure: false,
      },
    },
  },

  preview: {
    port: 3000,
  },

  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          http: ['axios'],
        },
      },
    },
  },
})
