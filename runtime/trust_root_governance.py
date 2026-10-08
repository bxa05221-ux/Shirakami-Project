"""Fail-closed governance for verifier trust roots."""
from __future__ import annotations

from typing import FrozenSet


class TrustRootGovernanceError(ValueError):
    pass


def validate_trust_root_transition(
    current: FrozenSet[str],
    proposed: FrozenSet[str],
    *,
    change_authorized: bool,
    revoked: FrozenSet[str] = frozenset(),
) -> FrozenSet[str]:
    if not change_authorized:
        raise TrustRootGovernanceError("trust-root change lacks authorization")

    if revoked & proposed:
        raise TrustRootGovernanceError("revoked verifier cannot be trusted")

    if any(not isinstance(v, str) or not v for v in proposed):
        raise TrustRootGovernanceError("invalid verifier identity")

    return frozenset(proposed)


def verifier_is_trusted(
    verifier: str,
    trusted: FrozenSet[str],
    revoked: FrozenSet[str] = frozenset(),
) -> bool:
    return verifier in trusted and verifier not in revoked
