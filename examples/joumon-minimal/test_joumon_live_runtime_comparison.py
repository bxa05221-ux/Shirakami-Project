from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_live_runtime_comparison import compare_live_runtimes, validate_boundary_invariants
from joumon_provider_contract_poc import Context, ProtocolSpec


def test_live_runtime_comparison_keeps_context_and_protocol_constant():
    context = Context(
        context_id="comparison-001",
        task="Produce one candidate observation.",
        constraints=("Human review required.",),
    )
    protocol = ProtocolSpec(
        protocol_id="comparison-protocol-001",
        input_context_id=context.context_id,
    )

    def runtime_a(request: LiveAdapterRequest) -> str:
        return "runtime-a candidate"

    def runtime_b(request: LiveAdapterRequest) -> str:
        return "runtime-b candidate"

    comparison = compare_live_runtimes(
        context=context,
        protocol=protocol,
        runtimes=(
            ("runtime-a", "provider-a", runtime_a),
            ("runtime-b", "provider-b", runtime_b),
        ),
    )
    validate_boundary_invariants(comparison)

    assert len(comparison.observations) == 2
    first, second = comparison.observations
    assert first.evidence.runtime_id != second.evidence.runtime_id
    assert first.evidence.provider != second.evidence.provider
    assert first.evidence.observed_output != second.evidence.observed_output
