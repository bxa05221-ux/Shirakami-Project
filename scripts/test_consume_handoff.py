from pathlib import Path

import pytest

from consume_handoff import consume


def test_ready_handoff_becomes_non_authoritative_context():
    handoff = Path(__file__).parents[1] / "handoff" / "SH-HO-20260925-001.yaml"
    context = consume(handoff)

    assert context["source_handoff_id"] == "SH-HO-20260925-001"
    assert context["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert context["authority"]["execution_authorized"] is False
    assert context["authority"]["publish_authorized"] is False
    assert context["authority"]["merge_authorized"] is False
    assert context["authority"]["human_gate_required"] is True
    assert context["next_action"].startswith("Inspect the local repository")


def test_non_consumable_status_is_rejected(tmp_path):
    source = Path(__file__).parents[1] / "handoff" / "SH-HO-20260925-001.yaml"
    text = source.read_text(encoding="utf-8").replace('status: "ready"', 'status: "draft"', 1)
    candidate = tmp_path / "draft.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError, match="not consumable"):
        consume(candidate)
