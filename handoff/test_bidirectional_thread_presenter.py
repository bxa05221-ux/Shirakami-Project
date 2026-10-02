from pathlib import Path


def load_fixture():
    text = Path("handoff/bidirectional_thread_presenter_fixture.yaml").read_text()
    return text


def test_bidirectional_handoff_preserves_boundaries():
    text = load_fixture()
    required = [
        "context:",
        "evidence:",
        "provenance:",
        "unresolved:",
        "human_gate:",
        "authority_transfer: false",
        "human_gate_required: true",
        "direction: \"project-b-to-project-a\"",
    ]
    for marker in required:
        assert marker in text


def test_thread_presenter_is_not_decision_authority():
    text = load_fixture()
    assert "authority_transferred: false" in text
    assert "decision authority" not in text.lower()
