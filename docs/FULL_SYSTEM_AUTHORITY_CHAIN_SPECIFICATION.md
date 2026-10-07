# Full-System Authority Chain v0.1

## Purpose

This boundary composes the existing temporal/verification/trust chain with the authenticated Human Gate chain.

## Required order

Observation/Event Graph -> Verification -> Trust-at-Time -> Decision Binding -> Persistence/Recovery -> Human Authentication -> Human Decision -> Human Gate.

## Security invariant

No verification result, verifier quorum, runtime output, recovery state, signature, or authenticated identity can independently create execution authority.

## Boundary rule

All cross-layer bindings must refer to the same approval, context, evidence, protocol, and proposal. A valid component from another context is not interchangeable with a valid component from the current context.

## Scope

This is a composition boundary, not a claim of production-grade cryptographic or real-world identity assurance.


## Authority Identity Uniqueness

The system permits multiple historical or unrelated candidates, but an authority-bearing semantic identity must resolve to exactly one event in the selected chain. Duplicate identities for evidence, protocol, proposal, verification, human decision, human approval, or execution are rejected as ambiguous. Candidate multiplicity must never become authority multiplicity.
