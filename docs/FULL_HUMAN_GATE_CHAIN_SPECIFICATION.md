# Full Human Gate Chain Specification v0.1

## Purpose
This boundary composes presentation, decision, execution-binding, authenticated-human, temporal, revocation, and persistence controls into one fail-closed validation path.

## Required order
UI/Adapter -> Human Decision Replay -> Decision Binding -> Authenticated Human Gate.

The composed chain does not grant authority to UI, runtime, verifier, signature, authentication, or recovery.

## Attack classes
- synthetic UI events
- runtime-generated UI events
- UI/decision binding mutation
- human decision replay
- execution binding mutation
- authenticated identity substitution
- authentication replay
- key rotation/revocation
- temporal key mismatch
- persisted cross-context substitution
- runtime authority injection
- missing human approval

## Security invariant
AI/runtime evidence is not human authorization.

## Scope limitation
This is a structural boundary test. It does not claim production-grade identity assurance, secure hardware, key custody, or real-world human presence.

## Verification target
The full chain must fail closed whenever any layer is mutated or replayed, while a valid end-to-end human decision remains admissible.
