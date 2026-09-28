# Shirakami Return Protocol v0.1

## Purpose

Shirakami は、clone された時点で利用を終えるのではなく、利用・観測・検証から得られた知見を、必要に応じて Shirakami Project へ戻せる循環を持ちます。

本プロトコルは、Shirakami を clone した利用者が「何を返せばよいのか分からない」という状態を減らし、観測・発見・変更を適切な GitHub artifact へ接続するための帰還経路を定義します。

> **Clone is the entry. Return is optional. Human judgment decides what returns.**

帰還は義務ではありません。利用者は、自分の環境だけで Shirakami を利用・改変できます。

---

## Return Loop

```text
Clone
  ↓
Use / Modify / Observe
  ↓
Something was learned
  ↓
Return Protocol
  ↓
Observation / Evidence / Issue / PR / 的目YAML
  ↓
Shirakami Project
  ↓
Verification
  ↓
Human Gate
  ↓
Adopt / Hold / Reject
  ↓
Evidence / Finding
  ↓
Research / Protocol / Runtime
```

Shirakami の既存の
**Observation → Evidence → Analysis → Protocol → Runtime → Verification → Evidence**
という循環を、外部利用者にも開くためのプロトコルです。

---

## What can be returned?

### 1. Observation

「使ってみたらこうなった」という観測。

例:
- 特定の環境での挙動
- 予想外の結果
- 新しい利用方法
- 実装して初めて分かったこと

→ Issue または Evidence として返せます。

### 2. Evidence

観測結果を、再確認可能な事実として整理したもの。

含めるとよい情報:
- Environment
- Input / Condition
- Observation
- Expected behavior
- Actual behavior
- Reproduction steps
- Related commit / version

→ Issue、PR、または将来の EvidenceRecord として扱えます。

### 3. Issue

問題、疑問、改善提案を GitHub 上で共有する場合。

「完成した修正」を要求しません。

### 4. Pull Request

コード、仕様、ドキュメント、テストなどを変更した場合。

PR は採用を意味しません。
Shirakami 側で Verification と Human Gate を通します。

### 5. 的目YAML

プロジェクト間で意味・目的・判断条件などを引き継ぐ必要がある場合。

実装変更だけではなく、
「なぜこの変更をしたのか」
「何を維持すべきなのか」
を返すために使用します。

---

## Return Decision

帰還データを受け取った後の判断は自動化しません。

```text
External Observation / Change
          ↓
       Return
          ↓
      Verification
          ↓
      Human Gate
          ↓
   ┌──────┼──────┐
   ↓      ↓      ↓
 Adopt   Hold   Reject
```

採用されなかった報告も、必要に応じて Evidence / Finding として記録できます。

**Return does not mean acceptance.**

---

## For first-time users

Shirakami を clone した利用者は、まず自由に読んだり、試したり、改変したりできます。

何か返したいと思ったら、次の質問だけで分類できます。

| What happened? | Return form |
|---|---|
| 使ってみた | Observation |
| 新しい事実を発見した | Evidence |
| 問題を見つけた | Issue |
| コードや仕様を変更した | Pull Request |
| 意味・目的・条件を引き継ぎたい | 的目YAML |

Git や GitHub に慣れていない場合でも、最初から完璧な形式にする必要はありません。
観測した事実をそのまま記述し、後から構造化できます。

---

## AI assistance

AI は Return の整理を支援できます。

```text
Human experience / observation
          ↓
           AI
  organize / classify / draft
          ↓
       Human Gate
          ↓
 Issue / Evidence / PR / 的目YAML
```

AI が自動的に帰還・採用・判断を行うことは、このプロトコルの前提ではありません。

**AI assists the return. Humans decide the return.**

---

## Scope

v0.1 は GitHub を中心とした帰還経路の概念・分類を定義します。

将来的に以下へ拡張できます。

- Return Template
- EvidenceRecord integration
- Semantic Handoff integration
- Issue / PR templates
- Local tooling
- AI-assisted return preparation
- Return metrics

これらは v0.1 の必須要件ではありません。

---

## Core Principle

> **Clone is the entry. Return is optional. Human judgment decides what returns.**

Shirakami は利用者を「貢献者」に変えることを目的としません。

利用者が何を観測し、何を返すかを自分で決められること。
それが Return Protocol の基本です。
