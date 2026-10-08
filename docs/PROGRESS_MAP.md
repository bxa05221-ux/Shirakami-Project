# Shirakami Progress & Human Gate Map

## Purpose

This document is the current milestone map for Shirakami.
It is a decision landscape, not a recommendation.

AIwitness may preserve this map.
AIwitness must not rank, recommend, or select a branch.

Selection authority: human_gate.

## Current Position

current_milestone: external-developer-handoff

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
| external-developer-handoff | pending | Make the existing system understandable and usable by an independent developer |
| joumon-v2 | paused | Multi-runtime collaboration/integration remains a later milestone |

## Current Decision Point

### DP-01: What happens after API v1.0?

Options:

1. handoff
   - Prepare the minimum external-developer onboarding surface.
   - Goal: another developer can inspect, run, and understand the existing boundary without the author explaining the architecture live.

2. productization
   - Build production deployment concerns such as authentication, TLS, rate limiting, operations, and hosting.
   - These are intentionally outside API v1.0.

3. joumon-v2
   - Resume JOUMON as a multi-runtime collaboration/integration layer.
   - This is intentionally later than the external handoff boundary.

Selected option: none
Selection authority: human_gate

## Completion Rules

- Completed milestones are not reopened merely because additional tests are possible.
- New work must either satisfy the current pending milestone or be explicitly declared a new research topic.
- A percentage must never replace the milestone map.
- The map records alternatives; it does not choose among them.

## Current Boundary

Shirakami API v1.0 is complete.

The next milestone is external-developer-handoff.
JOUMON/v2 and production deployment are separate branches, not hidden requirements of the current milestone.
