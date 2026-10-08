# Revocation × Decision × Recovery v0.1

## Threat

A verifier may have produced a valid approval before revocation. A persisted
approval must not silently resurrect authority after that verifier is revoked.

## Required bindings

Recovery requires exact equality of:
- approval_id
- context_version
- evidence_hash
- protocol_hash
- proposal_id

Both the approval and persisted record must contain these fields.

## Invariants

- a currently revoked verifier cannot resurrect persisted authority;
- missing binding fields fail closed;
- binding mutation fails closed;
- recovery requires explicit human approval;
- runtime authority cannot be restored by recovery.

## Principle

Persistence preserves state; it does not mint authority.
Revocation can invalidate present use without rewriting historical provenance.
