# Runtime view

The runtime view shows how the building blocks work together at runtime.
Each page covers one scenario or a small group of scenarios. Each page has
these parts:

- a sequence diagram with numbered steps,
- the data that each hop carries,
- the error and failure paths, with links to the tests in gbo-demo
  [v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0),
- the main observations, with links to requirements, findings, and open
  questions.

A *built* scenario is a scenario that gbo-demo v0.9.0 implements, with the
error paths that its page lists. A *design-level* scenario has no
implementation. A design-level page describes the intended sequence and
names the open points.

## Two planes

The scenarios fall into two planes:

- **Data plane.** A request reads source data about a citizen. Every
  request takes the same route
  ([ADR-0004](../decisions/0004-federated-authorization.md),
  [ADR-0002](../decisions/0002-opa-rego-authzen.md)), in this order:
    1. the FSC Outway of the consumer (afnemer),
    2. the FSC Inway of the source, as PEP,
    3. the PDP of the source,
    4. the source gateway,
    5. the source API.

    The scenarios differ in the evidence that the request carries.

- **Management plane.** No citizen data travels. The scenarios in this
  plane admit parties, take sources into use, and bring policy to the PDP.
  These scenarios come before the first request.

## Scenarios

| Scenario | Page | Route | Actor | Status | Main ADRs |
|---|---|---|---|---|---|
| Citizen grants consent | [DvTP consent](dvtp-consent.md) | DvTP | Citizen at a service provider (dienstverlener) | built | [0032](../decisions/0032-consent-proof.md), [0005](../decisions/0005-bsnk-pp.md), [0040](../decisions/0040-route-d-citizen-recognition.md) |
| Consumer requests data under consent, directly or through an integrator | [DvTP query](dvtp-query.md) | DvTP | Consumer or integrator | built | [0031](../decisions/0031-regime-from-evidence.md), [0032](../decisions/0032-consent-proof.md), [0033](../decisions/0033-gateway-decrypts-after-allow.md), [0034](../decisions/0034-integrator-delegation.md), [0013](../decisions/0013-pdp-request-mapper.md) |
| Citizen views and revokes consents | [DvTP citizen access](dvtp-citizen-access.md) | DvTP | Citizen | built | [0032](../decisions/0032-consent-proof.md), [0040](../decisions/0040-route-d-citizen-recognition.md) |
| Citizen receives an attestation (PuB-EAA route) | [EUDI issuance](eudi-issuance.md) | EUDI issuance | Citizen with a wallet | built | [0018](../decisions/0018-eudi-disclosure-issuance.md), [0016](../decisions/0016-source-owned-metadata.md), [0017](../decisions/0017-gbo-simple-v1.md), [0028](../decisions/0028-pubeaa-productization.md) |
| QTSP verifies or retrieves attributes | [ASI verification](asi-verification.md) | ASI verification | QTSP, citizen | built | [0037](../decisions/0037-asi-oauth-front-door.md), [0038](../decisions/0038-asi-data-service-per-source.md), [0039](../decisions/0039-asi-source-described-attributes.md), [0041](../decisions/0041-asi-seal-format.md) |
| Contract admission and source activation | [Admission and activation](admission.md) | all (management plane) | Consumer, FSC Manager of the provider, operator | built | [0015](../decisions/0015-contract-acceptance-by-policy.md), [0034](../decisions/0034-integrator-delegation.md), [0016](../decisions/0016-source-owned-metadata.md), [0023](../decisions/0023-identity-convergence.md) |
| Policy distribution | [Policy distribution](policy-distribution.md) | all (management plane) | Operator of the bronhouder | built (bundle mode is opt-in) | [0021](../decisions/0021-central-pap-signed-bundles.md), [0002](../decisions/0002-opa-rego-authzen.md) |
| Government consumer requests data under a legal basis | [Gov-to-Gov](design-level.md#gov-to-gov) | Gov-to-Gov | Government consumer | design-level | [0031](../decisions/0031-regime-from-evidence.md), [0004](../decisions/0004-federated-authorization.md) |
| Cross-border evidence request | [SDG-OOTS](design-level.md#sdg-oots) | SDG-OOTS | Competent authority in another member state | design-level | [0020](../decisions/0020-as4-bridge-for-oots.md), [0031](../decisions/0031-regime-from-evidence.md) |
| Citizen presents an attestation to a relying party | [Relying-party presentation](design-level.md#relying-party-presentation) | EUDI presentation | Citizen, relying party | design-level (no GBO runtime) | [0018](../decisions/0018-eudi-disclosure-issuance.md), [0028](../decisions/0028-pubeaa-productization.md), [0023](../decisions/0023-identity-convergence.md) |

## Routes {#trajectories}

A route is a path from a source to a party that uses the data. The
PDP of the source judges each request under one regime. The evidence in
the request selects the regime
([ADR-0031](../decisions/0031-regime-from-evidence.md),
[Authorization](../concepts/authorization.md#regime-selection)).

Three routes are built in gbo-demo v0.9.0:

- **DvTP.** A private consumer reads source data with the consent of the
  citizen. The request carries a signed consent proof, so the PDP uses
  the consent regime. The consumer never gets a BSN
  ([Consent](../concepts/consent.md)).
- **EUDI issuance.** The GBO issuance facility reads source data for a
  citizen who discloses a PID from the wallet. The request carries no
  consent proof, so the PDP uses the PID regime. The bronhouder is the
  PuB-EAA provider. GBO operates the technical facility
  ([ADR-0028](../decisions/0028-pubeaa-productization.md)).
- **ASI verification.** A QTSP verifies or retrieves attributes at the
  ASI provider (ASIP). The ASIP calls the source over FSC under the PID
  regime. The QTSP itself is not an FSC participant
  ([F-87](../traceability/findings.md#f-87)).

Three routes exist only at design level:

- **Gov-to-Gov.** A government consumer reads source data under a legal
  basis. The regime needs its own positive evidence. No rule set for this
  regime exists.
- **SDG-OOTS.** A competent authority in another member state requests
  evidence through the Once-Only Technical System. AS4 exists only at the
  edge. No implementation exists.
- **Relying-party presentation.** The citizen presents a wallet
  attestation to a relying party. No GBO decision component and no source
  take part.

## Data classification

The data-per-hop tables use the tags of the classification table in
[Consent: what travels where](../concepts/consent.md#what-travels-where).
That table gives each data item (for example the consent proof, VI, VP,
`subject_ref`, and BSN) a meaning, a sensitivity, and the hops where it
occurs. The runtime pages add only items that the table does not have,
for example contract proposals, admission records, and policy bundles.
Those items carry no citizen data.

The error tables give administrator codes. The consumer gets only a
coarse code ([REQ-06](../requirements/authorization.md#req-06),
[Authorization](../concepts/authorization.md#reason-codes-two-layers)).

## Traceability

- Requirements: [REQ-06](../requirements/authorization.md#req-06), [REQ-74](../requirements/authorization.md#req-74)
- Findings: [F-70](../traceability/findings.md#f-70) (open), [F-87](../traceability/findings.md#f-87) (open)
- Open questions: [Q-30](../traceability/open-questions.md#q-30) (open), [Q-79](../traceability/open-questions.md#q-79) (open)
- Demo increments: [SL-48](../traceability/increments.md#sl-48) (done)
