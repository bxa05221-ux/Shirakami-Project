# Decision Binding Attack Specification v0.1

## Purpose

Verify that a human approval cannot be detached from the exact scope that
was reviewed.

An approval is bound to:

- Context version
- Evidence hash
- Protocol hash
- Proposal identity
- Approval identity

Execution must match every binding exactly.

## Attack classes

1. Context substitution
2. Evidence substitution
3. Protocol substitution
4. Proposal substitution
5. Approval identity substitution
6. Missing binding
7. Runtime authority claim

## Security property

A valid approval for one decision scope MUST NOT authorize another scope.

This boundary preserves the distinction:

Human decision = authority
Runtime proposal = simulation/recommendation

Passing this validator does not itself authorize execution; the Human Gate
remains the authority boundary.
