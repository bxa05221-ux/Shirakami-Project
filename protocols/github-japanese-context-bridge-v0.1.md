# GitHub Japanese Context Bridge v0.1

## 1. Purpose

GitHub Japanese Context Bridge is an application experiment derived from the Shirakami model and implemented in the independent `github-context-bridge` repository.

Its purpose is not to translate GitHub mechanically from English into Japanese. It places a Shirakami-based context layer between GitHub and the human user so that GitHub's language, state, and evidence can be presented in a human-readable Japanese context.

```text
GitHub
  ↓
github-context-bridge
  ↓
Observation
  ↓
Evidence
  ↓
Context / Language Protocol
  ↓
Japanese Explanation
  ↓
Human Gate
```

The human remains the decision authority.

## 2. Problem Definition

GitHub presents repository state through English UI text, technical terminology, issues, pull requests, workflow results, notifications, and other artifacts.

A literal translation does not necessarily communicate:

- what happened;
- what is confirmed;
- what is inferred;
- what action is being requested;
- what action would change repository state;
- what requires human judgment.

Therefore the bridge treats Japanese presentation as a **context transformation**, not merely a translation task.

## 3. 日本語ブリッジの基本表示原則

このプロトコルでは、**日本語を単なる翻訳結果として扱わない**。

日本語表示は、GitHubから観測した状態を、人間が判断できるContextへ変換した結果である。

したがって、表示順序は原則として次のとおりとする。

```text
観測された事実
    ↓
証拠
    ↓
日本語によるContext説明
    ↓
未確認事項（UNKNOWN）
    ↓
可能な操作
    ↓
Human Gate
```

### 日本語表示のルール

- GitHub上の固有識別子は原文のまま保持する。
- 技術用語は必要に応じて日本語で意味を補足する。
- 原文にない事実を、日本語の自然さのために補わない。
- 推測・解釈は、確認済みの事実と明示的に分離する。
- 不明なものは「不明」「確認できない」などと表示し、推測で埋めない。
- 操作可能であることと、その操作を実行すべきことを分離する。
- 最終的な判断・承認はHuman Gateに残す。

つまり、**日本語の流暢さよりEvidence Boundaryを優先する。**

## 4. Human-readable Roles

The bridge should not expose internal agent names or personas as the primary user interface. Instead, each observation function is presented as a clear Japanese role describing its responsibility.

| Internal source | Display role | Responsibility |
|---|---|---|
| Issue | **問題・要望担当** | 何を解決したいのか、何が求められているのかを整理する |
| Code | **プログラム担当** | 実際のプログラムと関連する実装を確認する |
| Pull Request | **変更担当** | 何を変更しようとしているのかを整理する |
| CI / Workflow | **自動テスト担当** | 自動処理・テストの結果を確認する |
| Commit | **作業履歴担当** | いつ、何が変更されたかを確認する |
| Evidence | **事実確認担当** | 確認できる事実と未確認事項を分離する |
| Protocol | **ルール担当** | 定義された仕様・手順との整合性を確認する |
| Human Gate | **最終判断** | 採用・変更・保留などを人間が判断する |

Technical terms may be shown parenthetically when useful, for example **自動テスト担当（CI）** or **変更担当（Pull Request / PR）**. The role description remains the primary explanation.

Roles are observers and reporters, not independent decision authorities. Multiple roles may contribute to one context record.

## 5. 担当者間会議（保守安価）

複数の担当が関係するGitHub事象では、各担当の観測を持ち寄る担当者間会議を設ける。これを白神では**保守安価**と呼ぶ。

保守安価の役割は、担当者の代わりに判断することではなく、観測結果を照合し、共通点・相違点・未確認事項を整理して、人間が判断できるContextへまとめることである。

```text
問題・要望担当 ─┐
プログラム担当 ─┤
変更担当 ─────┤
自動テスト担当 ─┤
作業履歴担当 ───┤
事実確認担当 ───┤
ルール担当 ─────┘
          ↓
       保守安価
   （担当者間会議）
          ↓
    統合されたContext
          ↓
       最終判断
```

保守安価の役割は以下を明示する。

- 各担当の観測結果
- 観測間で一致している事項
- 観測間で食い違っている事項
- 証拠が不足している事項
- 人間による確認または判断が必要な事項

