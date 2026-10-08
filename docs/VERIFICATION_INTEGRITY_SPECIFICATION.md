# Verification Integrity v0.1

## Principle

Verification is an observation about whether defined checks passed. It is not human approval and it cannot create runtime authority.

## Required properties

A verification result must identify:

- verification_id;
- target_id;
- result (`pass` or `fail`);
- verifier.

The result must not assert human approval or runtime authority.

## Acceptance criterion

Even a valid `pass` must remain non-authoritative:

`verification_pass != human_approval`

and

`verification_pass != runtime_authority`

## Scope

This is the verification boundary. It does not claim that the verifier itself is correct, independent, or tamper-proof. Those are separate future attack surfaces.
