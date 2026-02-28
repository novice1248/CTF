---
name: forensics
description: CTFのForensics（フォレンジクス）ジャンル。パケット解析、ファイルカービング、ステガノグラフィ、メモリフォレンジクスについて説明。Forensics問題に取り組む際に参照。
---

# Forensics（フォレンジクス）

## 技術スタック

- **パケット解析**: Wireshark, tshark, scapy
- **ファイルカービング**: binwalk, foremost, scalpel
- **ステガノグラフィ**: steghide, zsteg, stegsolve, exiftool
- **メモリ解析**: Volatility 3
- **ディスクイメージ**: Autopsy, sleuthkit (fls, icat)
- **その他**: xxd, hexdump, file

## 初期解析手順

ファイルを受け取ったら、まず種類を特定する：

```bash
# 1. ファイル種別の確認
file ./evidence

# 2. マジックバイト確認
xxd ./evidence | head -5

# 3. メタデータ確認
exiftool ./evidence

# 4. 埋め込みファイル探索
binwalk ./evidence

# 5. 文字列抽出
strings ./evidence | grep -iE 'flag|ctf|password|key|secret'
```

## パケット解析 (pcap / pcapng)

### tshark でのフィルタリング

```bash
# HTTP リクエストの一覧
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.request.uri

# HTTP POST データ
tshark -r capture.pcap -Y "http.request.method==POST" -T fields -e http.file_data

# DNS クエリ
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e dns.qry.name

# TCP ストリームの追跡
tshark -r capture.pcap -z "follow,tcp,ascii,0"

# FTP データ転送の抽出
tshark -r capture.pcap -Y "ftp-data" -T fields -e data

# 統計情報
tshark -r capture.pcap -z conv,tcp -q
```

### scapy でのパケット解析

```python
from scapy.all import *

packets = rdpcap('capture.pcap')

# パケット概要
packets.summary()

# 特定プロトコルのフィルタリング
for pkt in packets:
    if pkt.haslayer(DNS):
        if pkt[DNS].qr == 0:  # クエリ
            print(pkt[DNS].qd.qname)

    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        data = pkt[Raw].load
        if b'flag' in data.lower():
            print(f'[!] Found: {data}')

# ICMP データ抽出 (データ隠蔽)
for pkt in packets:
    if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
        print(pkt[Raw].load)
```

## ファイルカービング

```bash
# binwalk で埋め込みファイル検出
binwalk ./evidence

# 自動抽出
binwalk -e ./evidence

# foremost で抽出
foremost -i ./evidence -o output/

# 手動カービング (dd)
dd if=evidence bs=1 skip=OFFSET count=SIZE of=extracted_file
```

## ステガノグラフィ

### 画像ファイル

```bash
# メタデータ確認
exiftool image.png

# PNG 特有の解析
zsteg image.png          # LSB ステガノグラフィ
pngcheck image.png       # PNG 構造の検証

# JPEG
steghide extract -sf image.jpg -p ""     # パスワード空で抽出
steghide extract -sf image.jpg -p "password"

# ビット平面解析
stegsolve                # GUI ツール
```

### Python での LSB 抽出

```python
from PIL import Image

img = Image.open('image.png')
pixels = img.load()
w, h = img.size

# LSB 抽出
bits = ''
for y in range(h):
    for x in range(w):
        r, g, b = pixels[x, y][:3]
        bits += str(r & 1)
        bits += str(g & 1)
        bits += str(b & 1)

# ビット列を文字列に変換
message = ''
for i in range(0, len(bits), 8):
    byte = bits[i:i+8]
    char = chr(int(byte, 2))
    if char == '\x00':
        break
    message += char

print(message)
```

## メモリフォレンジクス (Volatility 3)

```bash
# OS 情報の確認
vol3 -f memory.dmp windows.info

# プロセス一覧
vol3 -f memory.dmp windows.pslist
vol3 -f memory.dmp windows.pstree

# コマンド履歴
vol3 -f memory.dmp windows.cmdline

# ファイル抽出
vol3 -f memory.dmp windows.filescan | grep -i "flag\|secret\|password"
vol3 -f memory.dmp windows.dumpfiles --virtaddr OFFSET

# ネットワーク接続
vol3 -f memory.dmp windows.netscan

# レジストリ
vol3 -f memory.dmp windows.registry.printkey
```

## ZIP / アーカイブ解析

```bash
# ZIP の中身確認
zipinfo archive.zip

# パスワード付き ZIP の解析
fcrackzip -b -c 'aA1' -l 1-6 archive.zip   # ブルートフォース
john --wordlist=rockyou.txt hash.txt          # 辞書攻撃 (zip2john でハッシュ抽出)

# Known Plaintext Attack (pkcrack)
pkcrack -C encrypted.zip -c known_file -P plain.zip -p known_file
```
