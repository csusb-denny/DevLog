import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: { port: 5163, strictPort: true }, // strictPort forces error instead of auto-bumping
})
