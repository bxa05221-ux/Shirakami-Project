# ECC → Shirakami Adapter Prototype

This directory defines an integration boundary between Affaan Mustafa's ECC and the Shirakami Language Protocol OS.

## Intent

ECC remains the runtime/harness layer. Shirakami remains the protocol and human-control layer.

```text
Landscape
   ↓
Context
   ↓
Protocol
   ↓
Evidence requirements
   ↓
Shirakami Adapter
   ↓
ECC Runtime / Skills / Agents / Hooks
   ↓
Observation
   ↓
AIwitness
   ↓
Verification
   ↓
Human Gate
```

The adapter MUST NOT turn ECC into a Shirakami authority layer. It exists to make runtime execution observable and replaceable.

## Upstream

- Upstream project: https://github.com/affaan-m/ECC
- Upstream owner: Affaan Mustafa
- Upstream license: MIT
- Upstream runtime status should be checked before each synchronization.

This prototype does not copy ECC source files into Shirakami-Project. It defines the boundary first, so upstream provenance and license obligations remain explicit.

## Design rules

1. Preserve ECC attribution and MIT license when distributing ECC-derived material.
2. Do not remove or rewrite upstream license notices.
3. Keep Shirakami-specific code clearly separated from upstream-derived code.
4. Treat ECC as replaceable runtime infrastructure.
5. Do not grant ECC, an agent, or an LLM final decision authority.
6. Record execution facts separately from interpretation.
7. Require Human Gate before consequential decisions.
8. Preserve Context, Evidence, and Provenance across handoff.

## Proposed adapter contract

Input:

- `context`
- `protocol`
- `evidence_requirements`
- `human_constraints`

Runtime output:

- `observation`
- `execution_trace`
- `artifacts`
- `verification_status`
- `uncertainties`

The adapter returns execution evidence; it does not return a final human decision.

## License boundary

Shirakami-specific adapter material is governed by the license declared by the Shirakami repository.

ECC-derived material remains subject to the ECC MIT license and its notice requirements. Dependencies may have separate licenses and must be tracked independently.

This directory is therefore intentionally an integration specification/prototype rather than a wholesale copy of ECC.
