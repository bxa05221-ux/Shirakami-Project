# JOUMON End-to-End Protocol v0.1

status: experimental

## Complete flow

    Context
      ↓
    Protocol
      ↓
    Runtime A
      ↓
    Evidence A + Lineage A
      ↓
    Semantic Handoff
      ↓
    Matome artifact
      ↓
    Handoff Import
      ↓
    Runtime B
      ↓
    Evidence B + Lineage B
      ↓
    Runtime C
      ↓
    Evidence C + Lineage C
      ↓
    Verification
      ↓
    Comparative Evidence
      ↓
    Human Gate
      ↓
    Explicit human decision

## End-to-end invariants

- Context identity remains stable.
- Protocol identity remains stable.
- Each Runtime retains independent provenance.
- Evidence remains observational and non-authoritative.
- Lineage remains traceable across handoffs.
- Serialization/import does not alter authority semantics.
- Verification does not become decision authority.
- Comparative Evidence does not select a winner.
- Human Gate remains the final decision boundary.

## Status

The v0.1 implementation is a deterministic mock-runtime integration test. It demonstrates architectural continuity, not live provider quality, correctness, or production readiness.
