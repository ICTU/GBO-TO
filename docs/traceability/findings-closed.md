# Closed findings

These findings are closed, resolved in the demo, superseded, or no longer apply. Each entry says where the outcome landed: a requirement, a decision, or a page of this TO. The open findings are on [Findings](findings.md).

### F-02: Central PDP as an implicit choice {#f-02}

- **Status**: closed
- **Point**: one policy engine served every request. So the demo implied a central PDP, while PDP placement was an open design question.
- **Outcome**: [Q-02](answered-questions.md#q-02) set the direction: federated by default, with a PDP per source holder, and a central adapter variant as fallback. In demo v0.9.0, the PDP sits behind the Inway of each source.
- **Landed in**: [ADR-0004](../decisions/0004-federated-authorization.md), [Q-02](answered-questions.md#q-02).
- **Evidence**: [`docker-compose.yml`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml)

### F-03: The UI offered per-field selection against FR-10 (atomicity) {#f-03}

- **Status**: closed
- **Point**: the citizen was able to switch single fields on and off. FR-10 asks for an indivisible data set.
- **Outcome**: since [SL-13](increments.md#sl-13), policy decides per data set. Since [SL-06a](increments.md#sl-06a), the portal chooses per scope. FR-10 v0.9 has no partial consent, and [Q-03](answered-questions.md#q-03) is answered. Demo issue [#382](https://github.com/ICTU/GBO-demo/issues/382) covers the fixed minimal set.
- **Landed in**: [REQ-10](../requirements/consent.md#req-10).
- **Evidence**: [`ScopeToggle.tsx`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/components/consent/ScopeToggle.tsx)

### F-04: No consent lifecycle: no TTL, no single use, no status model {#f-04}

- **Status**: closed
- **Point**: a consent was only active or revoked. The demo did not enforce validity or use.
- **Outcome**: the PDP checks validity per request ([SL-01a](increments.md#sl-01a), [SL-47](increments.md#sl-47)). FR-11 v0.9 drops single use: a consent is reusable within its validity ([Q-04](answered-questions.md#q-04)). Demo issue [#389](https://github.com/ICTU/GBO-demo/issues/389) covers the "retrieved" status. [F-19](findings.md#f-19) holds the design question.
- **Landed in**: [REQ-19](../requirements/consent.md#req-19), [ADR-0032](../decisions/0032-consent-proof.md).
- **Evidence**: [`policies/gbo/consent.rego#L124`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L124)

### F-06: The source trusted the PEP without a check and had no fourth validation point (FR-26) {#f-06}

- **Status**: closed
- **Point**: the source accepted every request from a shared PEP and did no check of its own.
- **Outcome**: the shared PEP no longer exists. Every request passes the Inway of the source. The Inway asks the PDP of the source over AuthZEN. This design matches the GO, [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), and criterion 1 of FR-26 v0.9. One point stays open for the FR authors: the FR-26 dependency still names a "central authorization component" (FR-17). That dependency conflicts with the GO.
- **Landed in**: [REQ-04](../requirements/authorization.md#req-04), [ADR-0004](../decisions/0004-federated-authorization.md).
- **Evidence**: demo issue [#88](https://github.com/ICTU/GBO-demo/issues/88) (PEP service removed)

### F-07: Only OTel tracing, with no LDV and no non-repudiable decision log {#f-07}

- **Status**: closed
- **Point**: traceability was technical and short-lived. There was no processing log, no persistent decision log, and no citizen log.
- **Outcome**: [SL-10](increments.md#sl-10) built the correlation layer, and [SL-04](increments.md#sl-04) persisted decision logs. LDV per system came with demo issue [#302](https://github.com/ICTU/GBO-demo/issues/302) and [PR #366](https://github.com/ICTU/GBO-demo/pull/366). In [PR #373](https://github.com/ICTU/GBO-demo/pull/373), the ADL became the audit source. Protection and retention are norms in [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid) and are open in [Q-08](open-questions.md#q-08). [F-68](findings.md#f-68) and [Q-25](open-questions.md#q-25) cover citizen access.
- **Landed in**: [REQ-55](../requirements/logging-audit.md#req-55), [REQ-71](../requirements/logging-audit.md#req-71), [REQ-72](../requirements/logging-audit.md#req-72), [REQ-32](../requirements/logging-audit.md#req-32), [ADR-0026](../decisions/0026-ldv-integration.md), [ADR-0036](../decisions/0036-adl-decision-record.md).

### F-08: No mTLS or certificate-bound token on FSC {#f-08}

- **Status**: closed
- **Point**: the old FSC mock identified organizations with an HMAC JWT and an OIN lookup, without mTLS.
- **Outcome**: the outcome has five parts:
    - Transport runs on OpenFSC, with mTLS between Outway and Inway and with contract-bound authorization ([SL-39](increments.md#sl-39), [SL-42](increments.md#sl-42)).
    - The legal identity comes from the certificate ([F-60](#f-60)).
    - [Q-07](answered-questions.md#q-07) answers the question of the PKIoverheid anchor.
    - No source asks for a certificate-bound token (RFC 8705). FR-34 v0.9 asks for a binding only outside the secure connection.
    - The review found a further gap: nothing proves that the browser initiation comes from the dienstverlener (FR-34, criterion 1). Demo issue [#427](https://github.com/ICTU/GBO-demo/issues/427), [REQ-111](../requirements/consent.md#req-111), and [Q-60](open-questions.md#q-60) record this gap.
- **Landed in**: [REQ-46](../requirements/sources-identity.md#req-46), [REQ-67](../requirements/sources-identity.md#req-67), [ADR-0003](../decisions/0003-fsc-connectivity.md), [ADR-0023](../decisions/0023-identity-convergence.md).

### F-09: No policy lifecycle: hot reload without bundle, signing or versioning {#f-09}

- **Type**: design gap
- **Status**: closed (November 2, 2026: [ADR-0021](../decisions/0021-central-pap-signed-bundles.md) records the signing rule)
- **Trigger**: the first demo mounted Rego files as a volume and reloaded them. [SL-44](increments.md#sl-44) ([PR #208](https://github.com/ICTU/GBO-demo/pull/208)) built most of the lifecycle.
- **Observation**: the state of the policy lifecycle in demo v0.9.0 is as follows:
    - Built: git stays canonical. Policy goes out as an identified, versioned bundle. The PDP decides from the bundle with an empty policy directory ([RL-01](../requirements/authorization.md#rl-01)). [RL-02](../requirements/authorization.md#rl-02) and [RL-03](../requirements/authorization.md#rl-03) cover management authorization and role separation. [RL-04](../requirements/authorization.md#rl-04) and [RL-05](../requirements/authorization.md#rl-05) cover retire-not-delete and validation.
    - Not built: bundle signing. Nobody can verify the origin of a bundle.
    - The default demo configuration mounts `./policies` into the PDP ([`docker-compose.yml#L157`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L157)). Bundle pull is opt-in through `make demo-manager` ([`gbo-pdp.yaml`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/bundles/gbo-pdp.yaml)).
    - Demo issue [#426](https://github.com/ICTU/GBO-demo/issues/426) (signing) closed as not planned on October 28, 2026. [Q-21](answered-questions.md#q-21) keeps policy management at each source, so PAP and PDP are in one organization.
- **Why it matters**: [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie) asks that a party can check the authenticity and integrity of policy sets. Criteria 1 and 2 of FR-39 v0.9 ask for sealed bundles. The GO names signed policy bundles. If another party than the policy owner runs a PDP, that PDP cannot check the origin of a bundle without a signature.
- **Proposal**: record in [ADR-0021](../decisions/0021-central-pap-signed-bundles.md) that signing is a requirement for a bundle that crosses an organization boundary. Inside one organization, signing is not planned. Validation with fallback stays with [F-52](findings.md#f-52). The FR-39 text about a central policy authority is outdated ([Q-21](answered-questions.md#q-21)) and goes back to the FR-DvTP authors. When ADR-0021 records the rule, close this finding.
- **Related**: [F-51](findings.md#f-51), [F-52](findings.md#f-52), [F-59](#f-59), [RL-01](../requirements/authorization.md#rl-01) to [RL-05](../requirements/authorization.md#rl-05), [Q-21](answered-questions.md#q-21), [ADR-0021](../decisions/0021-central-pap-signed-bundles.md).

### F-11: The demo lets the consumer set the validity period {#f-11}

- **Status**: closed
- **Point**: the consumer sends `validity_seconds`. FR-05 names the citizen as the party that sets the period.
- **Outcome**: FR-05 and FR-11 v0.9 put the default per service in the catalog. The citizen can adjust the period within bounds. Demo issue [#380](https://github.com/ICTU/GBO-demo/issues/380) covers the demo deviation: a default of one year and no upper bound. [Q-13](open-questions.md#q-13) holds the question whether the citizen must adjust the period. That question reopened on November 2, 2026.
- **Landed in**: [REQ-19](../requirements/consent.md#req-19), [Q-13](open-questions.md#q-13).
- **Evidence**: [`consent-register/main.go#L403`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L403)

### F-14: The scope header is an untrusted catalog index, not a token claim {#f-14}

- **Status**: resolved in demo
- **Point**: `X-GBO-Scope` selected the policy context but was not proof of anything.
- **Outcome**: the header stayed untrusted, and policy checked the scope separately (demo issue [#101](https://github.com/ICTU/GBO-demo/issues/101)). Since demo issue [#483](https://github.com/ICTU/GBO-demo/issues/483), the DvTP flow does not send the header. The PDP checks the requested scope against the verified consent.
- **Landed in**: [REQ-48](../requirements/authorization.md#req-48), [REQ-18](../requirements/authorization.md#req-18).
- **Evidence**: [`CHANGELOG.md#L379`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L379)

### F-15: REQ-20 was worded BSN-only {#f-15}

- **Status**: closed
- **Point**: the claim was that the DigiD token and the pseudonym must not reach the consumer either. By that claim, REQ-20 was too narrow.
- **Outcome**: the GO and [PSA S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering) say that the dienstverlener never gets the BSN. It gets only a party-specific pseudonym. So REQ-20 is correct. In demo v0.9.0, the return redirect carries the signed consent proof. [Q-01](open-questions.md#q-01) covers the form of the pseudonym.
- **Landed in**: [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-80](../requirements/pseudonymization.md#req-80).

### F-16: No single trace across consent issuance and the DvTP query {#f-16}

- **Status**: closed (observation, no action)
- **Point**: consent issuance and a later query have separate traces.
- **Outcome**: the two are separate units of work, often hours or days apart. One trace for both conflicts with OTel semantics. The audit axis between them is `consent_id`. The decision record carries `consent_id` next to the trace ID.
- **Landed in**: [REQ-55](../requirements/logging-audit.md#req-55), [REQ-71](../requirements/logging-audit.md#req-71), [ADR-0035](../decisions/0035-w3c-trace-context.md).

### F-17: Scope descriptions in the consent portal are hard-coded {#f-17}

- **Status**: closed
- **Point**: the portal shows hard-coded scope texts, separate from what policy enforces. The DvTP scopes are spread over policy, a generated field map, and `scopeGroups.ts`.
- **Outcome**: demo issue [#382](https://github.com/ICTU/GBO-demo/issues/382) holds the finishing work (DvTP catalog per FR-32). [F-74](findings.md#f-74) holds the design.
- **Landed in**: [REQ-121](../requirements/consent.md#req-121).
- **Evidence**: [`ScopeToggle.tsx#L1`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/components/consent/ScopeToggle.tsx#L1) (reads `scopeGroups`)

### F-18: DvTP initiation is redirect-only and does not cover an asynchronous invitation {#f-18}

- **Status**: closed
- **Point**: FR-DvTP covers only a redirect while the citizen is present.
- **Outcome**: an asynchronous invitation is out of scope. FR-DvTP v0.9 knows only redirect initiation (FR-12 to FR-14). The GO and the PSA have no invitation route. Reusable consent within its validity covers retrieval without the citizen present ([Q-04](answered-questions.md#q-04), demo issue [#380](https://github.com/ICTU/GBO-demo/issues/380)). An invitation is a MijnOverheid function. The topic comes back only with a concrete use case.
- **Landed in**: [REQ-37](../requirements/consent.md#req-37).

### F-20: The integrator role in DvTP needed PSA elaboration {#f-20}

- **Status**: closed
- **Point**: the portal showed an empty integrator field. A small fix to that field implied at least eight design choices, among them end-to-end encryption (old FR-18).
- **Outcome**: FR-06 is dropped, and [Q-12](answered-questions.md#q-12) is answered. FR-18 v0.9 makes the integrator a processor that can see the data. FR-37 v0.9 covers its onboarding. The integrator connects under FSC delegation. [F-73](#f-73) holds the remaining gap (demo issue [#379](https://github.com/ICTU/GBO-demo/issues/379)). The integrator field is removed from the portal.
- **Landed in**: [REQ-106](../requirements/consent.md#req-106), [AV-06](../requirements/admission.md#av-06), [ADR-0034](../decisions/0034-integrator-delegation.md).

### F-21: The catalog role split between FDS and GBO was not explicit {#f-21}

- **Status**: closed
- **Point**: the PSA named no GBO component that consumes the catalog (a "catalog broker").
- **Outcome**: GBO has no catalog broker. PSA B-03 sets federated content management with a common profile for findability ([PSA vraagstukken](https://ictu.github.io/GBO-PSA/main/vraagstukken/)). S07 and [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus) agree. The source owns its service description ([F-57](findings.md#f-57)). The DvTP catalog follows [F-74](findings.md#f-74).
- **Landed in**: [REQ-64](../requirements/sources-identity.md#req-64), [ADR-0016](../decisions/0016-source-owned-metadata.md).

### F-22: The catalog runtime pattern for the PDP was undecided {#f-22}

- **Status**: closed
- **Point**: catalog data had two possible routes to the PDP: as a bundle, or per request as a PIP fetch.
- **Outcome**: policy goes out as a sealed bundle (FR-39 v0.9, [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie)). The PDP consults the catalog and the registers as PIPs ([PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)). Source metadata is pulled, validated, and activated atomically. [F-09](#f-09) and [F-52](findings.md#f-52) hold the open points.
- **Landed in**: [REQ-64](../requirements/sources-identity.md#req-64), [REQ-66](../requirements/sources-identity.md#req-66).

### F-23: Rich catalog or rich policy {#f-23}

- **Status**: closed
- **Point**: several demo increments moved content (allowlists, templates, and constraints) from policy code to catalog data, without a PSA choice.
- **Outcome**: [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus) says that the catalog does not duplicate authorization policy. Policy runs through S06, and the catalog is federated (B-03). The source owns the rich description ([F-57](findings.md#f-57)). GBO carries only the validation profile.
- **Landed in**: [ADR-0016](../decisions/0016-source-owned-metadata.md).

### F-24: An unknown consent gave an HTTP error instead of a clean deny {#f-24}

- **Status**: resolved in demo
- **Point**: the old PEP turned "consent not found" into HTTP 400, and the consumer saw `upstream_error`.
- **Outcome**: [SL-47](increments.md#sl-47) ([PR #238](https://github.com/ICTU/GBO-demo/pull/238)) built the fix: policy builds the consent context. An unknown consent gives `exists: false` and the decision `CONSENT_NOT_FOUND`. An unreachable register gives `status_available: false` and a clean deny. Both are policy decisions with a reason code in the decision record.
- **Landed in**: [REQ-06](../requirements/authorization.md#req-06), [ADR-0032](../decisions/0032-consent-proof.md).
- **Evidence**: [`policies/gbo/consent.rego#L273-L280`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L273-L280)

### F-25: PEP schema translation was regex-based and DvTP-specific {#f-25}

- **Status**: closed
- **Point**: the PEP rewrote the query with regular expressions that worked only for DvTP.
- **Outcome**: the PEP service no longer exists. The PDP maps the query by its AST. After the decision, the source gateway replaces the subject.
- **Landed in**: [REQ-21](../requirements/pseudonymization.md#req-21), [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md).
- **Evidence**: [`services/openftv-pdp/mapper/ftvgraphql.go`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go)

### F-26: Trace-driven UI coloring in the developer portal was fragile {#f-26}

- **Status**: closed
- **Point**: the portal colored the chain from Jaeger and Loki data with complex timing logic.
- **Outcome**: this finding concerns demo tooling only and is not a design finding. The proposed event stream is built and replaces the Jaeger polling.
- **Evidence**: [`useChainEvents.ts`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/developer-portal/src/hooks/useChainEvents.ts)

### F-27: AuthZEN envelope adopted, but not the RFC0052-GBO wire shape {#f-27}

- **Status**: closed
- **Point**: the PEP sent the query as a resource attribute. AuthZEN 1.0 puts the query in action properties.
- **Outcome**: the FSC Inway with OpenFTV v0.1.0 ([PR #337](https://github.com/ICTU/GBO-demo/pull/337)) is AuthZEN-conformant ([Q-16](answered-questions.md#q-16)). Demo issue [#331](https://github.com/ICTU/GBO-demo/issues/331) takes a GraphQL profile upstream (PSA B-02).
- **Landed in**: [REQ-42](../requirements/authorization.md#req-42), [ADR-0002](../decisions/0002-opa-rego-authzen.md).

### F-28: The tech lead agreed to the generic GBO chain {#f-28}

- **Status**: closed
- **Point**: in the architects' meeting, the position was that there is no separate EUDI authorization chain.
- **Outcome**: the tech lead agreed to the direction. There is one generic PEP and one generic PDP, and policies decide the behavior. Channels differ in access basis, policies, metadata, and identifier handling. All channels use the same components. The adapter stays thin. The demo showed this design in [F-31](#f-31), and [REQ-74](../requirements/authorization.md#req-74) holds the regime choice.
- **Landed in**: [ADR-0004](../decisions/0004-federated-authorization.md), [ADR-0031](../decisions/0031-regime-from-evidence.md).

### F-29: `consentId` in the query was DvTP-specific {#f-29}

- **Status**: closed
- **Point**: the consent belongs in policy and evidence. The business query does not carry it. This point revises the removed REQ-25 to REQ-27.
- **Outcome**: [SL-47](increments.md#sl-47) ([PR #238](https://github.com/ICTU/GBO-demo/pull/238)) built it: the proof travels in the `X-GBO-Consent-Token` header. Since [SL-51](increments.md#sl-51), the query names the subject by a placeholder. The subject comes only from the proof.
- **Landed in**: [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-17](../requirements/authorization.md#req-17), [ADR-0032](../decisions/0032-consent-proof.md).
- **Evidence**: [`dienstverlener-backend/outway/outway_test.go#L60-L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/outway/outway_test.go#L60-L66)

### F-30: De-pseudonymization belongs at the source, and the GBO core stays BSN-free (DvTP path) {#f-30}

- **Status**: resolved in demo
- **Point**: the conversion to a BSN must happen at the source, and the source uses its own keys for it. The conversion must not happen in the PEP or the PDP.
- **Outcome**: [SL-22](increments.md#sl-22) and demo issue [#88](https://github.com/ICTU/GBO-demo/issues/88) built this rule. Since [SL-51](increments.md#sl-51), the source gateway decrypts its own value from the proof after the allow, without BSNk at query time. This rule holds only for DvTP. The EUDI and ASI routes carry the BSN from the PID ([F-54](findings.md#f-54)).
- **Landed in**: [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-20](../requirements/pseudonymization.md#req-20), [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md) (supersedes ADR-0011).
- **Evidence**: [`services/bron-sidecar/`](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/bron-sidecar)

### F-31: Generic chain shown: two front doors through one PEP and one PDP {#f-31}

- **Status**: closed
- **Point**: [SL-20](increments.md#sl-20) sent EUDI issuance through the same chain as the DvTP query.
- **Outcome**: the demo proved the point. PEP and PDP stay generic. Rules and evidence carry the channel difference. The adapter only translates the protocol. [Q-17](open-questions.md#q-17) holds the remaining governance points (issuer model, adapter ownership).
- **Landed in**: [ADR-0004](../decisions/0004-federated-authorization.md), [ADR-0031](../decisions/0031-regime-from-evidence.md).

### F-32: Access basis from a self-declared `flow` field was an interim solution {#f-32}

- **Status**: resolved in demo
- **Point**: the consumer declared the flow, so a caller was able to try to skip the consent check.
- **Outcome**: demo issue [#88](https://github.com/ICTU/GBO-demo/issues/88) first moved `flow` to a grant property ([F-43](#f-43)). Since [PR #363](https://github.com/ICTU/GBO-demo/pull/363), the regime follows from the evidence that a request carries ([F-70](findings.md#f-70)). No consumer claim drives dispatch.
- **Landed in**: [REQ-74](../requirements/authorization.md#req-74), [ADR-0031](../decisions/0031-regime-from-evidence.md).

### F-34: Placement of per-request context in transport is a choice {#f-34}

- **Status**: resolved in demo
- **Point**: context in the request body mixed values that the consumer declared with values that the transport validated.
- **Outcome**: [SL-31](increments.md#sl-31) made the body pure GraphQL and put the context in headers with a trust prefix. The old FSC mock is gone. The rule stays: the PDP decides only on facts that it establishes itself. Consumer declarations do not count as facts.
- **Landed in**: [REQ-18](../requirements/authorization.md#req-18) (absorbs the removed REQ-49 and REQ-50).

### F-35: The FSC Inway has a built-in AuthZEN plugin, so the PEP service doubled the PEP role {#f-35}

- **Status**: resolved in demo
- **Point**: in the FSC model, the Inway is the PEP. A separate PEP service was a duplicate.
- **Outcome**: [SL-40](increments.md#sl-40) removed the EUDI branch of the PEP service. Demo issue [#88](https://github.com/ICTU/GBO-demo/issues/88) removed the service. DvTP and EUDI share one AuthZEN path to the PDP. Transformation after the decision happens at the source ([F-30](#f-30), [F-37](#f-37)).
- **Landed in**: [REQ-04](../requirements/authorization.md#req-04), [REQ-42](../requirements/authorization.md#req-42), [ADR-0002](../decisions/0002-opa-rego-authzen.md).

### F-36: A sector grant is not a native FSC concept {#f-36}

- **Status**: resolved in demo
- **Point**: FSC grants are per service and per peer. A sector grant needs a contract per peer or a policy attribute.
- **Outcome**: the demo did not continue the sector branch. The removed REQ-33 and REQ-34 carried it. Admission comes from the admission register and the contract decision of the PDP ([F-55](#f-55)). Demo issue [#378](https://github.com/ICTU/GBO-demo/issues/378) removed `sector-pip`.
- **Landed in**: [REQ-61](../requirements/admission.md#req-61), [ADR-0022](../decisions/0022-sector-grants.md) (history).
- **Evidence**: [`CHANGELOG.md#L779-L786`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L779-L786)

### F-37: Transformation after authorization is a gateway task, not a policy task {#f-37}

- **Status**: resolved in demo
- **Point**: a BSN must not enter the AuthZEN envelope. So the DvTP pipeline cannot move into the PDP.
- **Outcome**: demo issue [#88](https://github.com/ICTU/GBO-demo/issues/88) moved the transformation to the source gateway. After that change, the envelope on the DvTP path carries only a placeholder. The EUDI and ASI routes do not meet the rule "no BSN in the authorization envelope" ([F-54](findings.md#f-54)).
- **Landed in**: [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-81](../requirements/pseudonymization.md#req-81), [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md).

### F-38: The rich catalog extended to routing and policy lookup {#f-38}

- **Status**: closed
- **Point**: the EUDI adapter kept its own use-case catalog with FSC routing, next to the policy-side mapping.
- **Outcome**: the use-case catalog is gone. Routing comes from contract discovery and source metadata ([SL-46](increments.md#sl-46), [F-57](findings.md#f-57)). [F-74](findings.md#f-74) holds the DvTP remainder.
- **Landed in**: [REQ-64](../requirements/sources-identity.md#req-64), [ADR-0016](../decisions/0016-source-owned-metadata.md).

### F-39: FSC v2.4.0 has no OTel instrumentation, so trace context breaks at FSC hops {#f-39}

- **Status**: resolved in demo
- **Point**: traces broke after the move to real FSC.
- **Outcome**: Outway and Inway forward headers unchanged, so `traceparent` reaches the source. The only break is the AuthZEN hop ([F-41](#f-41)). The chain follows W3C Trace Context. The ADL records the FSC transaction ID next to the trace context ([F-67](#f-67)).
- **Landed in**: [REQ-55](../requirements/logging-audit.md#req-55), [ADR-0035](../decisions/0035-w3c-trace-context.md) (supersedes ADR-0019).

### F-40: `fsc-logging` defines a transaction log and `Fsc-Transaction-Id` correlation {#f-40}

- **Status**: resolved in demo
- **Point**: the Logius draft [fsc-logging](https://logius-standaarden.github.io/fsc-logging/) gives a shape for per-peer transaction logs. So GBO does not have to invent one.
- **Outcome**: [SL-38](increments.md#sl-38) showed the shape: the developer portal reads the transaction log of each peer. The fsc-logging draft is one of three related logging standards ([F-63](#f-63)).
- **Landed in**: [REQ-55](../requirements/logging-audit.md#req-55), [AV-01](../requirements/admission.md#av-01), [ADR-0035](../decisions/0035-w3c-trace-context.md).
- **Evidence**: [`dev-portal-backend/fsctxlog.go`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/fsctxlog.go)

### F-41: FSC plugins use `context.Background()` for downstream calls {#f-41}

- **Status**: resolved in demo (ADL side not met)
- **Point**: the trace context is lost at the AuthZEN hop.
- **Outcome**: the Inway sends only `X-Request-Id` to the PDP. The original headers are nested in `context.headers`. OpenFTV v0.1.0 reads neither of these values there. The ADL record behind the Inway has its own trace and no transaction ID. The developer portal finds the record through the stored request headers. The fix is upstream in OpenFSC (demo issue [#369](https://github.com/ICTU/GBO-demo/issues/369)).
- **Landed in**: [REQ-55](../requirements/logging-audit.md#req-55), [ADR-0035](../decisions/0035-w3c-trace-context.md).
- **Evidence**: [`dev-portal-backend/adl.go#L48-L68`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/adl.go#L48-L68)

### F-42: Two routes to the FSC transaction log {#f-42}

- **Status**: closed
- **Point**: the log API exists inside the organization and on the peer-facing Manager. The demo uses the internal API.
- **Outcome**: the internal route is a demo shortcut. The open [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid) decisions on access and aggregation, and [Q-08](open-questions.md#q-08), decide who can read the logs in production.
- **Evidence**: [`dev-portal-backend/fsctxlog.go`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/fsctxlog.go)

### F-43: Grant properties as a trusted dispatch signal per contract {#f-43}

- **Status**: superseded
- **Point**: move `flow` and `subject_id_type` from an untrusted header into signed FSC grant properties.
- **Outcome**: the first build used an additional-claims service ([PR #55](https://github.com/ICTU/GBO-demo/pull/55), [ADR-0014](../decisions/0014-provider-signed-flow-claims.md)). [PR #284](https://github.com/ICTU/GBO-demo/pull/284) then built the property route ([F-62](#f-62)). [PR #363](https://github.com/ICTU/GBO-demo/pull/363) removed `flow`, because the regime follows from the evidence ([F-70](findings.md#f-70)). Demo issue [#473](https://github.com/ICTU/GBO-demo/issues/473) removed `subject_id_type`.
- **Landed in**: [ADR-0030](../decisions/0030-grant-properties.md) (superseded by [ADR-0031](../decisions/0031-regime-from-evidence.md)).
- **Evidence**: [`CHANGELOG.md#L787-L790`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L787-L790)

### F-44: Where does the PI live, and how does policy bind to the subject? {#f-44}

- **Status**: resolved in demo
- **Point**: the register stored the PI to let the PDP look up consent by PI.
- **Outcome**: after [SL-47](increments.md#sl-47) ([PR #238](https://github.com/ICTU/GBO-demo/pull/238)), the PI is not in the register. The register keeps a portal-scoped subject reference. The subject travels in a signed, audience-bound proof. Policy binds to the subject in that proof. No lookup by PI exists. Since [SL-51](increments.md#sl-51), the proof carries an encrypted value per party.
- **Landed in**: [REQ-68](../requirements/consent.md#req-68), [REQ-69](../requirements/pseudonymization.md#req-69), [REQ-80](../requirements/pseudonymization.md#req-80), [ADR-0032](../decisions/0032-consent-proof.md).

### F-45: Grant-link configuration only through a Controller UI form {#f-45}

- **Status**: closed
- **Point**: FSC v2.4.0 has no REST endpoint for Outway grant links. The demo writes the grant links with SQL.
- **Outcome**: accepted as a demo shortcut. A REST endpoint is a candidate feature request to the FSC maintainers, together with [F-46](#f-46).
- **Evidence**: [`fsc-infra/scripts/seed-bri-contract.sh`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/scripts/seed-bri-contract.sh)

### F-46: Service endpoint update only through the Controller UI or database {#f-46}

- **Status**: closed
- **Point**: to change a service endpoint by REST, FSC v2.4.0 needs a delete and a re-create.
- **Outcome**: accepted as a demo shortcut. In demo v0.9.0, the seed sets the endpoint. A REST call for this change is a candidate feature request, together with [F-45](#f-45).

### F-49: A flow-name suffix as the PDP source-profile discriminator was ad hoc {#f-49}

- **Status**: premise lapsed
- **Point**: the PDP chose the source schema by a suffix on the flow name.
- **Outcome**: [SL-48](increments.md#sl-48) ([PR #236](https://github.com/ICTU/GBO-demo/pull/236)) removed the suffix. Later, the flow itself went too ([F-70](findings.md#f-70)). In demo v0.9.0, rules name the FSC services that they apply to ([F-90](#f-90)). The general question of schema selection went to a design spike, demo issue [#137](https://github.com/ICTU/GBO-demo/issues/137).
- **Landed in**: [REQ-97](../requirements/authorization.md#req-97), [ADR-0031](../decisions/0031-regime-from-evidence.md).

### F-50: Attestation issuer and purpose statement are bound to the signing certificate {#f-50}

- **Status**: closed
- **Point**: a fallback to another source's certificates made the wallet show the wrong issuer and purpose ([PR #125](https://github.com/ICTU/GBO-demo/pull/125)).
- **Outcome**: built. Every source holder has its own certificate set. Missing material causes a hard failure. [Q-17](open-questions.md#q-17) and demo issue [#225](https://github.com/ICTU/GBO-demo/issues/225) cover key management and the status list.
- **Landed in**: [REQ-58](../requirements/eudi-issuance.md#req-58), [ADR-0018](../decisions/0018-eudi-disclosure-issuance.md).

### F-53: Two decision logs side by side and no designated audit source {#f-53}

- **Status**: resolved in demo
- **Point**: the same decision landed in the ADL (Postgres) and in the console log of the engine (Loki). Neither log was named the audit source.
- **Outcome**: [SL-50](increments.md#sl-50): the ADL implements the Logius Authorization Decision Log standard. The ADL is the audit source. The console log is observability. [PR #373](https://github.com/ICTU/GBO-demo/pull/373) makes the developer portal read the ADL. The per-field detail stays in the console log only ([F-72](findings.md#f-72)). The governance decision on this choice runs with [Q-08](open-questions.md#q-08).
- **Landed in**: [REQ-71](../requirements/logging-audit.md#req-71), [ADR-0036](../decisions/0036-adl-decision-record.md).

### F-55: Admission is a registration instead of a policy rule, and the automatic "no" stays reversible {#f-55}

- **Status**: closed
- **Point**: admission was a hard-coded list in Rego, so every change was a policy release.
- **Outcome**: [SL-45](increments.md#sl-45) ([PR #228](https://github.com/ICTU/GBO-demo/pull/228), [PR #239](https://github.com/ICTU/GBO-demo/pull/239)) added an admission register. The PDP reads it as a PIP. The contract decision has its own rule set. A refused proposal stays pending, and a terminal refusal is a separate act. This design matches [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel) and S05. [Q-22](answered-questions.md#q-22) answers the governance question.
- **Landed in**: [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-63](../requirements/admission.md#req-63), [ADR-0015](../decisions/0015-contract-acceptance-by-policy.md).
- **Evidence**: [`policies/fsc/autosign.rego#L170-L171`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L170-L171)

### F-56: The contract payload is thin: the decider sees who, not what {#f-56}

- **Status**: closed
- **Point**: the FSC Manager sends only the hash, the grant types, and the peer IDs to the contract decision. As a result, admission per service is not possible. Admission is per source holder.
- **Outcome**: accepted on purpose (decision of September 2, 2026). Every regime authorizes the actor and the basis per request ([REQ-48](../requirements/authorization.md#req-48)). Since [PR #363](https://github.com/ICTU/GBO-demo/pull/363), no grant property authorizes anything. Admission per service runs through the catalog and the consent ([Q-22](answered-questions.md#q-22), demo issue [#382](https://github.com/ICTU/GBO-demo/issues/382)). Demo issue [#240](https://github.com/ICTU/GBO-demo/issues/240) lists the triggers to reopen this point.
- **Landed in**: [REQ-61](../requirements/admission.md#req-61), [ADR-0015](../decisions/0015-contract-acceptance-by-policy.md).

### F-58: A valid transport contract does not take a source into use {#f-58}

- **Status**: closed
- **Point**: the first version found sources implicitly. A valid FSC contract was enough to fetch metadata and to publish products.
- **Outcome**: [SL-46](increments.md#sl-46) ([PR #237](https://github.com/ICTU/GBO-demo/pull/237)) added explicit source configurations, a visible *blocked* status per source, and automatic promotion that is off by default. Transport and mandate are two separate decisions. This design matches [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel) and S07.
- **Landed in**: [REQ-65](../requirements/sources-identity.md#req-65), [ADR-0016](../decisions/0016-source-owned-metadata.md).

### F-59: Source releases have the lifecycle that policy bundles lack {#f-59}

- **Status**: closed
- **Point**: source metadata has validation before activation, bounded staleness, isolation, atomic promotion, and rollback. Policy bundles have none of these.
- **Outcome**: [REQ-66](../requirements/sources-identity.md#req-66) and [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie) state the requirement in generic form. The policy side follows [F-52](findings.md#f-52) and [Q-21](answered-questions.md#q-21). Signing (demo issue [#426](https://github.com/ICTU/GBO-demo/issues/426)) closed as not planned ([F-09](#f-09)).
- **Landed in**: [REQ-66](../requirements/sources-identity.md#req-66), [ADR-0016](../decisions/0016-source-owned-metadata.md), [ADR-0021](../decisions/0021-central-pap-signed-bundles.md).

### F-60: Three identity carriers, with the certificate authoritative for the legal identity {#f-60}

- **Status**: closed
- **Point**: the demo used one field for the FSC Peer ID and the OIN. In the simulation, these values differ.
- **Outcome**: [SL-49](increments.md#sl-49): since [PR #242](https://github.com/ICTU/GBO-demo/pull/242), the demo uses two fields. Since [PR #247](https://github.com/ICTU/GBO-demo/pull/247), the OIN and the organization name come from the validated issuer certificate. This follows the GO (PKIoverheid) and [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel). [Q-06](answered-questions.md#q-06) and [Q-07](answered-questions.md#q-07) are answered. The link between OIN, KvK, and eIDAS identifiers is an open S04 decision outside the GBO build.
- **Landed in**: [REQ-67](../requirements/sources-identity.md#req-67), [ADR-0023](../decisions/0023-identity-convergence.md).

### F-61: The legal basis travels as proof, the status stays online: a deliberate asymmetry in freshness {#f-61}

- **Status**: closed
- **Point**: the consent proof is a signed, audience-bound artifact. The PDP verifies the proof locally. On every request, the PDP fetches the consent status online. The PDP can cache keys, but it cannot cache a status. If the status is unknown, the PDP denies.
- **Outcome**: "status online, fail-closed" is the norm (GO, [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), FR-11 v0.9). Since [PR #371](https://github.com/ICTU/GBO-demo/pull/371), the policy itself verifies the proof and fetches the status. Keys stay in the cache for five minutes, with no stale fallback. [REQ-75](../requirements/consent.md#req-75) gives the numbers. To replay a decision, the record must hold the status answer (see [F-72](findings.md#f-72)).
- **Landed in**: [REQ-68](../requirements/consent.md#req-68), [REQ-75](../requirements/consent.md#req-75), [Q-05](answered-questions.md#q-05), [ADR-0032](../decisions/0032-consent-proof.md).
- **Evidence**: [`policies/gbo/consent.rego#L25`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L25)

### F-62: The additional-claims service is a version-compatibility workaround, and the contract-properties route is open again {#f-62}

- **Status**: resolved in demo
- **Point**: the source Manager injected the regime claims into the FSC token from a manual JSON file (`add` hook). The reason was a simulation peer on OpenFSC v1.44. That version cannot co-sign contract properties. FSC standardizes `grant.data.properties`: the properties are in the grant hash and in the `prp` claim of the token. OpenFSC supports them since v2.0.0.
- **Outcome**: [PR #284](https://github.com/ICTU/GBO-demo/pull/284) moved the properties into the co-signed contract and removed the `additional-claims-service`. [PR #363](https://github.com/ICTU/GBO-demo/pull/363) then removed `flow` as a property, because the regime follows from the proof ([F-70](findings.md#f-70)). [PR #475](https://github.com/ICTU/GBO-demo/pull/475) removed `subject_id_type`. REQ-56 and REQ-70 are removed. [Q-15](answered-questions.md#q-15) answers how contracts carry the correct properties.
- **Landed in**: [REQ-74](../requirements/authorization.md#req-74), [ADR-0031](../decisions/0031-regime-from-evidence.md) (supersedes [ADR-0030](../decisions/0030-grant-properties.md)).

### F-63: Logius has three related logging standards, and the demo decision log implements one of them {#f-63}

- **Status**: closed
- **Point**: Logius keeps a family of log standards with the same OTel record shape: LDV (processing), ADL (authorization decisions), and FSC-Logging (transport). The OpenFTV decision log already implements the ADL.
- **Outcome**: the family is the norm under [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid). ADL 1.0.0 is published. A PDP decision is not a processing in LDV terms, so it goes to the ADL. Since [PR #373](https://github.com/ICTU/GBO-demo/pull/373), the ADL is the audit source of the demo. This answered [F-53](#f-53). [REQ-59](../requirements/logging-audit.md#req-59) and [F-72](findings.md#f-72) hold the open conformance points.
- **Landed in**: [REQ-71](../requirements/logging-audit.md#req-71), [REQ-72](../requirements/logging-audit.md#req-72), [ADR-0036](../decisions/0036-adl-decision-record.md), [ADR-0026](../decisions/0026-ldv-integration.md).
- **Evidence**: [`OBSERVABILITY.md#L61-L64`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/OBSERVABILITY.md#L61-L64)

### F-64: The LDV gap is at the processing instead of the decision, and the sidecar transformation is itself a processing {#f-64}

- **Status**: resolved in demo
- **Point**: no component wrote LDV records. In LDV terms, these are all processings: the source query, de-pseudonymization at the source, register operations, and attestation building. Each controller (Verantwoordelijke) must log its own processings in its own logbook.
- **Outcome**: built in demo issue [#302](https://github.com/ICTU/GBO-demo/issues/302) and corrected in [PR #366](https://github.com/ICTU/GBO-demo/pull/366). The build has trace context, one logbook per system, and a pseudonym per controller. In demo v0.9.0, the register of processing activities is a stand-in ([Q-08](open-questions.md#q-08)).
- **Landed in**: [REQ-72](../requirements/logging-audit.md#req-72), [ADR-0026](../decisions/0026-ldv-integration.md).
- **Evidence**: [`services/ldv-logboek`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek), [`docs/ldv/README.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/ldv/README.md)

### F-65: `dataSubjectId` and the read extension fit the GBO pseudonym model and settle how citizen access works {#f-65}

- **Status**: closed
- **Point**: LDV puts the data subject in `dpl.core.data_subject_id`. LDV recommends a pseudonym, with an explicit type field. The read extension builds a chain from the starting application through `nextLogbookId`.
- **Outcome**: this supports [REQ-60](../requirements/logging-audit.md#req-60): a pseudonym in the log is the recommended form. With recipient-specific pseudonyms, access across organizations can search only on the trace ID. A search on the subject is not possible. The idea that the consent portal reads the whole chain through `nextLogbookId` does not work in DvTP, because GBO does not start the chain ([F-68](findings.md#f-68)). Citizen access goes per controller (GDPR art. 15). Each controller logs under its own pseudonym ([F-69](#f-69)).
- **Landed in**: [REQ-60](../requirements/logging-audit.md#req-60), [REQ-72](../requirements/logging-audit.md#req-72), [Q-01](open-questions.md#q-01), [Q-08](open-questions.md#q-08), [ADR-0026](../decisions/0026-ldv-integration.md).

### F-66: Erratum: the PuB-EAA seal and the Access CA were confused with PKIoverheid {#f-66}

- **Status**: closed
- **Point**: an earlier analysis said that PuB-EAAs are sealed with "PKIoverheid or the EUDI Access CA". That statement is wrong.
- **Outcome**: a PuB-EAA carries a qualified seal from a certificate that a QTSP issued (Regulation (EU) 2024/1183, Annex VII). Relying parties check the seal against the QTSP trust anchor or the PuB-EAA Provider LoTE (ETSI TS 119 602). An Access CA issues access certificates only for authentication to the wallet (ETSI TS 119 411-8). An Access CA never signs attestations. PKIoverheid is the Dutch PKI for mTLS and FSC. "PKIoverheid as Dutch Access CA" is an open recommendation, not a fact.
- **Landed in**: [Q-07](answered-questions.md#q-07), [REQ-58](../requirements/eudi-issuance.md#req-58), [REQ-67](../requirements/sources-identity.md#req-67), [ADR-0023](../decisions/0023-identity-convergence.md), [ADR-0028](../decisions/0028-pubeaa-productization.md).

### F-67: A trace ID equal to `Fsc-Transaction-Id` conflicts with LDV and the ADL {#f-67}

- **Status**: resolved in demo
- **Point**: [REQ-55](../requirements/logging-audit.md#req-55) made the trace ID equal to the FSC transaction ID. LDV and the ADL take the trace ID unchanged from `traceparent`. FSC-Logging makes a transaction ID unique per transaction. The equality breaks in three cases:
    - A caller brings its own `traceparent`.
    - One processing queries several sources.
    - The request takes an extra FSC hop, for example the consent status lookup.
- **Outcome**: [PR #366](https://github.com/ICTU/GBO-demo/pull/366): every component reads `traceparent` first. Each component records the transaction ID next to the trace ID (ADL `adl.fsc.transaction_id`). The transaction ID is a fallback only at an entry point without `traceparent`. REQ-55 is revised.
- **Landed in**: [REQ-55](../requirements/logging-audit.md#req-55), [ADR-0035](../decisions/0035-w3c-trace-context.md) (supersedes [ADR-0019](../decisions/0019-fsc-transaction-id-tracing.md)).
- **Evidence**: [`services/ldv-client/tracecontext.go#L25`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext.go#L25)

### F-69: A pseudonym that travels across the chain lands in the logbooks of two controllers {#f-69}

- **Status**: resolved in demo
- **Point**: the source sidecar logged the PI that it received from the consumer. The same PI was then in the consumer logbook and in the source logbook. A reader with access to both logbooks can join them on the person as well as on the trace.
- **Outcome**: [REQ-72](../requirements/logging-audit.md#req-72) states that each controller logs under a pseudonym from its own pseudonym space. A controller never logs under an identifier that the caller sends. The demo fixed this in demo issue [#367](https://github.com/ICTU/GBO-demo/issues/367) through [PR #366](https://github.com/ICTU/GBO-demo/pull/366). Since [SL-51](increments.md#sl-51), the cause is gone. No pseudonym travels: the consumer sends a placeholder ([F-76](findings.md#f-76)).
- **Landed in**: [REQ-72](../requirements/logging-audit.md#req-72), [ADR-0026](../decisions/0026-ldv-integration.md).

### F-73: The actor binding of consent assumes that the consumer calls itself, and an integrator breaks that assumption {#f-73}

- **Status**: closed
- **Point**: the consent proof binds the consumer to the transport caller. FR-18 and FR-37 v0.9 let an integrator call as a processor for the dienstverlener, with its own identity. In that case, the binding fails, or it needs an exception that empties it.
- **Outcome**: FR-37 v0.9, criterion 4, and [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie) answer the design: the decision uses both the acting party and the represented party. The consent binds the represented party. The integrator connects under an FSC delegated grant and needs a registered mandate. Demo issue [#379](https://github.com/ICTU/GBO-demo/issues/379) built this. In demo v0.9.0, the autosign policy admits a registered delegation pair. The broad representation model stays with PSA B-19.
- **Landed in**: [REQ-106](../requirements/consent.md#req-106), [AV-06](../requirements/admission.md#av-06), [Q-12](answered-questions.md#q-12), [Q-46](open-questions.md#q-46), [ADR-0034](../decisions/0034-integrator-delegation.md).
- **Evidence**: [`docs/integrator.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/integrator.md), [`policies/fsc/autosign.rego#L119-L124`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L119-L124)

### F-90: Field keys are unique only within one schema, so a rule without a service binding applied on every service {#f-90}

- **Status**: resolved in demo
- **Point**: the PDP bound rules to field keys `Type.field` ([REQ-17](../requirements/authorization.md#req-17)), without the service. `Query.ingeschrevenPersoon` is in the `bri` schema and in the `brp` schema. As a result, EUD0001 also applied on `brp`. A designated issuer that asked only `__typename` there learned whether a person exists and is a resident.
- **Outcome**: since [PR #527](https://github.com/ICTU/GBO-demo/pull/527), every rule names the FSC services it applies to, and a test enforces this. Regime and fields decide which rule judges a field, and the service is the third axis. A PDP that serves one source with several schemas also needs this axis. The TO proposes it for PSA S05 and for the guideline for bronhouders.
- **Landed in**: [REQ-97](../requirements/authorization.md#req-97), [REQ-74](../requirements/authorization.md#req-74), [ADR-0009](../decisions/0009-closed-world-rules.md).
- **Evidence**: [`policies/gbo/engine_test.rego#L497`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L497), [`asi0001.rego#L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego#L23)

