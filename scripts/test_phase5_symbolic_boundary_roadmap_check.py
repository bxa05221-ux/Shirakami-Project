from pathlib import Path


def test_symbolic_boundary_next_step_is_protocol_runtime():
    text = Path("docs/PHASE5_SYMBOLIC_BOUNDARY_ROADMAP.md").read_text(encoding="utf-8")
    assert "Human Gate → Protocol / Runtime" in text