保守安価自身は、マージ、採用、却下その他の最終決定を行わない。

会議の発言は、事実・解釈・未知を混同しない。担当者間で意見が一致しない場合も、その不一致自体をContextとして保持する。

## 6. Scope

### Phase A — Read-only context

The independent `github-context-bridge` repository may observe:

- repository metadata;
- branches;
- commits;
- issues;
- pull requests;
- changed files;
- review state;
- workflow / CI results;
- relevant GitHub terminology.

The Shirakami-side protocol defines how these observations become Japanese explanations without changing GitHub state.

### Phase B — Evidence-aware explanation

Each explanation should distinguish, where applicable:

- `FACT` — directly observed GitHub information;
- `INTERPRETATION` — contextual explanation;
- `UNKNOWN` — information not established by the available evidence;
- `ACTION` — an available GitHub operation;
- `HUMAN_GATE` — a decision reserved for the human.

### Phase C — Interactive assistance

After validation of Phase A/B, the bridge may assist with navigation, drafting, or other reversible operations.

Any operation that changes repository state remains behind a Human Gate unless an explicit protocol authorizes otherwise.

## 7. Translation Rule

The bridge should preserve technical identifiers and repository semantics.

Examples:

- Pull Request → PR（プルリクエスト）
- merge → マージ（変更を対象ブランチへ統合）
- commit → コミット（変更履歴）
- branch → ブランチ（作業系統）
- workflow → ワークフロー（自動処理）

Terminology may be explained, but identifiers such as repository names, branch names, commit SHAs, issue numbers, and PR numbers must not be translated.

## 8. Context Record

A future implementation SHOULD represent a GitHub observation in a structure equivalent to:

```yaml
source: github
resource_type: pull_request
resource_id: "PR#123"
observed_at: "timestamp"

role:
  display_name: "変更担当"
  internal_source: "pull_request"

facts:
  - type: state
    value: open
  - type: review
    value: requested

interpretation:
  - "PR #123 is awaiting review."

actions:
  - "review"
  - "comment"

human_gate:
  required: true
  reason: "Review and merge decisions belong to the human."
```

This record is a context handoff unit, not an authorization to act.

## 9. Evidence Boundary

The bridge MUST NOT silently convert:

- translation into fact;
- interpretation into fact;
- suggestion into authorization;
- AI output into repository state;
- repository state into human approval.

The distinction between observation and interpretation is part of the protocol.

## 10. Human Gate

The bridge may explain what GitHub can do.

It does not decide what the human should do.

```text
GitHub state
    ↓
github-context-bridge observation
    ↓
Role-based Japanese context
    ↓
担当者間会議（保守安価）
    ↓
Human judgment
    ↓
Optional GitHub operation
```

## 11. Verification

A prototype should be tested against real GitHub artifacts using a fixed set of cases:

1. repository overview;
2. issue with a clear request;
3. PR awaiting review;
4. PR with CI failure;
5. PR with changed files;
6. merge-ready PR;
7. ambiguous English wording;
8. terminology that has multiple Japanese interpretations.

For each case, the evaluator should be able to compare the original GitHub evidence with the Japanese context and identify any semantic loss or unsupported inference.

The role labels themselves should also be evaluated for comprehension by GitHub beginners.

The prototype should additionally test whether the担当者間会議（保守安価） can accurately surface agreement, disagreement, and missing evidence without creating an unsupported conclusion.

## 12. Non-goals

This protocol does not attempt to:

- replace GitHub's official UI;
- replace GitHub's own documentation;
- create a general-purpose machine translation system;
- give AI authority over repository decisions;
- conceal uncertainty behind fluent Japanese;
- duplicate the GitHub-specific runtime and adapter implementation maintained in the independent bridge repository.

## 13. Shirakami Principle

> **Do not translate only the words. Preserve the context that makes the words meaningful.**

The independent `github-context-bridge` repository is the application/adapter side; this Shirakami protocol defines the Context, Evidence, Language Protocol, Verification, and Human Gate boundary that the application implements.

GitHub Japanese Context Bridge is therefore an application test of the Shirakami proposition:

> **AI is a simulator, not an authority.**

The bridge should make GitHub easier to understand while keeping the repository, evidence, and final decision under human control.
