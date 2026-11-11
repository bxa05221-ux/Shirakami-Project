# Human Gate Authenticity Boundary v0.1

## Principle

A field saying `human_approval: true` is not, by itself, a Human Gate event.

The authority-bearing record must explicitly identify a human actor, carry an allowed human decision, and bind that decision to the exact approval scope: Context, Evidence, Protocol, and Proposal.

## Attack model

The test suite rejects:

- runtime impersonation of a human actor;
- synthetic `human_approval` claims;
- approval records without explicit human approval;
- Context/Evidence/Protocol/Proposal mutation;
- runtime authority claims;
- invalid decision values.

## Boundary

`AI proposal -> Human Gate -> human decision -> bound approval`

is valid.

`AI proposal -> human_approval=true`

is not.

This boundary validates structured provenance. It does not claim that a string field alone proves a real-world person's identity. Strong identity, authentication, signing, and replay protection remain separate security layers.
