"""Opt-in live OpenAI entrypoint for the JOUMON PoC.

This module executes one authenticated observation when explicitly invoked.
No key or model response is stored in the repository.
"""
import os
from joumon_openai_adapter import build_openai_compatible_adapter
from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_provider_contract_poc import Context, ProtocolSpec
from joumon_live_pipeline import run_live_observation


def require_live_config() -> tuple[str, str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("OPENAI_MODEL")
    statement = os.environ.get("JOUMON_STATEMENT")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set; live execution is opt-in")
    if not model:
        raise RuntimeError("OPENAI_MODEL is not set; choose the model explicitly")
    if not statement:
        raise RuntimeError("JOUMON_STATEMENT is not set; provide an observation statement")
    return api_key, model, statement


def build_live_adapter():
    api_key, model, _ = require_live_config()

    def invoke(request: LiveAdapterRequest, selected_model: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=selected_model,
            input=request.prompt,
        )
        return response.output_text

    return build_openai_compatible_adapter(model=model, invoke=invoke)


def run_live_observation_once():
    _, model, statement = require_live_config()
    adapter = build_live_adapter()
    context = Context(
        context_id=f"live:{model}",
        task=statement,
        constraints=("Observation only; final decision remains human.",),
    )
    protocol = ProtocolSpec(
        protocol_id=f"protocol:{context.context_id}",
        input_context_id=context.context_id,
    )
    evidence, lineage = run_live_observation(
        context=context,
        protocol=protocol,
        runtime_id=adapter.runtime_id,
        provider=adapter.provider,
        invoke=adapter.invoke,
    )
    return evidence, lineage


if __name__ == "__main__":
    evidence, lineage = run_live_observation_once()
    print({
        "evidence_id": evidence.evidence_id,
        "context_id": evidence.context_id,
        "protocol_id": evidence.protocol_id,
        "runtime_id": evidence.runtime_id,
        "provider": evidence.provider,
        "mode": evidence.mode,
        "lineage_evidence_id": lineage.evidence_id,
        "human_final_decision_authority": evidence.final_decision_authority,
        "observed_output": evidence.observed_output,
    })
