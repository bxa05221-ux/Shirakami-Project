"""Resistance to verifier quorum/collusion attacks.

A quorum is an evidence aggregation mechanism only. It can never create
human approval or runtime authority.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


class VerifierCollusionError(ValueError):
    pass


def validate_verifier_quorum(
    results: Sequence[Mapping[str, Any]],
    *,
    required_passes: int,
) -> None:
    if required_passes < 1:
        raise VerifierCollusionError("required_passes must be >= 1")
    if not results:
        raise VerifierCollusionError("no verifier results")

    identities = set()
    passes = 0
    for result in results:
        for field in ("verification_id", "target_id", "result", "verifier", "verifier_instance"):
            if result.get(field) in (None, ""):
                raise VerifierCollusionError(f"missing verifier field: {field}")
        if result.get("human_approval") is True:
            raise VerifierCollusionError("verifier quorum cannot create human approval")
        if result.get("runtime_authority") is True:
            raise VerifierCollusionError("verifier quorum cannot create runtime authority")
        identities.add(result["verifier"])
        if result["result"] == "pass":
            passes += 1

    if passes < required_passes:
        raise VerifierCollusionError("quorum not satisfied")

    # Even a unanimous quorum remains evidence. The caller must still pass
    # through the independent Human Gate.
    return
