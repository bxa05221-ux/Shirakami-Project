"""Read-only Japanese Context Bridge runtime primitive."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class JapaneseContext:
    resource_type: str
    resource_id: str
    role: str
    facts: List[str] = field(default_factory=list)
    interpretation: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    human_gate: bool = True


def build_pull_request_context(pr_number, state, draft, changed_files, additions, deletions, head_sha, ci_status="UNKNOWN"):
    facts = [
        f"PR #{pr_number} は {state} 状態です。",
        f"Draft: {'はい' if draft else 'いいえ'}。",
        f"変更ファイル数: {changed_files}。",
        f"追加: {additions} 行、削除: {deletions} 行。",
        f"HEADコミット: {head_sha}。",
    ]
    unknowns = []
    if ci_status == "UNKNOWN":
        unknowns.append("このコミットについて、CI/statusの結果は確認できていません。")
    else:
        facts.append(f"CI/status: {ci_status}。")
    return JapaneseContext(
        resource_type="pull_request",
        resource_id=f"PR#{pr_number}",
        role="変更担当",
        facts=facts,
        interpretation=["このContextはPRの観測結果を整理したもので、マージ判断そのものではありません。"],
        unknowns=unknowns,
        actions=["レビュー", "コメント", "状態確認"],
        human_gate=True,
    )


def render_japanese_context(context):
    sections = [
        ("観測された事実", context.facts),
        ("解釈", context.interpretation),
        ("未確認事項（UNKNOWN）", context.unknowns),
        ("可能な操作", context.actions),
    ]
    lines = [f"## {context.role} — {context.resource_id}"]
    for title, items in sections:
        lines.append(f"\n### {title}")
        lines.extend(f"- {item}" for item in items) if items else lines.append("- なし")
    lines.append("\n### Human Gate")
    lines.append("- 最終判断・承認は人間に残します。")
    return "\n".join(lines)
