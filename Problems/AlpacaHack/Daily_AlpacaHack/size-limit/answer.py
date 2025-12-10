from Crypto.Util.number import long_to_bytes

# 変数を初期化
N = e = c = d = 0

# ファイルから値を読み取る
with open('output.txt', 'r') as f:
    for line in f:
        if line.startswith('N ='):
            N = int(line.split(' = ')[1])
        elif line.startswith('e ='):
            e = int(line.split(' = ')[1])
        elif line.startswith('c ='):
            c = int(line.split(' = ')[1])
        elif line.startswith('d ='):
            d = int(line.split(' = ')[1])

# 復号した値（これは m mod N です）
m_mod_N = pow(c, d, N)

# k を総当たりする
# フラグは "CTF{" などの文字で始まると予想されます
print("Searching for the flag...")

for k in range(20000000): # 十分な範囲を探索
    m_candidate = m_mod_N + k * N
    flag_candidate = long_to_bytes(m_candidate)
    
    # フラグらしい文字列が含まれているかチェック
    # 一般的なフラグの形式 "CTF{" や "flag{" を探します
    if b'TSGLIVE{' in flag_candidate:
        print(f"Found k = {k}")
        print(flag_candidate)
        break
