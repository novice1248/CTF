---
name: crypto
description: CTFのCrypto（暗号）ジャンル。RSA、AES、古典暗号、PyCryptodome、数論ライブラリの使い方について説明。暗号問題に取り組む際に参照。
---

# Crypto（暗号）

## 技術スタック

- **暗号ライブラリ**: PyCryptodome (`from Crypto.Cipher import AES`)
- **数論計算**: gmpy2, sympy, SageMath
- **汎用**: hashlib, itertools, z3-solver
- **オンラインツール**: factordb.com, dcode.fr, CyberChef

## 基本ツール

```python
from Crypto.Util.number import *
from Crypto.Cipher import AES
import gmpy2
from sympy import factorint, isprime, nextprime

# 数値 ↔ バイト変換
n = bytes_to_long(b'flag{test}')
b = long_to_bytes(n)
```

## RSA

### RSA の基本

```
公開鍵: (n, e)  ※ n = p * q
秘密鍵: d ≡ e^(-1) mod φ(n)  ※ φ(n) = (p-1)(q-1)
暗号化: c ≡ m^e mod n
復号:   m ≡ c^d mod n
```

### 基本的な RSA 解法テンプレート

```python
from Crypto.Util.number import long_to_bytes, inverse

# 既知: n, e, c, p, q
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)
flag = long_to_bytes(m)
print(flag)
```

### よくある RSA 攻撃パターン

| 条件 | 攻撃手法 | 解法 |
| --- | --- | --- |
| n が小さい | 素因数分解 | factordb.com / sympy.factorint |
| e が小さい (e=3) | Low exponent attack | `gmpy2.iroot(c, e)` |
| e が大きい → d が小さい | Wiener's attack | 連分数展開 |
| 同じ n, 異なる e | Common modulus attack | 拡張ユークリッド |
| 同じ m, 異なる n (e=3) | Hastad's broadcast | CRT (中国剰余定理) |
| p ≈ q | Fermat's factorization | `gmpy2.isqrt(n)` 付近を探索 |

### 小さい e の攻撃 (e=3)

```python
import gmpy2

# m^3 = c (mod n だが m^3 < n なら mod 不要)
m, exact = gmpy2.iroot(c, 3)
if exact:
    print(long_to_bytes(int(m)))
```

### Wiener's Attack (d が小さい場合)

```python
# pip install owiener
import owiener

d = owiener.attack(e, n)
if d:
    m = pow(c, d, n)
    print(long_to_bytes(m))
```

## AES

### AES-ECB の特徴と攻撃

```python
from Crypto.Cipher import AES

# ECB モードは同じ平文ブロック → 同じ暗号文ブロック
# → Chosen Plaintext Attack (バイトずらし) が有効

# 復号テンプレート
cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)
```

### AES-CBC

```python
# CBC Bit-Flipping Attack
# padding oracle attack
from Crypto.Cipher import AES

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)
```

## 古典暗号

```python
# シーザー暗号 (ROT13 含む全探索)
def caesar_bruteforce(ciphertext):
    for shift in range(26):
        decrypted = ''
        for c in ciphertext:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                decrypted += chr((ord(c) - base - shift) % 26 + base)
            else:
                decrypted += c
        print(f'shift={shift:2d}: {decrypted}')

# ヴィジュネル暗号
# → CyberChef の Vigenère Decode を使うか、鍵長推定 → 各列でシーザー全探索
```

## 便利な数論関数

```python
from sympy import factorint, gcd, mod_inverse
import gmpy2

# 素因数分解
factors = factorint(n)

# GCD (共通因数の発見)
common = gcd(n1, n2)  # 共通の素因数 p が見つかることがある

# 中国剰余定理 (CRT)
from sympy.ntheory.modular import crt
remainders = [r1, r2, r3]
moduli = [m1, m2, m3]
result, mod = crt(moduli, remainders)

# 離散対数
from sympy.ntheory.residues import discrete_log
x = discrete_log(p, a, g)  # g^x ≡ a (mod p)
```
