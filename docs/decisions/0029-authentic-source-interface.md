# ADR-0029: Authentic Source Interface per ETSI TS 119 478

- Status: superseded by [ADR-0037](0037-asi-oauth-front-door.md)
- Date: 2026-08-24, superseded on 2026-11-02
- Satisfies: eIDAS Article 45e, [GO: verification and retrieval service for QTSPs](https://ictu.github.io/GBO-GO/main/#verificatie-en-retrievedienst-voor-qtsps-asi-provider), [PSA open decisions: central verification and retrieval service](https://ictu.github.io/GBO-PSA/main/vraagstukken/)
- Superseded by: [ADR-0037](0037-asi-oauth-front-door.md)
- Deliberation: reference architecture v0.6.2, gap 8 and ASI design (archived and unpublished)
- Implemented in: not implemented in this form. The built route is [ADR-0037](0037-asi-oauth-front-door.md).

## Why superseded

The demo built the Authentic Source Interface after this ADR
([SL-28](../traceability/increments.md#sl-28)). Three core points of this
proposal changed:

- Retrieve is implemented. The ASIP offers clause 6.1.2 next to 6.1.1.
  EUDI issuance does not replace retrieve, because the QTSP issues the
  QEAA, and GBO does not ([REQ-101](../requirements/asi.md#req-101),
  [REQ-112](../requirements/asi.md#req-112)).
- The QTSP is outside FSC. This proposal saw the ASI as a protocol
  adapter "in front of" the FSC chain. The ASI is an OAuth front door
  with its own trust model. The authorization server admits the QTSP, and
  the PDP does not. The generic chain starts behind the ASIP, which is an
  FSC peer of its own ([F-87](../traceability/findings.md#f-87)).
- Clause numbers replace the labels I1 to I5. The labels came from the
  reference architecture:
    - I1 is clause 5 (discovery).
    - I2 is 6.1.1 (verify).
    - I3 is 6.1.2 (retrieve).
    - I4 is 6.1.3 (authorization server).
    - I5 is citizen identification inside 6.1.3.

    The TO uses the ETSI clause numbers and roles.

[ADR-0037](0037-asi-oauth-front-door.md) records the decision that
replaces this ADR. [ADR-0038](0038-asi-data-service-per-source.md),
[ADR-0039](0039-asi-source-described-attributes.md),
[ADR-0041](0041-asi-seal-format.md), and
[ADR-0042](0042-asi-attribute-token-binding.md) record the details. The
following sections hold the original proposal as history.

## Context and problem statement

Article 45e of the amended eIDAS regulation obliges member states to let
QTSPs verify attributes against authentic sources at the request of the
user. ETSI TS 119 478 specifies the interfaces. Without this interface,
QTSPs cannot issue QEAAs based on Dutch government registers.

## Proposed decision

The proposal builds the ASI provider as a GBO edge service, in the
HTTP/OAuth variant:

- Implement I2 (Verify). The service translates verification requests
  into GraphQL queries over FSC, through the standard PEP-PDP chain, and
  compares the values.
- Implement I4 and I5: citizen authorization through OAuth, with a
  wallet or eID.
- Skip I3 (Retrieve), because the EUDI chain covers direct issuance
  ([ADR-0018](0018-eudi-disclosure-issuance.md)).
- Register the data services in the EU catalogue of attributes (I1).

## Open points

The proposal left these points open:

- The PDP policy set for QTSP verification (Trusted List check, citizen
  authorization, attribute scope).
- The design of the authorization server (I4), and its relation to the
  consent facility (toestemmingsvoorziening).
- The timeline pressure from the Article 45e deadline. For more
  information, see [Risks and technical debt](../risks.md).

## Traceability

- Requirements: [REQ-101](../requirements/asi.md#req-101),
  [REQ-112](../requirements/asi.md#req-112)
- Findings: [F-80](../traceability/findings.md#f-80) (open),
  [F-87](../traceability/findings.md#f-87) (open)
- Demo increments: [SL-28](../traceability/increments.md#sl-28)
