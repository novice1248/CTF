def read_output_txt(path: str = "output.txt") -> int:
	"""指定されたパスのテキストファイルを読み込み、16進数として解釈した整数を返します。

	- ファイル中の空白・改行は無視します。
	- `0x` または `0X` プレフィックスを許容します。
	- ファイルが空の場合は `ValueError` を投げます。
	"""
	with open(path, "r", encoding="utf-8") as f:
		s = f.read().strip()

	# 空白や改行をすべて除去
	s = "".join(s.split())

	if s.startswith(("0x", "0X")):
		s = s[2:]

	if s == "":
		raise ValueError(f"{path} is empty")

	return int(s, 16)


if __name__ == "__main__":
	# 16進数として読み込んだ整数を表示
	a = read_output_txt()

# all prime numbers less than 300
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]

# 素因数のカウントを保持する辞書を作る
count_primes = {p: 0 for p in primes}

# a を素因数分解して各素因数の出現回数を数える
for i in primes:
	while a % i == 0:
		count_primes[i] += 1
		a //= i
	print(f"{i}: {count_primes[i]}")

# 各素因数の個数をASCIIに変換する
# - 0..255 の範囲はそのまま `chr` で変換
# - 範囲外は `?` を使う
chars = []
for p in primes:
	cnt = count_primes[p]
	if 0 <= cnt <= 255:
		chars.append(chr(cnt))
	else:
		chars.append('?')

result = ''.join(chars)
print('\nASCII string:')
print(result)
print('\nASCII bytes (hex):')
print(' '.join(f"{ord(c):02x}" for c in result))

