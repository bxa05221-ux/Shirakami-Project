#!/usr/bin/env python3
"""Execute a RuntimeRequest through a provider-neutral adapter and validate the return path."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

from provider_adapter import ProviderAdapter, RuntimeRequest


class FixtureProvider(ProviderAdapter):
    """Deterministic provider used for boundary verification; replaceable in production."""

    @property
    def provider_name(self) -> str:
        return "fixture"

    def __init__(self, output: object):
        self._output = output

    def execute(self, request: RuntimeRequest):
        from provider_adapter import RuntimeResult
        result = RuntimeResult(
            handoff_id=request.handoff_id,
            trace_id=request.trace_id,
            execution_id=request.execution_id,
            provider=self.provider_name,
            output=self._output,
            evidence_ids=request.evidence_ids,
        )
        self.validate_result(result)
        return result


def execute(document: dict, output: object = None) -> dict:
    request = document.get("runtime_request")
    if not isinstance(request, dict):
        raise ValueError("missing runtime_request")
    if not request.get("request_id"):
        raise ValueError("request_id is required")
    evidence_ids = request.get("evidence_ids") or []
    if not evidence_ids:
        raise ValueError("evidence_ids are required")
    provider = FixtureProvider(output if output is not None else {"status": "fixture"})
    runtime_request = RuntimeRequest(
        handoff_id=request.get("request_id"),
        trace_id=request.get("trace_id"),
        execution_id=request.get("execution_id"),
        project=request.get("project", "shirakami"),
        objective=request.get("objective", "execute approved protocol proposal"),
        protocol_ids=tuple(request.get("protocol_ids", [])),
        evidence_ids=tuple(evidence_ids),
        verification_scope=request.get("verification_scope", "boundary"),
        input_data=request.get("proposal", {}),
        runtime_target=request.get("runtime_target"),
    )
    result = provider.execute(runtime_request)
    return {"runtime_result": {
        "handoff_id": result.handoff_id,
        "trace_id": result.trace_id,
        "execution_id": result.execution_id,
        "provider": result.provider,
        "output": result.output,
        "evidence_ids": list(result.evidence_ids),
        "authority": {
            "execution_authorized": result.execution_authorized,
            "publish_authorized": result.publish_authorized,
            "merge_authorized": result.merge_authorized,
            "human_gate_required": result.human_gate_required,
        },
    }}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    document = yaml.safe_load(args.request.read_text(encoding="utf-8"))
    result = execute(document or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Runtime result recorded: {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
