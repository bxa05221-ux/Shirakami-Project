# Shirakami Progress & Human Gate Map

## Purpose

This document records the current milestone position for Shirakami.
It is a decision landscape, not a recommendation.

AIwitness may preserve this map.
AIwitness must not rank, recommend, or select a branch.

Selection authority: human_gate.

## Current Position

current_milestone: joumon-v2

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
| external-developer-handoff | complete | An independent developer can inspect and run the API v1.0 boundary without live author explanation |
| joumon-v2 | paused | Multi-runtime collaboration/integration remains a later milestone |

## Decision Point

### DP-02: What happens after external developer handoff?

Options:

1. joumon-v2
   - Resume JOUMON as a multi-runtime collaboration/integration layer.

2. productization
   - Build production deployment concerns such as authentication, TLS, rate limiting, operations, and hosting.
   - These remain separate from the completed API v1.0 and handoff milestones.

Selected option: none
Selection authority: human_gate

## Completion Rules

- Completed milestones are not reopened merely because additional tests are possible.
- New work must either satisfy the current pending milestone or be explicitly declared a new research topic.
- A percentage must never replace the milestone map.
- The map records alternatives; it does not choose among them.

## Current Boundary

The following milestones are complete:

- API v1.0
- AIwitness Decision Map
- External Developer Handoff

The next milestone is JOUMON v2, currently paused pending Human Gate selection.
Production deployment remains a separate productization branch.
