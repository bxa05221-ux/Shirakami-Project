# Trust Root Temporal Boundary v0.1

## Threat

A verifier can be trusted at one point in time and revoked later. A stale
verification record may then be replayed after revocation.

## Boundary

Trust evaluation is bound to event time, while current revocation state can
also reject replay into the present.

## Invariants

- unknown verifier fails closed;
- revoked verifier fails closed;
- invalid timestamps fail closed;
- a revoked verifier's stale result cannot be replayed as current authority;
- revocation does not silently rewrite historical provenance.

## Security principle

Historical evidence and current authority are distinct states. A historical
verification record must not silently become a current authorization.
