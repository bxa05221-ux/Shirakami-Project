"""Verifier trust-root boundary.

A verifier may be cryptographically authentic yet still be untrusted.
This layer separates signature validity from trust authorization.
"""
from __future__ import annotations

from typing import Any, Mapping

from runtime.verifier_authenticity import (
    sign_verification,
    VerifierAuthenticityError,
)


class TrustRootError(ValueError):
    pass


def validate_trusted_verifier(
    record: Mapping[str, Any],
    signature: str,
    secret: bytes,
    trusted_verifiers: set[str],
) -> None:
    verifier = record.get("verifier")
    if verifier in (None, ""):
        raise TrustRootError("missing verifier identity")

    if verifier not in trusted_verifiers:
        raise TrustRootError("verifier is not trusted")

    try:
        expected = sign_verification(record, secret)
    except Exception as exc:
        raise TrustRootError("cannot authenticate verifier record") from exc

    if not __import__("hmac").compare_digest(expected, signature):
        raise TrustRootError("untrusted or invalid verifier signature")

    if record.get("human_approval") is True:
        raise TrustRootError("trust root cannot create human approval")

    if record.get("runtime_authority") is True:
        raise TrustRootError("trust root cannot create runtime authority")
