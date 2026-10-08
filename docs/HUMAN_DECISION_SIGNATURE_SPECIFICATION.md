# Human Decision Signature Boundary v0.1

The Human Gate must not treat a mutable record as proof that a human approved it.

This boundary binds a test-only cryptographic signature to the Decision, Approval, Context, Evidence, Protocol, Proposal, principal, and authentication identifiers.

Mutation of any bound field invalidates the signature. A valid signature still does not itself create authority: it is an authenticity signal that must remain inside the existing Human Gate and decision-binding chain.

The HMAC mechanism is intentionally test-only. Production deployment must select an appropriate asymmetric signature, key protection, identity provider, rotation, revocation, and trust-root model.

Invariant:

`valid signature -> authenticated decision evidence`

not:

`valid signature -> automatic authority`.
