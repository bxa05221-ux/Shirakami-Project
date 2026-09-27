"""Provider-neutral Protocol Registry and Semantic Integrity verification.

This boundary verifies protocol identity and provenance without granting authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class SemanticIntegrityResult:
    status: str
    protocol_id: str
    resolved_version: str | None = None
    reason: str | None = None
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True

    def __post_init__(self) -> None:
        if self.status not in {
            "resolved",
            "unresolved",
            "ambiguous",
            "incomplete",
            "unverified",
            "mismatch",
        }:
            raise ValueError("invalid semantic integrity status")
        if not self.protocol_id:
            raise ValueError("protocol_id is required")
        if self.execution_authorized is not False:
            raise ValueError("execution_authorized must remain false")
        if self.publish_authorized is not False:
            raise ValueError("publish_authorized must remain false")
        if self.merge_authorized is not False:
            raise ValueError("merge_authorized must remain false")
        if self.human_gate_required is not True:
            raise ValueError("human_gate_required must remain true")


class ProtocolRegistry:
    """Read-only registry used to resolve Protocol IDs."""

    def __init__(self, protocols: Mapping[str, Any]):
        self._protocols = protocols

    def resolve(self, protocol_id: str) -> list[Mapping[str, Any]]:
        if not protocol_id:
            raise ValueError("protocol_id is required")
        value = self._protocols.get(protocol_id)
        if value is None:
            return []
        if isinstance(value, Mapping):
            return [value]
        if isinstance(value, (list, tuple)):
            return [item for item in value if isinstance(item, Mapping)]
        raise ValueError("protocol registry entry must be a mapping or sequence")


def verify_protocol_reference(
    registry: ProtocolRegistry,
    *,
    protocol_id: str,
    handoff_protocol_id: str,
) -> SemanticIntegrityResult:
    """Verify identity and provenance without selecting or approving a protocol."""
    if protocol_id != handoff_protocol_id:
        return SemanticIntegrityResult(status="mismatch", protocol_id=protocol_id, reason="protocol_id does not match handoff protocol_id")
    matches = registry.resolve(protocol_id)
    if not matches:
        return SemanticIntegrityResult(status="unresolved", protocol_id=protocol_id, reason="protocol_id was not found")
    if len(matches) != 1:
        return SemanticIntegrityResult(status="ambiguous", protocol_id=protocol_id, reason="protocol_id resolves to multiple definitions")
    protocol = matches[0]
    if not protocol.get("protocol_id") or protocol.get("protocol_id") != protocol_id:
        return SemanticIntegrityResult(status="mismatch", protocol_id=protocol_id, reason="resolved definition has inconsistent protocol_id")
    if not protocol.get("version"):
        return SemanticIntegrityResult(status="incomplete", protocol_id=protocol_id, reason="protocol version is missing")
    if not protocol.get("source_candidate_id") or not protocol.get("evidence_ids"):
        return SemanticIntegrityResult(status="incomplete", protocol_id=protocol_id, reason="protocol lineage is incomplete")
    approval = protocol.get("approval")
    if not isinstance(approval, Mapping):
        return SemanticIntegrityResult(status="unverified", protocol_id=protocol_id, resolved_version=str(protocol["version"]), reason="human_gate approval provenance is missing")
    if approval.get("source") != "human_gate" or approval.get("approved") is not True:
        return SemanticIntegrityResult(status="unverified", protocol_id=protocol_id, resolved_version=str(protocol["version"]), reason="human_gate approval provenance is invalid")
    authority = protocol.get("authority")
    if not isinstance(authority, Mapping):
        return SemanticIntegrityResult(status="unverified", protocol_id=protocol_id, resolved_version=str(protocol["version"]), reason="authority envelope is missing")
    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(key) is not False:
            return SemanticIntegrityResult(status="unverified", protocol_id=protocol_id, resolved_version=str(protocol["version"]), reason=f"{key} must remain false")
    if authority.get("human_gate_required") is not True:
        return SemanticIntegrityResult(status="unverified", protocol_id=protocol_id, resolved_version=str(protocol["version"]), reason="human_gate_required must remain true")
    return SemanticIntegrityResult(status="resolved", protocol_id=protocol_id, resolved_version=str(protocol["version"]))
