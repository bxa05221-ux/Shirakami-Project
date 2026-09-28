from pathlib import Path


def test_symbolic_human_gate_summary():
    text = Path("docs/PHASE5_SYMBOLIC_HUMAN_GATE_SUMMARY.md").read_text(encoding="utf-8")
    assert "Human Gate" in text
    assert "Protocol / Runtime" in text
