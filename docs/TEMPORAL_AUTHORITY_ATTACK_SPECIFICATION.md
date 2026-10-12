# Temporal Authority Attack Specification v0.1

## Purpose

Verify that a previously valid human approval cannot be reused outside the
time/context/evidence boundary for which it was granted.

## Boundary

Observation → Evidence → Runtime Proposal → Human Approval → Execution

Temporal integrity adds a second constraint:

**an approval is valid only within its bound causal and contextual history.**

## Attack cases

1. Stale approval replay
2. Future evidence
3. Replayed decision identity
4. Out-of-order parent/child event
5. Missing provenance parent
6. Context-version mismatch
7. Invalid timestamp

## Invariants

- A decision identity is single-use.
- An execution cannot precede its approval.
- An execution cannot use an approval from another Context version.
- A decision cannot depend on evidence that occurs later in the claimed timeline.
- Every causally linked event must identify an existing parent.
- Invalid temporal state fails closed.
- Timestamps are consistency claims, not trusted truth by themselves.

## Non-goals

This boundary does not prove that a local clock is truthful. Trusted time,
signed external timestamps, or other clock-attestation mechanisms are separate
security concerns.

## Expected result

All seven attack classes are rejected without granting authority to Runtime.
