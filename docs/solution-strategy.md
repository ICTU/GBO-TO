# Solution strategy

The design rests on the pillars in the following tables. Each pillar links
to the decisions that record its rationale and to the page that gives the
details. The pillars realize the
[capabilities](https://ictu.github.io/GBO-PSA/main/capabilities/) of the
PSA within the solution shape of the
[GO](https://ictu.github.io/GBO-GO/main/#5-te-ontwikkelen-componenten).
gbo-demo [v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0) implements
every pillar that is marked "built".

## The generic chain

| Pillar | Approach | Decisions | Detail |
|---|---|---|---|
| Data access | Each bronhouder has one GraphQL API. The query is the authorization object. | [ADR-0001](decisions/0001-graphql-source-access.md), [ADR-0025](decisions/0025-graphql-fds-datadienst.md) | [Building blocks](building-blocks/components.md) |
| Connectivity | All domestic traffic uses FSC. Protocol adapters at the edge handle all other traffic. | [ADR-0003](decisions/0003-fsc-connectivity.md) | [Deployment view](deployment.md) |
| Authorization | The FSC Inway is the PEP. OPA/Rego in OpenFTV is the PDP, behind AuthZEN with the FTV GraphQL profile. Authorization has five separable concerns and one PDP per source holder. There is no central authorization server. Rules are plain Rego, bound by regime, FSC service, and field. | [ADR-0002](decisions/0002-opa-rego-authzen.md), [ADR-0004](decisions/0004-federated-authorization.md), [ADR-0009](decisions/0009-closed-world-rules.md), [ADR-0013](decisions/0013-pdp-request-mapper.md) | [Authorization](concepts/authorization.md) |
| Regime from evidence | The evidence that a request carries selects the regime. A consent proof gives the consent regime. Without a consent proof, the PID regime applies. Grants carry no properties. | [ADR-0031](decisions/0031-regime-from-evidence.md) | [Regime selection](concepts/authorization.md#regime-selection) |
| Admission | A register admits parties. The decision policy does not admit parties. A separate policy decides on FSC contracts. An integrator connects under FSC delegation with a registered mandate. | [ADR-0015](decisions/0015-contract-acceptance-by-policy.md), [ADR-0034](decisions/0034-integrator-delegation.md) | [Admission and activation](runtime/admission.md) |
| Policy management | Each source holder manages and distributes its own policy. GBO supplies a reference policy set and guidelines (RL-01 to RL-05). GBO does not supply a central PAP. | [ADR-0021](decisions/0021-central-pap-signed-bundles.md) | [Policy lifecycle](concepts/policy-lifecycle.md) |
| Source onboarding | Sources publish their own service description. A reconciler validates the description, and an operator activates it. A valid contract alone does not activate a source. | [ADR-0016](decisions/0016-source-owned-metadata.md) | [Source onboarding](concepts/source-onboarding.md) |

## Consent and pseudonymization (DvTP)

| Pillar | Approach | Decisions | Detail |
|---|---|---|---|
| Consent proof | A signed consent proof carries an encrypted value per source. The consumer names the subject with a placeholder. For every request, the policy verifies the proof and asks for the status online over FSC. | [ADR-0032](decisions/0032-consent-proof.md) | [Consent](concepts/consent.md), [DvTP query](runtime/dvtp-query.md) |
| Pseudonymization | The design uses BSNk PP only at consent time. After the allow decision, the source gateway decrypts the value for its own OIN. Only the FSC Inway reaches the gateway. The consent service recognizes the citizen by its own keyed reference (route D, proposed). | [ADR-0005](decisions/0005-bsnk-pp.md), [ADR-0033](decisions/0033-gateway-decrypts-after-allow.md), [ADR-0040](decisions/0040-route-d-citizen-recognition.md) | [Pseudonymization](concepts/pseudonymization.md) |

## EUDI routes

| Pillar | Approach | Decisions | Detail |
|---|---|---|---|
| EUDI issuance | Issuance is disclosure-based OpenID4VCI on the nl-wallet stack. Sources feed it over FSC under the PID regime. The bronhouder is the PuB-EAA provider, and GBO operates the facility. Built. The PSA treats wallet support (P-06) as a hook outside version 1. | [ADR-0018](decisions/0018-eudi-disclosure-issuance.md), [ADR-0017](decisions/0017-gbo-simple-v1.md), [ADR-0028](decisions/0028-pubeaa-productization.md) | [EUDI issuance](runtime/eudi-issuance.md) |
| ASI verification | An OAuth front door as specified in ETSI TS 119 478 clause 6.1 (verify, retrieve, authorization server). The QTSP is an OAuth client and does not take part in FSC. The design has one data service per authentic source and one token per data service. The source describes its ASI attributes. Built, demo grade. | [ADR-0037](decisions/0037-asi-oauth-front-door.md), [ADR-0038](decisions/0038-asi-data-service-per-source.md), [ADR-0039](decisions/0039-asi-source-described-attributes.md) | [ASI verification](runtime/asi-verification.md) |

## Audit and traceability

| Pillar | Approach | Decisions | Detail |
|---|---|---|---|
| Audit | The design has three authoritative records: the ADL for authorization decisions, the LDV logbook of each controller for processings, and FSC-Logging for transport. Observability tools are not audit records. | [ADR-0036](decisions/0036-adl-decision-record.md), [ADR-0026](decisions/0026-ldv-integration.md) | [Logging, audit and traceability](concepts/logging.md) |
| Traceability | W3C Trace Context is the correlation key. Each component records the FSC transaction ID next to the trace ID. | [ADR-0035](decisions/0035-w3c-trace-context.md) | [Correlation](concepts/logging.md#correlation-trace-id-and-transaction-id) |

## Design-level and proposed elements

Two strategy elements exist at design level only. Both reuse the generic
chain:

- The AS4 bridge for SDG-OOTS
  ([ADR-0020](decisions/0020-as4-bridge-for-oots.md)) is a protocol
  adapter in front of the same FSC and authorization chain.
- Gov-to-Gov needs its own positive evidence for the legal-basis regime
  ([ADR-0031](decisions/0031-regime-from-evidence.md)). No rule set
  exists for this regime ([R3](risks.md#r3)).

Four decisions have the status proposed. Each one waits for an open
question or a demo issue:

- [ADR-0040](decisions/0040-route-d-citizen-recognition.md), citizen
  recognition, waits for [Q-49](traceability/open-questions.md#q-49).
- [ADR-0041](decisions/0041-asi-seal-format.md), seal format of ASI
  results, waits for [Q-32](traceability/open-questions.md#q-32).
- [ADR-0042](decisions/0042-asi-attribute-token-binding.md), per-attribute
  token binding, waits for [Q-33](traceability/open-questions.md#q-33).
- [ADR-0043](decisions/0043-identifiers-out-of-pdp-input.md), identifiers
  out of the PDP input, waits for demo issue
  [#368](https://github.com/ICTU/GBO-demo/issues/368).

## Traceability

- Requirements: [REQ-17](requirements/authorization.md#req-17),
  [REQ-21](requirements/pseudonymization.md#req-21),
  [REQ-55](requirements/logging-audit.md#req-55),
  [REQ-61](requirements/admission.md#req-61),
  [REQ-64](requirements/sources-identity.md#req-64),
  [REQ-68](requirements/consent.md#req-68),
  [REQ-71](requirements/logging-audit.md#req-71),
  [REQ-72](requirements/logging-audit.md#req-72),
  [REQ-74](requirements/authorization.md#req-74),
  [REQ-80](requirements/pseudonymization.md#req-80),
  [REQ-97](requirements/authorization.md#req-97),
  [REQ-106](requirements/consent.md#req-106),
  [REQ-112](requirements/asi.md#req-112)
- Findings: [F-70](traceability/findings.md#f-70) (open),
  [F-79](traceability/findings.md#f-79) (open),
  [F-87](traceability/findings.md#f-87) (open),
  [F-89](traceability/findings.md#f-89) (open)
- Open questions: [Q-21](traceability/answered-questions.md#q-21) (answered),
  [Q-32](traceability/open-questions.md#q-32) (open),
  [Q-33](traceability/open-questions.md#q-33) (open),
  [Q-38](traceability/open-questions.md#q-38) (partly answered),
  [Q-49](traceability/open-questions.md#q-49) (open)
- Demo increments: [SL-28](traceability/increments.md#sl-28) (done),
  [SL-45](traceability/increments.md#sl-45) (done),
  [SL-46](traceability/increments.md#sl-46) (done),
  [SL-47](traceability/increments.md#sl-47) (done),
  [SL-48](traceability/increments.md#sl-48) (done),
  [SL-50](traceability/increments.md#sl-50) (done),
  [SL-51](traceability/increments.md#sl-51) (done)
