from pathlib import Path


def test_symbolic_human_gate_final():
    text = Path("docs/PHASE5_SYMBOLIC_HUMAN_GATE_FINAL.md").read_text(encoding="utf-8")
    assert "non-authoritative" in text
    assert "Human Gate → Protocol / Runtime" in text
