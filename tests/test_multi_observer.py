from protocol.multi_observer import ObserverPerspective, observe_from_perspectives


def test_perspectives_remain_independent_and_non_authoritative():
    handoff = {
        "context": {"topic": "thread-presenter"},
        "unresolved": ["open-question"],
    }
    perspectives = [
        ObserverPerspective("anon-a", "structure"),
        ObserverPerspective("anon-b", "counterpoint"),
        ObserverPerspective("anon-c", "unresolved"),
    ]

    results = observe_from_perspectives(handoff, perspectives)

    assert [r["observer_id"] for r in results] == ["anon-a", "anon-b", "anon-c"]
    assert [r["perspective"] for r in results] == ["structure", "counterpoint", "unresolved"]
    assert all(r["decision_authority"] is False for r in results)
    assert all(r["persistent_personality"] is False for r in results)
    assert all(r["human_gate_required"] is True for r in results)
    assert all(r["unresolved"] == handoff["unresolved"] for r in results)
