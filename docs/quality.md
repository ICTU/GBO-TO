# Quality requirements

The scenarios on this page refine the
[quality goals](index.md#quality-goals) and make them testable. The
scenarios use the IDs QS-01 to QS-52. The Q-NN IDs belong to the
[open questions](traceability/open-questions.md).

The column "Pinned by" links the test in gbo-demo
[v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0) that holds the
scenario. "Not pinned" means that no automated test holds the scenario.
In that case, the scenario is an acceptance criterion for future work, or
it fails in demo v0.9.0. If a scenario fails in demo v0.9.0, its expected
outcome says so.

Reason codes have two layers
([Reason codes](concepts/authorization.md#reason-codes-two-layers)). The
consumer and the ADL get a client code, for example
`FIELD_NOT_PERMITTED`. The operator gets the rule code per field in the
console decision log, for example `YEAR_NOT_COVERED`. Each scenario names
the code at the layer where the test checks it.

## Data minimization and authorization

The following scenarios test data minimization and authorization:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-01 | A consumer asks for a field that no rule covers, for example `box2Inkomen` next to permitted income fields | Deny. Rule code `NO_APPLICABLE_RULE` for that field. No data leaves the source. | [`engine_test.rego#L210`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L210) |
| QS-02 | A query asks for a year that the citizen did not give consent for | Deny. Rule code `YEAR_NOT_COVERED`. | [`dvt0001_test.rego#L167`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L167) |
| QS-03 | A query has no year filter | Deny (fail closed). | [`dvt0001_test.rego#L172`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L172) |
| QS-04 | The mapper cannot prove the field list because of a parse error, an exceeded limit (depth 64, 100 fragments, 1 MiB body), or an unknown schema | Deny. Client code `COVERAGE_UNVERIFIABLE` with a subcode. A mutation or subscription gives `OPERATION_NOT_SUPPORTED`. | [`engine_test.rego#L117`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L117) |
| QS-05 | A request carries a consent proof, or carries none | With a consent proof, only consent-regime rules judge the request. Without one, only PID-regime rules judge it ([REQ-74](requirements/authorization.md#req-74)). | [`engine_test.rego#L227`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L227), [`#L234`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L234) |
| QS-06 | The actor list of a PID rule contains a consent consumer | The test fails. The lists stay disjoint. The test knows only the local consumers ([F-70](traceability/findings.md#f-70), [R21](risks.md#r21)). | [`engine_test.rego#L371`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L371) (local consumers only) |
| QS-07 | A rule for service `brp` meets a request on service `bri` | The rule does not bind, and the field gets `NO_APPLICABLE_RULE`. Every rule names its services ([REQ-97](requirements/authorization.md#req-97)). | [`engine_test.rego#L397`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L397), [`#L497`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L497) |
| QS-08 | The PDP gets a schema for a service whose digest the bundle does not pin | Deny. | [`engine_test.rego#L108`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L108) |
| QS-09 | A consumer gets a deny | The consumer sees only the client code. This code names no field and no rule code ([REQ-06](requirements/authorization.md#req-06)). | [`engine_test.rego#L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L29) |

## Consent integrity

The following scenarios test the integrity of consent:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-10 | The citizen revokes a consent between grant and use | The PDP denies the next request. Rule code `CONSENT_WITHDRAWN` ([REQ-14](requirements/consent.md#req-14)). | [`consent_test.rego#L202`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L202) |
| QS-11 | A forged or tampered consent token reaches the PDP | Deny. Rule code `CONSENT_SIGNATURE_INVALID`. | [`consent_test.rego#L318`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L318), [`#L324`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L324) |
| QS-12 | A consumer other than the one in the consent presents a valid consent proof | Deny. Rule code `CONSENT_ACTOR_MISMATCH`. | [`dvt0001_test.rego#L84`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L84) |
| QS-13 | The status service of the register does not answer | Deny (fail closed). Rule code `CONSENT_STATUS_UNAVAILABLE`, and the consumer sees `ACCESS_DENIED`. | [`consent_test.rego#L303`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L303) |
| QS-14 | A consumer puts a literal BSN in the query under a valid consent | Deny. Rule code `CONSTRAINT_MISMATCH` ([REQ-79](requirements/pseudonymization.md#req-79)). | [`dvt0001_test.rego#L131`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L131) |
| QS-15 | A request carries two consent proofs | Deny. The PDP picks neither proof. Rule code `CONSENT_CONTEXT_INVALID`. | [`consent_test.rego#L438`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L438) |
| QS-16 | A citizen revokes an expired or already revoked consent | The backend refuses the revocation with `CONSENT_NOT_REVOCABLE` ([REQ-109](requirements/consent.md#req-109)). Fails in demo v0.9.0: the backend answers 200 ([#600](https://github.com/ICTU/GBO-demo/issues/600), [R31](risks.md#r31)). | Not pinned |

## Admission and integrators

The following scenarios test admission and integrators:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-17 | A suspended participant submits an FSC contract | The contract stays proposed. Reason `PARTY_NOT_ACTIVE`. | [`autosign_test.rego#L138`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L138) |
| QS-18 | A participant asks for a source outside its `allowed_source_peer_ids` | The contract stays proposed. Reason `SOURCE_NOT_ALLOWED`. | [`autosign_test.rego#L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L109) |
| QS-19 | The admission register is missing from the PDP data | The contract stays proposed. Reason `ADMISSION_REGISTER_UNAVAILABLE`. The reason is not "party unknown". | [`autosign_test.rego#L86`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L86) |
| QS-20 | An integrator proposes a delegated contract for a provider for which it has no registered integration | The contract stays proposed. Reason `DELEGATION_NOT_REGISTERED`. | [`autosign_test.rego#L176`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L176) |
| QS-21 | An integrator calls for a provider without a mandate, or the register is unavailable | Deny. Rule code `INTEGRATOR_NOT_REGISTERED`, or `INTEGRATOR_REGISTER_UNAVAILABLE` ([REQ-106](requirements/consent.md#req-106)). | [`engine_test.rego#L621`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L621), [`#L631`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L631) |
| QS-22 | A suspended consumer with an existing contract sends a query under a valid consent | Deny ([REQ-110](requirements/admission.md#req-110)). Fails in demo v0.9.0: the request passes until the contract is revoked. | Not pinned |

## Privacy

The following scenarios test privacy:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-23 | A DvTP consumer asks for income data under a consent | The consumer request names the subject with the placeholder `consent:identity`. The request, the PDP input, and the ADL hold no citizen identifier ([REQ-20](requirements/pseudonymization.md#req-20)). | [`consumer_test.go#L86`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/consumer/consumer_test.go#L86) |
| QS-24 | The proof carries a value made for another OIN | The source gateway refuses the value and does not forward the request ([REQ-80](requirements/pseudonymization.md#req-80)). | [`substitution_test.go#L112`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution_test.go#L112) |
| QS-25 | A consumer tries to reach a source gateway or a source API directly | Unreachable ([REQ-81](requirements/pseudonymization.md#req-81)). Partly met in demo v0.9.0: Docker Compose isolates the gateways, but the source APIs share networks with consumers ([R25](risks.md#r25)). | Not pinned (manual check of the gateways, October 5, 2026) |
| QS-26 | A consent record is read from the register | The record holds no BSN and no per-party value. The register keeps PI and PP under the `subject_ref` of the portal, and no consent answer carries them ([REQ-69](requirements/pseudonymization.md#req-69)). | [`polymorphic_test.go#L39`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/polymorphic_test.go#L39), [`#L85`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/polymorphic_test.go#L85) |
| QS-27 | Two sources get values for the same citizen | The values differ per recipient and cannot be linked. Not demonstrated in demo v0.9.0: the BSNk mock does not encrypt, and the demo sources share one OIN. | Not pinned |
| QS-28 | An EUDI or ASI request reaches the PDP | The PDP input and both decision logs hold no BSN ([REQ-60](requirements/logging-audit.md#req-60)). Fails in demo v0.9.0 ([#368](https://github.com/ICTU/GBO-demo/issues/368), [R22](risks.md#r22)). | Not pinned |
| QS-29 | A component writes an LDV record that contains a valid BSN anywhere | The logbook refuses the record. | [`validate_test.go#L94`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/validate_test.go#L94) |

## Traceability and audit

The following scenarios test traceability and audit:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-30 | A caller sends both `traceparent` and `Fsc-Transaction-Id` | The component takes the trace ID from `traceparent`. The transaction ID is recorded next to it ([REQ-55](requirements/logging-audit.md#req-55)). | [`tracecontext_test.go#L100`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext_test.go#L100) |
| QS-31 | An auditor reads all processing records of one request | Each logbook returns the records of that trace ([REQ-72](requirements/logging-audit.md#req-72)). | [`logbook_test.go#L180`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/logbook_test.go#L180) |
| QS-32 | The logbook is unavailable while a request runs | The request is served. Later, the outbox delivers the record once ([REQ-72](requirements/logging-audit.md#req-72)). | [`outbox_test.go#L86`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/outbox_test.go#L86), [`#L119`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/outbox_test.go#L119) |
| QS-33 | An auditor holds a transaction ID and looks for the ADL record | The ADL record carries the trace ID and the transaction ID ([REQ-71](requirements/logging-audit.md#req-71)). Partly met in demo v0.9.0: behind the FSC Inway, the record has neither. The reader finds the record through the stored request header ([#369](https://github.com/ICTU/GBO-demo/issues/369), [R23](risks.md#r23)). | Not pinned (code: [`adl.go#L49-L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/adl.go#L49-L66)) |
| QS-34 | An auditor asks which policy version made the decision | The ADL record names the policy version ([REQ-59](requirements/logging-audit.md#req-59)). Fails in demo v0.9.0. | Not pinned |
| QS-35 | A citizen asks which parties processed data under one consent | The answer is available per consent. Partly met in demo v0.9.0: each controller can answer from its logbook, but the citizen view per consent is not built ([R19](risks.md#r19)). | Not pinned |

## EUDI issuance

The following scenarios test EUDI issuance:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-36 | A caller outside the designated issuers asks for an attestation | Deny. Rule code `ACTOR_NOT_ALLOWED`. | [`eud0001_test.rego#L65`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0001_test.rego#L65) |
| QS-37 | A caller posts a BSN to the adapter callback without the issuance server | Refused ([REQ-45](requirements/eudi-issuance.md#req-45)). Fails in demo v0.9.0: the callback is unauthenticated ([#133](https://github.com/ICTU/GBO-demo/issues/133), [R5](risks.md#r5)). | Not pinned |
| QS-38 | A source has no certificate set | Only that source is blocked. Other sources keep working ([REQ-58](requirements/eudi-issuance.md#req-58)). | [`service_test.go#L130`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service_test.go#L130) |
| QS-39 | The source metadata endpoint is unavailable | The last candidate stays in use within the stale grace ([REQ-66](requirements/sources-identity.md#req-66)). | [`service_test.go#L213`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service_test.go#L213) |
| QS-40 | A published Type Metadata version is fetched twice | The responses are byte-identical, and `vct#integrity` matches. | [`type_metadata_test.go#L17`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/type_metadata_test.go#L17) |

## Authentic Source Interface

The following scenarios test the Authentic Source Interface:

| # | Scenario | Expected outcome | Pinned by |
|---|---|---|---|
| QS-41 | A QTSP uses a token issued for another data service | 401. A token is valid for one data service only ([REQ-95](requirements/asi.md#req-95)). | [`dataservices_test.go#L16`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/dataservices_test.go#L16) |
| QS-42 | A request has no DPoP proof, or replays one | 401. | [`token_test.go#L158`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L158), [`#L200`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L200) |
| QS-43 | A request asks for an attribute outside the approved `authorization_details` | 401 `insufficient_scope` ([REQ-103](requirements/asi.md#req-103)). | [`token_test.go#L217`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L217) |
| QS-44 | A verify or retrieve succeeds | The body is sealed with a detached JWS in `X-JWS-Signature`. Errors are not sealed ([REQ-83](requirements/asi.md#req-83)). | [`handler_test.go#L238`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L238) |
| QS-45 | A verify gives `Match` | The response carries no value from the source ([REQ-85](requirements/asi.md#req-85)). | [`handler_test.go#L108`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L108) |
| QS-46 | The source holds no value, or the chain fails | No value gives `Unknown`. A failed chain gives an error, never `Unknown` ([REQ-84](requirements/asi.md#req-84), [REQ-93](requirements/asi.md#req-93)). | [`handler_test.go#L140`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L140), [`source_test.go#L141`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/source_test.go#L141) |
| QS-47 | A retrieve asks for an attribute for which the source has no value | 404. No partial result ([REQ-101](requirements/asi.md#req-101)). | [`handler_test.go#L291`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L291) |
| QS-48 | A QTSP reads the discovery records of the ASIP | Each record leads to the data service endpoint, its contract, and the authorization server metadata ([REQ-99](requirements/asi.md#req-99), [REQ-100](requirements/asi.md#req-100)). | [`discovery_test.go#L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/discovery_test.go#L66), [`#L105`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/discovery_test.go#L105) |
| QS-49 | A QTSP without `QEAA_Provider` in the register registers, or loses the entitlement later | Registration refused (`unapproved_software_statement`). After a withdrawal, the next re-check deactivates the client ([REQ-88](requirements/asi.md#req-88), [REQ-89](requirements/asi.md#req-89)). If the register is unreachable, the client stays active ([R27](risks.md#r27)). | [`registration_test.go#L152`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L152), [`#L276`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L276), [`#L306`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L306) |
| QS-50 | The wallet returns on the same device but in another browser | Refused before the verifier is asked. | [`wallet_test.go#L123`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L123) |
| QS-51 | An FSC peer other than the ASIP asks for BRP personal data under the PID regime | Deny. Rule code `ACTOR_NOT_ALLOWED`. ASI0001 judges service `brp` only. | [`asi0001_test.rego#L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001_test.rego#L29), [`#L56`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001_test.rego#L56) |
| QS-52 | The QTSP holds the access token | The QTSP cannot read the BSN ([F-86](traceability/findings.md#f-86)). Fails in demo v0.9.0 ([#595](https://github.com/ICTU/GBO-demo/issues/595), [R26](risks.md#r26)). | Not pinned |

The ETSI conformance matrix
[`etsi-ts-119478.yaml`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml)
gives each ETSI TS 119 478 requirement a status and the tests that hold
it. The CI check fails in each of these cases:

- A requirement ID has no entry.
- A status lacks what it requires.
- A named test does not exist.

One entry has the status `failing`: fuzzy matching against a response
without a value ([R30](risks.md#r30)).

## Open quality targets

Availability, capacity, and performance targets have no scenarios in
this version of the TO. By design, the demo runs one instance of each
component. For more information, see the
[availability model](deployment.md#availability-model). Two targets are
open:

- The volumes that the chain must handle
  ([Q-47](traceability/open-questions.md#q-47)).
- The propagation time, availability, and latency of the consent status
  ([REQ-75](requirements/consent.md#req-75)). The register is a
  dependency of every DvTP decision ([R10](risks.md#r10)).

## Traceability

- Requirements: [REQ-06](requirements/authorization.md#req-06),
  [REQ-14](requirements/consent.md#req-14),
  [REQ-20](requirements/pseudonymization.md#req-20),
  [REQ-45](requirements/eudi-issuance.md#req-45),
  [REQ-55](requirements/logging-audit.md#req-55),
  [REQ-58](requirements/eudi-issuance.md#req-58),
  [REQ-59](requirements/logging-audit.md#req-59),
  [REQ-60](requirements/logging-audit.md#req-60),
  [REQ-66](requirements/sources-identity.md#req-66),
  [REQ-69](requirements/pseudonymization.md#req-69),
  [REQ-71](requirements/logging-audit.md#req-71),
  [REQ-72](requirements/logging-audit.md#req-72),
  [REQ-74](requirements/authorization.md#req-74),
  [REQ-75](requirements/consent.md#req-75),
  [REQ-79](requirements/pseudonymization.md#req-79),
  [REQ-80](requirements/pseudonymization.md#req-80),
  [REQ-81](requirements/pseudonymization.md#req-81),
  [REQ-83](requirements/asi.md#req-83) to
  [REQ-89](requirements/asi.md#req-89),
  [REQ-93](requirements/asi.md#req-93),
  [REQ-95](requirements/asi.md#req-95),
  [REQ-97](requirements/authorization.md#req-97),
  [REQ-99](requirements/asi.md#req-99) to
  [REQ-103](requirements/asi.md#req-103),
  [REQ-106](requirements/consent.md#req-106),
  [REQ-109](requirements/consent.md#req-109),
  [REQ-110](requirements/admission.md#req-110)
- Findings: [F-70](traceability/findings.md#f-70) (open),
  [F-79](traceability/findings.md#f-79) (open),
  [F-86](traceability/findings.md#f-86) (open),
  [F-90](traceability/findings-closed.md#f-90) (resolved in demo)
- Open questions: [Q-47](traceability/open-questions.md#q-47) (open)
- Demo increments: [SL-28](traceability/increments.md#sl-28) (done),
  [SL-45](traceability/increments.md#sl-45) (done),
  [SL-47](traceability/increments.md#sl-47) (done),
  [SL-50](traceability/increments.md#sl-50) (done),
  [SL-51](traceability/increments.md#sl-51) (done)
