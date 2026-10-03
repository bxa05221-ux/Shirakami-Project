"""Provider-neutral live runtime comparison harness for JOUMON.

The harness holds Context and Protocol constant while executing the same
observation through injected runtime adapters. It compares boundary metadata
and lineage, not model quality.
"""
from dataclasses import dataclass
from typing import Callable

from joumon_evidence_adapter import UnifiedEvidence
from joumon_lineage import EvidenceLineage
from joumon_provider_contract_poc import Context, ProtocolSpec
from joumon_live_pipeline import run_live_observation


@dataclass(frozen=True)
class RuntimeObservation:
    evidence: UnifiedEvidence
    lineage: EvidenceLineage


@dataclass(frozen=True)
class RuntimeComparison:
    context_id: str
    protocol_id: str
    observations: tuple[RuntimeObservation, ...]


def compare_live_runtimes(
    *,
    context: Context,
    protocol: ProtocolSpec,
    runtimes: tuple[tuple[str, str, Callable], ...],
) -> RuntimeComparison:
    """Run one fixed Context/Protocol through injected runtime callables.

    Each tuple is (runtime_id, provider, invoke). Authentication, SDKs, and
    network access remain outside this harness.
    """
    observations = []
    for runtime_id, provider, invoke in runtimes:
        evidence, lineage = run_live_observation(
            context=context,
            protocol=protocol,
            runtime_id=runtime_id,
            provider=provider,
            invoke=invoke,
        )
        observations.append(RuntimeObservation(evidence=evidence, lineage=lineage))

    return RuntimeComparison(
        context_id=context.context_id,
        protocol_id=protocol.protocol_id,
        observations=tuple(observations),
    )


def validate_boundary_invariants(comparison: RuntimeComparison) -> None:
    """Raise AssertionError if the declared JOUMON boundary changed."""
    if not comparison.observations:
        raise AssertionError("at least one runtime observation is required")

    for observation in comparison.observations:
        evidence = observation.evidence
        lineage = observation.lineage
        assert evidence.context_id == comparison.context_id
        assert evidence.protocol_id == comparison.protocol_id
        assert evidence.final_decision_authority == "human"
        assert evidence.evidence_authority == "non-authoritative"
        assert lineage.context_id == comparison.context_id
        assert lineage.protocol_id == comparison.protocol_id
        assert lineage.evidence_id == evidence.evidence_id
