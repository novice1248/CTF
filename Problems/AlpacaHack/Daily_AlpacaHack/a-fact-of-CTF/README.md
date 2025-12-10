2025-12-02

https://alpacahack.com/daily/challenges/a-fact-of-CTF

##Crypto

初心者向けヒント
この問題は Crypto カテゴリー、すなわち暗号（Cryptography）に関する問題です。
AlpacaHack では現在 Crypto, Pwn, Rev, Web の 4 つのカテゴリーをメインに出題し、その他の問題は Misc カテゴリーに分類しています。
まずは、添付ファイル a-fact-of-CTF.tar.gz をダウンロードして解凍してみましょう。
chall.py では環境変数 FLAG を読み込んでいます。これがフラグです。
そして、そのフラグを素数を用いて変換しています。
この chall.py の出力が output.txt です。
output.txt の値からフラグを逆算するのがこの問題のゴールです。
