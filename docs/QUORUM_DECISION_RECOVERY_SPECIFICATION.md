# Quorum × Decision × Recovery Boundary v0.1

## Objective

Prevent a verifier quorum from manufacturing decision authority or resurrecting execution authority during persistence recovery.

## Required invariant

Verifier agreement is evidence. Human approval is authority. These are separate objects and must remain separate across recovery.

Recovery is permitted only when the persisted state already contains an independently established human approval and all decision bindings match exactly.

## Attack cases

- unanimous malicious PASS;
- quorum member claiming human approval;
- quorum member claiming runtime authority;
- evidence/context/protocol/proposal binding mutation;
- missing persisted human approval;
- revoked verifier participating in recovery.

All attacks must fail closed.

`verifier quorum -> evidence -> Human Gate -> bound decision -> recovery`

must never collapse into:

`verifier quorum -> execution`.
