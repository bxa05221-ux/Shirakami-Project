# JOUMON Evidence Verification Specification v0.1

status: experimental
purpose: Verify provenance and authority invariants of Evidence without turning verification into decision authority.

## Verification boundary

Evidence -> Verification -> Human Gate

Verification checks structural facts such as Context identity, Protocol identity, declared execution mode, Runtime provenance, non-authoritative Evidence, and human final authority.

## Important distinction

A verified Evidence record means only that the declared checks passed. It does not mean:

- the model output is correct;
- one provider is better than another;
- a recommendation is valid;
- the runtime should be selected;
- a production system is ready.

## Failure behavior

A mismatched Context or Protocol must fail verification. Missing Runtime/provider provenance, undeclared execution mode, or changed authority fields must also fail.

## Authority invariant

Verification itself is non-authoritative. Human Gate remains the final decision boundary.

## Current scope

The v0.1 verifier is deterministic and local. It does not verify cryptographic signatures, remote logs, provider-side execution, or independent third-party attestations.
