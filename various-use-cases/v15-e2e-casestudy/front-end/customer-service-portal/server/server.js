import express from 'express'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const app = express()
const PORT = process.env.PORT || 9090
const DIST_PATH = join(__dirname, '../dist')

// ── Serve static React build files ───────────────
app.use(express.static(DIST_PATH))

// ── Health check (local, not proxied to backend) ─
app.get('/api/ping', (_req, res) => {
  res.json({ status: 'ok', service: 'msav15-frontend', port: PORT })
})

// ── Catch-all: serve index.html for React Router ─
app.get('*', (_req, res) => {
  res.sendFile(join(DIST_PATH, 'index.html'))
})

// ── Start server ─────────────────────────────────
app.listen(PORT, () => {
  console.log(`[MSAv15 Frontend] Server running on http://localhost:${PORT}`)
  console.log(`[MSAv15 Frontend] NODE_ENV: ${process.env.NODE_ENV || 'development'}`)
  console.log(`[MSAv15 Frontend] API_BASE_URL: ${process.env.API_BASE_URL || 'http://localhost:9080'}`)
})
