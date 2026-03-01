import { serve } from '@hono/node-server'
import { serveStatic } from '@hono/node-server/serve-static'
import { Hono } from 'hono'
import { html } from 'hono/html'
import { readFile, writeFile } from 'node:fs/promises'

function randomString() {
  return Math.floor(Math.random() * 4294967296).toString(16)
}

async function getResultContent(type) {
  return await readFile(`${import.meta.dirname}/${type}`, 'utf-8')
}

const app = new Hono()

app.use('/*', serveStatic({ root: './public' }))

app.get('/draw', async c => {
  const candidates = ['daikichi', 'kyo']
  const resultType = candidates[Math.floor(Math.random() * candidates.length)]
  const resultContent = await getResultContent(resultType)
  return c.json({
    type: resultType,
    content: resultContent
  })
})

app.post('/save', async c => {
  const type = await c.req.text()
  const content = await getResultContent(type)
  const filename = randomString()
  await writeFile(`${import.meta.dirname}/public/result/${filename}.html`, html`
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.css">
</head>
<body>
    <pre>${content}</pre>
    <a href="/">Back to Top</a>
</body>
</html>
  `)
  return c.json({
    location: `/result/${filename}.html`
  })
})

const port = 3000
console.log(`Server is running on port ${port}`)

serve({
  fetch: app.fetch,
  port
})
