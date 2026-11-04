# ADR-0003: FSC for all domestic connectivity

- Status: accepted
- Date: 2026-08-24 (ported from the reference architecture, updated 2026-11-02 for REQ-46 and the ASIP peer, gbo-demo v0.9.0)
- Satisfies: [D-03](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel), [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) (trust through recognized admission and trust anchors)
- Deliberation: Reference architecture v0.6.2, decision 6 (archived and unpublished), [REQ-46](../requirements/sources-identity.md#req-46)
- Implemented in: [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml) (OpenFSC v2.4.0 group: a directory peer and nine organization peers, among them the ASIP peer `…1200` at [#L1664-L1669](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L1664-L1669)). Each channel has its own Outway in [dienstverlener-backend/main.go#L82](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/main.go#L82), [eudi-adapter/main.go#L115](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L115), and [asi-provider/main.go#L83-L85](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L83-L85).

## Context and problem statement

Bronhouders must implement one connectivity stack for all routes,
and not one stack for each route.

## Decision

FSC (Federated Service Connectivity) carries all domestic traffic. FSC
gives these functions:

- mTLS with group certificates
- contracts with grant hashes
- access tokens from the Manager of the provider
- transaction logs for each hop

A channel that calls a source for an external party uses its own FSC
Outway with a valid certificate
([REQ-46](../requirements/sources-identity.md#req-46)). FSC establishes the
identity of the calling organization. The authorization of each request
stays a separate layer ([ADR-0031](0031-regime-from-evidence.md)).

External protocols end at the edge of GBO:

- A bridge at the edge translates cross-border OOTS traffic to FSC
  ([ADR-0020](0020-as4-bridge-for-oots.md)).
- Wallet protocols end at the EUDI chain
  ([ADR-0018](0018-eudi-disclosure-issuance.md)). The EUDI adapter is an
  FSC consumer.
- QTSP protocols (ETSI TS 119 478 clause 6.1) end at the ASIP
  ([ADR-0037](0037-asi-oauth-front-door.md)). The QTSP is not an FSC
  participant. The ASIP is an FSC consumer with a peer of its own
  (`…1200`), so the source sees the ASIP as the actor.

## Consequences

- A bronhouder connects once (Inway plus contracts) and serves every
  route.
- The Inway is also the PEP
  ([ADR-0004](0004-federated-authorization.md)).
- No channel goes directly into a source service or into its
  authorization.
- FSC refuses a connection with an expired or revoked certificate.
  open-fsc checks revocation with a CRL cache. The Inway, the Outway, and
  the Manager each have a switch that turns this check off. That switch
  must stay on. The demo does not check the revocation behavior.
- FSC does not propagate W3C trace context. The correlation model of
  [ADR-0035](0035-w3c-trace-context.md) compensates for this.

## Open points

There is no decision on the time within which a certificate revocation or
a suspension takes effect
([Q-53](../traceability/open-questions.md#q-53)).

## Traceability

- Requirements: [REQ-46](../requirements/sources-identity.md#req-46)
- Open questions: [Q-53](../traceability/open-questions.md#q-53)
- Demo increments: [SL-34](../traceability/increments.md#sl-34),
  [SL-39](../traceability/increments.md#sl-39),
  [SL-42](../traceability/increments.md#sl-42)
