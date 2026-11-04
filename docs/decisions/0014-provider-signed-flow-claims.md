# ADR-0014: Flow and subject identifier semantics through a provider-side Additional Claims service

- Status: superseded by [ADR-0030](0030-grant-properties.md), which [ADR-0031](0031-regime-from-evidence.md) supersedes in turn
- Date: 2026-08-24
- Satisfies: [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Deliberation: [gbo-demo CHANGELOG, v0.6.11](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L839), [F-62](../traceability/findings-closed.md#f-62)
- Implemented in: removed from gbo-demo in v0.6.11 (September 2026)

## Context and problem statement

The PDP selects rules by the flow of the request (`dvtp:query`,
`eudi:attestation`, `gbo:source-metadata`). The source gateway interprets the
subject identifier (`pseudonym` or `direct`). If callers supply these
values as headers, a caller can choose the authorization regime that
applies to its request.

## Decision (superseded)

An Additional Claims service that the provider owned mapped each validated
connection grant `(outway peer, service peer, service name)` to an `add`
claim object. The FSC Manager of the provider signed this object into the
access token. The PDP mapper and the source gateway read only the `add` claim.

## Why it was superseded

The mechanism was a workaround for a version limit. The simulation
environment ran OpenFSC v1.44, which is older than grant properties. The
mechanism had two costs:

- Only the provider signed the regime. The consumer never countersigned
  it.
- The mapping file from grants to claims was outside the contracts.
  People had to maintain it by hand, and it broke twice during the
  Peer-ID migration.

When OpenFSC v2.4.0 became available, the regime moved into the contract
itself, as FSC-normative grant properties. For this design, see
[ADR-0030](0030-grant-properties.md).

## Traceability

- Requirements: [REQ-74](../requirements/authorization.md#req-74)
- Findings: [F-32](../traceability/findings-closed.md#f-32) (resolved in demo), [F-45](../traceability/findings-closed.md#f-45) (closed), [F-62](../traceability/findings-closed.md#f-62) (resolved in demo)
- Open questions: [Q-15](../traceability/answered-questions.md#q-15) (answered)
- Demo increments: [SL-48](../traceability/increments.md#sl-48) (done)
