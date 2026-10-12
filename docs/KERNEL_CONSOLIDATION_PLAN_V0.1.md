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


## First-pass file audit (2026-10-12)

### Confirmed current-main differences

- `main` contains `runtime/human_gate_http_api.py` and `runtime/human_gate_profile.py`, which expose configurable Human Gate review profiles. They are explicitly documented as configuration/review endpoints, not decision endpoints.
- `main` does not contain the candidate branch's `runtime/http_api.py`, `runtime/full_system_authority.py`, `scripts/run_core_conformance.py`, `scripts/test_full_system_authority.py`, `docs/API_V1.md`, or `docs/CORE_CONFORMANCE.md`. These are genuine candidate additions, not simple duplicate files. Their dependencies and authority semantics still require review before porting.
- The candidate's `runtime/http_api.py` imports `runtime.api.ShirakamiAPI`; therefore, porting the transport alone would be incomplete. The full dependency closure must be classified before implementation is copied.
- PR #73 changes 21 files and includes `docs/PROGRESS_MAP.md`. Its copy sets `current_milestone: joumon-v2`, while the current `main` map sets `current_milestone: threadrpg-derived-core-mapping-complete`. The PR copy is stale/conflicting for the current project baseline and must not replace the `main` map.
- The existing Human Gate profile API and the candidate API v1 are not automatically duplicates: the former documents profile/configuration access, while the latter is a provider-neutral Semantic Handoff API. Review their contracts and authorization boundaries rather than merging them by filename or naming.

### Current workflow evidence inspected

- PR #71 head `bc4a602790c0f5eae540845fcd17fe4b7fe8a71a`: Full-System Authority Chain workflow failed at test collection due to a parametrization mismatch; most focused workflows shown for that SHA succeeded.
- PR #72 head `f136c5fafe08ba7f4eb2df3f67f4cb126fad80b7`: Full-System Authority Chain workflow failed; the prior job log reported 8 failures, 146 passes, and 1 error. This fix branch is not the final #73 head.
- PR #73 head `859842dbf46a176ad5945425a8002e4d5f1fa74c`: all six reported PR workflows succeeded, including Full-System Authority Chain and Core Conformance.
- None of these results is a run on the new consolidation branch based on current `main`. The correct conclusion is: #73 is the strongest verified candidate so far, but its changes have not been verified against the current baseline.

### First-pass disposition

| Change group | Disposition | Reason |
|---|---|---|
| Full-system authority runtime + its focused test | Carry forward as a candidate | Missing on `main`; required for the #71/#73 authority-chain claim, but test semantics must be audited. |
| Core Conformance runner, contract, and workflow | Carry forward as a candidate | Missing on `main`; offers an aggregate gate. Confirm its test list and workflow scope before adoption. |
| API v1 transport, API implementation/contracts, examples and tests | Carry forward as a candidate group, not as isolated files | Missing on `main`; transport imports a separate API implementation. Preserve the existing Human Gate profile API. |
| PR #73 copy of `docs/PROGRESS_MAP.md` | Exclude | Conflicts with the current main milestone. Keep one canonical map. |
| PR #70/#71 individual workflows and threat-model specs | Do not mass-delete or mass-port | Many focus on distinct failure classes. Audit whether each is a distinct guarantee and whether the aggregate gate invokes it. |
| PR #72 as an independent integration unit | Exclude as a standalone unit | One-file corrective branch with a failed workflow; relevant test corrections are already represented in the #73 candidate head and must be verified there. |

### Next technical step

Create a fresh integration candidate from the current `main` SHA, then reapply the smallest dependency-complete set for (1) full-system authority validation and (2) Core Conformance. Include API v1 only after the API dependency group and authority contract are reviewed together. Run the exact focused tests and aggregate gate on that candidate. Do not merge PR #70–#73 while this candidate is being prepared.


## Follow-up implementation candidate (2026-10-12)

A fresh branch from current `main` was created to test the dependency-complete Full-System Authority Chain without importing the whole #71/#73 branches:

- Candidate PR: #85, `integration/full-system-authority-minimal-v0.1` → `main`.
- Candidate head at initial verification: `93a0067eeef4a039dbfd18df8ad2d316bb2a2819`.
- Scope: 18 runtime modules forming the import dependency closure, one focused test file, the chain specification, and one focused workflow (21 files total).
- Explicit exclusions: API v1 files, aggregate Core Conformance runner, unrelated threat-model layers, and the conflicting copy of `docs/PROGRESS_MAP.md`.
- Focused workflow result on that candidate SHA: **168 passed**; workflow conclusion **success**.
- Other repository workflows triggered on the same push were not treated as proof of this chain's correctness. At the time of this note, Codex Handoff Consumer Verification was still in progress.
- This is evidence that the isolated chain and its focused tests execute on current `main`; it is not evidence that the entire kernel has been re-certified, nor that the chain provides production-grade cryptographic or real-world identity assurance.

### Decision boundary

Do not merge #85 automatically. Review whether this extra composition boundary is warranted given the existing completed core-conformance milestone. If accepted, integrate the narrow chain first; only then assess whether one aggregate conformance runner is needed. Do not pull in API v1 or the remaining #70/#71 threat-model suite merely to increase the file or test count.
