---
name: reversing
description: CTFのReversing（リバースエンジニアリング）ジャンル。Ghidra、静的解析・動的解析、アンチデバッグ回避について説明。Rev問題に取り組む際に参照。
---

# Reversing（リバースエンジニアリング）

## 技術スタック

- **逆コンパイラ**: Ghidra (無料), IDA Free
- **デバッガ**: GDB + Pwndbg, strace, ltrace
- **バイナリ解析**: objdump, readelf, nm
- **クロスアーキテクチャ逆アセンブル**: capstone (Python) — ARM 上で x86_64 を解析する場合に必須
- **文字列抽出**: strings, FLOSS
- **Python解析**: uncompyle6, pycdc, dis モジュール

## 初期解析フロー

問題バイナリを受け取ったら、以下の順で解析する：

### Step 1: 基本情報の収集

```bash
# ファイル種別
file ./challenge

# シンボル情報
nm ./challenge 2>/dev/null | head -20

# セクション情報
readelf -S ./challenge

# 文字列の抽出 (フラグの手がかり)
strings ./challenge | grep -iE 'flag|ctf|{|}|password|key|secret'
```

### Step 2: 静的解析 (Ghidra)

1. **Ghidra を起動** → 新規プロジェクト作成 → バイナリをインポート
2. **Auto Analysis** を実行（デフォルト設定でOK）
3. **Symbol Tree** → Functions → `main` を探す
4. デコンパイル結果を読み、ロジックを理解する
5. 重要な関数名・文字列・定数をメモする

### Step 3: 動的解析 (必要な場合)

```bash
# システムコールのトレース
strace ./challenge

# ライブラリコールのトレース
ltrace ./challenge

# GDB でブレークポイントを設定して解析
gdb ./challenge
pwndbg> b main
pwndbg> r
pwndbg> ni    # 次の命令 (step over)
pwndbg> si    # 次の命令 (step into)
```

## よくあるパターンと解法

### ① 文字列比較型

入力とフラグを1文字ずつ比較する。

```python
# Ghidra で比較対象の文字列/配列を見つけて復元
flag_chars = [0x66, 0x6c, 0x61, 0x67, 0x7b, ...]
flag = ''.join(chr(c) for c in flag_chars)
print(flag)
```

### ② XOR エンコード型

暗号化されたフラグをXORで復号する。

```python
encrypted = [0x12, 0x34, 0x56, ...]  # Ghidra から抽出
key = 0x42  # or キー配列

# 単一キーの場合
flag = ''.join(chr(c ^ key) for c in encrypted)

# キー配列の場合
key_arr = [0x11, 0x22, 0x33, ...]
flag = ''.join(chr(e ^ k) for e, k in zip(encrypted, key_arr))
print(flag)
```

### ③ インデックス依存エンコード型 (Twilight で使用)

各文字がインデックスに依存する演算でエンコードされるパターン。
関数ポインタ配列で偶数/奇数番目で別の関数を適用する場合がある。

```python
# エンコード: even → add(char, i), odd → xor(char, i)
# デコード: 逆変換を適用
for i, c in enumerate(enc):
    if i % 2 == 0:
        flag += chr(c - i)   # add の逆 → 減算
    else:
        flag += chr(c ^ i)   # xor の逆 → 同じ xor
```

**見分け方**: `nm` で `a`, `b` 等の短い関数名 → 関数ポインタ配列 → `i % N` で分岐

### ④ カスタムアルゴリズム型

独自のエンコード/暗号化ロジックを逆算する。

```python
# Ghidra でアルゴリズムを特定 → 逆関数を実装
def decode(encoded):
    result = []
    for i, c in enumerate(encoded):
        # 逆変換ロジックをここに実装
        result.append(chr(c))  
    return ''.join(result)
```

### ④ angr による自動解析

条件分岐が多い場合は angr (シンボリック実行) を活用。

```python
import angr
import claripy

proj = angr.Project('./challenge', auto_load_libs=False)

# 入力をシンボリック変数として定義
flag_len = 32
flag = claripy.BVS('flag', 8 * flag_len)

state = proj.factory.entry_state(stdin=angr.SimFileStream(name='stdin', content=flag))

# 成功・失敗アドレスを指定
simgr = proj.factory.simgr(state)
simgr.explore(find=0x401234, avoid=0x401256)  # アドレスは Ghidra で確認

if simgr.found:
    solution = simgr.found[0]
    print(solution.solver.eval(flag, cast_to=bytes))
```

## Ghidra ショートカット

| 操作 | ショートカット |
| --- | --- |
| 関数名の変更 | `L` |
| 変数名の変更 | `L` |
| 型の変更 | `Ctrl+L` |
| 相互参照 (Xref) | `Ctrl+Shift+F` |
| コメント追加 | `;` (行末), `Ctrl+;` (行前) |
| 検索 (文字列) | `Search > For Strings` |

## capstone で x86_64 を ARM 上で逆アセンブルする

Ghidra が使えない環境やスクリプトから自動解析する場合に有用。

```python
from capstone import *
from elftools.elf.elffile import ELFFile

with open('./chall', 'rb') as f:
    elf = ELFFile(f)
    text = elf.get_section_by_name('.text')
    code = text.data()
    base = text['sh_addr']

md = Cs(CS_ARCH_X86, CS_MODE_64)

# nm で取得した関数アドレスから逆アセンブル
func_addr = 0x11c9  # nm ./chall | grep ' T func_name'
offset = func_addr - base
for insn in md.disasm(code[offset:offset+0x100], func_addr):
    print(f'  0x{insn.address:x}: {insn.mnemonic}\t{insn.op_str}')
    if insn.mnemonic == 'ret':
        break
```
