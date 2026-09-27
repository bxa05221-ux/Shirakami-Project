from protocol.thread_presenter import present_observation_set


def test_thread_presenter_does_not_collapse_perspectives():
    source = {
        "observations": [
            {"observer_id": "a", "perspective": "structure", "observation": "x"},
            {"observer_id": "b", "perspective": "counterpoint", "observation": "y"},
        ],
        "agreement": [],
        "differences": [
            {"observer_id": "a", "perspective": "structure", "observation": "x"},
            {"observer_id": "b", "perspective": "counterpoint", "observation": "y"},
        ],
    }

    result = present_observation_set(source)

    assert len(result["entries"]) == 2
    assert result["entries"][0]["perspective"] == "structure"
    assert result["entries"][1]["perspective"] == "counterpoint"
    assert result["differences"] == source["differences"]
    assert result["decision_authority"] is False
    assert result["human_gate_required"] is True
