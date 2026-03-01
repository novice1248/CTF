# Log Viewer

| 項目 | 値 |
|---|---|
| **大会** | AlpacaHack / DailyAlpacaHack |
| **ジャンル** | Web (RCE) |
| **難易度** | Medium |
| **フラグ** | `Alpaca{th3_AWK_Pr0gr4mming_Lan9u4g3}` |
| **日付** | 2026-03-01 |

## 概要

正規表現でログを検索できるログビューア。Flask + awk 構成。

## 脆弱性

**awk Code Injection**

ユーザー入力が `awk` コマンドのプログラム部分に直接注入される：

```python
command = ["awk", f"/{query}/", "info.log"]
subprocess.run(command, capture_output=True, timeout=0.5, text=True)
```

awk はチューリング完全な言語であり、`system()` や `getline` を用いてOSコマンドを実行できる。

## 解法

AWK の `getline` を使ってコマンド出力を変数に取り込み、`print` で出力。`exit` でタイムアウト（0.5秒）を回避。

```
ペイロード: ./ { "cat /flag-*.txt" | getline l; print l; exit } /.
```

- `/./ ... /./` で全行マッチのパターンを構成
- `"cmd" | getline var` でコマンド出力を awk 変数に読み込む
- `system()` だと子プロセスのstdoutが `capture_output=True` で捕捉されないため `getline` が必要

## 学んだこと

- awk は `system()` と `getline` の2つのコマンド実行手段を持つ
- `subprocess.run(capture_output=True)` は子プロセス (`system()`) の出力を直接キャプチャしない → `getline` で awk 内に取り込んで `print` する必要がある
- awk injection ではタイムアウト対策に `exit` が有効
- フラグファイルが md5 でリネームされている場合は2段階 (`ls` → `cat`) で攻撃
