import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Listen on all network interfaces
    port: 8001,       // Changed from 3000 to 8001
    proxy: {
      '/api': {
        target: 'http://localhost:44001',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:44001',
        ws: true,
      },
    },
  },
})

