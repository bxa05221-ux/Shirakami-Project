# Shirakami Disclosure Boundary Strategy v0.1

## Purpose

This document defines the disclosure strategy for Shirakami Project after the repository was moved to private visibility.

The immediate objective is not monetization or public release. It is to determine, asset by asset, what may be disclosed, what must be abstracted, what remains internal, and what should be treated as a confidential/core candidate.

## Decision principle

The question is not:

> Can this material legally be published?

The first question is:

> Is there a strategic reason to publish it?

A permissive software license does not constitute authorization to publish project knowledge, research conclusions, internal operating procedures, confidential application designs, or unpublished intellectual assets.

## Four disclosure classes

### P — Public candidate

Material whose disclosure is intentionally useful for external review and does not materially reveal confidential composition.

Examples:
- high-level project purpose
- general problem statement
- AI is a simulator, not an authority
- Human Gate as a principle
- Evidence and inference distinction
- Observation Space is not World Totality
- general research questions
- deliberately selected public examples

### A — Abstracted public

Material that may be disclosed only after removing implementation-specific composition, internal state transitions, operational details, or confidential application knowledge.

Examples:
- Semantic Handoff as a concept
- AIwitness as a general witness-layer concept
- Reality–User World Clutch as a conceptual model
- Frame Reopening as a research question
- generalized verification principles

### I — Internal

Material required for development, testing, coordination, or reproducibility inside the project, but not currently intended for public disclosure.

Examples:
- agent instructions
- agent coordination rules
- project state
- runtime implementations
- detailed schemas
- validation scripts
- E2E tests
- internal handoff records
- detailed security boundaries
- provider adapter implementation

### C — Core / confidential candidate

Material whose disclosure could reveal unpublished composition, competitive know-how, application assets, IP candidates, or business-critical design.

Examples:
- the composition connecting Evidence, Meaning, Presence, Dream, Memory, Protocol, Runtime and Human Gate
- detailed Reality–User World Clutch implementation
- frame-reopening mechanisms
- hidden integration logic
- unpublished application designs
- care/education application assets
- gadget architecture
- unreleased domain-specific protocols
- combinations whose joint disclosure would permit reconstruction of the core

C is a strategic classification, not a legal conclusion. Legal protection, trade-secret status, copyright, patentability, and ownership require separate review.

## Current repository triage

| Asset / area | Initial class | Reason |
|---|---|---|
| README.md | A | Useful public explanation, but currently exposes internal repository topology and operational flow |
| README.en.md | A | Same issue as Japanese README |
| AGENTS.md | I | Internal agent operating instructions and authority boundaries |
| AGENT_COORDINATION.yaml | I/C candidate | Internal multi-agent roles, authority and synchronization |
| SHIRAKAMI_STATE.yaml | I | Live project state |
| AIWITNESS_BOUNDARY_CONTRACT.yaml | I/A | Valuable concept, but concrete contract and authority boundary details are internal |
| Semantic Integrity Boundary | I/A | General concept may be public; concrete verification composition should remain internal |
| Semantic Handoff implementation | I/C candidate | Core implementation composition |
| Semantic Handoff template | I | Operational handoff structure |
| Matome Library index | I/C candidate | Internal semantic library organization |
| Core principle Matome files | A | Concepts may be selectively abstracted for public explanation |
| Security Boundary Matome | I/C candidate | Security model and protected assets reveal internal boundary assumptions |
| Input Trust / Protocol Injection / Evidence Integrity | I/C candidate | Internal security and integrity design |
| Runtime implementation | I | Implementation know-how and operational detail |
| Runtime execution boundary specification | I | Detailed execution boundary |
| API boundary contracts | I | Concrete internal architecture |
| Provider adapter | I | Implementation detail |
| Test suite | I/A | Selected tests may later become public evidence; full suite remains internal until disclosure review |
| Reviewer Protocol | A | Candidate for public review methodology after disclosure audit |
| Legacy research | I/C candidate | Historical material may reveal unpublished concepts and should be reviewed individually |
| Aoike / Bunka / Narrative research | I/C candidate | Application/domain assets; do not assume they are merely examples |
| Brass Band / ThreadRPG material | I/C candidate | Application design and semantic integration may reveal core composition |
| 保育レジリエンス material | C candidate | Treat as an independent intellectual/application asset until explicitly classified |
| Gadget architecture | C candidate | Potentially business-critical and/or IP-relevant |
| Reality–User World Clutch | C candidate | Current differentiator hypothesis; public version should initially be conceptual only |
| User World / Meaning / Presence / Dream model | C candidate | Potentially central to the Reality–User World Clutch composition |
| Frame Reopening / unknown-unknown mechanism | C candidate | Potentially central to Shirakami's meta-level advantage |
| Business / monetization material | I/C | Do not expose until business strategy is intentionally defined |

## Combination risk

Disclosure review must consider not only individual files but also reconstruction risk.

A set of individually harmless documents may become sensitive when combined.

In particular, review combinations of:

- Evidence + Meaning + Presence + Dream
- Semantic Handoff + Runtime + Human Gate
- AIwitness + Trace + Evidence lineage
- Frame Reopening + Observation Space boundary
- ThreadRPG + Matome + Reality–User World Clutch
- care/education applications + core protocols
- gadget architecture + local AI connection
- public README + protocol names + implementation examples

The question is:

> Could a reader reconstruct a material part of the unpublished Shirakami composition from the combination?

If yes, classify the relevant combination as I or C even if individual pieces appear public-safe.

## MIT license boundary test

MIT or another software license answers a licensing question. It does not answer:

- whether the project may be published;
- whether confidential knowledge may be disclosed;
- whether a new file may be created;
- whether a branch may be pushed;
- whether a change may be merged;
- whether a business decision has been authorized.

Required reasoning boundary:

License information
→ determine permitted use of licensed material
→ STOP
→ identify current human instruction and authorized scope
→ check disclosure class
→ check repository visibility
→ check Human Gate
→ execute only if authorized.

An external license must never be promoted into project authority.

## Public repository policy

The current Shirakami-Project repository is treated as an internal/private working repository.

No return to public visibility should occur until:

1. disclosure classes have been assigned;
2. combination/reconstruction risk has been reviewed;
3. C candidates have been isolated;
4. public-facing material has been intentionally selected;
5. license and ownership questions have been reviewed;
6. a human has authorized the public release boundary.

## Next verification

The next verification is not a publication.

It is a disclosure audit:

1. enumerate every current file;
2. assign P/A/I/C;
3. identify combination risks;
4. identify items that were previously public;
5. record unresolved classification questions;
6. produce a proposed public tree separately from the internal tree.

## Status

status: disclosure-audit-started
repository_visibility: private
publication_authorized: false
monetization_phase: deferred
primary_objective: confirm_and_protect_shirakami_core
