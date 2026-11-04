# Demo increments

A demo increment (ID SL-NN) is a bounded piece of demo work. Each
increment proved part of the design and produced requirements, findings,
and open questions. The IDs are stable anchors: the
[design to demo matrix](matrix.md), the [findings](findings.md), the
[open questions](open-questions.md), and the requirement pages refer to
them. The issues and pull requests of
[ICTU/GBO-demo](https://github.com/ICTU/GBO-demo) track the work itself.

Each increment entry uses the same fields:

- **Status values**: done, planned, blocked, dropped, merged, or partly
  covered.
- **Demo work**: links go to ICTU/GBO-demo only. The public repository
  started with v0.1.0 on July 20, 2026. Increments SL-01a to SL-42 were
  built before that date, so they have no public pull request. The code
  that they produced is in the public history from v0.1.0.
- **Produced**: the IDs that the increment created or changed. If a
  later increment replaced the result, the entry names the successor.
- **Explained in**: the TO page that explains the result.

[Demo work outside increments](#outside-increments) lists the demo work
that was not part of an increment.

## Increments

### SL-01a: Consent TTL and finer denial reasons {#sl-01a}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the consent register (toestemmingsregister) sets an expiry time, and the
  policy denies an expired consent. If the expiry time is missing or
  unreadable, the policy also denies. The policy gives a separate reason
  code for each failed check (not found, withdrawn, expired, scope
  mismatch, and field not in consent).
- **Produced**: [REQ-19](../requirements/consent.md#req-19),
  [REQ-06](../requirements/authorization.md#req-06) (made more precise),
  and part of [F-04](findings-closed.md#f-04).
- **Explained in**: [Consent](../concepts/consent.md)

### SL-01b: Single use and status machine {#sl-01b}

- **Status**: blocked
- **Demo work**: none.
- **What it showed**: not built. The increment waited on
  [Q-04](answered-questions.md#q-04) (single use or repeatable). Q-04 is
  answered: FR-DvTP v0.9 makes a consent repeatable within its validity
  period, so single use is not necessary. The status
  "retrieved" from FR-22 is open: [Q-42](open-questions.md#q-42) asks
  who marks a consent as retrieved, and when.
- **Produced**: rest of [F-04](findings-closed.md#f-04) (closed),
  [F-19](findings.md#f-19).
- **Explained in**: [Consent](../concepts/consent.md)

### SL-02: Pseudonymization in the path {#sl-02}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the demo kept the BSN away from private consumers
  without a decision on the pseudonym form ([Q-01](open-questions.md#q-01)).
  The consent register stored a polymorphic identity (PI) instead of the
  BSN. The PEP resolved the BSN only after an allow. For a denied
  request, the PEP did not resolve the BSN at all.
- **Produced**: [REQ-20](../requirements/pseudonymization.md#req-20) and
  [REQ-21](../requirements/pseudonymization.md#req-21). Later, the
  conversion moved to the source source gateway ([SL-22](#sl-22)). Since
  [SL-51](#sl-51), the proof carries a value per source, and the source
  decrypts it after the decision.
- **Explained in**: [Pseudonymization](../concepts/pseudonymization.md)

### SL-03a: AST field parsing in OPA {#sl-03a}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the policy parses the real GraphQL query, with
  schema validation, instead of a regex in the PEP. The fields in the
  query must be a subset of the allowed fields of the scope. If a query
  does not parse, it gets a deny.
- **Produced**: [REQ-17](../requirements/authorization.md#req-17), and
  model B (field allowlist) for [Q-14](open-questions.md#q-14).
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-03b: Constraint axis (4b) and two-schema model {#sl-03b}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the policy checked that the query carried the
  consent ID and that it matched the authorization context. A
  consumer-facing schema without BSN stood next to the internal source
  schema, and the PEP translated between them.
- **Produced**: REQ-25 to REQ-27 (removed later, successors
  [REQ-79](../requirements/pseudonymization.md#req-79) and
  [REQ-17](../requirements/authorization.md#req-17)), and
  [REQ-06](../requirements/authorization.md#req-06) (new reason codes).
  Later, the query translation moved to the source source gateway
  ([SL-42](#sl-42)).
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-04: Persist OPA decision logs {#sl-04}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the PDP logs every decision with a decision ID, the
  reason, and the trace ID of the request. Loki stores the log, and a
  Grafana panel links each decision to its trace.
- **Produced**: [REQ-32](../requirements/logging-audit.md#req-32)
  (REQ-31 merged into [REQ-71](../requirements/logging-audit.md#req-71)),
  and the audit part of [F-07](findings-closed.md#f-07).
- **Explained in**: [Logging](../concepts/logging.md)

### SL-05: FSC sector-grant check {#sl-05}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: organization permission is an authorization concern
  of its own, next to the legal basis. The demo checked a sector-level
  grant per service. FSC has no sector concept ([F-36](findings-closed.md#f-36)).
  [#378](https://github.com/ICTU/GBO-demo/issues/378) removed the
  `sector-pip`. Since [SL-45](#sl-45), a register gives the admission.
- **Produced**: part of [F-08](findings-closed.md#f-08) (REQ-33 and REQ-34,
  removed later).
- **Explained in**: [ADR-0022](../decisions/0022-sector-grants.md),
  [Contract admission and source activation](../runtime/admission.md)

### SL-06a: User demo flow A: consent issuance {#sl-06a}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a citizen goes from a mock service provider (dienstverlener) website
  to the consent portal (toestemmingsportaal) inside a MijnOverheid shell. He logs in with a
  DigiD mock, gives consent, and returns. The redirect carries the
  consumer, the service, the purpose, the data sets, and the return
  address. The result page fetches real data through the whole chain.
- **Produced**: [REQ-37](../requirements/consent.md#req-37),
  [F-15](findings-closed.md#f-15), [F-16](findings-closed.md#f-16),
  [F-17](findings-closed.md#f-17), and [F-18](findings-closed.md#f-18).
- **Explained in**: [Citizen grants consent](../runtime/dvtp-consent.md)

### SL-06b: User demo flow B: access under MijnOverheid {#sl-06b}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a citizen sees his consents under MijnOverheid,
  with status active, expired, or revoked, and opens a detail page. He
  can revoke a consent after he approves the revoke in a dialog. The next
  request on that consent gets a deny.
- **Produced**:
    - requirements [REQ-38](../requirements/consent.md#req-38),
      [REQ-39](../requirements/consent.md#req-39),
      [REQ-40](../requirements/consent.md#req-40), and
      [REQ-14](../requirements/consent.md#req-14) (REQ-41 merged into it)
    - findings [F-19](findings.md#f-19), [F-20](findings-closed.md#f-20), and
      [F-17](findings-closed.md#f-17) (widened)
- **Explained in**: [Citizen views and revokes consents](../runtime/dvtp-citizen-access.md)

### SL-07: Restore trace correlation {#sl-07}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: trace context propagates end to end. One trace
  covered all services of a request.
- **Produced**: no requirement. The result is the basis for
  [REQ-55](../requirements/logging-audit.md#req-55).
- **Explained in**: [Logging](../concepts/logging.md)

### SL-08: Consent PIP through PEP pre-fetch {#sl-08}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the PEP fetched the consent record and gave it to
  the policy as input, so the policy engine made no network call. Since
  [PR #371](https://github.com/ICTU/GBO-demo/pull/371), the flow is
  reversed: the policy verifies the signed consent proof and asks the
  register for the status itself.
- **Produced**: [REQ-18](../requirements/authorization.md#req-18) and
  [F-22](findings-closed.md#f-22). Later,
  [REQ-68](../requirements/consent.md#req-68) replaced this result.
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-09: Onboarding and gatekeeper flow {#sl-09}

- **Status**: partly covered
- **Demo work**: covered by [SL-45](#sl-45).
- **What it showed**: [SL-45](#sl-45) delivered the admission register and
  the contract decision by the PDP. Missing: an onboarding interface for
  consumers, and the test of the connection conditions
  ([Q-74](open-questions.md#q-74)). [Q-22](answered-questions.md#q-22)
  answers who keeps the register and on which grounds.
- **Produced**: see [SL-45](#sl-45).
- **Explained in**: [Contract admission and source activation](../runtime/admission.md)

### SL-10: Observability infrastructure (Loki and Grafana) {#sl-10}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: structured logs carry the trace ID. Loki and Grafana
  link a log line to its trace and back.
- **Produced**: REQ-28 and REQ-29 (merged into
  [REQ-55](../requirements/logging-audit.md#req-55) and
  [REQ-60](../requirements/logging-audit.md#req-60)), and the
  correlation part of [F-07](findings-closed.md#f-07).
- **Explained in**: [Logging](../concepts/logging.md)

### SL-11: Consent portal backend (S02) {#sl-11}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the consent portal (PSA S02) became a service of
  its own, apart from the consent register (S01). The DigiD mock gives a
  token, and the backend takes the citizen identity only from that token.
  The backend calls BSNk, so the register gets no BSN.
- **Produced**: [REQ-23](../requirements/consent.md#req-23),
  [REQ-24](../requirements/consent.md#req-24) (REQ-22 and REQ-35
  were removed later).
- **Explained in**: [Building blocks](../building-blocks/components.md),
  [Citizen grants consent](../runtime/dvtp-consent.md)

### SL-12: Consent register persistence {#sl-12}

- **Status**: planned
- **Demo work**: none as an increment.
- **What it showed**: not built as planned. In demo v0.9.0, the register
  has a Postgres store. If `DATABASE_URL` is set, the register uses this
  store
  ([`postgres_store.go`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/postgres_store.go)).
  The local compose stack does not set the variable and runs in memory.
- **Produced**: none. [Q-54](open-questions.md#q-54) holds the open
  durability requirements.
- **Explained in**: [Consent](../concepts/consent.md)

### SL-13: Rego structure clean-up {#sl-13}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a structure in three parts (common helpers, entry
  point, rules per use case) scales to more access bases without
  duplicated code. Consent moved to the level of a data set (scope).
- **Produced**: [REQ-10](../requirements/consent.md#req-10) (reworked)
  and [F-03](findings-closed.md#f-03) (put into context).
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-14: Query template as upper bound (POC) {#sl-14}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a proof of concept of variant D from
  [Q-14](open-questions.md#q-14) on one scope. A query template sets the
  upper bound of what a consumer can ask. The proof of concept gave the
  discussion a concrete example. It is no production evidence.
- **Produced**: no requirement. The result is input for
  [Q-14](open-questions.md#q-14).
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-15: Phase out orchestrator {#sl-15}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the demo needs no coordinating service. The three
  front ends call their own capability service directly. This design
  supports the separation of generic and specific functions (PSA P-14).
- **Produced**: no requirement.
- **Explained in**: [Building blocks](../building-blocks/components.md)

### SL-16: Developer portal {#sl-16}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a separate developer portal (scenarios, request
  builder, replay, architecture strip, links to traces) keeps the
  technical controls out of the citizen demo.
- **Produced**: no requirement.
- **Explained in**: [Building blocks](../building-blocks/components.md)

### SL-17: AuthZEN envelope adoption {#sl-17}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the PDP answers in the AuthZEN decision envelope,
  with a reason code for the operator on a deny. At that time, the wire
  shape between PEP and PDP did not follow the GBO profile
  ([F-27](findings-closed.md#f-27)).
- **Produced**: [F-27](findings-closed.md#f-27),
  [REQ-42](../requirements/authorization.md#req-42).
- **Explained in**: [Authorization](../concepts/authorization.md),
  [ADR-0002](../decisions/0002-opa-rego-authzen.md)

### SL-18: RFC0052-GBO policy refactor and PDP handler {#sl-18}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a context handler in front of the policy engine
  parses the GraphQL request. The policy has named rules that bind to
  types and fields, and it decides per field. Each decision lists the
  rules that it evaluated. The handler became the request mapper inside
  the OpenFTV PDP.
- **Produced**: [F-27](findings-closed.md#f-27).
- **Explained in**: [Authorization](../concepts/authorization.md),
  [ADR-0013](../decisions/0013-pdp-request-mapper.md)

### SL-19: EUDI stand-alone in the demo compose stack {#sl-19}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the issuance server of nl-wallet runs in the demo
  compose stack. A pre-production wallet received a real attestation from
  the demo, without the GBO chain.
- **Produced**: [Q-17](open-questions.md#q-17),
  [Q-18](open-questions.md#q-18).
- **Explained in**: [EUDI issuance](../runtime/eudi-issuance.md),
  [ADR-0018](../decisions/0018-eudi-disclosure-issuance.md)

### SL-20: EUDI adapter with AuthZEN dispatch through the PEP {#sl-20}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a thin adapter between the issuance server and the
  source sends EUDI requests through the same PDP as DvTP. One generic
  chain serves two front doors. The `flow` field in the body that chose
  the regime was an interim solution ([F-32](findings-closed.md#f-32)).
- **Produced**:
    - findings [F-31](findings-closed.md#f-31), [F-32](findings-closed.md#f-32), and
      [F-25](findings-closed.md#f-25)
    - requirements [REQ-44](../requirements/authorization.md#req-44) and
      [REQ-45](../requirements/eudi-issuance.md#req-45) (REQ-43 removed)
    - open questions [Q-15](answered-questions.md#q-15),
      [Q-16](answered-questions.md#q-16), and [Q-17](open-questions.md#q-17)
- **Explained in**: [EUDI issuance](../runtime/eudi-issuance.md)

### SL-21: Level C multi-policy demo {#sl-21}

- **Status**: planned
- **Demo work**: none.
- **What it showed**: not started. The increment has no worked-out
  scope.
- **Produced**: none.
- **Explained in**: no page.

### SL-22: Source source gateway de-pseudonymization (DvTP) {#sl-22}

- **Status**: done
- **Demo work**: before the public repository. It was built together
  with [SL-23](#sl-23) in [SL-42](#sl-42).
- **What it showed**: the conversion from pseudonym to BSN moved from the
  PEP to a source gateway at the source, with the keys of the source. Since
  then, the GBO core (PEP, PDP, and policy engine) handles no BSN in the
  DvTP path.
- **Produced**: [F-30](findings-closed.md#f-30),
  [REQ-21](../requirements/pseudonymization.md#req-21) (place of the
  conversion).
- **Explained in**: [Pseudonymization](../concepts/pseudonymization.md),
  [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)

### SL-23: Consent out of the query, pseudonym in the query, and policy binding {#sl-23}

- **Status**: done
- **Demo work**: before the public repository. It was built in
  [SL-42](#sl-42).
- **What it showed**: the consent ID left the GraphQL query. The query
  carried a pseudonym on the subject place, and the policy bound that
  value to the consent. Consent became a matter for the policy instead of
  the business flow.
- **Produced**: [F-29](findings-closed.md#f-29) and [F-44](findings-closed.md#f-44).
  REQ-25 to REQ-27 were revised and removed later. Since
  [SL-51](#sl-51), the query carries a placeholder instead of a pseudonym
  ([REQ-79](../requirements/pseudonymization.md#req-79)).
- **Explained in**: [Pseudonymization](../concepts/pseudonymization.md),
  [ADR-0032](../decisions/0032-consent-proof.md)

### SL-24: Access-basis dispatch through component metadata or certificate {#sl-24}

- **Status**: dropped
- **Demo work**: none of its own.
- **What it showed**: the plan was to derive the regime (consent or PID)
  from verified component identity instead of a declared `flow` field.
  First, signed FSC grant properties replaced the plan. Since
  [PR #363](https://github.com/ICTU/GBO-demo/pull/363), the regime
  follows from the evidence that a request carries.
- **Produced**: replaced by
  [REQ-74](../requirements/authorization.md#req-74), with
  [F-32](findings-closed.md#f-32), [F-43](findings-closed.md#f-43), and
  [Q-15](answered-questions.md#q-15).
- **Explained in**: [ADR-0031](../decisions/0031-regime-from-evidence.md)

### SL-25: PID signature verification in the EDI adapter {#sl-25}

- **Status**: dropped
- **Demo work**: none.
- **What it showed**: not necessary. The issuance server verifies the
  PID, and the adapter gets plain JSON attributes. One gap stays: the
  callback from the issuance server to the adapter has no authentication
  ([#133](https://github.com/ICTU/GBO-demo/issues/133)).
- **Produced**: input for [REQ-45](../requirements/eudi-issuance.md#req-45)
  and [F-70](findings.md#f-70).
- **Explained in**: [EUDI issuance](../runtime/eudi-issuance.md)

### SL-26: EDI issuer through an FSC Outway (OIN): PuB-EAA route {#sl-26}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the issuer fetches source data through an FSC
  Outway under its own OIN. EUDI and DvTP arrive at the source in the
  same way. The access basis stays different per route.
- **Produced**: [REQ-46](../requirements/sources-identity.md#req-46)
  (REQ-47 removed).
- **Explained in**: [EUDI issuance](../runtime/eudi-issuance.md)

### SL-27: Legitimation of the authorization context (signed envelope) {#sl-27}

- **Status**: merged
- **Demo work**: none of its own.
- **What it showed**: the question was how the claims of a request
  (subject, consumer, and scopes) stay legitimate and bound to each other.
  The question merged into the work on the consent binding
  ([F-44](findings-closed.md#f-44)). [SL-47](#sl-47) answered it with a signed,
  actor-bound consent proof.
- **Produced**: see [SL-47](#sl-47).
- **Explained in**: [ADR-0032](../decisions/0032-consent-proof.md)

### SL-28: Authentic Source Interface (QTSP verification) {#sl-28}

- **Status**: done
- **Demo work**: epic [ICTU/GBO-demo#336](https://github.com/ICTU/GBO-demo/issues/336),
  closed on October 27, 2026. The numbered list after this entry gives
  the parts of the epic.
- **What it showed**: an ASIP mock to ETSI TS 119 478 clause 6.1, with its
  own authorization server, a reference QTSP, and a conformance matrix in
  CI. The QTSP is not an FSC participant. The generic chain (FSC, PDP,
  source gateway, and source) starts behind the ASIP ([F-87](findings.md#f-87)).
  The citizen logs in with a DigiD mock or the NL Wallet.
- **Explained in**: [QTSP verification (ASI route)](../runtime/asi-verification.md),
  [ADR-0037](../decisions/0037-asi-oauth-front-door.md),
  [ADR-0038](../decisions/0038-asi-data-service-per-source.md),
  [ADR-0039](../decisions/0039-asi-source-described-attributes.md),
  [Feedback on ETSI TS 119 478](standards-feedback.md)

Epic #336 has 14 parts:

1. **Verify and retrieve with a seal**
   ([#498](https://github.com/ICTU/GBO-demo/issues/498),
   [PR #499](https://github.com/ICTU/GBO-demo/pull/499)). The ASIP
   verifies and retrieves against an in-memory source. It gives the four
   verification results, the published contract, and a seal on each
   result. Produced: [REQ-83](../requirements/asi.md#req-83),
   [REQ-84](../requirements/asi.md#req-84),
   [REQ-85](../requirements/asi.md#req-85), [F-80](findings.md#f-80),
   and [Q-32](open-questions.md#q-32).
2. **Authorization server**
   ([#503](https://github.com/ICTU/GBO-demo/issues/503),
   [PR #504](https://github.com/ICTU/GBO-demo/pull/504),
   [PR #522](https://github.com/ICTU/GBO-demo/pull/522), and refactor
   [PR #505](https://github.com/ICTU/GBO-demo/pull/505)). The
   authorization server implements clause 6.1.3 with PKCE,
   `private_key_jwt`, DPoP, and JWT tokens. It also has dynamic client
   registration with a sealed software statement, a stub register, and a
   periodic re-check. Produced: [REQ-86](../requirements/asi.md#req-86) to
   [REQ-89](../requirements/asi.md#req-89), [F-84](findings.md#f-84),
   [F-85](findings.md#f-85), [F-86](findings.md#f-86),
   [Q-33](open-questions.md#q-33), [Q-34](open-questions.md#q-34), and
   [Q-35](open-questions.md#q-35).
3. **Citizen approves or refuses**
   ([#523](https://github.com/ICTU/GBO-demo/issues/523),
   [PR #524](https://github.com/ICTU/GBO-demo/pull/524)). The transaction
   is one-time, short-lived, and bound to the browser. The token carries
   PID attributes. Produced: [REQ-90](../requirements/asi.md#req-90),
   [REQ-91](../requirements/asi.md#req-91),
   [F-88](findings.md#f-88), and [Q-36](open-questions.md#q-36).
4. **Chain behind the ASIP**
   ([#525](https://github.com/ICTU/GBO-demo/issues/525),
   [PR #526](https://github.com/ICTU/GBO-demo/pull/526),
   [PR #527](https://github.com/ICTU/GBO-demo/pull/527),
   [PR #529](https://github.com/ICTU/GBO-demo/pull/529),
   [PR #530](https://github.com/ICTU/GBO-demo/pull/530),
   [PR #532](https://github.com/ICTU/GBO-demo/pull/532)). The ASIP is an
   FSC peer and asks the BRP over FSC under rule ASI0001. Each source has
   one data service and one token, each request causes one source
   request, and every rule names its services. Produced:
   [REQ-92](../requirements/asi.md#req-92) to
   [REQ-95](../requirements/asi.md#req-95),
   [REQ-97](../requirements/authorization.md#req-97),
   [F-87](findings.md#f-87), [F-89](findings.md#f-89),
   [F-90](findings-closed.md#f-90), [Q-37](open-questions.md#q-37), and
   [Q-38](open-questions.md#q-38). REQ-96 merged into REQ-91, and REQ-98
   was removed.
5. **Discovery records**: merged into part 6.
6. **Discovery and conformance matrix**
   ([#533](https://github.com/ICTU/GBO-demo/issues/533),
   [PR #534](https://github.com/ICTU/GBO-demo/pull/534),
   [PR #535](https://github.com/ICTU/GBO-demo/pull/535),
   [PR #536](https://github.com/ICTU/GBO-demo/pull/536),
   [PR #537](https://github.com/ICTU/GBO-demo/pull/537),
   [PR #538](https://github.com/ICTU/GBO-demo/pull/538),
   [PR #539](https://github.com/ICTU/GBO-demo/pull/539),
   [PR #540](https://github.com/ICTU/GBO-demo/pull/540),
   [PR #541](https://github.com/ICTU/GBO-demo/pull/541),
   [PR #542](https://github.com/ICTU/GBO-demo/pull/542)). The part added
   a record per data service for the Discover Interface, and a reference
   QTSP. It also added a conformance matrix per ETSI requirement with a
   check in CI, and a 404 for a retrieve without a value. Produced:
   [REQ-99](../requirements/asi.md#req-99) to
   [REQ-101](../requirements/asi.md#req-101), [F-91](findings.md#f-91),
   [F-92](findings.md#f-92), [Q-39](open-questions.md#q-39), and
   [Q-29](open-questions.md#q-29).
7. **NL Wallet identification**
   ([#546](https://github.com/ICTU/GBO-demo/issues/546),
   [PR #550](https://github.com/ICTU/GBO-demo/pull/550),
   [PR #551](https://github.com/ICTU/GBO-demo/pull/551),
   [PR #552](https://github.com/ICTU/GBO-demo/pull/552)). The ASI route
   uses OpenID4VP with the verifier of nl-wallet. A run with the real NL
   Wallet is recorded. Produced:
   [REQ-102](../requirements/asi.md#req-102),
   [F-93](findings.md#f-93), [F-94](findings.md#f-94), and
   [Q-40](open-questions.md#q-40).
8. **Documentation and security notes**
   ([PR #574](https://github.com/ICTU/GBO-demo/pull/574)). The
   documentation tells what is real, stub, interpretation, or shortcut.
   It gives a choice per point of RFC 9700 and FAPI 2.0. Produced:
   [F-96](findings.md#f-96), [Q-41](open-questions.md#q-41),
   [F-84](findings.md#f-84) (extended), and the
   [ETSI feedback list](standards-feedback.md).
9. **Protect the BSN in the token**: not done.
   [#595](https://github.com/ICTU/GBO-demo/issues/595) tracks the
   follow-up.
10. **DigiD mock and one request screen**
    ([#544](https://github.com/ICTU/GBO-demo/issues/544),
    [PR #545](https://github.com/ICTU/GBO-demo/pull/545)). The legal name
    of the QTSP comes from the register. The consent is fixed only after
    a successful identification. The token carries the means
    (`acr`/`amr`). Produced:
    [REQ-86](../requirements/asi.md#req-86),
    [REQ-90](../requirements/asi.md#req-90),
    [REQ-91](../requirements/asi.md#req-91) (validated),
    [F-88](findings.md#f-88), and [Q-36](open-questions.md#q-36).
11. **House style and consent screen**
    ([#547](https://github.com/ICTU/GBO-demo/issues/547),
    [PR #559](https://github.com/ICTU/GBO-demo/pull/559), and optional
    binding in [#571](https://github.com/ICTU/GBO-demo/issues/571),
    [PR #572](https://github.com/ICTU/GBO-demo/pull/572)). The consent
    screen uses plain language. RFC 9396 `authorization_details` binds
    the token to the attributes. Without a configuration that requires
    it, this binding is optional. Produced:
    [REQ-91](../requirements/asi.md#req-91),
    [REQ-103](../requirements/asi.md#req-103),
    [F-95](findings.md#f-95), and [Q-33](open-questions.md#q-33).
12. **Same-device login with the NL Wallet**
    ([#548](https://github.com/ICTU/GBO-demo/issues/548),
    [PR #573](https://github.com/ICTU/GBO-demo/pull/573)). The ASI route
    accepts the return only in the browser of the transaction. Produced:
    [REQ-102](../requirements/asi.md#req-102) and
    [F-93](findings.md#f-93). [#596](https://github.com/ICTU/GBO-demo/issues/596)
    tracks the real run on one phone.
13. **Wallet issuance by the reference QTSP**
    ([#549](https://github.com/ICTU/GBO-demo/issues/549),
    [PR #570](https://github.com/ICTU/GBO-demo/pull/570), and tools
    [PR #566](https://github.com/ICTU/GBO-demo/pull/566),
    [PR #567](https://github.com/ICTU/GBO-demo/pull/567)). After a
    successful result, the reference QTSP issues a marked test
    attestation. Produced: [F-93](findings.md#f-93). REQ-105 was
    removed.
14. **Citizen logs in at the reference QTSP**
    ([#560](https://github.com/ICTU/GBO-demo/issues/560),
    [PR #562](https://github.com/ICTU/GBO-demo/pull/562),
    [PR #563](https://github.com/ICTU/GBO-demo/pull/563),
    [PR #564](https://github.com/ICTU/GBO-demo/pull/564)). Produced:
    [F-93](findings.md#f-93) and [Q-40](open-questions.md#q-40). REQ-104
    was removed.

The close of the epic ([PR #590](https://github.com/ICTU/GBO-demo/pull/590),
[PR #591](https://github.com/ICTU/GBO-demo/pull/591),
[PR #593](https://github.com/ICTU/GBO-demo/pull/593)) made the consent
page name the QTSP that gets consent
([REQ-91](../requirements/asi.md#req-91)). On October 28, 2026, the GBO
profile on ETSI TS 119 478 followed
([ASI profile](../requirements/asi.md#asi-profile)). The profile produced
[REQ-112](../requirements/asi.md#req-112) to
[REQ-115](../requirements/asi.md#req-115) and
[Q-64](open-questions.md#q-64) to [Q-67](open-questions.md#q-67).

Epic #336 has four follow-ups:

- [#592](https://github.com/ICTU/GBO-demo/issues/592): the source
  describes its attributes in its source metadata. Steps 1 to 5 are in
  v0.9.0 ([PR #623](https://github.com/ICTU/GBO-demo/pull/623),
  [PR #624](https://github.com/ICTU/GBO-demo/pull/624), and earlier). In
  demo v0.9.0, every ASI data service names an authentic source
  ([Q-38](open-questions.md#q-38),
  [ADR-0039](../decisions/0039-asi-source-described-attributes.md)).
- [#594](https://github.com/ICTU/GBO-demo/issues/594): the ASI route in
  the simulation environment, and an external QTSP.
- [#595](https://github.com/ICTU/GBO-demo/issues/595): protect the BSN in
  the token ([F-86](findings.md#f-86)).
- [#596](https://github.com/ICTU/GBO-demo/issues/596): the real run of
  same-device login.

### SL-29: BSN out of the EDI decision logs {#sl-29}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: a masking rule kept the BSN out of the decision log.
  [SL-44](#sl-44) showed that the masking rule did not work in the
  OpenFTV PDP ([F-54](findings.md#f-54)). Since
  [PR #370](https://github.com/ICTU/GBO-demo/pull/370), the EUDI BSN is
  in both decision logs. It stays there until a decision on
  [#368](https://github.com/ICTU/GBO-demo/issues/368).
- **Produced**: input for [REQ-60](../requirements/logging-audit.md#req-60)
  (not met in demo v0.9.0) and [F-54](findings.md#f-54).
- **Explained in**: [Logging](../concepts/logging.md),
  [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md)

### SL-30: Dev portal EUDI flow tracing {#sl-30}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the developer portal shows the EUDI issuance chain
  next to the two DvTP chains, with trace links and history.
- **Produced**: input for [Q-08](open-questions.md#q-08) (wallet side).
- **Explained in**: [Building blocks](../building-blocks/components.md)

### SL-31: FSC Inway payload is pure GraphQL and a token, with no envelope {#sl-31}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the Inway passes the body unchanged and writes
  trusted context only from token claims. A header prefix separates
  trusted context from untrusted context ([F-34](findings-closed.md#f-34)).
- **Produced**: [F-34](findings-closed.md#f-34) and
  [REQ-18](../requirements/authorization.md#req-18) (REQ-50 merged into
  it, and REQ-49 removed).
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-32: Adapter parameters from a use-case catalog instead of code {#sl-32}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the EUDI adapter took scope, tax year, and
  attestation type from a catalog instead of from code. [SL-46](#sl-46)
  replaced the catalog with metadata that the source publishes.
- **Produced**: [Q-19](answered-questions.md#q-19) (route b) and
  [F-23](findings-closed.md#f-23).
- **Explained in**: [Source onboarding](../concepts/source-onboarding.md)

### SL-33: EUD0001 explicit scope and actor authorization {#sl-33}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: every policy path checks actor and scope itself.
  The DvTP rule checks that the consent covers the scope. The EUDI rule
  declares which actors and scopes it allows.
- **Produced**: [REQ-48](../requirements/authorization.md#req-48), and
  model B for both paths ([Q-14](open-questions.md#q-14)).
- **Explained in**: [Authorization](../concepts/authorization.md)

### SL-34: FSC exploration {#sl-34}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: an analysis of OpenFSC v2.4.0. The Inway has an
  AuthZEN plugin, so a separate PEP service duplicates its role. FSC has
  no sector grant. Data transformation after the decision belongs in the
  source gateway instead of the PDP.
- **Produced**:
    - findings [F-35](findings-closed.md#f-35), [F-36](findings-closed.md#f-36), and
      [F-37](findings-closed.md#f-37)
    - REQ-52, removed and absorbed by
      [ADR-0002](../decisions/0002-opa-rego-authzen.md)
    - progress on [Q-06](answered-questions.md#q-06) and
      [Q-07](answered-questions.md#q-07)
- **Explained in**: [Deployment](../deployment.md),
  [ADR-0003](../decisions/0003-fsc-connectivity.md)

### SL-34a: Root CA and self-hosted certificate portal (offline CA) {#sl-34a}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the demo runs its own root CA with a certificate
  portal, so FSC peers get certificates without an external CA.
- **Produced**: no requirement. The result is input for
  [Q-07](answered-questions.md#q-07).
- **Explained in**: [Organization identity and trust](../concepts/identity-trust.md),
  [Deployment](../deployment.md)

### SL-34b: Tracer bullet: one organization running before broad roll-out {#sl-34b}

- **Status**: merged
- **Demo work**: covered by [SL-34a](#sl-34a) and [SL-34c](#sl-34c).
- **What it showed**: the plan was to run one FSC organization before the
  roll-out. [SL-34a](#sl-34a) and [SL-34c](#sl-34c) covered the purpose.
  Step 2 of the plan was removed.
- **Produced**: none.
- **Explained in**: [Deployment](../deployment.md)

### SL-34c: Self-hosted directory peer and directory UI (offline registry) {#sl-34c}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the demo runs its own FSC directory peer with a
  user interface, so it does not depend on an external directory.
- **Produced**: no requirement.
- **Explained in**: [Deployment](../deployment.md)

### SL-35: Bootstrap of the FSC organization EDI issuer (consumer) {#sl-35}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the EUDI issuer runs as an FSC consumer
  organization of its own, with its own peer and certificate.
- **Produced**: no requirement.
- **Explained in**: [Deployment](../deployment.md)

### SL-36: Bootstrap of the FSC organization Belastingdienst mock (provider) {#sl-36}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the Belastingdienst mock runs as an FSC provider
  organization of its own, with its own Manager and Inway.
- **Produced**: no requirement.
- **Explained in**: [Deployment](../deployment.md)

### SL-37: FSC service bri and contract negotiation between organizations {#sl-37}

- **Status**: done
- **Demo work**: before the public repository. Seed automation came
  later.
- **What it showed**: the source publishes the service `bri`, and the
  organizations negotiate a contract for it. A contract has one service
  connection grant, for one Outway and one service. The contract cannot
  express a sector ([F-36](findings-closed.md#f-36)).
- **Produced**: [F-36](findings-closed.md#f-36) (detail).
- **Explained in**: [Contract admission and source activation](../runtime/admission.md)

### SL-38: FSC txlog observability and trace ID equal to Fsc-Transaction-Id {#sl-38}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: FSC v2.4.0 does not propagate trace context, and its
  plugins drop the request context. The demo made the trace ID equal to
  the FSC transaction ID and read the FSC transaction logs. [SL-50](#sl-50)
  reversed the key: W3C Trace Context is the key, and the demo records
  the transaction ID next to it ([F-67](findings-closed.md#f-67)).
- **Produced**: [F-39](findings-closed.md#f-39), [F-40](findings-closed.md#f-40),
  [F-41](findings-closed.md#f-41), [F-42](findings-closed.md#f-42), and
  [REQ-55](../requirements/logging-audit.md#req-55) (REQ-54 merged into
  it).
- **Explained in**: [Logging](../concepts/logging.md),
  [ADR-0035](../decisions/0035-w3c-trace-context.md)

### SL-39: Eudi-adapter to real FSC Outway {#sl-39}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the EUDI adapter calls the source through a real FSC
  Outway, with mTLS and contract-based authorization up to the Inway. The
  scope header is an untrusted catalog index, and the policy checks it
  independently ([F-14](findings-closed.md#f-14)).
- **Produced**: [F-23](findings-closed.md#f-23) (widened),
  [F-14](findings-closed.md#f-14) (resolved).
- **Explained in**: [EUDI issuance](../runtime/eudi-issuance.md)

### SL-40: Pdp-service as AuthZEN endpoint behind FSC Inway (EUDI) {#sl-40}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the AuthZEN plugin of the FSC Inway calls the PDP
  directly. No separate PEP is necessary in the FSC chain.
- **Produced**: [F-35](findings-closed.md#f-35) (shown live),
  [REQ-42](../requirements/authorization.md#req-42).
- **Explained in**: [ADR-0002](../decisions/0002-opa-rego-authzen.md)

### SL-41: Documentation and developer portal update: real FSC nodes {#sl-41}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: the documentation and the developer portal show the
  real FSC nodes instead of the `fsc-mock`.
- **Produced**: no requirement. [F-31](findings-closed.md#f-31) stays valid.
- **Explained in**: [Building blocks](../building-blocks/components.md)

### SL-42: Follow-up: fully phase out fsc-mock (option B, DvTP) {#sl-42}

- **Status**: done
- **Demo work**: before the public repository.
- **What it showed**: DvTP runs over real FSC too, with a second consumer
  organization. The demo removed the `fsc-mock` and the PEP service. The
  PDP is the only policy endpoint for DvTP and EUDI. The source source gateway
  does the conversion after the decision ([SL-22](#sl-22),
  [SL-23](#sl-23)).
- **Produced**:
    - findings [F-44](findings-closed.md#f-44), [F-45](findings-closed.md#f-45), and
      [F-46](findings-closed.md#f-46)
    - updates of [F-30](findings-closed.md#f-30), [F-32](findings-closed.md#f-32),
      [F-35](findings-closed.md#f-35), and [F-37](findings-closed.md#f-37)
- **Explained in**: [Consumer queries under consent](../runtime/dvtp-query.md),
  [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)

### SL-43: Death certificate: BRP source and second EUDI attestation (subject differs from discloser) {#sl-43}

- **Status**: done
- **Demo work**: [PR #125](https://github.com/ICTU/GBO-demo/pull/125)
- **What it showed**: a second source (BRP) and a second attestation. A
  surviving partner discloses his PID and gets the death certificate of
  the partner. The subject of the attestation is not the person who
  discloses. Each source holder (bronhouder) needs its own certificate set for
  issuance.
- **Produced**:
    - findings [F-47](findings.md#f-47), [F-49](findings-closed.md#f-49), and
      [F-50](findings-closed.md#f-50)
    - requirements [REQ-57](../requirements/eudi-issuance.md#req-57) and
      [REQ-58](../requirements/eudi-issuance.md#req-58)
    - open question [Q-20](answered-questions.md#q-20)
    - matrix row EUDI-11
- **Explained in**: [EUDI issuance](../runtime/eudi-issuance.md)

### SL-44: OpenFTV Manager: policy management and distribution through bundles (PAP) {#sl-44}

- **Status**: done
- **Demo work**: [PR #208](https://github.com/ICTU/GBO-demo/pull/208)
- **What it showed**: the PAP runs at the source side. Git stays the
  source of truth, and policy goes to the PDP as an identified, versioned
  bundle. The management API has its own policy set. If the store is
  empty, the management API denies. Push distribution, delete, and
  masking of decision logs do not work in this configuration.
- **Produced**:
    - findings [F-51](findings.md#f-51), [F-52](findings.md#f-52),
      [F-53](findings-closed.md#f-53), and [F-54](findings.md#f-54)
    - requirements [REQ-59](../requirements/logging-audit.md#req-59) and
      [REQ-60](../requirements/logging-audit.md#req-60)
    - guidelines [RL-01](../requirements/authorization.md#rl-01) to
      [RL-05](../requirements/authorization.md#rl-05)
    - open question [Q-21](answered-questions.md#q-21)
    - most of [F-09](findings-closed.md#f-09) closed
- **Explained in**: [Policy distribution](../runtime/policy-distribution.md),
  [Policy lifecycle](../concepts/policy-lifecycle.md),
  [ADR-0021](../decisions/0021-central-pap-signed-bundles.md)

### SL-45: Admission as a register and contract decision by the PDP {#sl-45}

- **Status**: done
- **Demo work**: [PR #228](https://github.com/ICTU/GBO-demo/pull/228),
  [PR #239](https://github.com/ICTU/GBO-demo/pull/239),
  [PR #241](https://github.com/ICTU/GBO-demo/pull/241)
- **What it showed**: admission is a registration instead of a policy
  rule. The PDP decides each contract proposal in a policy tree of its
  own, with machine-readable reason codes. An automatic "no" leaves the
  proposal pending, so it is recoverable. Admission is per source holder.
  The demo has no admission per service.
- **Produced**:
    - findings [F-55](findings-closed.md#f-55) and [F-56](findings-closed.md#f-56)
    - requirements [REQ-61](../requirements/admission.md#req-61),
      [REQ-62](../requirements/admission.md#req-62), and
      [REQ-63](../requirements/admission.md#req-63)
    - open question [Q-22](answered-questions.md#q-22)
- **Explained in**: [Contract admission and source activation](../runtime/admission.md),
  [ADR-0015](../decisions/0015-contract-acceptance-by-policy.md)

### SL-46: Generic source metadata: source publishes, GBO validates and activates {#sl-46}

- **Status**: done
- **Demo work**: [PR #219](https://github.com/ICTU/GBO-demo/pull/219),
  [PR #224](https://github.com/ICTU/GBO-demo/pull/224),
  [PR #237](https://github.com/ICTU/GBO-demo/pull/237),
  [PR #247](https://github.com/ICTU/GBO-demo/pull/247),
  [PR #276](https://github.com/ICTU/GBO-demo/pull/276)
- **What it showed**: each source publishes its service description on
  `/.well-known/gbo`: query, parameters, mapping, attestation schema, and
  offers. GBO validates the description against a profile and activates
  it as an explicit step. A valid contract does not activate the
  description. If a description is bad or old, it fails closed per
  source, and it can be rolled back.
- **Produced**:
    - findings [F-57](findings.md#f-57), [F-58](findings-closed.md#f-58), and
      [F-59](findings-closed.md#f-59)
    - requirements [REQ-64](../requirements/sources-identity.md#req-64),
      [REQ-65](../requirements/sources-identity.md#req-65), and
      [REQ-66](../requirements/sources-identity.md#req-66)
    - [Q-19](answered-questions.md#q-19) answered for EUDI
    - a direction for [F-21](findings-closed.md#f-21), [F-22](findings-closed.md#f-22),
      and [F-23](findings-closed.md#f-23)
    - [Q-17](open-questions.md#q-17) (sub-question 6)
    - in demo v0.9.0, REQ-64 built for EUDI and the ASIP
      ([#592](https://github.com/ICTU/GBO-demo/issues/592)) and not for
      DvTP
- **Explained in**: [Source onboarding](../concepts/source-onboarding.md),
  [ADR-0016](../decisions/0016-source-owned-metadata.md)

### SL-47: Signed, actor-bound consent proof {#sl-47}

- **Status**: done
- **Demo work**: [PR #238](https://github.com/ICTU/GBO-demo/pull/238)
- **What it showed**: the consent register issues a signed consent proof
  (ES256, with a JWKS). The policy verifies the signature and binds the
  consumer in the proof to the verified caller. The status check stays
  online and fails closed. The validity period is in the signed proof, so
  the consumer cannot change it.
- **Produced**: [F-61](findings-closed.md#f-61),
  [REQ-68](../requirements/consent.md#req-68), and
  [REQ-69](../requirements/pseudonymization.md#req-69). The increment
  closed [F-24](findings-closed.md#f-24) and [F-44](findings-closed.md#f-44), and
  sharpened [Q-05](answered-questions.md#q-05). REQ-13, REQ-25, and REQ-27
  were revised and removed later.
- **Explained in**: [Consent](../concepts/consent.md),
  [ADR-0032](../decisions/0032-consent-proof.md)

### SL-48: Flow dispatch cleaned up: no default regime, no flow header {#sl-48}

- **Status**: done
- **Demo work**: [PR #236](https://github.com/ICTU/GBO-demo/pull/236)
- **What it showed**: the demo removed the default regime, and the
  regime header that a consumer was able to send. If a request had no
  signed flow property, it matched no rule and got a deny.
  [PR #363](https://github.com/ICTU/GBO-demo/pull/363) removed the flow
  property too ([REQ-74](../requirements/authorization.md#req-74)).
- **Produced**: the premise of [F-49](findings-closed.md#f-49) lapsed. REQ-56
  was tightened, then removed and replaced by
  [REQ-74](../requirements/authorization.md#req-74).
- **Explained in**: [ADR-0031](../decisions/0031-regime-from-evidence.md)

### SL-49: Identity separation: FSC Peer ID separate from source OIN {#sl-49}

- **Status**: done
- **Demo work**: [PR #242](https://github.com/ICTU/GBO-demo/pull/242),
  [PR #244](https://github.com/ICTU/GBO-demo/pull/244),
  [PR #247](https://github.com/ICTU/GBO-demo/pull/247),
  [PR #277](https://github.com/ICTU/GBO-demo/pull/277)
- **What it showed**: the FSC Peer ID (transport identity) and the OIN of
  the source (legal identity) are recorded apart. The OIN and the name of
  the organization come from the verified issuer certificate. CA private
  keys stay out of the application runtime.
- **Produced**: [F-60](findings-closed.md#f-60) and
  [REQ-67](../requirements/sources-identity.md#req-67). The increment
  sharpened [Q-06](answered-questions.md#q-06) and
  [Q-07](answered-questions.md#q-07).
- **Explained in**: [Organization identity and trust](../concepts/identity-trust.md)

### SL-50: LDV and ADL exploration: three logging standards, one trace ID {#sl-50}

- **Status**: done
- **Demo work**: build in [#302](https://github.com/ICTU/GBO-demo/issues/302),
  and review and correction in
  [PR #366](https://github.com/ICTU/GBO-demo/pull/366).
- **What it showed**: three related logging standards apply. The decision
  log already implements the Authorization Decision Log (ADL). The gap is
  at the processing: each GBO component that processes personal data
  writes a Logboek Dataverwerkingen (LDV) log line at its controller
  (Verantwoordelijke). The trace ID from `traceparent` links the logs,
  and each controller logs its own pseudonym.
- **Produced**:
    - findings [F-63](findings-closed.md#f-63), [F-64](findings-closed.md#f-64),
      [F-65](findings-closed.md#f-65), [F-67](findings-closed.md#f-67),
      [F-68](findings.md#f-68), and [F-69](findings-closed.md#f-69)
    - requirements [REQ-71](../requirements/logging-audit.md#req-71),
      [REQ-72](../requirements/logging-audit.md#req-72),
      [REQ-55](../requirements/logging-audit.md#req-55) (revised), and
      [AV-01](../requirements/admission.md#av-01) (was REQ-73)
    - open questions [Q-08](open-questions.md#q-08),
      [Q-23](answered-questions.md#q-23), [Q-24](answered-questions.md#q-24), and
      [Q-25](open-questions.md#q-25)
    - [F-53](findings-closed.md#f-53) answered
- **Explained in**: [Logging](../concepts/logging.md),
  [ADR-0026](../decisions/0026-ldv-integration.md),
  [ADR-0035](../decisions/0035-w3c-trace-context.md),
  [ADR-0036](../decisions/0036-adl-decision-record.md)

### SL-51: Encrypted identity per source in the consent proof, replaced after the decision {#sl-51}

- **Status**: done
- **Demo work**:
    - [ICTU/GBO-demo#468](https://github.com/ICTU/GBO-demo/issues/468)
      and [PR #469](https://github.com/ICTU/GBO-demo/pull/469), the first
      part of [#364](https://github.com/ICTU/GBO-demo/issues/364), on the
      BSNk mock from [PR #466](https://github.com/ICTU/GBO-demo/pull/466).
    - the follow-up in [#473](https://github.com/ICTU/GBO-demo/issues/473):
      [PR #475](https://github.com/ICTU/GBO-demo/pull/475) removed
      `subject_id_type`, and
      [PR #476](https://github.com/ICTU/GBO-demo/pull/476) added two
      placeholders, one per form.
      [PR #477](https://github.com/ICTU/GBO-demo/pull/477) added a
      pseudonym for each source, an identity for a source on the BSN
      authorization list, and more than four parties.
- **What it showed**: the design works with the BSNk interface. At the
  consent, the portal backend activates and transforms. The proof carries
  an encrypted value per source, and the consumer sends a placeholder.
  The PDP decides on that placeholder. Only after an allow, the source
  decrypts its own value, without a call to BSNk.
- **Produced**:
    - findings [F-76](findings.md#f-76), [F-77](findings.md#f-77),
      [F-78](findings.md#f-78), and [F-79](findings.md#f-79)
    - requirements [REQ-79](../requirements/pseudonymization.md#req-79),
      [REQ-80](../requirements/pseudonymization.md#req-80),
      [REQ-81](../requirements/pseudonymization.md#req-81),
      [REQ-82](../requirements/pseudonymization.md#req-82), and
      [REQ-21](../requirements/pseudonymization.md#req-21) (revised)
    - open questions [Q-27](open-questions.md#q-27),
      [Q-26](open-questions.md#q-26) (sub-question 8), and
      [Q-01](open-questions.md#q-01) (extended)
    - [BSNK-05](../requirements/pseudonymization.md#bsnk-05) and
      [BSNK-06](../requirements/pseudonymization.md#bsnk-06), tried on
      the mock
- **Not built**:
    - a pseudonym for the consumer
      ([#478](https://github.com/ICTU/GBO-demo/issues/478))
    - the subject variable in one place
      ([#479](https://github.com/ICTU/GBO-demo/issues/479))
    - an API that answers on a pseudonym
      ([#474](https://github.com/ICTU/GBO-demo/issues/474))
    - onboarding of keys ([#467](https://github.com/ICTU/GBO-demo/issues/467))
- **Explained in**: [Pseudonymization](../concepts/pseudonymization.md),
  [Consumer queries under consent](../runtime/dvtp-query.md),
  [ADR-0032](../decisions/0032-consent-proof.md),
  [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)

## Demo work outside increments {#outside-increments}

From September 14 to 16, 2026, the demo work ran through demo issues
instead of an increment. This work produced the following IDs:

- [PR #284](https://github.com/ICTU/GBO-demo/pull/284) and
  [PR #363](https://github.com/ICTU/GBO-demo/pull/363): the regime
  follows from the evidence of the request instead of a grant property.
  Produced: [F-70](findings.md#f-70) and
  [REQ-74](../requirements/authorization.md#req-74).
  [F-62](findings-closed.md#f-62) is resolved, and [SL-24](#sl-24) is dropped.
  REQ-56 was partly replaced and removed later.
- [PR #370](https://github.com/ICTU/GBO-demo/pull/370) and
  [PR #371](https://github.com/ICTU/GBO-demo/pull/371): the request mapper
  does only GraphQL mapping. The policy verifies the consent proof and
  asks for the status. Produced:
  [REQ-68](../requirements/consent.md#req-68), [F-61](findings-closed.md#f-61),
  [Q-05](answered-questions.md#q-05), [Q-23](answered-questions.md#q-23), and
  [Q-25](open-questions.md#q-25). The BSN is in both decision logs on
  purpose, so [REQ-60](../requirements/logging-audit.md#req-60) is not
  met ([F-54](findings.md#f-54)).
- [PR #372](https://github.com/ICTU/GBO-demo/pull/372): `make
  policy-check` is a local safety net. Produced:
  [RL-05](../requirements/authorization.md#rl-05) and
  [F-52](findings.md#f-52).
- [PR #373](https://github.com/ICTU/GBO-demo/pull/373): the ADL is the
  audit source. Produced: [F-72](findings.md#f-72) and
  [REQ-71](../requirements/logging-audit.md#req-71). The rest of
  [F-53](findings-closed.md#f-53) and [F-63](findings-closed.md#f-63) is done. A check
  against a running stack showed the gap of
  [REQ-59](../requirements/logging-audit.md#req-59): the records carry
  no policy version.
- [PR #337](https://github.com/ICTU/GBO-demo/pull/337): OpenFTV v0.1.0
  makes the ADL mandatory
  ([REQ-71](../requirements/logging-audit.md#req-71)). A silent bundle
  403 led to [F-52](findings.md#f-52) and
  [RL-05](../requirements/authorization.md#rl-05).
- [PR #318](https://github.com/ICTU/GBO-demo/pull/318): the demo has a
  `file` transport for source metadata. Produced:
  [F-71](findings.md#f-71), an exception in
  [REQ-64](../requirements/sources-identity.md#req-64), and
  [Q-06](answered-questions.md#q-06).
- [PR #321](https://github.com/ICTU/GBO-demo/pull/321): the description
  of the issuer comes from the certificate
  ([REQ-67](../requirements/sources-identity.md#req-67)).

The same round recorded three observations in issues:

- [#369](https://github.com/ICTU/GBO-demo/issues/369): the ADL record
  behind the Inway has no trace and no transaction ID. Related:
  [F-41](findings-closed.md#f-41),
  [REQ-55](../requirements/logging-audit.md#req-55), and
  [REQ-71](../requirements/logging-audit.md#req-71).
- [#225](https://github.com/ICTU/GBO-demo/issues/225): the choice
  between one shared certificate set and a set per source. Related:
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [Q-07](answered-questions.md#q-07), and [Q-17](open-questions.md#q-17).
- [#133](https://github.com/ICTU/GBO-demo/issues/133): the callback from
  the issuance server to the adapter has no authentication. Related:
  [F-70](findings.md#f-70) and [Q-18](open-questions.md#q-18).

Later, [PR #464](https://github.com/ICTU/GBO-demo/pull/464)
([#379](https://github.com/ICTU/GBO-demo/issues/379)) added more demo
work outside increments. An integrator calls under FSC delegation, and
the consent binds the represented party. Produced:
[REQ-106](../requirements/consent.md#req-106),
[F-73](findings-closed.md#f-73), [Q-46](open-questions.md#q-46), and
[ADR-0034](../decisions/0034-integrator-delegation.md).

## Traceability

- Requirements: each increment lists the requirements it produced.
- Findings: each increment lists its findings. For all findings, see
  [Findings](findings.md).
- Open questions: each increment lists its open questions. For all
  questions, see [Open questions](open-questions.md).
- Design coverage: [Design to demo matrix](matrix.md).
