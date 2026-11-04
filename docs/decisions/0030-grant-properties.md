# ADR-0030: Flow and subject identifier semantics as FSC grant properties

- Status: superseded by [ADR-0031](0031-regime-from-evidence.md)
- Date: 2026-09-07, superseded on 2026-11-02
- Satisfies: [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [D-08](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Supersedes: [ADR-0014](0014-provider-signed-flow-claims.md)
- Superseded by: [ADR-0031](0031-regime-from-evidence.md)
- Deliberation: [gbo-demo CHANGELOG, v0.6.11](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L839), and issues [#244](https://github.com/ICTU/GBO-demo/issues/244), [#277](https://github.com/ICTU/GBO-demo/issues/277), [#279](https://github.com/ICTU/GBO-demo/issues/279)
- Implemented in: removed from gbo-demo. [#334](https://github.com/ICTU/GBO-demo/issues/334) removed the `flow` property ([PR #363](https://github.com/ICTU/GBO-demo/pull/363)). [#473](https://github.com/ICTU/GBO-demo/issues/473) removed the `subject_id_type` property ([PR #475](https://github.com/ICTU/GBO-demo/pull/475)). In gbo-demo v0.9.0, the seeds create grants without properties ([CHANGELOG](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L787-L793)).

## Why superseded

The regime does not need a declaration. The regime follows from the
evidence that the request carries
([ADR-0031](0031-regime-from-evidence.md)):

- A consent proof puts the request in the consent regime.
- A request without a consent proof is in the PID regime.

After that change, no component read the `flow` property. The
`subject_id_type` property also lost its reader. The source gateway
takes the subject from the consent proof, and not from the contract
([ADR-0033](0033-gateway-decrypts-after-allow.md)). The demo removed both
properties. The following sections hold the original decision as
history.

## Context and problem statement

The PDP judges a request under an authorization regime. The regime has
two parts: the `flow`, and the way to read the subject identifier
(`subject_id_type`). The regime must be bound to the connection and
signed, and the caller must not control it.
[ADR-0014](0014-provider-signed-flow-claims.md) describes the mechanism
that this ADR replaced.

## Decision (superseded)

The decision put `flow` and `subject_id_type` as properties in the
`GRANT_TYPE_SERVICE_CONNECTION` grant of the FSC contract (fsc-core,
section Properties). It worked as follows:

- The properties are inside the grant, so they are part of the grant
  hash. Both peers countersign the regime when they sign the contract.
- The Manager of the provider puts the properties in the access token,
  as the FSC-normative `prp` claim.
- The PDP request mapper reads the flow from `prp` only. It uses no
  header and no default.
- If a token has no `prp`, the flow is empty. An empty flow matches no
  rule, so the PDP denies with `NO_APPLICABLE_RULE`.
- The source gateway reads `subject_id_type` from the same claim.

The demo seeded three property sets:

| Contract | Properties |
|---|---|
| EDI issuer → data services (`bri`, `brp`) | `{"flow": "eudi:attestation", "subject_id_type": "direct"}` |
| Hypotheekverlener → `bri` | `{"flow": "dvtp:query", "subject_id_type": "pseudonym"}` |
| EDI issuer → metadata services | `{"flow": "gbo:source-metadata"}` (not subject-bound) |

## Consequences (at the time)

The decision had these consequences:

- The provider needed no mapping file and no extra service. The contract
  was the single source of truth for the regime.
- Contracts are immutable, so a regime change meant a new contract. The
  seed scripts matched on properties and moved the grant link to the new
  contract.
- Every peer on a contract needed OpenFSC 2.0 or later. If the contract
  of a peer carried no properties, the PDP denied the peer until a new
  seed.
- If `subject_id_type` was missing, the fail-safe default of the source gateway
  was `direct` (pass-through). If the flow was missing, the default of
  the PDP was deny. This difference was safe, because the PDP decided
  first.

## Traceability

- Requirements: [REQ-74](../requirements/authorization.md#req-74)
- Findings: [F-32](../traceability/findings-closed.md#f-32) (resolved in demo), [F-43](../traceability/findings-closed.md#f-43) (superseded), [F-62](../traceability/findings-closed.md#f-62) (resolved in demo), [F-70](../traceability/findings.md#f-70) (open)
- Open questions: [Q-15](../traceability/answered-questions.md#q-15) (answered)
- Demo increments: [SL-24](../traceability/increments.md#sl-24) (dropped), [SL-48](../traceability/increments.md#sl-48) (done)
