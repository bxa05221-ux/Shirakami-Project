# Shirakami Project

## AIを人間の意思のもとで扱うための Language Protocol OS

Shirakami Project は、AIそのものを賢くするのではなく、**人間がAIを自分の意思で使える環境をつくる**ための研究・設計・実装プロジェクトです。

白神モデルは、LLMそのものを置き換えるものではありません。
人間の言葉を整理し、Language Protocol として扱い、AI Runtime との間に構造を与えることで、AIとの協働を人間側から制御できるようにします。

> **AI is a simulator, not an authority.**
>
> AIは判断主体ではなく、人間が判断するためのシミュレータである。

---

## Reviewer Entry

白神をレビューする場合、説明だけを読む必要はありません。
**Reviewer Protocol** に沿って、Landscape → Evidence → Protocol → Runtime → Verification → Human Gate の経路を実際に確認できます。

> **A reviewer should not have to believe Shirakami in order to review Shirakami.**
>
> 白神をレビューするために、レビュアーが白神を信じる必要はありません。

→ [`protocols/reviewer-protocol-v0.1.md`](protocols/reviewer-protocol-v0.1.md)

レビュープロトコルは評価を自動化するものではありません。Runtimeの観測とEvidenceを提示し、最終的な判断をレビュアーに返します。

---

## Landscape

Shirakami Project は、単一のアプリケーションではありません。
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

### Repository roles

| Repository | Role |
|---|---|
| [`shirakami-research`](https://github.com/bxa05221-ux/shirakami-research) | 理論・仮説・研究実験 |
| [`shirakami-model`](https://github.com/bxa05221-ux/shirakami-model) | 白神モデル / Language Protocol OS |
| [`shirakami-specification`](https://github.com/bxa05221-ux/shirakami-specification) | Protocol・構造・仕様 |
| [`shirakami-OS`](https://github.com/bxa05221-ux/shirakami-OS) | Runtime・実装・Tests |

関連するApplicationや実験用Repositoryは、それぞれの責任範囲に応じて接続されます。

---

## 基本構造

Shirakami は、次の流れを基本とします。

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

白神は、AIの回答を人間の判断材料として扱い、必要な情報・推定・創造的要素を構造的に分離することを目指します。

---

## Language Protocol OS

白神モデルは、言語 Protocol を強力にサポートする、いわば **Language Protocol OS** です。

人間のプロンプトを整理し、AIが理解しやすい形に展開し、それを計算対象としてタスクを実行します。

さらに、ユーザーの言葉遣い・思考パターン・言い回しなどを観測し、ユーザー固有の Language Protocol に適応していくことを目指します。

これはAIの性能そのものを向上させるものではありません。

**AIの性能ではなく、AIを使う人間の体験を向上させる。**

---

## Evidence

AIとの対話では、確認された情報と推定・解釈・創造的要素が混在することがあります。

Shirakami では、意味の逸脱を含む問題を Evidence として扱い、確認済みの情報と未確認の要素を区別できる構造を目指します。

これにより、AIの出力をそのまま「事実」や「判断」として扱うことを避けます。

---

## Human Judgment

Shirakami の中心にあるのは、AIではなく人間です。

AIがタスクを先導することを前提とせず、複数の視点や選択肢を提示し、最終的な判断を人間に返します。

```text
AI → 提案・シミュレーション・整理
                 ↓
              人間
                 ↓
              判断・決定
```

---

## Semantic Handoff

Shirakami Project では、プロジェクトを分離しても意味を切断しないため、**的目YAML**を意味の正式な引継ぎ単位として扱います。

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

ChatGPT Project は作業空間として利用できますが、会話履歴そのものを唯一の正本とはしません。

- **的目YAML** — 意味の引継ぎ
- **Local Repository** — 開発中の状態
- **GitHub Repository** — 確定した実装と履歴
- **Mother** — 全体Landscapeと調整

この分離によって、研究と実装を混在させず、それでも意味と履歴を維持します。

---

## Development Status

Shirakami は現在、プロトタイプから実運用へ向けたシェイクダウン段階にあります。

完成した「製品」や完成した「理論」を宣言するものではありません。

実装・検証・運用から得られた知見を Evidence / Finding として扱い、必要に応じてResearchへ戻しながら更新していきます。

**一変更一検証。**

---

## Start Here

白神を初めて見る場合は、次の順序を推奨します。

1. **Reviewer Protocol** — 白神を実際にレビューする
2. **Model** — 白神が何を目指すのか
3. **Specification** — どのような構造で扱うのか
4. **OS / Runtime** — それをどう実装するのか
5. **Research** — 背後にある理論・仮説・実験

---

## Core Principle

> **Do not make AI smarter.**  
> **Make it possible for people to use AI on their own terms.**

AIを賢くするのではなく、
**人間がAIを自分の意思で使えるようにする。**

## Project Status

**Prototype / β1.0 Operational Rollout**

Shirakami Project is an ongoing research, specification, implementation, and application landscape.
