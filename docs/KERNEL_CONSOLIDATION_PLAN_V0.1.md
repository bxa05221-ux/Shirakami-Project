# Kernel Consolidation Plan v0.1

## Status

- Type: integration plan; no implementation change authorized by this document alone.
- Baseline: current `main` at plan creation.
- Objective: consolidate existing kernel responsibilities and verification without reopening completed milestones or expanding scope.
- Application-specific Anka work is frozen separately; this plan does not depend on Anka.

## Governing rules

1. `main` is the integration baseline, not an older feature branch.
2. Do not merge PRs #70–#73 as a bundle or merge any of them solely because their workflows passed.
3. Preserve existing evidence and commit history. Do not force-update or delete the source branches during the audit.
4. A completed milestone is not reopened merely because additional tests are possible.
5. Add no new kernel invariant unless a concrete gap in the current normative specification is demonstrated.
6. A passing workflow is evidence for that exact commit and environment, not proof that a divergent branch is safe to integrate.
7. Human approval remains authoritative; automation may report evidence but must not select or merge a branch.

## Repository evidence checked

- `docs/PROGRESS_MAP.md` on `main` marks core architecture, Human Gate authority, verification, runtime/adapter, core conformance, API v1, external developer handoff, and ThreadRPG-derived core mapping as complete.
- The same map says completed milestones are not reopened merely because additional tests are possible, and percentages must not replace milestone status.
- PR #70 (`phase/full-human-gate-chain-v0.1`) is open Draft, based on `main`, with 111 changed files.
- PR #71 (`phase/full-system-authority-chain-v0.1`) is open Draft, based on `main`, with 115 changed files. It adds the full-system authority-chain layer to the Human Gate work.
- PR #72 (`fix/full-system-authority-parametrize-v0.1`) is open and targets the #71 branch; it changes one test file and is not an independent integration target.
- PR #73 (`fix/full-system-authority-hardening-v0.1`) is open Draft and targets the #71 branch; its 21 changed files include API/conformance files and a copy of `docs/PROGRESS_MAP.md`.
- The #73 head had six reported successful related workflows in the prior audit. This is not a current-main integration result.
- A prior run on #71 failed at test collection due to a parametrization mismatch. A run on #72 fixed collection but still reported substantive test failures. Those results must be checked against the current head before interpreting them as current failures.

## Responsibility map

| Responsibility | Canonical location to verify first | Consolidation rule |
|---|---|---|
| Project-level milestones and scope | `docs/PROGRESS_MAP.md` on `main` | Keep one canonical map; do not overwrite it with a stale branch copy. |
| Human Gate / authority-chain contracts | Existing specification documents under `docs/` | Preserve distinct threat models only where they assert distinct invariants. |
| Authority-chain runtime | `runtime/full_system_authority.py` on the candidate branch | Treat as a candidate integration surface, not automatically canonical until conformance is demonstrated. |
| HTTP API | `runtime/http_api.py`, `docs/API_V1.md`, and API tests | Compare with the existing strategic Human Gate API on `main`; avoid parallel API entry points with unclear authority semantics. |
| Core conformance | `scripts/run_core_conformance.py`, `docs/CORE_CONFORMANCE.md`, and `.github/workflows/core-conformance.yml` | Prefer one documented aggregate gate that calls explicit focused checks. |
| Focused security/integrity tests | `scripts/test_*.py` and matching workflow files | Retain tests for distinct guarantees; deduplicate duplicated orchestration, not coverage. |
| AIwitness evidence recording | Existing AIwitness boundary contract and record/validation scripts | Keep evidence provenance separate from interpretation and approval. |

## Required integration sequence

### 1. Establish the baseline
- Record the current `main` SHA and verify the work branch is based on it.
- Re-read current `main` versions of the progress map, API contracts, AIwitness boundary contract, and relevant workflows.
- Do not infer the current `main` SHA from old PR metadata.

### 2. Classify candidate changes
For each changed file in #70–#73, assign exactly one primary classification:
- already present on current `main`;
- required new implementation;
- required focused test;
- required specification clarification;
- duplicated workflow/orchestration;
- unresolved failure or unclear ownership;
- application/research scope, not kernel scope.

No file is carried forward merely because it exists in a passing branch.

### 3. Resolve the test failures before porting
- Re-run the current #71/#72/#73 heads or inspect their latest run IDs.
- Separate test fixture/collection defects (for example missing fixture fields or undefined constants) from implementation failures where an invalid authority mutation is accepted.
- Every claimed invariant must have a test that demonstrates both the valid path and the relevant rejected mutation.
- Do not weaken an assertion just to obtain a green workflow.

### 4. Build a minimal candidate on top of current `main`
- Cherry-pick or manually reapply only changes classified as required.
- Preserve the current canonical progress map unless a human-approved milestone change is necessary.
- Avoid importing a large branch wholesale when a small, auditable patch is sufficient.
- Keep source PRs open until the replacement candidate has been verified and the human decides their disposition.

### 5. Verify and report
- Run focused tests for each changed responsibility.
- Run the aggregate Core Conformance gate on the candidate commit.
- Confirm all relevant workflows refer to that exact candidate SHA.
- Report failures, skipped checks, and limitations explicitly.
- Request human review; do not merge automatically.

## Exit criteria

The consolidation candidate is ready for review only when:

1. Each carried-forward change has a stated kernel responsibility.
2. There is one canonical project milestone map.
3. No unresolved test-collection error remains in the selected verification path.
4. Authority-chain mutation tests reject the invalid cases required by the normative contract.
5. The aggregate conformance gate passes on the candidate SHA.
6. No application-specific requirement has been silently promoted into a kernel invariant.
7. The PR description lists what was deliberately excluded and why.

Passing these criteria means “ready for human review,” not “automatically merged” and not a claim that every possible security property has been proven.
