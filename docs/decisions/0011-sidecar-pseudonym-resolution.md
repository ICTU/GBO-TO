# ADR-0011: Source-owned sidecar resolves pseudonyms, and the PDP never sees a BSN

- Status: superseded by [ADR-0033](0033-gateway-decrypts-after-allow.md)
- Date: 2026-08-24 (superseded 2026-11-02)
- Satisfies: [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Supersedes: [ADR-0010](0010-pep-bsn-resolution.md)
- Superseded by: [ADR-0033](0033-gateway-decrypts-after-allow.md)
- Deliberation: source sidecar de-pseudonymization ([SL-22](../traceability/increments.md#sl-22), [F-30](../traceability/findings-closed.md#f-30))
- Implemented in: changed in gbo-demo. The sidecar does not call BSNk and does not read `subject_id_type` any more ([PR #469](https://github.com/ICTU/GBO-demo/pull/469), [#473](https://github.com/ICTU/GBO-demo/issues/473)). The request mapper does not pseudonymize any more ([#364](https://github.com/ICTU/GBO-demo/issues/364)). Code in gbo-demo v0.9.0: [services/bron-sidecar](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar)

## Why superseded

The mechanism changed in three places:

- The sidecar does not call BSNk Transform at query time. It takes the
  value for its own OIN from the consent proof. The decryption component
  of the source reads this value.
- The sidecar acts when a consent proof is present. The demo removed the
  `subject_id_type` grant property
  ([ADR-0031](0031-regime-from-evidence.md)).
- The PDP request mapper does not pseudonymize a disclosed BSN any more.
  In the EUDI and ASI routes, the PDP input holds the plain BSN
  ([ADR-0043](0043-identifiers-out-of-pdp-input.md), proposed). So the
  claim "the PDP never sees a BSN" in the title is true only for the
  consent route.

For this reason, [ADR-0033](0033-gateway-decrypts-after-allow.md) records
the mechanism again. The resolution by the source after the allow stays.
The following sections keep the original decision as history.

## Context and problem statement

A component between the allow decision and the source API must resolve
the pseudonym to the BSN. Shared infrastructure must not get BSN
authorization. The BSN must not leak into policy inputs or logs.

## Decision (superseded)

A sidecar that the source owns sits between the Inway and the GraphQL API.
The sidecar does the resolution. It reads the `subject_id_type` claim from
the FSC access token:

- For `pseudonym`, it transforms the PI to the BSN through BSNk, with its
  own OIN. Then it substitutes the query variable.
- For `direct`, it passes the request through.

In addition, the PDP request mapper pseudonymizes any disclosed BSN (EUDI
flows) before policy evaluation. So the engine input and the decision log
contain only the PI.

## Consequences (at the time)

- Each role stays separate, in line with datasoevereiniteit:
    - The PEP stays a pure enforcement point.
    - The PDP does no data transformation.
    - Only the bronhouder holds BSN authority.
- The meaning of the identifier is a grant property that both peers
  countersign ([ADR-0030](0030-grant-properties.md)). So a caller cannot
  choose how the source interprets its subject identifier.
- A pseudonym that cannot be resolved is a hard error (HTTP 400). The
  fail-safe default is pass-through (`direct`).

## Traceability

- Requirements: [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-60](../requirements/logging-audit.md#req-60)
- Findings: [F-30](../traceability/findings-closed.md#f-30) (resolved in demo), [F-37](../traceability/findings-closed.md#f-37) (resolved in demo), [F-54](../traceability/findings.md#f-54) (open)
- Open questions: none
- Demo increments: [SL-02](../traceability/increments.md#sl-02) (done), [SL-22](../traceability/increments.md#sl-22) (done), [SL-29](../traceability/increments.md#sl-29) (done)
