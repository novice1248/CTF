# Copilot Instructions for CTF Practice Workspace

## 前提条件

- **回答は必ず日本語でしてください。**
- CTFの問題を解く際は、まずジャンル（Pwn, Rev, Web, Crypto, Forensics, Misc）を特定し、該当するスキルを参照してください。
- ソルバースクリプトは Python 3 で書いてください。
- exploitコードを書く際は、まず脆弱性の説明と攻撃方針を日本語で説明してから実装してください。

## 参照スキルガイド (Skills)

特定のタスクを実行する際は、必ず以下の対応するドキュメントを参照し、その指針に従ってください。

- **Pwn（バイナリエクスプロイト）**
  - Pwntools、GDB/Pwndbg、ROP、シェルコード
  - 📄 `.github/skills/pwn/SKILL.md`

- **Reversing（リバースエンジニアリング）**
  - Ghidra、静的/動的解析、アンチデバッグ
  - 📄 `.github/skills/rev/SKILL.md`

- **Web**
  - SQLi、XSS、SSTI、ディレクトリ探索
  - 📄 `.github/skills/web/SKILL.md`

- **Crypto（暗号）**
  - RSA、AES、PyCryptodome、数論
  - 📄 `.github/skills/crypto/SKILL.md`

- **Forensics（フォレンジクス）**
  - パケット解析、ファイルカービング、ステガノグラフィ
  - 📄 `.github/skills/forensics/SKILL.md`

- **Misc / OSINT**
  - エンコーディング、CyberChef、OSINT
  - 📄 `.github/skills/misc/SKILL.md`

## プロジェクト概要

**CTF Practice Workspace** は、各種CTF大会の練習・参加用ワークスペースです。

### 技術スタック概要

| カテゴリ | 技術 |
| --- | --- |
| **言語** | Python 3 |
| **Pwn** | Pwntools, GDB + Pwndbg, Ropper, QEMU + binfmt |
| **Rev** | Ghidra, objdump, strace/ltrace |
| **Web** | Gobuster, SecLists, Burp Suite, curl |
| **Crypto** | PyCryptodome, gmpy2, sympy, SageMath |
| **Forensics** | Wireshark/tshark, scapy, binwalk, volatility |
| **環境** | Kali Linux, Docker |

### ディレクトリ構成

```
ctf/
├── .github/              # Copilot設定 & Skills
├── AlpacaHack/           # AlpacaHack大会
├── cyber_contest/        # サイバーコンテスト
├── interpol_ai_quest/    # INTERPOL AI Quest
└── ctf_setup_memo.md     # 環境構築メモ
```
