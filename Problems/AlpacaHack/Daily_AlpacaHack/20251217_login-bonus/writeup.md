# login-bonus

| 項目 | 値 |
|---|---|
| **大会** | AlpacaHack / DailyAlpacaHack |
| **ジャンル** | Pwn |
| **難易度** | Medium |
| **フラグ** | `Alpaca{h0w_d1d_U_gu3s5_i7}` |
| **日付** | 2026-02-28 |

## 概要

パスワード認証プログラム。ランダム生成されたパスワード (`secret`) と一致する入力を求められ、正解するとシェルが起動する。

## 脆弱性

- `scanf("%[^\n]", password)` に **長さ制限がない** → BOF
- `password[32]` の直後に `secret[32]` がBSS領域で隣接（`nm` で確認: `password`=0x4040, `secret`=0x4060）
- `scanf` の `%[^\n]` フォーマットは **NULバイト (`\x00`) も読み取れる**

## 解法

NULバイトを32個送信する。

1. `password[0..31]` が全て `\x00` → `password` は空文字列 `""`
2. `scanf` が `password[32]` (= `secret[0]`) にNUL終端を書き込む → `secret` も `""`
3. `strcmp("", "") == 0` → 認証突破 → シェル起動

```python
io.sendlineafter(b'Password: ', b'\x00' * 32)
```

## 学んだこと

- `scanf("%[^\n]")` は `\x00` (NULバイト) も文字として読み取る
- グローバル変数のBSS配置順は `nm ./binary` で確認できる
- BOFで文字列のNUL終端位置を操作して `strcmp` を騙す手法
- M4 Mac (ARM) で x86_64 バイナリを動かすには `libc6:amd64` + `qemu-user-binfmt` が必要
