"""Provider-neutral API facade for the Semantic Handoff boundary."""
from __future__ import annotations

from typing import Any, Mapping

from .semantic_handoff import SemanticHandoffStore


class ShirakamiAPI:
    def __init__(self, traces: Mapping[str, Mapping[str, Any]]):
        self._handoffs = SemanticHandoffStore(traces)
        self._state = dict(traces.get("__shirakami_state__", {}))
        self.capabilities = {
            "semantic_handoff": True,
            "candidate_creation": True,
            "human_gate": False,
            "state_snapshot": True,
        }

    def get_state(self) -> dict[str, Any]:
        return dict(self._state)

    def get_semantic_handoff(
        self, trace_id: str, *, project: str, objective: str,
        protocol_ids: list[str] | tuple[str, ...],
        verification_scope: str, activity_id: str | None = None,
    ) -> dict[str, Any]:
        return self._handoffs.get(
            trace_id, project=project, objective=objective,
            protocol_ids=protocol_ids, verification_scope=verification_scope,
            activity_id=activity_id,
        ).to_dict()

    def get(self, path: str, **kwargs: Any) -> tuple[int, dict[str, Any]]:
        prefix = "/v1/semantic-handoff/"
        if not path.startswith(prefix) or not path[len(prefix):]:
            return 404, {"error": "not_found"}
        trace_id = path[len(prefix):]
        try:
            return 200, self.get_semantic_handoff(trace_id, **kwargs)
        except KeyError:
            return 404, {"error": "trace_not_found", "trace_id": trace_id}

    def create_candidate(
        self, handoff_document: Mapping[str, Any], *,
        candidate_id: str, proposal: Mapping[str, Any],
        validation: Mapping[str, Any],
    ) -> dict[str, Any]:
        from scripts.build_candidate import build_candidate
        return build_candidate(
            dict(handoff_document), candidate_id,
            dict(proposal), dict(validation),
        )
