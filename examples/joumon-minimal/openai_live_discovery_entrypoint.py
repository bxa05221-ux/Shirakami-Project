"""JOUMON live OpenAI entrypoint with API-visible model discovery."""

import os
import time
from typing import Any

from joumon_openai_adapter import build_openai_compatible_adapter
from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_provider_contract_poc import Context, ProtocolSpec
from joumon_live_pipeline import run_live_observation

PREFERRED_MODEL_IDS = (
    "gpt-5.6",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "gpt-5.6-luna",
    "gpt-5",
)

DISCOVERY_RETRY_DELAYS_SECONDS = (5, 15, 30)


def discover_model(client: Any) -> str:
    last_error = None
    for attempt in range(len(DISCOVERY_RETRY_DELAYS_SECONDS) + 1):
        try:
            models = client.models.list().data
            available = {model.id for model in models}
            for model_id in PREFERRED_MODEL_IDS:
                if model_id in available:
                    return model_id
            fallback = sorted(
                model_id for model_id in available if model_id.startswith("gpt-")
            )
            if fallback:
                return fallback[0]
            raise RuntimeError(
                "No GPT model is available to the supplied OpenAI API key"
            )
        except Exception as exc:
            last_error = exc
            if attempt >= len(DISCOVERY_RETRY_DELAYS_SECONDS):
                raise
            time.sleep(DISCOVERY_RETRY_DELAYS_SECONDS[attempt])
    raise RuntimeError("Model discovery failed") from last_error


def require_live_config() -> tuple[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    statement = os.environ.get("JOUMON_STATEMENT")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set; live execution is opt-in")
    if not statement:
        raise RuntimeError("JOUMON_STATEMENT is not set; provide an observation statement")
    return api_key, statement


def run_live_observation_once():
    api_key, statement = require_live_config()
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    selected_model = discover_model(client)

    def invoke(request: LiveAdapterRequest, requested_model: str) -> str:
        response = client.responses.create(model=requested_model, input=request.prompt)
        return response.output_text

    adapter = build_openai_compatible_adapter(
        model=selected_model,
        invoke=invoke,
    )
    context = Context(
        context_id=f"live:{selected_model}",
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
    return selected_model, evidence, lineage


if __name__ == "__main__":
    selected_model, evidence, lineage = run_live_observation_once()
    print({
        "selected_model": selected_model,
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
