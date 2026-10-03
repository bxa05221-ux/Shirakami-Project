"""Opt-in live Fugu runtime for the JOUMON comparison harness.

No provider credential is stored here. The caller supplies SAKANA_API_KEY and
a statement/model through environment variables.
"""
import os

from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_live_runtime_comparison import (
    compare_live_runtimes,
    validate_boundary_invariants,
)
from joumon_provider_contract_poc import Context, ProtocolSpec


def require_config() -> tuple[str, str, str]:
    api_key = os.environ.get("SAKANA_API_KEY")
    model = os.environ.get("FUGU_MODEL", "fugu")
    statement = os.environ.get("JOUMON_STATEMENT")
    if not api_key:
        raise RuntimeError("SAKANA_API_KEY is not set; live execution is opt-in")
    if not statement:
        raise RuntimeError("JOUMON_STATEMENT is not set")
    return api_key, model, statement


def run_fugu_comparison():
    api_key, model, statement = require_config()

    # Keep the provider SDK outside the deterministic protocol/test dependency
    # surface. The live entrypoint imports it only when a live run is requested.
    from openai import OpenAI

    client = OpenAI(base_url="https://api.sakana.ai/v1", api_key=api_key)
    context = Context(
        context_id="live-comparison-001",
        task=statement,
        constraints=("Observation only; final decision remains human.",),
    )
    protocol = ProtocolSpec(
        protocol_id="live-comparison-protocol-001",
        input_context_id=context.context_id,
    )

    def invoke(request: LiveAdapterRequest) -> str:
        response = client.responses.create(
            model=model,
            input=request.prompt,
            timeout=120.0,
        )
        return response.output_text

    comparison = compare_live_runtimes(
        context=context,
        protocol=protocol,
        runtimes=(("runtime-sakana-fugu", "sakana-ai", invoke),),
    )
    validate_boundary_invariants(comparison)
    return comparison


if __name__ == "__main__":
    comparison = run_fugu_comparison()
    for observation in comparison.observations:
        evidence = observation.evidence
        print(
            {
                "evidence_id": evidence.evidence_id,
                "context_id": evidence.context_id,
                "protocol_id": evidence.protocol_id,
                "runtime_id": evidence.runtime_id,
                "provider": evidence.provider,
                "mode": evidence.mode,
                "evidence_authority": evidence.evidence_authority,
                "final_decision_authority": evidence.final_decision_authority,
                "lineage_evidence_id": observation.lineage.evidence_id,
                "observed_output": evidence.observed_output,
            }
        )
