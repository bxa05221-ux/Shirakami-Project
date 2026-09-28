from pathlib import Path


def test_symbolic_human_gate_pr_checkpoint():
    text = Path("docs/PHASE5_SYMBOLIC_HUMAN_GATE_PR.md").read_text(encoding="utf-8")
    assert "Human Gate" in text
    assert "Protocol / Runtime" in text
