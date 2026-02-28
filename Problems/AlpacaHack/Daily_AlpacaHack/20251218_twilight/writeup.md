# Twilight

| 項目 | 値 |
|---|---|
| **大会** | AlpacaHack / DailyAlpacaHack |
| **ジャンル** | Rev |
| **難易度** | Medium |
| **フラグ** | `Alpaca{AlpacaHack_in_Wonderland}` |
| **日付** | 2026-02-28 |

## 概要

フラグを入力するとエンコードされた出力が得られるプログラム。`out.txt` にエンコード済みデータが与えられるので、逆変換してフラグを復元する。

## 解析

バイナリには `main` のほかに `a` と `b` の2つの関数がある。

| 関数 | ロジック |
|---|---|
| `a(x, y)` | `return x + y` （加算） |
| `b(x, y)` | `return x ^ y` （XOR） |

`main` は関数ポインタ配列 `[a, b]` を使い、各文字をインデックスに応じて変換：

- **偶数番目** (`i % 2 == 0`): `output[i] = a(input[i], i)` → `input[i] + i`
- **奇数番目** (`i % 2 == 1`): `output[i] = b(input[i], i)` → `input[i] ^ i`

## 解法

逆変換を適用するだけ：

- 偶数番目: `input[i] = output[i] - i`
- 奇数番目: `input[i] = output[i] ^ i`

```python
for i, c in enumerate(enc):
    if i % 2 == 0:
        flag += chr(c - i)
    else:
        flag += chr(c ^ i)
```

## 学んだこと

- `nm` でシンボル一覧からカスタム関数を特定する手法
- ARM 環境での x86_64 バイナリ解析には `capstone` (Python) が便利
- 関数ポインタ配列 + `i % 2` で処理を分岐するパターン
- 加算とXORの逆変換（加算 → 減算、XOR → 同じXOR）
