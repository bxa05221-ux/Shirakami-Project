from joumon_full_cycle import run_full_cycle
from joumon_live_adapter_boundary import LiveAdapterRequest


def provider_a(request: LiveAdapterRequest) -> str:
    return "A: independent observation"


def provider_b(request: LiveAdapterRequest) -> str:
    return "B: independent observation"


def provider_c(request: LiveAdapterRequest) -> str:
    return "C: independent observation"


def document():
    return {
        "matome": {
            "codename": "JOUMON",
            "version": "0.1",
            "statement": "Run a shared observation through independent runtimes.",
        },
        "purpose": {"primary": ["preserve context", "preserve evidence", "preserve lineage"]},
        "human_gate": {"input": ["Evidence", "Verification", "Lineage"]},
    }


def test_full_cycle_reaches_human_gate():
    result = run_full_cycle(document(), [
        ("runtime-a", "provider-a", provider_a),
        ("runtime-b", "provider-b", provider_b),
        ("runtime-c", "provider-c", provider_c),
    ], "proceed after human review")
    assert len(result["handoff"].evidence) == 3
    assert all(v.verified for v in result["verification"])
    assert result["human_gate"].authority == "human"
    assert result["human_gate"].decision == "proceed after human review"


def test_full_cycle_preserves_provider_provenance():
    result = run_full_cycle(document(), [
        ("runtime-a", "provider-a", provider_a),
        ("runtime-b", "provider-b", provider_b),
        ("runtime-c", "provider-c", provider_c),
    ], "hold")
    providers = tuple(e.provider for e in result["handoff"].evidence)
    assert providers == ("provider-a", "provider-b", "provider-c")
