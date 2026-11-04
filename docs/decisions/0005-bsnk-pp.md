# ADR-0005: BSNk PP polymorphic pseudonyms for private-sector access

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: BSNk only at consent time)
- Satisfies: [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering), [PSA vraagstukken: keuze BSNk PP](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister)
- Deliberation: Reference architecture v0.6.2, decision 4 (archived and unpublished), [BSNk preconditions](../requirements/pseudonymization.md#bsnk-preconditions), [F-75](../traceability/findings.md#f-75), demo [#364](https://github.com/ICTU/GBO-demo/issues/364), [PR #469](https://github.com/ICTU/GBO-demo/pull/469), [PR #477](https://github.com/ICTU/GBO-demo/pull/477)
- Implemented in: [consent-portal-backend/bsnk](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/bsnk/bsnk.go) (activate, transform, BSN authorization list), [consent/portal.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L194-L202) (values per party), [services/bsnk-mock](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bsnk-mock/README.md) (mock of the BSNk interface, also the sources' decryption component)

## Context and problem statement

Private parties are not allowed to process the BSN. But DvTP lets them
request data from government sources about a specific citizen. Plain
encryption of the BSN still gives them a universal correlation key.

## Decision

GBO uses the BSNk PP polymorphic pseudonym infrastructure and calls it
only at consent time. The decision has these parts:

- The consent service activates the BSN of the citizen once, into a PI
  and a PP. These belong to the consent service only
  ([BSNK-03](../requirements/pseudonymization.md#bsnk-03)).
  [ADR-0040](0040-route-d-citizen-recognition.md) (proposed) describes how
  the consent service recognizes the citizen later.
- At each consent, while the citizen is logged in
  ([BSNK-04](../requirements/pseudonymization.md#bsnk-04)), the consent
  service asks BSNk to transform the PI and the PP. BSNk returns values
  for each recipient OIN:
    - an encrypted pseudonym (VP) for every source
    - an encrypted identity (VI) only for a source on the BSN
      authorization list
      ([BSNK-06](../requirements/pseudonymization.md#bsnk-06))
- The consent service splits the call into requests of four parties at
  most ([BSNK-05](../requirements/pseudonymization.md#bsnk-05)).
- The values travel in the consent proof
  ([ADR-0032](0032-consent-proof.md)). After the allow, each recipient
  decrypts its own value locally, with its own keys
  ([ADR-0033](0033-gateway-decrypts-after-allow.md)).
- BSNk is not in the query path. The consumer gets no identifier.

## Consequences

- The values of different parties cannot be linked. No party outside
  government can derive the BSN.
- The consent service must be a recognized BSNk participant
  ([BSNK-01](../requirements/pseudonymization.md#bsnk-01),
  [F-75](../traceability/findings.md#f-75),
  [Q-26](../traceability/open-questions.md#q-26)).
- At consent, the parties, the key versions, and the form of the proof
  become fixed for the whole validity period
  ([F-78](../traceability/findings.md#f-78)).
- Every recipient needs its keys in advance, as a step of admission
  ([BSNK-09](../requirements/pseudonymization.md#bsnk-09),
  [#467](https://github.com/ICTU/GBO-demo/issues/467)).
- A pseudonym for the consumer itself is optional. The demo does not
  build it ([#478](https://github.com/ICTU/GBO-demo/issues/478),
  [Q-01](../traceability/open-questions.md#q-01)).
- The demo mock follows the BSNk interface, but uses JSON instead of SOAP
  ([BSNK-11](../requirements/pseudonymization.md#bsnk-11)). The mock
  enforces the requester-only PI, the BSN authorization list, and the
  four-party limit. The mock does not encrypt, so anyone can read the
  values. The three demo sources share one OIN and one decryption
  component.
- For the identifier flow at each boundary, see
  [Pseudonymization](../concepts/pseudonymization.md).

## Traceability

- Requirements: [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-80](../requirements/pseudonymization.md#req-80), [REQ-82](../requirements/pseudonymization.md#req-82), [BSNK-01](../requirements/pseudonymization.md#bsnk-01), [BSNK-03](../requirements/pseudonymization.md#bsnk-03), [BSNK-04](../requirements/pseudonymization.md#bsnk-04), [BSNK-05](../requirements/pseudonymization.md#bsnk-05), [BSNK-06](../requirements/pseudonymization.md#bsnk-06), [BSNK-09](../requirements/pseudonymization.md#bsnk-09), [BSNK-11](../requirements/pseudonymization.md#bsnk-11)
- Findings: [F-15](../traceability/findings-closed.md#f-15) (closed), [F-75](../traceability/findings.md#f-75) (open), [F-78](../traceability/findings.md#f-78) (open)
- Open questions: [Q-01](../traceability/open-questions.md#q-01) (partly answered), [Q-26](../traceability/open-questions.md#q-26) (open)
- Demo increments: [SL-02](../traceability/increments.md#sl-02) (done), [SL-51](../traceability/increments.md#sl-51) (done)
