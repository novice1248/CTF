# RSA debug?

| 項目 | 値 |
|---|---|
| **大会** | AlpacaHack / DailyAlpacaHack ([Mirror] TSG LIVE! CTF) |
| **ジャンル** | Crypto |
| **難易度** | Medium |
| **フラグ** | `TSGLIVE{g0od_Mult1plic4t10N-Algor1thm_6y_ru55iAn_Pea5ants}` |
| **日付** | 2026-03-01 |

## 概要

RSA暗号の実装にバグがあり、復号に失敗する。バグを特定して正しく復号する問題。

## 脆弱性

`my_pow(a, n, m)` は `pow(a, n, m)` (べき乗) のつもりだが、乗算 (`*`) が加算 (`+`) になっている：

```python
result = (result + a) % m  # 本来は result * a
a = (a + a) % m            # 本来は a * a
```

これは**ロシア農民の乗算法** (binary multiplication) になっており、実際には `(a * n + 1) % m` を計算する（初期値 `result=1` が加算で残る）。

## 解法

暗号化は `c = (flag * e + 1) % N` と等価なので、逆変換：

```python
flag = (c - 1) * inverse(e, N) % N
```

## 学んだこと

- 二進法べき乗 (binary exponentiation) と二進法乗算 (binary multiplication / Russian peasant multiplication) は構造が同じで、`*` → `+` の違いだけ
- バグがあるコードも「何を計算しているか」を正確に理解すれば逆変換できる
- `my_pow(e, -1, phi)` は `n = -1 < 0` でループが実行されず `d = 1` が返る
