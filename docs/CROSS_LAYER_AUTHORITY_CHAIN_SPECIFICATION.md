# Cross-Layer Authority Chain v0.1

This test composes the existing temporal, verification, trust-root, decision-binding,
and recovery boundaries into one fail-closed authority chain.

## Chain

Observation/Event Graph
-> Verification Integrity + Forgery Resistance
-> Trust Root Temporal Check
-> Human Decision Binding
-> Revocation-aware Persistence Recovery

Every boundary must pass.

## Attack target

The primary attack is authority resurrection:

1. a verifier is trusted and produces a valid verification;
2. a human approval is persisted;
3. the verifier is later revoked;
4. an attacker replays the persisted approval through recovery.

The chain must reject the replay.

## Security property

A historical valid verification proves provenance for its historical event.
It does not, by itself, grant present execution authority.

Persistence preserves state. Recovery revalidates authority; it does not mint it.

## Fail-closed cases

- revoked verifier;
- mutated verification;
- verifier substitution;
- approval scope mutation;
- incomplete persisted bindings;
- runtime authority claim.

The next boundary is independent verifier trust: multiple verifiers must not
become an implicit AI consensus authority.
