# Verification Forgery Resistance v0.1

## Threat

A valid verification result may be copied, altered, or relabeled after verification. A downstream component must not accept altered content as the original verification result.

## Boundary

The digest binds `verification_id`, `target_id`, `result`, and `verifier`.

Any mutation of those fields produces a digest mismatch and fails closed.

Authority claims are deliberately checked separately: a record cannot gain `human_approval` or `runtime_authority` merely by preserving its verification digest.

## Acceptance criteria

- original record + original digest: accepted;
- result mutation: rejected;
- target mutation: rejected;
- verifier mutation: rejected;
- missing binding field: rejected;
- human approval claim: rejected;
- runtime authority claim: rejected.

## Non-claim

A digest provides tamper evidence, not authenticity of the producer. Authenticity, key management, and independent verifier trust are separate future surfaces.
