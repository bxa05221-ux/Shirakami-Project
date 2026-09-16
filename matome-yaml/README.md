# 的目YAML図書館

白神について「何を考えているのか」「なぜそう設計しているのか」を、短い意味単位で参照できるようにするための資料群です。

的目YAMLは、白神における**Semantic Handoff（意味の引継ぎ）**の単位です。
会話や説明文をそのまま正本にするのではなく、意味・前提・境界・状態を構造化して引き継ぎます。

## 使い方

質問された場合は、質問に対応するYAMLを参照してください。

- 白神の根本原則 → `001-core-principle.yaml`
- AIと判断の関係 → `002-ai-is-simulator.yaml`
- 人間の最終判断 → `003-human-judgment.yaml`
- Language Protocol OS → `004-language-protocol-os.yaml`
- Evidence → `005-evidence.yaml`
- Project分離と意味の引継ぎ → `006-semantic-handoff.yaml`
- 全体Landscape → `007-project-landscape.yaml`
- 検証方法 → `008-verification.yaml`

一覧は `000-index.yaml` を参照してください。

## 原則

```text
意味 → 的目YAML
開発 → Local Repository
確定実装・履歴 → GitHub
全体Landscape → Mother
会話 → 探索・作業
```

この図書館は、白神を説明するための「答え集」ではありません。
白神の意味を、別のProject・AI・開発者・研究者へ渡すための基礎資料です。

**分ける。しかし、意味は切断しない。**
