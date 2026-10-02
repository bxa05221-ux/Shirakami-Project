"""Run the JOUMON PoC starting from a Matome-shaped mapping."""
from typing import Any, Mapping
from joumon_matome_loader import load_matome_mapping
from joumon_live_pipeline import run_live_observation
from joumon_provider_contract_poc import Context, ProtocolSpec


def run_from_matome(document: Mapping[str, Any], providers):
    context, protocol = load_matome_mapping(document)
    observations = []
    for runtime_id, provider_name, invoke in providers:
        evidence, lineage = run_live_observation(
            context=context,
            protocol=protocol,
            runtime_id=runtime_id,
            provider=provider_name,
            invoke=invoke,
        )
        observations.append((evidence, lineage))
    return context, protocol, tuple(observations)
