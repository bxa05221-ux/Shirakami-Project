# Human Decision Authentication & Replay Boundary v0.1

A Human Gate decision is a distinct event, not a reusable boolean.

## Required properties

- unique `decision_id`;
- explicit `actor_type: human`;
- allowed decision: `approve`, `reject`, or `revise`;
- explicit `human_approval: true`;
- exact Context/Evidence/Protocol/Proposal bindings;
- no runtime authority claim.

A decision ID may not be accepted twice. Replaying an old approval, even with a changed approval identifier, is rejected when the decision event identity is reused.

This layer detects structural replay. Real-world human identity authentication and cryptographic signatures remain separate boundaries.
