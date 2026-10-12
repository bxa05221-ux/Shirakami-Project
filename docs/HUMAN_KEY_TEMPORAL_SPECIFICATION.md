# Human Signing-Key Temporal Boundary v0.1

A signature can be cryptographically valid while its signing key was not authorized at the time of the decision.

This boundary evaluates key trust against the decision timestamp and explicit activation, expiry, and revocation times.

Therefore:

`valid signature + currently trusted key != automatically valid historical decision`

The key must have been within its authorized interval at the decision time.

This contract is intentionally independent of production key storage and rotation infrastructure. Those mechanisms must provide authoritative timestamps and a governed trust history.
