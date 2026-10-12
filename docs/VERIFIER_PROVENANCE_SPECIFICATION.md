# Verifier Provenance v0.1

## Threat

A verification record may identify a verifier, but an identifier alone must not silently become authority. A replayed or forged verifier label must not create human approval or runtime authority.

## Boundary

Verifier provenance records:
- verification identity;
- target identity;
- verifier identity;
- verifier instance identity.

This establishes provenance metadata. It does **not** claim cryptographic authentication.

## Acceptance criteria

- missing provenance fields fail closed;
- verifier identity is recorded;
- verifier instance distinguishes separate verifier executions;
- verifier provenance cannot create verifier authority;
- verifier provenance cannot create human approval;
- verifier provenance cannot create runtime authority.

## Future hardening

Cryptographic signer identity, key rotation, trust roots, revocation, and independent attestation remain separate implementation surfaces.
