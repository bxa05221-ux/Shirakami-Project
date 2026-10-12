# Trust Root Boundary v0.1

## Threat

A cryptographically valid verifier record can still be produced by a verifier that the system does not trust.

Therefore:

cryptographic authenticity != trust authorization

## Boundary

The trust-root layer requires both:
1. verifier identity to exist in an explicit trusted-verifier set;
2. the verification record to authenticate with the expected secret.

Neither condition grants human approval or runtime authority.

## Attack cases

- authentic but unknown verifier;
- wrong signing key;
- trusted-verifier list substitution;
- trust-root attempt to create human approval;
- trust-root attempt to create runtime authority.

## Future hardening

A production trust root needs explicit key management, rotation, revocation, provenance of trust-list changes, and independent administrative control.
