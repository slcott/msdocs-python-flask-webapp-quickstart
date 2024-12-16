import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      // string shorthand:
      // http://localhost:5173/foo
      //   -> http://localhost:4567/foo
      // '/foo': 'http://localhost:4567',
      // with options:
      // http://localhost:5173/api/bar
      //   -> http://jsonplaceholder.typicode.com/bar
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      // with RegExp:
      // http://localhost:5173/fallback/
      //   -> http://jsonplaceholder.typicode.com/
      '^/fallback/.*': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/fallback/, ''),
      },
      // Using the proxy instance
      // '/api': {
      //   target: 'http://127.0.0.1:5000',
      //   changeOrigin: true,
      //   configure: (proxy, options) => {
      //     // proxy will be an instance of 'http-proxy'
      //   },
      // },
      // Proxying websockets or socket.io:
      // ws://localhost:5173/socket.io
      //   -> ws://localhost:5174/socket.io
      // Exercise caution using `rewriteWsOrigin` as it can leave the
      // proxying open to CSRF attacks.
      // '/socket.io': {
      //   target: 'ws://localhost:5174',
      //   ws: true,
      //   rewriteWsOrigin: true,
      // },
    },
  },
  plugins: [react()],
})
