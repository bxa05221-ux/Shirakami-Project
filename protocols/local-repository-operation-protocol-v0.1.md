# Shirakami Local Repository Operation Protocol v0.1

## Purpose

This protocol defines the operational boundary between Human, ChatGPT, Codex, the Local Repository, and GitHub.

The purpose is not to remove GitHub from Shirakami development, but to prevent the remote repository from becoming the only working memory of the project.

> Local Repository is the operational source of truth.
> GitHub is the public, review, and synchronization layer.

## Core Pipeline

```text
Human
  ↓
Protocol / Evidence / Semantic Handoff
  ↓
ChatGPT
  ↓
Local Repository
  ↓
Codex
  ↓
Verification
  ↓
Git Commit
  ↓
GitHub
  ↓
Review / Release / Public Evidence
```

## 1. Source of Truth

During active development, the Local Repository is the operational source of truth.

The Local Repository contains:

- current implementation
- tests
- protocol files
- Evidence references
- project state
- development configuration

GitHub is not required for every development operation.

GitHub remains the authoritative public record for committed and published project history.

## 2. Human Gate

Human judgment remains the controlling authority.

The protocol must not allow ChatGPT or Codex to silently:

- redefine project objectives
- replace a Protocol with an inferred requirement
- promote an unverified observation to Evidence
- merge or publish a consequential change without the required human gate

## 3. ChatGPT Role

ChatGPT primarily handles:

- project-level reasoning
- Protocol design
- Evidence interpretation
- Semantic Handoff
- architecture and specification
- review preparation
- change proposals

ChatGPT should prefer the Local Repository state supplied through the project workspace when available, rather than repeatedly reconstructing project state from GitHub.

## 4. Codex Role

Codex primarily handles repository-local implementation work.

A Codex task should identify:

- target repository state
- applicable Protocol
- relevant Evidence IDs
- requested change
- verification procedure
- expected artifacts

Codex may inspect, modify, test, and locally validate the repository within the authorized scope.

Codex output is an implementation result, not automatic project approval.

## 5. GitHub Role

GitHub is used for:

- public distribution
- commit history
- pull requests
- external review
- release/reference points
- synchronization with the operational repository

Routine repository inspection should not require GitHub access when the required state already exists locally.

## 6. Project State

The Local Repository should contain a machine-readable project state file when practical.

Recommended path:

`SHIRAKAMI_STATE.yaml`

Example:

```yaml
project:
  phase: "Phase 2"
  status: "active"

source_of_truth:
  operational: "local_repository"
  public_record: "github"

current_focus:
  - "Evidence ID"
  - "Semantic Handoff"
  - "API boundary"

verification:
  rule: "一変更一検証"
```

The state file is a coordination artifact. It does not replace detailed Protocol or Evidence records.

## 7. Semantic Handoff

When work moves between ChatGPT, Codex, Local Repository, and GitHub, the handoff should preserve:

- project identity
- current objective
- relevant Protocol
- Evidence IDs
- repository state
- requested change
- verification scope
- unresolved questions

The handoff unit is the project-defined 的目YAML / Semantic Handoff record.

## 8. Evidence Traceability

Every consequential implementation change should be traceable, where practical, through:

```text
Evidence ID
   ↓
Semantic Handoff
   ↓
Change
   ↓
Verification
   ↓
Commit
   ↓
Published Evidence
```

A commit does not itself prove that the change is correct.

## 9. Verification

The default rule is:

> 一変更一検証

At minimum:

1. identify the change
2. execute the relevant verification
3. record the observed result
4. identify deviations
5. update Evidence or project state when required

A wider overview verification may follow individual change verification.

## 10. GitHub Synchronization

GitHub synchronization should occur after local verification, unless the task specifically concerns GitHub itself.

Recommended sequence:

```text
Local change
  ↓
Local verification
  ↓
Evidence update
  ↓
Commit
  ↓
Push / PR
  ↓
External review
```

## 11. Failure and Recovery

If Local Repository state and GitHub state diverge:

1. do not silently choose one
2. identify the commit / version of each state
3. compare the changes
4. preserve Evidence and Semantic Handoff context
5. resolve the divergence through a human-controlled decision
6. re-run verification after reconciliation

## 12. Reviewer Boundary

A reviewer may use GitHub as the public inspection surface.

The Reviewer Protocol should identify:

- repository
- commit
- Protocol version
- Evidence
- verification method

The existence of a local operational source does not reduce the reviewability of the public repository.

## Non-Goals

This protocol does not:

- replace GitHub
- require a specific IDE or coding agent
- declare Codex authoritative
- make Local Repository immutable
- automate human approval
- treat successful tests as proof of the entire Shirakami theory

## Relationship to Existing Protocols

```text
Shirakami Project Protocol
│
├─ Core Runtime Protocol
├─ Evidence Protocol
├─ Semantic Handoff Protocol
├─ Reviewer Protocol
└─ Local Repository Operation Protocol
```

The Local Repository Operation Protocol defines the operational boundary. It does not replace the other protocols.

## Design Principle

> Work locally. Verify locally. Publish deliberately.

The project should minimize unnecessary remote reconstruction while preserving public reproducibility, Evidence traceability, and human control.
