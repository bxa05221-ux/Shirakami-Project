# Cooperative Showcase Candidate Registry v0.1

Status: private planning artifact — candidate inventory only.

This registry records possible external projects for a future `shirakami-showcase`. Listing a project does not imply consent, endorsement, partnership, license compatibility, or planned publication.

## Candidate intake rule

Before any code is copied, forked, vendored, or redistributed:

1. Confirm the exact upstream repository.
2. Identify the applicable license from the repository's authoritative files/metadata.
3. Record the version or commit.
4. Determine whether the intended integration requires copying, linking, forking, or only an adapter.
5. Preserve attribution and required notices.
6. Separate upstream code from Shirakami-authored code.
7. Run the publication/IP Human Gate.

## Initial candidates observed

| Candidate | Upstream | Initial role | License status | Current action |
|---|---|---|---|---|
| dbunt1tled profile repository | `dbunt1tled/dbunt1tled` | GitHub/profile-context experiment candidate | Not verified from a LICENSE file | Observe; no copying |
| GitHub Badge Sandbox | `MaxCode917/github-badge-sandbox` | GitHub automation/showcase candidate | Not verified from a LICENSE file | Observe; no copying |
| Amazing Frontend Design | `shinobi-coder701/amazing-frontend-design` | UI/showcase candidate | README displays an MIT badge, but authoritative LICENSE file was not found during this check | Verify before reuse |

## Important distinction

A repository being public does **not** by itself mean its code may be copied or redistributed.

The showcase should prefer:

```
Upstream repository
      ↓
Reference / pinned dependency
      ↓
Shirakami adapter
      ↓
Integration test
      ↓
Evidence / provenance
```

rather than cloning entire repositories into a new combined codebase.

## Provenance record template

For each accepted candidate:

```yaml
upstream:
  repository: ""
  owner_or_project: ""
  license: ""
  version_or_commit: ""
  source_url: ""

integration:
  method: adapter | dependency | fork | vendored
  shirakami_code: ""
  modifications: ""

review:
  license_checked: false
  ip_checked: false
  human_gate: false
  publication_authorized: false
```

## Current conclusion

The three candidates above are useful as **observed examples**, but none is currently authorized for code incorporation into a public showcase.

The next concrete showcase work should begin only after the upstream/license/provenance record is complete.
