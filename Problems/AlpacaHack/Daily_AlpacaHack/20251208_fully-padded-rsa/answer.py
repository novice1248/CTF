from Crypto.Util.number import long_to_bytes
import gmpy2
import sys

# -----------------------------------------------------
# ファイル読み込み (output.txtがある場所で実行してください)
# -----------------------------------------------------
try:
    with open('output.txt', 'r') as f:
        data = f.read()
        # 簡易パース
        for line in data.splitlines():
            if line.startswith('n ='):
                n = int(line.split('=')[1].strip())
            elif line.startswith('c1 ='):
                c1 = int(line.split('=')[1].strip())
            elif line.startswith('c2 ='):
                c2 = int(line.split('=')[1].strip())
except FileNotFoundError:
    print("Error: output.txt が見つかりません。")
    sys.exit(1)

e1 = 65517
e2 = 65577

# -----------------------------------------------------
# ステップ1: Common Modulus Attack で m^3 mod n を求める
# -----------------------------------------------------
print("[*] Calculating m^3 mod n ...")

# GCD(e1, e2) = 3 となる s, t を求める
g, s, t = gmpy2.gcdext(e1, e2)

# g != 3 なら前提が崩れるのでチェック
if g != 3:
    print(f"Error: GCD is not 3 (g={g})")
    sys.exit(1)

# c1^s * c2^t mod n を計算
# s, t の負号処理
if s < 0:
    c1_part = gmpy2.powmod(gmpy2.invert(c1, n), -s, n)
else:
    c1_part = gmpy2.powmod(c1, s, n)

if t < 0:
    c2_part = gmpy2.powmod(gmpy2.invert(c2, n), -t, n)
else:
    c2_part = gmpy2.powmod(c2, t, n)

# これが m^3 mod n
c_combined = (c1_part * c2_part) % n

# -----------------------------------------------------
# ステップ2: 単純な算数で解く (Small Difference)
# m = n - x (xは小さい)
# m^3 = (n - x)^3 = -x^3 (mod n) = n - x^3
# -----------------------------------------------------
print("[*] Solving for x (n - m) ...")

# x^3 = n - (m^3 mod n)
val_x3 = n - c_combined

# x = 3乗根(val_x3)
x, is_exact = gmpy2.iroot(val_x3, 3)

if is_exact:
    print("[+] Perfect cube root found!")
    # m を復元
    m = n - x
    
    # バイト列に変換
    flag_bytes = long_to_bytes(m)
    
    # 表示
    print("-" * 50)
    try:
        # フラグ部分だけ抽出してデコードを試みる
        # nのバイト列の長さを見て、末尾を表示
        print("Decoded Full Message:\n", flag_bytes[-60:]) # 末尾60バイトを表示
        print("\n[SUCCESS] Flag candidate:")
        print(flag_bytes[-50:].decode(errors='ignore'))
    except:
        print(flag_bytes)
    print("-" * 50)
else:
    print("[-] Failed to find integer cube root. Assumption incorrect.")
    print(f"Remainder: {val_x3 % x}")
