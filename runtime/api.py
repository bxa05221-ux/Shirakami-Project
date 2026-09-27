"""Provider-neutral API facade for the Semantic Handoff boundary."""
from __future__ import annotations

from typing import Any, Mapping

from .semantic_handoff import SemanticHandoffStore


class ShirakamiAPI:
    def __init__(self, traces: Mapping[str, Mapping[str, Any]]):
        self._handoffs = SemanticHandoffStore(traces)
        self.capabilities = {"semantic_handoff": True}

    def get_semantic_handoff(
        self,
        trace_id: str,
        *,
        project: str,
        objective: str,
        protocol_ids: list[str] | tuple[str, ...],
        verification_scope: str,
        activity_id: str | None = None,
    ) -> dict[str, Any]:
        """Return a lineage envelope; no authority is created by retrieval."""
        return self._handoffs.get(
            trace_id,
            project=project,
            objective=objective,
            protocol_ids=protocol_ids,
            verification_scope=verification_scope,
            activity_id=activity_id,
        ).to_dict()

    def get(self, path: str, **kwargs: Any) -> tuple[int, dict[str, Any]]:
        """Minimal HTTP-shaped boundary for GET /v1/semantic-handoff/{trace_id}."""
        prefix = "/v1/semantic-handoff/"
        if not path.startswith(prefix) or not path[len(prefix):]:
            return 404, {"error": "not_found"}
        trace_id = path[len(prefix):]
        try:
            return 200, self.get_semantic_handoff(trace_id, **kwargs)
        except KeyError:
            return 404, {"error": "trace_not_found", "trace_id": trace_id}
