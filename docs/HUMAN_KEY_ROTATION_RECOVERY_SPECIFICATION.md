# Human Signing-Key Rotation × Replay × Recovery Boundary v0.1

A human decision signed with an old key must not regain authority merely because the persisted record survives key rotation or because the system recovers after interruption.

Recovery therefore rechecks the decision/persisted bindings and current key trust. A revoked or rotated-out key fails closed. Persistence preserves evidence; it does not mint authority.

This boundary is intentionally structural. Production key lifecycle, secure storage, rotation ceremonies, and identity infrastructure remain separate trust roots.
