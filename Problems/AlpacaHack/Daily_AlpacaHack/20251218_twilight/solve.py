#!/usr/bin/env python3
"""
Twilight solver - AlpacaHack DailyAlpacaHack (Rev)

エンコードロジック:
  関数 a(x, y) = x + y  (加算)
  関数 b(x, y) = x ^ y  (XOR)

  偶数番目 (i%2==0): output[i] = input[i] + i
  奇数番目 (i%2==1): output[i] = input[i] ^ i

逆変換:
  偶数番目: input[i] = output[i] - i
  奇数番目: input[i] = output[i] ^ i
"""

enc = [
    0x41, 0x6D, 0x72, 0x62, 0x67, 0x64, 0x81, 0x46,
    0x74, 0x79, 0x6B, 0x68, 0x6D, 0x45, 0x6F, 0x6C,
    0x7B, 0x4E, 0x7B, 0x7D, 0x73, 0x42, 0x85, 0x79,
    0x7C, 0x7C, 0x8C, 0x77, 0x7D, 0x73, 0x82, 0x62,
]

flag = ''
for i, c in enumerate(enc):
    if i % 2 == 0:
        flag += chr(c - i)
    else:
        flag += chr(c ^ i)

print(flag)
