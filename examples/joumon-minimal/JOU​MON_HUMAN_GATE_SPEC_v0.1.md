# JOUMON Human Gate Specification v0.1

status: experimental
purpose: Make the final decision boundary explicit after multi-runtime Evidence and Verification.

## Flow

    Runtime A/B/C
         |
      Evidence
         |
     Verification
         |
  Comparative Evidence
         |
      Human Gate
         |
   explicit human decision

## Invariants

- Human Gate consumes Evidence and verification references, not hidden model authority.
- Runtime output cannot become a decision merely by passing Verification.
- Comparative Evidence does not select a winner.
- A decision must be explicitly supplied at the Human Gate.
- The recorded authority is human.

## Scope

v0.1 records the boundary and decision event locally. It does not implement authentication, signatures, UI approval workflows, or organizational delegation.
