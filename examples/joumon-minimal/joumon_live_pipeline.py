"""Provider-neutral live pipeline harness.

The harness deliberately knows nothing about a provider SDK. A caller injects
an adapter callable and receives the same Evidence boundary used by mocks.
"""
from typing import Callable, Tuple
from joumon_provider_contract_poc import Context, ProtocolSpec
from joumon_live_adapter_boundary import LiveAdapterRequest, LiveRuntimeAdapter
from joumon_evidence_adapter import UnifiedEvidence, to_evidence
from joumon_lineage import EvidenceLineage, build_lineage


def run_live_observation(*, context: Context, protocol: ProtocolSpec, runtime_id: str,
                         provider: str, invoke: Callable[[LiveAdapterRequest], str]) -> Tuple[UnifiedEvidence, EvidenceLineage]:
    adapter = LiveRuntimeAdapter(runtime_id, provider, invoke)
    result = adapter.execute(context, protocol)
    evidence = to_evidence(context.context_id, protocol.protocol_id, result.runtime_id, result.output, result.metadata)
    lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id,
                            runtime_id=evidence.runtime_id, evidence_id=evidence.evidence_id)
    return evidence, lineage
