---
name: misc
description: CTFのMisc / OSINTジャンル。エンコーディング変換、CyberChef活用、OSINT手法、プログラミング問題について説明。Misc問題やOSINT問題に取り組む際に参照。
---

# Misc / OSINT

## 技術スタック

- **エンコーディング**: Python標準ライブラリ, CyberChef
- **OSINT**: Google Dorks, Shodan, Wayback Machine, ExifTool
- **自動化**: Python (pwntools, requests, itertools)
- **その他**: nc (netcat), socat

## エンコーディング変換

### Python でよく使う変換

```python
import base64
import binascii
import codecs

# Base64
encoded = base64.b64encode(b'flag{test}')
decoded = base64.b64decode(encoded)

# Base32
base64.b32encode(b'flag{test}')
base64.b32decode(b'MZWGCZ33...')

# Hex
binascii.hexlify(b'flag{test}')     # → b'666c61677b746573747d'
binascii.unhexlify(b'666c61677b746573747d')

# ROT13
codecs.decode('synt{grfg}', 'rot_13')

# URL エンコード
from urllib.parse import quote, unquote
quote('flag{test}')
unquote('flag%7Btest%7D')

# バイナリ文字列
bin_str = '01100110 01101100 01100001 01100111'
''.join(chr(int(b, 2)) for b in bin_str.split())

# モールス信号
MORSE = {'.-': 'A', '-...': 'B', '-.-.': 'C', ...}
```

### 多段エンコードの解読

```python
import base64

data = b'初期データ'

# よくある多段パターン: Base64 → Hex → Base64 → ...
# 自動検出ループ
for _ in range(10):
    try:
        # Base64 を試す
        decoded = base64.b64decode(data)
        if decoded.isascii():
            data = decoded
            print(f'Base64: {data}')
            continue
    except Exception:
        pass

    try:
        # Hex を試す
        decoded = bytes.fromhex(data.decode())
        data = decoded
        print(f'Hex: {data}')
        continue
    except Exception:
        pass

    break

print(f'Final: {data}')
```

## CyberChef 活用

[CyberChef](https://gchq.github.io/CyberChef/) でよく使うレシピ：

| 操作 | レシピ |
| --- | --- |
| Base64 デコード | From Base64 |
| Hex デコード | From Hex |
| ROT13 / ROT47 | ROT13 / ROT47 |
| XOR | XOR (key指定) |
| Magic (自動検出) | Magic |
| URL デコード | URL Decode |
| QR コード読み取り | Parse QR Code |

## OSINT 手法

### Google Dorks

```
# 特定サイト内検索
site:example.com "flag"

# ファイルタイプ指定
filetype:pdf site:example.com

# インデックスに残ったページ
cache:example.com

# ディレクトリリスティング
intitle:"index of" site:example.com
```

### 画像 OSINT

```bash
# EXIF データ (GPS情報等)
exiftool image.jpg

# 逆画像検索
# → Google Images, TinEye, Yandex Images
```

### その他 OSINT ツール

- **Wayback Machine**: `web.archive.org` で過去のウェブページを確認
- **Shodan**: IoTデバイス・サーバーの情報検索
- **WHOIS**: ドメイン情報の確認 (`whois example.com`)
- **DNS**: `dig`, `nslookup` でDNSレコード確認

## プログラミング問題 (pwntools + netcat)

```python
from pwn import *

io = remote('host', port)

# サーバーとの対話
while True:
    line = io.recvline().decode().strip()
    print(line)

    # 問題文のパース → 回答
    if 'What is' in line:
        # 例: 計算問題
        expr = line.split('What is ')[1].rstrip('?')
        answer = eval(expr)
        io.sendline(str(answer).encode())
    elif 'flag' in line.lower():
        print(f'[FLAG] {line}')
        break

io.close()
```

## jail 問題 (Python jail escape)

```python
# よく使うペイロード
__import__('os').system('cat /flag')
eval('__imp' + 'ort__("os").system("cat /flag")')
().__class__.__bases__[0].__subclasses__()  # 使えるクラスの列挙

# builtins が制限されている場合
getattr(__builtins__, '__import__')('os').system('sh')
```
