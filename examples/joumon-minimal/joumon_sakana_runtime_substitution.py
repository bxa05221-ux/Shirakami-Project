"""Deterministic JOUMON runtime substitution experiment.

The same Context and Protocol are executed through two different runtime
adapters. The experiment checks that the semantic/authority boundary remains
constant while runtime provenance and output may change.
"""

from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_sakana_adapter import build_sakana_fugu_adapter
from joumon_live_pipeline import run_live_observation
from joumon_provider_contract_poc import Context, ProtocolSpec


def fugu_runtime(request: LiveAdapterRequest, model: str) -> str:
    return f"{model}: candidate from a multi-agent runtime"


def alternate_runtime(request: LiveAdapterRequest) -> str:
    return "alternate-runtime: independent candidate"


def run_substitution_experiment():
    context = Context(
        context_id="joumon-substitution-001",
        task="Produce one candidate observation.",
        constraints=("Candidate output requires human review.",),
    )
    protocol = ProtocolSpec(
        protocol_id="joumon-substitution-protocol-001",
        input_context_id=context.context_id,
    )

    fugu_evidence, fugu_lineage = run_live_observation(
        context=context,
        protocol=protocol,
        runtime_id="runtime-sakana-fugu",
        provider="sakana-ai",
        invoke=lambda request: fugu_runtime(request, "fugu"),
    )

    alternate_evidence, alternate_lineage = run_live_observation(
        context=context,
        protocol=protocol,
        runtime_id="runtime-alternate",
        provider="alternate-provider",
        invoke=alternate_runtime,
    )

    return context, protocol, (
        (fugu_evidence, fugu_lineage),
        (alternate_evidence, alternate_lineage),
    )
