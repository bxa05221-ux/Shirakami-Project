from pathlib import Path


def test_phase5_roadmap_keeps_runtime_after_human_gate():
    text = Path("docs/PHASE5_SYMBOLIC_BOUNDARY_ROADMAP.md").read_text(encoding="utf-8")
    assert "Human Gate → Protocol / Runtime" in text
    assert text.index("Human Gate → Protocol / Runtime") < len(text)
