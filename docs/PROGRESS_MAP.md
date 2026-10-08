# Shirakami Progress & Human Gate Map

## Purpose

This document is the current milestone map for Shirakami.
It is a decision landscape, not a recommendation.

AIwitness may preserve this map.
AIwitness must not rank, recommend, or select a branch.

Selection authority: human_gate.

## Current Position

current_milestone: threadrpg-derived-core-mapping

## Milestones

| ID | Status | Meaning |
|---|---|---|
| core-architecture | complete | Shirakami reference architecture and core semantic boundaries established |
| authority-human-gate | complete | Human Gate remains final authority |
| verification | complete | Verification integrity and forgery-resistance boundaries established |
| runtime-adapter | complete | Runtime/provider exchangeability established without transferring authority |
| core-conformance | complete | Core authority chain has a reproducible CI conformance gate |
| api-v1 | complete | Real HTTP API v1.0 boundary implemented and CI-verified |
| aiwitness-decision-map | complete | Decision landscape and branch structure can be preserved for Human Gate |
| external-developer-handoff | complete | Make the existing system understandable and usable by an independent developer |
| threadrpg-integration-assessment | complete | Historical ThreadRPG assets and published development record verified; ThreadRPG is treated as an origin/discovery system rather than merely a later application |
| threadrpg-derived-core-mapping | pending | Map ThreadRPG-origin invariants to current Shirakami boundaries and distinguish implemented, documented-only, and unverified mappings |

## Current Decision Point

### DP-02: How should ThreadRPG relate to current Shirakami architecture?

Options:

1. port ThreadRPG as an application
   - Treat ThreadRPG primarily as a product/runtime integration target.
   - Not selected as the default interpretation.

2. derive core invariants
   - Trace which principles were discovered through ThreadRPG and later generalized into Shirakami Model / Architecture.
   - This is the current assessment direction.

3. reopen completed architecture boundaries
   - Rebuild existing Runtime/API/Human Gate work around ThreadRPG-specific semantics.
   - Explicitly out of scope unless the invariant mapping demonstrates a concrete necessity.

Selected option: 2
Selection authority: human_gate

## Completion Rules

- Completed milestones are not reopened merely because additional tests are possible.
- New work must either satisfy the current pending milestone or be explicitly declared a new research topic.
- A percentage must never replace the milestone map.
- The map records alternatives; it does not choose among them.
- Historical lineage must not be used to smuggle application-specific semantics into the Runtime kernel.

## Current Boundary

Shirakami API v1.0 is complete.

The external-developer-handoff milestone is complete.

The ThreadRPG integration assessment is complete at the historical/documentary level.

The current question is not "how do we put ThreadRPG into the OS?" but:

> Which principles discovered through ThreadRPG became Shirakami Model invariants, and which of those invariants are now implemented and verified by Shirakami OS?

The bounded next milestone is threadrpg-derived-core-mapping.

JOUMON/v2 and production deployment remain separate branches, not hidden requirements of the current milestone.