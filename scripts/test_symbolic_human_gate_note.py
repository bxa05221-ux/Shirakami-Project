from pathlib import Path


def test_human_gate_note():
    text = Path("docs/PHASE5_SYMBOLIC_HUMAN_GATE_NOTE.md").read_text(encoding="utf-8")
    assert "Human Gate" in text
    assert "Protocol / Runtime" in text
