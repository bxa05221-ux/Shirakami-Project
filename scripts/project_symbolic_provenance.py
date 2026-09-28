"""Attach symbolic provenance to an existing Evidence/AIwitness record.

This module deliberately does not create or alter an Evidence ID. Symbolic
interpretation explains the path to re-observation; it is not itself evidence.
"""
from __future__ import annotations

from typing import Any, Mapping


def project_symbolic_provenance(
    witness: Mapping[str, Any],
    symbolic_record: Mapping[str, Any],
) -> dict:
    result = dict(witness)
    aiwitness = dict(result.get("aiwitness") or {})
    provenance = dict(aiwitness.get("provenance") or {})
    evidence_ids = list(provenance.get("evidence_ids") or [])

    if "evidence_ids" not in provenance or not evidence_ids:
        raise ValueError("AIwitness evidence_ids are required")
    if symbolic_record.get("evidence_id") is not None:
        raise ValueError("symbolic record must not carry an evidence_id")

    symbolic = {
        "symbol_id": symbolic_record["symbol_id"],
        "expression": symbolic_record["expression"],
        "interpretations": list(symbolic_record.get("interpretations", [])),
        "context_refs": list(symbolic_record.get("context_refs", [])),
        "reobservation": {
            "link_id": symbolic_record["link_id"],
            "request_id": symbolic_record["request_id"],
            "source_observation_id": symbolic_record["source_observation_id"],
            "result_observation_id": symbolic_record["result_observation_id"],
        },
    }

    observation = dict(aiwitness.get("observation") or {})
    observed = dict(observation.get("verification_observed") or {})
    observed["symbolic_provenance"] = symbolic
    observation["verification_observed"] = observed

    aiwitness["provenance"] = provenance
    aiwitness["observation"] = observation
    result["aiwitness"] = aiwitness
    return result
