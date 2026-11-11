# Trust Root Governance v0.1

The trust list is itself a security boundary.

## Invariants

1. An unauthorized trust-list mutation fails closed.
2. A revoked verifier cannot be newly trusted.
3. Revocation overrides trust.
4. Unknown verifiers remain untrusted.
5. Invalid identities fail closed.

## Scope

This module models the governance boundary only. It does not define the human authorization mechanism used to approve a trust-root change.

## Security principle

Changing who is trusted must not be an implicit side effect of verification, runtime execution, recovery, or AI output.
