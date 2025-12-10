#!/usr/bin/python3

from Crypto.Util.number import getPrime, bytes_to_long
import flag 

## flagの中身が131バイトであることを確認
assert(len(flag.flag) == 131)

## RSA鍵の生成
p = getPrime(512)
q = getPrime(512)
N = p * q
phi = (p - 1) * (q - 1)
e = 0x10001
d = pow(e, -1, phi)

## flagを整数に変換
flag = bytes_to_long(flag.flag)


## flagを暗号化
## c = flag^e mod N
c = pow(flag, e, N)

## 結果の出力
print(f'N = {N}')
print(f'e = {e}')
print(f'c = {c}')
print(f'd = {d}')

m = pow(c, d, N)
print(f'flag = {m.to_bytes(131, "big")}')
flag = bytes_to_long(flag)
print(flag)
