# Verifier Collusion Resistance v0.1

## Security objective

A verifier quorum may aggregate evidence, but verifier agreement must never become a substitute for the Human Gate.

### Attack model

Assume one or more verifiers are compromised and coordinate their outputs. Even unanimous malicious PASS results must not manufacture:

- human approval;
- runtime authority;
- a decision event;
- permission to bypass the Human Gate.

### Boundary

The quorum validator answers only:

> Is the evidence quorum satisfied?

It does not answer whether the system may execute.

Execution authority remains outside the verifier layer and requires the existing decision-binding and Human Gate controls.

### Independence

Quorum counting and verifier independence are separate properties. Callers must compose the independent-verifier boundary when independence is required.

Therefore:

N verifier PASS results != human approval

and

N colluding verifiers != authority.

This is a deliberate defense against replacing a human authority boundary with an AI or verification majority vote.
