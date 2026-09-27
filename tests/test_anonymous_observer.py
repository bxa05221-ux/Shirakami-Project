from protocol.anonymous_observer import AnonymousObserver


def test_anonymous_observer_preserves_boundary():
    handoff = {
        "context": {"topic": "handoff"},
        "unresolved": ["open-question"],
        "evidence_ids": ["E-1"],
        "provenance": {"source": "project-a"},
    }

    result = AnonymousObserver(
        perspective="reviewer",
        observer_id="anon-1",
    ).observe(handoff)

    assert result["observation"] == handoff["context"]
    assert result["unresolved"] == handoff["unresolved"]
    assert result["human_gate_required"] is True
    assert result["decision_authority"] is False
    assert result["persistent_personality"] is False
    assert result["candidate"] is None
