# Human Identity Authentication Boundary v0.1

The Human Gate must distinguish a structured claim of `actor_type: human` from an authenticated human principal.

The decision is accepted only when an authenticated principal and authentication event are explicitly present and bound to the same Decision ID, Approval ID, Context, Evidence, Protocol, and Proposal.

Principal substitution and authentication-event substitution fail closed.

This specification defines an abstract security contract for testing. It does not select a production identity provider, biometric system, password system, or cryptographic key infrastructure.

The architectural invariant is:

`authenticated human identity -> bound decision -> Human Gate`

not:

`string says human -> authority`.
