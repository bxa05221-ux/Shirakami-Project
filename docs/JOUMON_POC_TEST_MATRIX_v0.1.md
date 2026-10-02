# JOUMON PoC Test Matrix v0.1

| ID | Test | Expected result | Status |
|---|---|---|---|
| J-P01 | Same Context sent to Runtime A and B | Same `context_id` | planned |
| J-P02 | Same Protocol sent to Runtime A and B | Same `protocol_id` | planned |
| J-P03 | Runtime provenance | Each Evidence record identifies its runtime | planned |
| J-P04 | Evidence authority | Evidence remains `non-authoritative` | planned |
| J-P05 | Human Gate | Final decision authority remains `human` | planned |
| J-P06 | Runtime replacement | A can be replaced by B without changing Context/authority semantics | planned |
| J-P07 | Provider neutrality | Canonical Context contains no provider-specific requirement | planned |
| J-P08 | Credential isolation | No secrets appear in fixtures or evidence | planned |
| J-P09 | Deterministic baseline | Mock adapters produce reproducible outputs | planned |
| J-P10 | Verification trace | Each execution can be traced from Context to Evidence to Human Gate | planned |

## Pass criterion

The PoC is architecturally successful only when J-P01 through J-P10 pass.

This matrix measures boundary preservation, not model quality.

## Evidence rule

A test result is evidence about the implementation run. It is not an authorization to publish, deploy, or transfer decision authority.
