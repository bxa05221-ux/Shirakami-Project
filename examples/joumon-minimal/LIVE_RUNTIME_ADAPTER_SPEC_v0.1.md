# JOUMON Live Runtime Adapter Boundary v0.1

status: experimental

## Purpose

Define the smallest boundary required to replace a mock Runtime with a live provider without coupling JOUMON to a vendor SDK.

## Contract

The protocol layer supplies:
- Context ID
- Protocol ID
- task/context description

The injected provider callable returns an observation string.

The adapter records:
- runtime identity
- provider identity
- mode=live
- runtime type
- Context identity

## Boundary

    JOUMON Protocol
          |
          v
    LiveRuntimeAdapter
          |
          v
    injected provider callable / SDK

Provider credentials, network transport and SDK-specific request/response formats remain outside the protocol core.

## Important limitation

This file defines a live boundary but does not claim that a real provider has been executed. A real adapter must supply its own authenticated callable and must be tested separately.

## Invariant

Changing the provider implementation must not require changing Context, Protocol, Evidence, Lineage, Semantic Handoff or Human Gate semantics.
