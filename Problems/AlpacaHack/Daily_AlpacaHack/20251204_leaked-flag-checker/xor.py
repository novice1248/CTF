# Ghidraのコードから数値を抽出（100はそのまま10進数として扱います）
targets = [0x46, 0x6b, 0x77, 0x66, 100, 0x66, 0x7c, 0x6b, 0x72, 100, 0x6c, 0x7e, 0x7a]

flag = ""
for t in targets:
    # chr()で数値を文字に変換、 t ^ 7 で復号
    flag += chr(t ^ 7)

print(flag)
