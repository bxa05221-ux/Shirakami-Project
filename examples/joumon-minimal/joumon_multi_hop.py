"""Three-stage JOUMON chain using serialized semantic handoffs."""
from joumon_roundtrip_runtime import ConsumerRuntime
from joumon_provider_contract_poc import Context, ProtocolSpec
from joumon_evidence_adapter import to_evidence
from joumon_lineage import build_lineage
from joumon_semantic_handoff import create_handoff
from joumon_matome_yaml import handoff_to_matome_yaml, validate_matome_document
from joumon_handoff_import import matome_to_handoff


def run_multi_hop():
    context = Context("joumon-multihop-001", "Process the same task through independent runtimes.", ("Human gate remains final.",))
    protocol = ProtocolSpec("joumon-multihop-protocol-001", context.context_id)
    current = None
    stages = []
    for index, provider in enumerate(("provider-a", "provider-b", "provider-c"), start=1):
        runtime = ConsumerRuntime(f"runtime-{index}", provider)
        if current is None:
            result = runtime.execute_handoff(type("Initial", (), {"context_id": context.context_id, "protocol_id": protocol.protocol_id, "evidence": ()})())
        else:
            result = runtime.execute_handoff(current)
        evidence = to_evidence(context.context_id, protocol.protocol_id, result.runtime_id, result.output, result.metadata)
        lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=evidence.runtime_id, evidence_id=evidence.evidence_id)
        current = create_handoff(handoff_id=f"multihop-{index}", context_id=context.context_id, protocol_id=protocol.protocol_id, evidence=((current.evidence if current else ()) + (evidence,)), lineage=((current.lineage if current else ()) + (lineage,)))
        current = matome_to_handoff(validate_matome_document(handoff_to_matome_yaml(current)))
        stages.append((runtime.runtime_id, provider, current))
    return context, protocol, stages
