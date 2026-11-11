"""Independent verifier boundary.

Multiple verifier results are evidence only. Agreement does not mint human
authority, and independent verifiers require distinct identities.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


class IndependentVerifierError(ValueError):
    pass


def validate_independent_verifiers(
    results: Sequence[Mapping[str, Any]],
    *,
    minimum_independent: int = 2,
) -> None:
    if minimum_independent < 2:
        raise IndependentVerifierError("minimum_independent must be >= 2")
    if len(results) < minimum_independent:
        raise IndependentVerifierError("insufficient independent verifiers")

    identities = []
    instances = []
    for result in results:
        for field in ("verification_id", "target_id", "result", "verifier", "verifier_instance"):
            if result.get(field) in (None, ""):
                raise IndependentVerifierError(f"missing verifier field: {field}")
        if result.get("human_approval") is True:
            raise IndependentVerifierError("verifier cannot create human approval")
        if result.get("runtime_authority") is True:
            raise IndependentVerifierError("verifier cannot create runtime authority")
        identities.append(result["verifier"])
        instances.append((result["verifier"], result["verifier_instance"]))

    if len(set(identities)) < minimum_independent:
        raise IndependentVerifierError("verifier identities are not independent")
    if len(set(instances)) < len(instances):
        raise IndependentVerifierError("verifier instances are duplicated")

    return
