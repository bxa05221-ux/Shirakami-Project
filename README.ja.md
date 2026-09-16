# Shirakami Project

## AIを人間の意思のもとで扱うための Language Protocol OS

Shirakami Project（白神プロジェクト）は、AIそのものを賢くするのではなく、**人間がAIを自分の意思で使える環境をつくる**ための研究・設計・実装プロジェクトです。

白神モデルはLLMそのものを置き換えるものではありません。
人間の言葉を整理し、Language Protocolとして扱い、AI Runtimeとの間に構造を与えることで、AIとの協働を人間側から制御できるようにすることを目指します。

> **AI is a simulator, not an authority.**
>
> AIは判断主体ではなく、人間が判断するためのシミュレータである。

---

## 白神プロジェクトのLandscape

Shirakami Projectは、単一のアプリケーションではありません。
研究・意味・仕様・実装・応用を分離しながら、それらを切断しない構造を採用しています。

```text
                 Shirakami Project
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     Research         Model        Specification
        │               │               │
    理論・仮説     Language Protocol     仕様
        │               OS               │
        └───────────────┼───────────────┘
                        │
                     Runtime
                        │
                  AI / Application
                        │
                    Evidence
                        │
                 Human Judgment
```

### Repositoryの役割

| Repository | 役割 |
|---|---|
| `shirakami-research` | 理論・仮説・研究実験 |
| `shirakami-model` | 白神モデル / Language Protocol OS |
| `shirakami-specification` | Protocol・構造・仕様 |
| `shirakami-OS` | Runtime・実装・Tests |

関連するApplicationや実験用Repositoryは、それぞれの責任範囲に応じて接続されます。

---

## 基本構造

Shirakamiは、次の流れを基本とします。

```text
Human Language
      ↓
Prompt Organization
      ↓
Language Protocol
      ↓
Computational Task
      ↓
AI Runtime
      ↓
Evidence / Observation
      ↓
Human-readable Options
      ↓
Human Judgment
```

重要なのは、**AIの出力を最終判断にしないこと**です。

白神は、AIの回答を人間の判断材料として扱い、確認された情報・推定・創造的要素などを構造的に区別できる環境を目指します。

---

## Language Protocol OS

白神モデルは、言語Protocolを強力にサポートする、いわば**Language Protocol OS**です。

人間のプロンプトを整理し、AIが理解しやすい形に展開し、それを計算対象としてタスクを実行します。

さらに、ユーザーの言葉遣い、思考のパターン、言い回しなどを観測し、それらをユーザー固有のLanguage Protocolとして適応していくことを目指します。

これはAIの性能そのものを向上させるものではありません。

**AIの性能ではなく、AIを使う人間の体験を向上させる。**

---

## AIに先導させない

白神は、AIがユーザーの意思決定を先導することを前提としません。

不要な冗長性を減らし、ユーザーの現在地に合わせて複数の視点や選択肢を提示することで、判断を人間に返します。

ユーザーが望む場合には、AIに補助的な先導をさせることもできます。

```text
AI → 提案・シミュレーション・整理
                 ↓
              人間
                 ↓
              判断・決定
```

---

## Evidence

AIとの対話では、確認された情報と推定・解釈・創造的要素が混在することがあります。

Shirakamiでは、意味の逸脱を含む問題をEvidenceとして扱い、確認済みの情報と未確認の要素を区別できる構造を目指します。

これにより、AIの出力をそのまま「事実」や「判断」として扱うことを避けます。

---

## 的目YAMLによるSemantic Handoff

Shirakami Projectでは、プロジェクトを分離しても意味を切断しないため、**的目YAML**を意味の正式な引継ぎ単位として扱います。

```text
Mother
  ↓
Research
  ↓
的目YAML
  ↓
Local Repository
  ↓
Verification
  ↓
GitHub
  ↓
Operation
  ↓
Evidence
  ↓
Mother
```

それぞれの役割は明確に分離します。

- **的目YAML** — 意味の引継ぎ
- **Local Repository** — 開発中の状態
- **GitHub Repository** — 確定した実装と履歴
- **Mother** — 全体Landscapeと調整
- **ChatGPT Project** — 作業空間。唯一の正本にはしない

この分離によって、研究と実装を混在させず、それでも意味と履歴を維持します。

---

## 開発状況

Shirakamiは現在、プロトタイプから実運用へ向けたシェイクダウン段階にあります。

完成した「製品」や完成した「理論」を宣言するものではありません。

実装・検証・運用から得られた知見をEvidence / Findingとして扱い、必要に応じてResearchへ戻しながら更新していきます。

**一変更一検証。**

---

## 初めて見る人へ

白神を初めて見る場合は、次の順序で読むことを推奨します。

1. **Model** — 白神が何を目指すのか
2. **Specification** — どのような構造で扱うのか
3. **OS / Runtime** — それをどう実装するのか
4. **Research** — 背後にある理論・仮説・実験

---

## Core Principle

> **Do not make AI smarter.**  
> **Make it possible for people to use AI on their own terms.**

AIを賢くするのではなく、
**人間がAIを自分の意思で使えるようにする。**

---

## Project Status

**Prototype / β1.0 Operational Rollout**

Shirakami Projectは、研究・仕様・実装・応用を継続的に進めるプロジェクトLandscapeです。
