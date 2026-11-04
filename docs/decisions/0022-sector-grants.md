# ADR-0022: Sector-level grants with organizational attribute verification

- Status: deferred
- Date: 2026-08-24 (proposed), deferred on 2026-11-02
- Satisfies: [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel), [P-16](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: reference architecture v0.6.2, authorization models analysis §9.5 (archived and unpublished), [F-36](../traceability/findings-closed.md#f-36), [SL-05](../traceability/increments.md#sl-05)
- Implemented in: not implemented. gbo-demo removed the `sector-pip` scaffolding ([#378](https://github.com/ICTU/GBO-demo/issues/378), [CHANGELOG](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L779-L786)).

## Why deferred

In gbo-demo v0.9.0, admission runs through the Admission register
and the contract decision of the PDP
([REQ-61](../requirements/admission.md#req-61),
[ADR-0015](0015-contract-acceptance-by-policy.md)). No component called
the sector PIP, so the demo removed it. A sector grant is not a native
FSC concept ([F-36](../traceability/findings-closed.md#f-36)). The proposal
stays in the log for one case: per-organization admission does not
scale. Work on it starts only after a new decision.

## Context and problem statement

PKI proves which organization calls (OIN). PKI does not prove what kind
of organization it is. Per-organization contracts do not scale to
sectors. For example, 800 notariskantoren need 800 contracts with each
source.

## Proposed decision (deferred)

The proposal extends contract acceptance and token issuance with
organizational attributes:

- Sector PIPs (KvK SBI, KNB, BIG, AFM) verify sector membership.
- A sector-level grant type expresses "this sector may use this
  service".
- The access token carries verified sector claims.

This proposal builds on contract acceptance by policy
([ADR-0015](0015-contract-acceptance-by-policy.md)). The autosign input
then must carry more than peer IDs.

## Open points

The proposal leaves three points open:

- An extension of the FSC grant schema, through the Logius standards
  process.
- The freshness of sector register data, and the liability for it.
- The relation with the Admission register: admission versus
  membership.

## Traceability

- Requirements: [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62)
- Findings: [F-36](../traceability/findings-closed.md#f-36) (resolved in demo), [F-56](../traceability/findings-closed.md#f-56) (closed)
- Open questions: none
- Demo increments: [SL-05](../traceability/increments.md#sl-05) (done)
