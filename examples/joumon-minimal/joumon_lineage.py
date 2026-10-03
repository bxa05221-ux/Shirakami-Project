"""Minimal lineage graph for JOUMON Evidence."""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class LineageNode:
    node_id: str
    node_type: str

@dataclass(frozen=True)
class LineageEdge:
    source_id: str
    relation: str
    target_id: str

@dataclass(frozen=True)
class EvidenceLineage:
    evidence_id: str
    nodes: Tuple[LineageNode, ...]
    edges: Tuple[LineageEdge, ...]
    authority: str = "non-authoritative"


def build_lineage(*, context_id: str, protocol_id: str, runtime_id: str, evidence_id: str) -> EvidenceLineage:
    nodes = (
        LineageNode(context_id, "context"),
        LineageNode(protocol_id, "protocol"),
        LineageNode(runtime_id, "runtime"),
        LineageNode(evidence_id, "evidence"),
    )
    edges = (
        LineageEdge(context_id, "bound-by", protocol_id),
        LineageEdge(protocol_id, "executed-by", runtime_id),
        LineageEdge(runtime_id, "produced-observation", evidence_id),
    )
    return EvidenceLineage(evidence_id, nodes, edges)
