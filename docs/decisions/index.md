# Architecture decisions

The decision log holds every architecture decision of GBO in MADR
format. It contains the decisions of the archived reference architecture
v0.6.2. It also contains the decisions that the GBO team made during the
build of the demo.

Each ADR names the PSA or GO constraint that it satisfies and the
deliberation that produced it. Each ADR also links to its implementation
in [gbo-demo](https://github.com/ICTU/GBO-demo) at release v0.9.0. A
"Traceability" section at the end of each ADR lists the requirements,
findings, open questions, and demo increments that the ADR depends on.

If a later decision replaces an earlier one, both stay in the log. At the
top of its body, the superseded ADR gives the reason. It keeps its text as
history.

The column "Serves" names the main requirements of each decision. The
full list is in the ADR.

## Accepted

These decisions are accepted:

| ADR | Decision | Serves | Notes |
|---|---|---|---|
| [0001](0001-graphql-source-access.md) | GraphQL as the source access interface | [REQ-08](../requirements/authorization.md#req-08), [REQ-17](../requirements/authorization.md#req-17) | |
| [0002](0002-opa-rego-authzen.md) | OPA/Rego in OpenFTV, the FSC Inway as PEP, AuthZEN with the FTV GraphQL profile | [REQ-04](../requirements/authorization.md#req-04), [REQ-42](../requirements/authorization.md#req-42) | Includes the decision "the FSC Inway is the PEP" |
| [0003](0003-fsc-connectivity.md) | FSC for all domestic connectivity | [REQ-46](../requirements/sources-identity.md#req-46) | |
| [0004](0004-federated-authorization.md) | Five authorization concerns, federated evaluation, no central authorization server | [REQ-18](../requirements/authorization.md#req-18), [REQ-48](../requirements/authorization.md#req-48) | The legal-basis path is not implemented |
| [0005](0005-bsnk-pp.md) | BSNk PP polymorphic pseudonyms for private-sector access | [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-80](../requirements/pseudonymization.md#req-80), [REQ-82](../requirements/pseudonymization.md#req-82) | BSNk is called only at consent time. The mock follows the BSNk interface and does not encrypt |
| [0009](0009-closed-world-rules.md) | Closed-world per-field rules: the rule is the catalog | [REQ-48](../requirements/authorization.md#req-48), [REQ-97](../requirements/authorization.md#req-97) | Supersedes 0008. Rules are bound by regime and service |
| [0013](0013-pdp-request-mapper.md) | GraphQL request mapping in the PDP ahead of policy evaluation | [REQ-17](../requirements/authorization.md#req-17), [REQ-42](../requirements/authorization.md#req-42) | Supersedes 0012. The mapper only maps |
| [0015](0015-contract-acceptance-by-policy.md) | FSC contract acceptance by policy | [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-63](../requirements/admission.md#req-63) | Eight ordered refusal codes |
| [0016](0016-source-owned-metadata.md) | Source-owned metadata and reconciliation-based onboarding | [REQ-64](../requirements/sources-identity.md#req-64), [REQ-65](../requirements/sources-identity.md#req-65), [REQ-66](../requirements/sources-identity.md#req-66) | The mechanism is accepted. The document format is a proposal for PSA S10 |
| [0017](0017-gbo-simple-v1.md) | gbo-simple-v1 as the attestation mapping profile | [REQ-116](../requirements/eudi-issuance.md#req-116), [REQ-124](../requirements/eudi-issuance.md#req-124) | Applies to the `eudi` capability only |
| [0018](0018-eudi-disclosure-issuance.md) | EUDI issuance through disclosure-based OpenID4VCI on the nl-wallet stack | [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-57](../requirements/eudi-issuance.md#req-57), [REQ-78](../requirements/eudi-issuance.md#req-78) | |
| [0020](0020-as4-bridge-for-oots.md) | AS4 bridge for SDG-OOTS | [REQ-44](../requirements/authorization.md#req-44) | Not implemented in gbo-demo v0.9.0 |
| [0021](0021-central-pap-signed-bundles.md) | Policy management and distribution per bronhouder | [RL-01](../requirements/authorization.md#rl-01) to [RL-05](../requirements/authorization.md#rl-05) | Rewritten. Signing applies only across an organization boundary |
| [0023](0023-identity-convergence.md) | Organization identity from the certificate, and separate EUDI certificate roles (part A: organization identity) | [REQ-67](../requirements/sources-identity.md#req-67), [REQ-46](../requirements/sources-identity.md#req-46) | Part B is proposed |
| [0026](0026-ldv-integration.md) | Each controller logs its own processing in an LDV logbook | [REQ-72](../requirements/logging-audit.md#req-72) | Rewritten |
| [0031](0031-regime-from-evidence.md) | The authorization regime follows from the evidence a request carries | [REQ-74](../requirements/authorization.md#req-74) | Supersedes 0030 |
| [0032](0032-consent-proof.md) | The consent proof: signed, a value per source, a placeholder in the query, status online over FSC, verified in policy | [REQ-68](../requirements/consent.md#req-68), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-80](../requirements/pseudonymization.md#req-80) | Supersedes 0007 |
| [0033](0033-gateway-decrypts-after-allow.md) | The source gateway decrypts its own value after the allow, and only the Inway reaches it | [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-81](../requirements/pseudonymization.md#req-81) | Supersedes 0011 |
| [0034](0034-integrator-delegation.md) | An integrator connects under FSC delegation, and the consent binds the represented party | [REQ-106](../requirements/consent.md#req-106) | |
| [0035](0035-w3c-trace-context.md) | W3C Trace Context is the correlation key, and the FSC transaction ID is recorded next to it | [REQ-55](../requirements/logging-audit.md#req-55) | Supersedes 0019 |
| [0036](0036-adl-decision-record.md) | The ADL is the authoritative record of authorization decisions | [REQ-71](../requirements/logging-audit.md#req-71) | |
| [0037](0037-asi-oauth-front-door.md) | Authentic Source Interface as an OAuth front door per ETSI TS 119 478 clause 6.1 | [REQ-112](../requirements/asi.md#req-112), [REQ-87](../requirements/asi.md#req-87), [REQ-102](../requirements/asi.md#req-102) | Supersedes 0029. Demo grade |
| [0038](0038-asi-data-service-per-source.md) | One data service per authentic source, one token per data service | [REQ-94](../requirements/asi.md#req-94), [REQ-95](../requirements/asi.md#req-95), [REQ-99](../requirements/asi.md#req-99) | |
| [0039](0039-asi-source-described-attributes.md) | ASI attributes described by the source (`asi` capability in source metadata) | [REQ-64](../requirements/sources-identity.md#req-64), [REQ-92](../requirements/asi.md#req-92) | Partly implemented ([#592](https://github.com/ICTU/GBO-demo/issues/592)) |

## Proposed

A proposed ADR waits for an open question, a PSA decision, or demo work.
These decisions are proposed:

| ADR | Proposal | Serves | Waits for |
|---|---|---|---|
| [0023](0023-identity-convergence.md) | Organization identity from the certificate, and separate EUDI certificate roles (part B: EUDI certificate roles) | [REQ-58](../requirements/eudi-issuance.md#req-58) | Part A is accepted |
| [0024](0024-canonical-semantic-models.md) | Canonical semantic models per bronhouder | — | |
| [0025](0025-graphql-fds-datadienst.md) | GraphQL as a recognized data service (datadienst) type of the Federatief Datastelsel (FDS) | [REQ-08](../requirements/authorization.md#req-08) | |
| [0027](0027-onboarding-toolkit.md) | Bronhouder onboarding toolkit | [REQ-64](../requirements/sources-identity.md#req-64), [AV-07](../requirements/admission.md#av-07) | [Q-74](../traceability/open-questions.md#q-74) |
| [0028](0028-pubeaa-productization.md) | PuB-EAA Provider productization | [REQ-58](../requirements/eudi-issuance.md#req-58), [REQ-77](../requirements/eudi-issuance.md#req-77) | |
| [0040](0040-route-d-citizen-recognition.md) | Citizen recognition and the BSNk participant: route D | [REQ-69](../requirements/pseudonymization.md#req-69), [REQ-23](../requirements/consent.md#req-23) | [Q-49](../traceability/open-questions.md#q-49) |
| [0041](0041-asi-seal-format.md) | Seal format of ASI results | [REQ-83](../requirements/asi.md#req-83) | [Q-32](../traceability/open-questions.md#q-32) |
| [0042](0042-asi-attribute-token-binding.md) | Optional per-attribute token binding for ASI tokens | [REQ-103](../requirements/asi.md#req-103) | [Q-33](../traceability/open-questions.md#q-33) |
| [0043](0043-identifiers-out-of-pdp-input.md) | Keep identifiers out of the PDP input instead of masking decision logs | [REQ-60](../requirements/logging-audit.md#req-60) | Demo [#368](https://github.com/ICTU/GBO-demo/issues/368) |
| [0044](0044-issuance-flows.md) | Issuance offers the authorization code flow, and pre-auth only after identification in the same session | [REQ-45](../requirements/eudi-issuance.md#req-45) | Open question on the authorization server for issuance |

## Superseded

These decisions are superseded:

| ADR | Decision | Serves | Superseded by |
|---|---|---|---|
| [0006](0006-consent-register-as-pip.md) | Consent register (toestemmingsregister) as runtime PIP | [REQ-68](../requirements/consent.md#req-68) | [0007](0007-consent-signed-token.md), then [0032](0032-consent-proof.md) |
| [0007](0007-consent-signed-token.md) | Consent as a signed token with a live status check | [REQ-68](../requirements/consent.md#req-68) | [0032](0032-consent-proof.md) |
| [0008](0008-dienstencatalogus-ceiling.md) | Service catalog (dienstencatalogus) as a data-driven policy ceiling | [REQ-08](../requirements/authorization.md#req-08) | [0009](0009-closed-world-rules.md) |
| [0010](0010-pep-bsn-resolution.md) | BSN resolution inside the PEP | [REQ-21](../requirements/pseudonymization.md#req-21) | [0011](0011-sidecar-pseudonym-resolution.md), then [0033](0033-gateway-decrypts-after-allow.md) |
| [0011](0011-sidecar-pseudonym-resolution.md) | Source-owned source gateway resolves pseudonyms, and the PDP never sees a BSN | [REQ-21](../requirements/pseudonymization.md#req-21) | [0033](0033-gateway-decrypts-after-allow.md) |
| [0012](0012-opa-graphql-parse.md) | Query AST inspection with OPA's `graphql.parse_query` | [REQ-17](../requirements/authorization.md#req-17) | [0013](0013-pdp-request-mapper.md) |
| [0014](0014-provider-signed-flow-claims.md) | Flow and subject identifier semantics through a provider-side Additional Claims service | [REQ-74](../requirements/authorization.md#req-74) | [0030](0030-grant-properties.md), then [0031](0031-regime-from-evidence.md) |
| [0019](0019-fsc-transaction-id-tracing.md) | FSC transaction ID as the end-to-end correlation key | [REQ-55](../requirements/logging-audit.md#req-55) | [0035](0035-w3c-trace-context.md) |
| [0029](0029-authentic-source-interface.md) | Authentic Source Interface per ETSI TS 119 478 | [REQ-112](../requirements/asi.md#req-112) | [0037](0037-asi-oauth-front-door.md) |
| [0030](0030-grant-properties.md) | Flow and subject identifier semantics as FSC grant properties | [REQ-74](../requirements/authorization.md#req-74) | [0031](0031-regime-from-evidence.md) |

## Rejected or deferred

This decision is deferred:

| ADR | Proposal | Serves | Status |
|---|---|---|---|
| [0022](0022-sector-grants.md) | Sector-level grants with organizational attribute verification | [REQ-61](../requirements/admission.md#req-61) | Deferred. Admission runs through the admission register (toelatingsregister). The demo removed `sector-pip` ([#378](https://github.com/ICTU/GBO-demo/issues/378)) |

## Traceability

- Requirements: see the column "Serves" and the footer of each ADR.
- Findings: see the footer of each ADR.
- Open questions: [Q-32](../traceability/open-questions.md#q-32), [Q-33](../traceability/open-questions.md#q-33), [Q-49](../traceability/open-questions.md#q-49), [Q-74](../traceability/open-questions.md#q-74) (block proposed ADRs)
- Demo increments: see the footer of each ADR.
