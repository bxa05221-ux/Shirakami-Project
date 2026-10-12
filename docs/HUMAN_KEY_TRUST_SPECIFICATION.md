# Human Signing-Key Trust Boundary v0.1

A valid signature does not establish that its signing key is currently trusted.

This boundary separates cryptographic validity from authorization of the signing principal. A decision is accepted by this layer only when its principal is in the explicit trusted set and its signing key is not revoked.

The trust set and revocation set are inputs to the boundary. Their governance, temporal validity, key rotation, and production key storage remain separate security boundaries.

Invariant:

`valid signature != trusted signer`

and:

`trusted signer != Human Gate approval`.

The final authority remains the Human Gate.
