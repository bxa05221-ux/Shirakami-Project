"""Project symbolic re-observation provenance into Evidence lineage metadata.

This module intentionally does not create or validate evidence. It only
projects the causal/provenance relationship so downstream Evidence handling
can distinguish symbolic origin from observed grounding.
"""
from __future__ import annotations

from typing import Any, Mapping

from runtime.symbolic_reobservation import SymbolicReObservationRecord


def project_symbolic_provenance(
    record: SymbolicReObservationRecord,
    *,
    observation_id: str,
    evidence_id: str,
) -> Mapping[str, Any]:
    return {
        "observation_id": observation_id,
        "evidence_id": evidence_id,
        "symbolic_origin": {
            "symbol_id": record.symbol_id,
            "expression": record.expression,
            "interpretations": list(record.interpretations),
            "context_refs": list(record.context_refs),
            "reobservation_link_id": record.link_id,
            "reobservation_request_id": record.request_id,
        },
        "symbolic_is_evidence": False,
        "decision_authority": False,
        "human_gate_required": True,
    }
