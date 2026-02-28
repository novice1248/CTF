# alloc-101

| 項目 | 値 |
|---|---|
| **大会** | AlpacaHack / DailyAlpacaHack |
| **ジャンル** | Pwn (Heap) |
| **難易度** | Hard |
| **フラグ** | `Alpaca{dive_into_heap_23af5b4f}` |
| **日付** | 2026-02-28 |

## 概要

ヒープ操作メニュー（allocate / free / read / allocate flag）を持つプログラム。フラグファイルは起動時に `fopen` されているが、直接読む手段はない。

## 脆弱性

**Use-After-Free (UAF)**

```c
case 2: {
    assert(item != NULL);
    free(item);
    //item == NULL;   // ← コメントアウト！NULL代入されない
}
```

`free(item)` の後に `item = NULL` がされていない（`==` で比較になっている上にコメントアウト）。解放後も `item` ポインタが有効なまま残るため、case 3 の `puts(item)` で freed メモリを読み出せる。

## 解法

tcache の再利用を悪用してフラグを読み取る：

1. **allocate** (`f_sz` バイト) → `item` = chunk A
2. **free** → chunk A が tcache に入る（`item` はまだ chunk A を指す）
3. **allocate flag** → `malloc(f_sz)` で tcache から chunk A が再利用 → フラグが chunk A に書き込まれる
4. **read** → `puts(item)` で chunk A の内容（= フラグ）が出力される

```
[*] item allocated at: 0x55b22f388490
[*] flag allocated at: 0x55b22f388490  ← 同じアドレス！
[+] FLAG: Alpaca{dive_into_heap_23af5b4f}
```

## 学んだこと

- `free()` 後にポインタを NULL にしないと UAF が発生する
- glibc の tcache は同じサイズの `malloc` で直前に `free` されたチャンクを再利用する (LIFO)
- UAF で freed チャンクを別の `malloc` で再利用させ、その内容を読み出すテクニック
