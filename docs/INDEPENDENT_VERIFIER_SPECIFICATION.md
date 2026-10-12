# Independent Verifier Boundary v0.1

## Purpose

Independent verifiers provide independent evidence. They do not become an authority layer merely because they agree.

## Independence

A verifier is identified by both:
- verifier identity
- verifier instance

Two instances of the same verifier identity are not sufficient for the minimum independence requirement.

## Consensus rule

Two or more pass results may strengthen evidence, but:

- verifier consensus is not human approval;
- verifier consensus is not runtime authority;
- verifier disagreement is evidence, not automatic rejection or approval;
- no verifier may manufacture a human decision.

This prevents the architecture from accidentally replacing the Human Gate with an AI quorum.

## Security property

N verifiers agree must never imply human_authority = true.

The Human Gate remains a separate authority boundary.
