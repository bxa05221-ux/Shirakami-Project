# Cooperative Showcase Provenance Schema v0.1

## Status

- status: draft
- purpose: Define a minimal provenance record for each cooperative showcase item.
- publication: not authorized by this schema alone.
- repository creation: not authorized by this schema alone.
- IP review: required before public release.

## 1. Design Principle

A showcase item must preserve the identity of the upstream project while making the Shirakami integration boundary explicit.

The record answers:

1. Who created the upstream work?
2. Which exact version was used?
3. What license governs it?
4. How was it integrated?
5. Which part was added or modified by Shirakami?
6. What execution or verification evidence exists?
7. Has license/IP review and Human Gate been completed?

## 2. Canonical Record

The following YAML is the normative minimal shape for v0.1:

```yaml
showcase_item:
  id: "<stable-item-id>"

  upstream:
    repository: "<owner>/<repository>"
    source_url: "<canonical-source-url>"
    author_or_project: "<upstream-author-or-project>"
    commit: "<pinned-commit-or-version>"
    license:
      name: "<verified-license>"
      source: "<license-file-or-authoritative-source>"
      verified: false

  integration:
    method: "adapter"
    shirakami_component: "<adapter-or-integration-component>"
    upstream_code_copied: false
    shirakami_code_added: true
    modifications_documented: true

  provenance:
    upstream_identity_preserved: true
    upstream_code_distinguishable: true
    shirakami_code_distinguishable: true
    endorsement_claimed: false

  verification:
    execution_observed: false
    evidence_recorded: false
    evidence_reference: null
    reproducibility_checked: false

  publication:
    license_review: "pending"
    ip_review: "pending"
    human_gate: "pending"
    publication_authorized: false
```

## 3. Field Rules

### upstream

The upstream section identifies the source work.

- `repository` is required.
- `source_url` must point to the canonical upstream location.
- `author_or_project` records attribution.
- `commit` or an equivalent immutable version should be pinned whenever technically possible.
- `license.name` must be verified from an authoritative source before reuse or redistribution.
- Public availability does not by itself establish permission to copy or redistribute code.

### integration

The integration section describes the relationship between upstream and Shirakami.

Preferred methods:

- adapter
- connector
- pinned dependency
- documented external reference

Copying an entire upstream repository is not the default integration method.

If upstream code is copied, the copied material must remain clearly attributable and its license obligations must be recorded.

### provenance

Provenance must remain visible after integration.

The showcase must not make upstream work appear to have been authored by Shirakami.

No endorsement, partnership, or official relationship may be implied without explicit authorization.

### verification

Verification records what actually happened during execution.

Evidence is observational. It does not grant authority to the runtime, upstream project, adapter, or model.

Where applicable, evidence should connect:

`Runtime → Observation → Evidence → Verification → AIwitness → Human Gate`

### publication

Publication is a separate decision.

All three gates are independent:

- `license_review`
- `ip_review`
- `human_gate`

A record with any pending gate is not a public-release authorization.

## 4. Example: Adapter-Based Integration

```yaml
showcase_item:
  id: "example-github-agent"

  upstream:
    repository: "example/project"
    source_url: "https://github.com/example/project"
    author_or_project: "Example Project"
    commit: "abc1234"
    license:
      name: "MIT"
      source: "LICENSE"
      verified: true

  integration:
    method: "adapter"
    shirakami_component: "ExampleAgentAdapter"
    upstream_code_copied: false
    shirakami_code_added: true
    modifications_documented: true

  provenance:
    upstream_identity_preserved: true
    upstream_code_distinguishable: true
    shirakami_code_distinguishable: true
    endorsement_claimed: false

  verification:
    execution_observed: true
    evidence_recorded: true
    evidence_reference: "evidence://example-run-001"
    reproducibility_checked: true

  publication:
    license_review: "approved"
    ip_review: "approved"
    human_gate: "approved"
    publication_authorized: true
```

The example is illustrative only and does not authorize incorporation of the named placeholder project.

## 5. Relationship to the Forest Principle

The provenance record is the metadata layer of the Shirakami forest model.

- Upstream projects remain identifiable trees.
- Adapters define the paths between trees.
- Evidence records what happened in the forest.
- Provenance records where each component came from.
- Human Gate controls whether an artifact enters the public forest.

A forest is not a single tree.

## 6. Non-Goals

This schema does not:

- establish patentability or novelty;
- grant permission to use third-party code;
- establish an official partnership;
- authorize publication;
- authorize repository creation;
- replace individual license review;
- replace IP review;
- transfer authority from a human to an AI runtime.

## 7. Review Sequence

`Candidate → License Verification → Version Pinning → Integration Design → Minimal Integration → Provenance Record → Execution/Evidence → License/IP Review → Human Gate → Publication`

When uncertainty remains, the item stays pending.

---

**Shirakami principle:**  
**AI may move. Authority does not move.**
