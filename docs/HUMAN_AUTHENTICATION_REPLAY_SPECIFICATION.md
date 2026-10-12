# Human Authentication Replay Boundary v0.1

An authenticated human session is not an infinitely reusable authority token.

The boundary rejects reuse of an authentication event after it has already been consumed or explicitly revoked. The authenticated principal and authentication event must also match the decision record exactly.

This protects against:

- captured approval-session replay;
- authentication ID substitution;
- principal substitution;
- reuse after revocation;
- runtime impersonation;
- runtime authority claims.

Historical provenance may remain evidence, but a revoked authentication event cannot silently regain current authority.

Production authentication protocols, token formats, cryptographic signing, and key rotation remain implementation choices outside this abstract boundary.
