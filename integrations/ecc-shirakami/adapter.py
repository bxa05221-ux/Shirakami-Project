"""Minimal Shirakami boundary adapter for an ECC-style runtime.

This module deliberately does not embed ECC.  It converts a Shirakami task
context into a runtime-neutral request, records the runtime result as
observation/evidence, and blocks consequential completion until a human gate
is explicitly passed.

The adapter is intentionally stdlib-only so the boundary can be exercised in
a private repository before selecting a concrete ECC installation method.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
import uuid


@dataclass(frozen=True)
class ShirakamiContext:
    task: str
    context: Mapping[str, Any]
    protocol: str
    evidence_requirements: list[str] = field(default_factory=list)
    human_constraints: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RuntimeRequest:
    request_id: str
    runtime: str
    authority: str
    task: str
    context: Mapping[str, Any]
    protocol: str
    evidence_requirements: list[str]
    human_constraints: list[str]


@dataclass
class RuntimeObservation:
    request_id: str
    runtime: str
    started_at: str
    finished_at: str
    status: str
    observation: Any
    artifacts: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    verification_status: str = "unverified"


@dataclass
class HumanGate:
    required: bool = True
    approved: bool = False
    decided_by: str | None = None
    decision_note: str | None = None


class ECCShirakamiAdapter:
    """Boundary object between Shirakami and an ECC runtime."""

    runtime_name = "ECC"
    runtime_authority = "none"

    def prepare(self, ctx: ShirakamiContext) -> RuntimeRequest:
        if not ctx.task.strip():
            raise ValueError("task must not be empty")
        if not ctx.protocol.strip():
            raise ValueError("protocol must not be empty")
        if not ctx.evidence_requirements:
            raise ValueError("at least one evidence requirement is required")

        return RuntimeRequest(
            request_id=f"SH-ECC-{uuid.uuid4().hex[:12]}",
            runtime=self.runtime_name,
            authority=self.runtime_authority,
            task=ctx.task,
            context=dict(ctx.context),
            protocol=ctx.protocol,
            evidence_requirements=list(ctx.evidence_requirements),
            human_constraints=list(ctx.human_constraints),
        )

    def observe(
        self,
        request: RuntimeRequest,
        result: Any,
        *,
        status: str = "completed",
        artifacts: list[str] | None = None,
        uncertainties: list[str] | None = None,
        verification_status: str = "unverified",
        started_at: str | None = None,
        finished_at: str | None = None,
    ) -> RuntimeObservation:
        now = datetime.now(timezone.utc).isoformat()
        return RuntimeObservation(
            request_id=request.request_id,
            runtime=request.runtime,
            started_at=started_at or now,
            finished_at=finished_at or now,
            status=status,
            observation=result,
            artifacts=artifacts or [],
            uncertainties=uncertainties or ["Runtime output has not been independently verified."],
            verification_status=verification_status,
        )

    def gate(self, observation: RuntimeObservation, gate: HumanGate) -> dict[str, Any]:
        """Return a decision envelope; never silently grant consequential authority."""
        if gate.required and not gate.approved:
            return {
                "request_id": observation.request_id,
                "status": "awaiting_human_gate",
                "runtime": observation.runtime,
                "verification_status": observation.verification_status,
                "authority": "human",
                "decision": None,
            }

        return {
            "request_id": observation.request_id,
            "status": "human_approved",
            "runtime": observation.runtime,
            "verification_status": observation.verification_status,
            "authority": "human",
            "decision": gate.decision_note,
            "decided_by": gate.decided_by,
        }

    @staticmethod
    def envelope(
        request: RuntimeRequest,
        observation: RuntimeObservation,
        gate_result: Mapping[str, Any],
    ) -> dict[str, Any]:
        return {
            "request": asdict(request),
            "observation": asdict(observation),
            "human_gate": dict(gate_result),
            "provenance": {
                "adapter": "ecc-shirakami-adapter",
                "runtime": request.runtime,
                "authority": "none",
            },
        }


if __name__ == "__main__":
    # Deterministic local smoke demonstration.  No model or ECC installation
    # is required: the result is explicitly marked as an observation.
    adapter = ECCShirakamiAdapter()
    request = adapter.prepare(
        ShirakamiContext(
            task="inspect the repository change",
            context={"source": "local-smoke-test"},
            protocol="reviewer-protocol-v0.1",
            evidence_requirements=["execution_trace", "verification_status"],
        )
    )
    observation = adapter.observe(
        request,
        {"message": "ECC runtime result placeholder"},
    )
    print(adapter.envelope(request, observation, adapter.gate(observation, HumanGate())))
