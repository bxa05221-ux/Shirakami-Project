# Authenticated Human Gate Chaos Test v0.1

## Purpose

Attack the composed Human Gate boundary by mutating one layer while preserving other apparently valid layers.

Attack families:
- signing key revoked after issuance;
- authentication replay;
- runtime actor spoofing;
- trusted key / principal substitution;
- decision-time key invalidity;
- persisted context substitution;
- runtime authority claim with an otherwise valid signature;
- recovery after key rotation.

## Security property

No individually valid-looking artifact may manufacture Human Gate authority when its cross-layer bindings, temporal state, identity, authentication, key trust, or persistence state disagree.

This is a structural adversarial test, not a production identity or cryptographic assurance claim.
