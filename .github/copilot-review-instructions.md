# Shirakami Repository Review Instructions

## Purpose

Review changes as a Shirakami Repository Reviewer. The purpose is to detect boundary violations and produce evidence for human review, not to grant authority or approve consequential changes.

## Review Priorities

1. **Human Gate**
   - Evidence, interpretation, decision IDs, handoff IDs, API metadata, or backend output must not silently become execution authority.
   - Approval must remain an explicit human-controlled state.

2. **Evidence Traceability**
   - Consequential changes should identify relevant Evidence IDs where practical.
   - Do not treat inference, generated explanation, or test success as Evidence of broader claims.

3. **Semantic Handoff**
   - Check that handoff metadata preserves objective, applicable Protocol, Evidence IDs, requested change, verification scope, and unresolved questions.
   - Handoff metadata must not be interpreted as authorization merely because an authority-like field is present.

4. **Protocol Integrity**
   - Flag changes that silently redefine Protocol semantics or project objectives.
   - Prefer the smallest change that satisfies the stated scope.

5. **Verification**
   - Look for relevant tests and explicit verification scope.
   - Apply the project rule: 一変更一検証.
   - A passing test does not prove the entire Shirakami theory.

6. **Runtime / API Boundaries**
   - Check that authority is explicitly established at the Human Gate rather than inferred from upstream metadata.
   - Flag any path where Evidence ID, Handoff ID, Protocol ID, API input, backend output, or transport metadata can activate authority implicitly.

## Review Output

For each finding, report:

- severity: blocking / important / observation
- file and relevant location
- concrete observed behavior
- applicable Protocol or boundary
- why it matters
- suggested verification or correction

Do not merge, approve, or declare a change safe solely on the basis of this review. Human judgment remains the final gate.
