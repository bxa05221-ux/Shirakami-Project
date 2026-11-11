# Verifier Authenticity v0.1

## Purpose

Verifier provenance says which verifier claims to have produced a result.
This layer tests whether the record was produced with the expected secret.

## Boundary

A canonical verification payload is authenticated with HMAC-SHA256 in this test implementation.

Authentication proves integrity relative to a supplied secret. It does not by itself establish who is trusted to make human decisions.

## Acceptance criteria

- valid signature passes;
- verification result mutation fails;
- verifier substitution fails;
- verifier instance substitution fails;
- wrong secret fails;
- authenticated verifier output cannot create human approval;
- authenticated verifier output cannot create runtime authority.

## Explicit limitation

The test secret is not a production trust root. Production deployment requires a separate key-management and trust-store design, including rotation and revocation.

## Security invariant

authenticated_verifier_output != human_authority
