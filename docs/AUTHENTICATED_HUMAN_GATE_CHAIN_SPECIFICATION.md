# Authenticated Human Gate Chain v0.1

This composition verifies that a Human Gate decision remains structurally bound across UI-independent human identity, authentication replay resistance, decision signature, signing-key trust, key temporal validity, revocation, and persistence/recovery.

The chain is fail-closed: failure at any boundary prevents the composed validation from succeeding.

This does not claim real-world identity assurance or production cryptographic security. Those remain deployment-specific trust roots.

Core invariant:

`authenticated human evidence != AI authority`

A valid signature, trusted key, successful recovery, or passing verification may establish evidence, but none may manufacture Human Gate authority.