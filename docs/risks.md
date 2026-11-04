# Risks and technical debt

The design and gbo-demo
[v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0) have known risks
and technical debt. The risk list carries forward the gap analysis of the
archived reference architecture v0.6.2, with updates from the demo
findings. Every entry names its follow-up: a decision, a hardening action,
a demo issue, or an open question. Each entry links the findings (F), open
questions (Q), requirements (REQ), and decisions (ADR) that it rests on.

## Overview

Each risk belongs to one group:

| ID | Risk | Group |
|---|---|---|
| [R1](#r1) | The ASI exists at demo grade only | Routes |
| [R2](#r2) | The SDG-OOTS bridge is design-level only | Routes |
| [R3](#r3) | No Gov-to-Gov regime and no positive evidence for it | Routes |
| [R4](#r4) | The consent proof is a bearer token | Security |
| [R5](#r5) | The EUDI adapter accepts unauthenticated issuance callbacks | Security |
| [R6](#r6) | No rate limiting or quota | Security |
| [R7](#r7) | Data-chain responses are not sealed | Security |
| [R8](#r8) | Contract acceptance sees the parties but not the service | Security |
| [R9](#r9) | Demo-grade shared services | Production readiness |
| [R10](#r10) | The consent register (toestemmingsregister) is a dependency of every DvTP decision | Production readiness |
| [R11](#r11) | The demo runs one PDP for all providers | Production readiness |
| [R12](#r12) | Policy distribution has no integrity chain and no visible fallback | Production readiness |
| [R13](#r13) | The PDP mapper is a patch on OpenFTV | Production readiness |
| [R14](#r14) | New sources need a restart of the issuance server | Production readiness |
| [R15](#r15) | The legal ceiling of the service catalog (dienstencatalogus) has no technical counterpart | Governance |
| [R16](#r16) | Rego instead of ODRL | Governance |
| [R17](#r17) | GraphQL is not a recognized FDS datadienst type | Governance |
| [R18](#r18) | Integrator mandates have no validity and no governance | Governance |
| [R19](#r19) | LDV gaps: citizen view, activity register, ASIP | Governance |
| [R20](#r20) | Onboarding cost for small bronhouders | Governance |
| [R21](#r21) | The absence of a consent proof selects the PID regime | Security |
| [R22](#r22) | BSN in the decision logs of the EUDI and ASI routes | Privacy |
| [R23](#r23) | The ADL record is incomplete behind the FSC Inway | Audit |
| [R24](#r24) | The consent proof freezes at consent | DvTP |
| [R25](#r25) | Source isolation is incomplete | Security |
| [R26](#r26) | The QTSP can read the BSN in the ASI token | Privacy |
| [R27](#r27) | No national register for QTSP admission | ASI |
| [R28](#r28) | No link between the QTSP login and the source login | ASI |
| [R29](#r29) | The NL PID has no place of birth | ASI |
| [R30](#r30) | Fuzzy matching without returning a value | ASI |
| [R31](#r31) | The backend revokes a revoked consent again | DvTP |
| [R32](#r32) | Only the network protects the register listener | Security |
| [R33](#r33) | A suspended consumer keeps access | DvTP |
| [R34](#r34) | Any connected peer can read any consent status | Security |
| [R35](#r35) | The consumer sets the consent validity | DvTP |
| [R36](#r36) | Attestations are valid 365 days without a change feed | EUDI |
| [R37](#r37) | BSNk recognition of the consent facility (toestemmingsvoorziening) is not settled | DvTP |

## Routes {#trajectories}

### R1: The ASI exists at demo grade only {#r1}

- **Risk**: The Authentic Source Interface is built
  ([ADR-0037](decisions/0037-asi-oauth-front-door.md)), but only as a
  local demo stack. From January 1, 2027, the interface of CIR 2026/1735
  Annex IV and the seal obligation apply
  ([F-80](traceability/findings.md#f-80)).
- **Impact**: Production needs these parts, which the demo does not have:
    - a qualified seal certificate and its holder
      ([Q-17](traceability/open-questions.md#q-17),
      [Q-28](traceability/open-questions.md#q-28),
      [Q-32](traceability/open-questions.md#q-32))
    - the national register of relying parties and access certificates
      ([R27](#r27))
    - real identification means: the DigiD route is a mock, and the wallet
      verifier also trusts the development issuer CA
      ([Q-36](traceability/open-questions.md#q-36))
    - a decision on the role of GBO
      ([Q-37](traceability/open-questions.md#q-37)) and on catalog
      registration ([Q-31](traceability/open-questions.md#q-31),
      [Q-67](traceability/open-questions.md#q-67))
    - a simulation deployment
      ([#594](https://github.com/ICTU/GBO-demo/issues/594))
- **Follow-up**: Three items track this risk:
    - the proposed ADRs [0041](decisions/0041-asi-seal-format.md) and
      [0042](decisions/0042-asi-attribute-token-binding.md)
    - the ASI risks [R26](#r26) to [R30](#r30)
    - the standards feedback
      [E1 to E10](traceability/standards-feedback.md), which is not sent.
- **Related**: [F-80](traceability/findings.md#f-80),
  [F-84](traceability/findings.md#f-84),
  [F-87](traceability/findings.md#f-87),
  [REQ-112](requirements/asi.md#req-112),
  [SL-28](traceability/increments.md#sl-28).

### R2: The SDG-OOTS bridge is design-level only {#r2}

- **Risk**: The AS4 bridge for SDG-OOTS has no implementation.
- **Impact**: Until the bridge is built, the EU obligation is not met.
- **Follow-up**: [ADR-0020](decisions/0020-as4-bridge-for-oots.md),
  [ADR-0024](decisions/0024-canonical-semantic-models.md). It is open who
  builds the adapter ([Q-79](traceability/open-questions.md#q-79)).
- **Related**: [SDG-OOTS scenario](runtime/design-level.md#sdg-oots).

### R3: No Gov-to-Gov regime and no positive evidence for it {#r3}

- **Risk**: The PDP knows two regimes: consent and PID. No legal-basis
  regime, rule set, or legal basis (grondslag) data exists. A request without a consent
  proof falls in the PID regime
  ([ADR-0031](decisions/0031-regime-from-evidence.md)).
- **Impact**: The two-path access-basis model of
  [ADR-0004](decisions/0004-federated-authorization.md) is only half
  proven. A Gov-to-Gov regime cannot reuse "absence of a token" as its
  evidence, because the PID regime already uses it ([R21](#r21)).
- **Follow-up**: Define the positive evidence for a legal basis. Then add
  a regime and a rule set.
- **Related**: [REQ-74](requirements/authorization.md#req-74),
  [Gov-to-Gov scenario](runtime/design-level.md#gov-to-gov).

## Security hardening

### R4: The consent proof is a bearer token {#r4}

- **Risk**: The actor binding stops another consumer from using a proof.
  It does not stop replay by the same consumer within the validity
  period.
- **Impact**: A stolen proof gives data access for its remaining life.
- **Follow-up**: Make the validity period shorter. Bind the proof to the
  FSC identity with proof of possession
  ([ADR-0032](decisions/0032-consent-proof.md)).
- **Related**: [REQ-68](requirements/consent.md#req-68),
  [Bearer token](concepts/consent.md#bearer-token).

### R5: The EUDI adapter accepts unauthenticated issuance callbacks {#r5}

- **Risk**: The issuance server verifies the PID disclosure. The gap is
  behind it: the adapter route `POST /attestations/{source}/{type}` has
  no caller authentication
  ([`source_release_runtime.go#L69-L81`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L69-L81),
  plain `ListenAndServe` at
  [`main.go#L700`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L700)).
  The developer portal shows the gap: its playground posts a typed BSN
  straight to the adapter through `/eudi-api/`
  ([`EudiQrPanel.tsx#L36-L51`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/developer-portal/src/components/EudiQrPanel.tsx#L36-L51),
  [`nginx.conf#L36-L42`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/developer-portal/nginx.conf#L36-L42)).
- **Impact**: Any caller that reaches the adapter can post an arbitrary
  BSN. The adapter calls the source over FSC as the designated issuer. As
  a result, the PDP allows the request, and the adapter returns the claims
  without any wallet. Two more gaps add to this risk:
    - nothing binds the BSN in the source query to the verified
      disclosure
    - the PID trust list of the issuance server also holds non-PID
      anchors, including the GBO development issuer CA.
- **Follow-up**: Authenticate the callback (mTLS or a signed request from
  the issuance server), or let the adapter verify the SD-JWT itself. Bind
  the disclosure to the request. Restrict the PID trust list to PID
  issuers ([REQ-45](requirements/eudi-issuance.md#req-45),
  [#133](https://github.com/ICTU/GBO-demo/issues/133)). The QTSP callback
  already uses a secret path and CA-pinned TLS.
- **Related**: [F-70](traceability/findings.md#f-70),
  [Q-18](traceability/open-questions.md#q-18),
  [ADR-0018](decisions/0018-eudi-disclosure-issuance.md),
  [SL-25](traceability/increments.md#sl-25) (dropped),
  [the callback gap](runtime/eudi-issuance.md#the-callback-gap).

### R6: No rate limiting or quota {#r6}

- **Risk**: Authorization concern ⑤ exists only as structural checks:
  parse, depth, size, and coverage. Rate limiting and quota are not built.
- **Impact**: Only the FSC contracts limit enumeration and abuse.
- **Follow-up**: Define limits per grant. Enforce them at the Inway or
  the PDP ([ADR-0004](decisions/0004-federated-authorization.md)).
- **Related**: [REQ-17](requirements/authorization.md#req-17).

### R7: Data-chain responses are not sealed {#r7}

- **Risk**: DvTP and EUDI source responses carry no qualified electronic
  seal. ASI verification results carry a seal: a detached JWS (ES256,
  `x5c`) over the exact body. The ASI certificate is a development
  certificate and is not qualified
  ([REQ-83](requirements/asi.md#req-83)).
- **Impact**: Non-repudiation of a data-chain response rests on the FSC
  transaction log and the ADL. No seal supports it.
- **Follow-up**: Decide whether every source response gets one seal,
  whatever the channel ([Q-75](traceability/open-questions.md#q-75)). The
  ASI seal format waits for [Q-32](traceability/open-questions.md#q-32)
  ([ADR-0041](decisions/0041-asi-seal-format.md)). The BSN in the
  decision logs is a separate risk ([R22](#r22)).
- **Related**: [F-80](traceability/findings.md#f-80),
  [E4](traceability/standards-feedback.md#e4).

### R8: Contract acceptance sees the parties but not the service {#r8}

- **Risk**: The autosign input carries peer IDs and grant types only.
- **Impact**: At contract time, the policy cannot enforce admission per
  service.
- **Follow-up**: An upstream FSC change. Until that change, request-time
  rules compensate
  ([ADR-0015](decisions/0015-contract-acceptance-by-policy.md)).
- **Related**: [F-56](traceability/findings-closed.md#f-56) (closed),
  [REQ-62](requirements/admission.md#req-62).

### R21: The absence of a consent proof selects the PID regime {#r21}

- **Risk**: A request without a consent proof is in the PID regime
  ([`engine.rego#L168-L181`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L168-L181)).
  The only control is the list of designated issuers per EUDI rule. A
  consumer on that list can skip consent: it leaves out the consent
  proof.
- **Impact**: The PID regime rests on an identifier whose origin no one
  in the chain checks. A test keeps the issuer list disjoint from the
  DvTP consumers, but the test knows only the local consumers. For the
  simulation consumer, only an inspection shows that it is disjoint.
- **Follow-up**: Make positive PID evidence at the point where the wallet
  presentation is verified. Bind this evidence to the subject of the
  query ([REQ-45](requirements/eudi-issuance.md#req-45),
  [#133](https://github.com/ICTU/GBO-demo/issues/133),
  [#381](https://github.com/ICTU/GBO-demo/issues/381)). Until then, test
  the disjointness per environment.
- **Related**: [F-70](traceability/findings.md#f-70),
  [REQ-74](requirements/authorization.md#req-74),
  [Q-18](traceability/open-questions.md#q-18),
  [Q-22](traceability/answered-questions.md#q-22),
  [ADR-0031](decisions/0031-regime-from-evidence.md).

### R25: Source isolation is incomplete {#r25}

- **Risk**: The rule "Decrypt only after the allow" depends on one
  condition: only the FSC Inway reaches the source gateway
  ([REQ-81](requirements/pseudonymization.md#req-81)). In Docker Compose,
  the gateways publish no port and are only on `source-gateways` and
  `sources`. However, the source APIs (`graphql-server`,
  `brp-graphql-server`, `lvg-graphql-server`) are also on `backend` and
  `fsc-infra`
  ([`docker-compose.yml#L631-L636`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L631-L636)),
  together with the consumer backend
  ([`#L1080-L1082`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L1080-L1082)).
- **Impact**: A party on those networks can reach a source API without
  the Inway, the PDP, and the gateway. The Helm chart has no
  NetworkPolicy. The decrypted value is not bound to one consent (no
  nonce).
- **Follow-up**: Take the source APIs off the shared networks. Outside
  Compose, add a NetworkPolicy or an equal control. Add the nonce as a
  second safeguard
  ([BSNk preconditions](requirements/pseudonymization.md#spec-extras)).
- **Related**: [F-79](traceability/findings.md#f-79),
  [REQ-21](requirements/pseudonymization.md#req-21),
  [ADR-0033](decisions/0033-gateway-decrypts-after-allow.md),
  [network isolation](concepts/pseudonymization.md#network-isolation-is-the-control).

### R32: Only the network protects the register listener {#r32}

- **Risk**: The register listener for create, list, read, and revoke has
  no caller authentication. The consent portal (toestemmingsportaal) backend is its only
  intended caller ([REQ-39](requirements/consent.md#req-39)). In
  Compose, the register is on `backend`
  ([`docker-compose.yml#L737-L740`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L737-L740)).
- **Impact**: Any party that reaches the register directly can create or
  revoke consents for every citizen.
- **Follow-up**: Decide between authentication of the backend and network
  isolation ([Q-58](traceability/open-questions.md#q-58)). Isolation alone
  works only under one condition: the register and the backend run at one
  participant ([Q-49](traceability/open-questions.md#q-49)).
- **Related**: [REQ-76](requirements/consent.md#req-76) (the status
  listener goes over FSC).

### R34: Any connected peer can read any consent status {#r34}

- **Risk**: The status service over FSC answers every peer that has a
  contract for it. It does not check that the caller is the PDP of a
  source in the consent.
- **Impact**: A connected peer with a `consent_id` learns its status.
- **Follow-up**: Restrict the status answer to the PDPs of the sources in
  the consent ([REQ-76](requirements/consent.md#req-76),
  [#382](https://github.com/ICTU/GBO-demo/issues/382)).
- **Related**: [ADR-0032](decisions/0032-consent-proof.md).

## Privacy and audit

### R22: BSN in the decision logs of the EUDI and ASI routes {#r22}

- **Risk**: In the EUDI and ASI routes, the query names the citizen with
  the plain BSN. The PDP input, the ADL, and the console decision log hold
  it. Nothing masks the BSN, and the mapper stopped pseudonymizing it.
- **Impact**: [REQ-60](requirements/logging-audit.md#req-60) is not met
  for these routes. Masking alone also does not meet the requirement.
- **Follow-up**: Keep identifiers out of the PDP input
  ([ADR-0043](decisions/0043-identifiers-out-of-pdp-input.md), proposed).
  The decision is made in
  [#368](https://github.com/ICTU/GBO-demo/issues/368).
- **Related**: [F-54](traceability/findings.md#f-54),
  [SL-29](traceability/increments.md#sl-29) (reversed by
  [PR #370](https://github.com/ICTU/GBO-demo/pull/370)),
  [the BSN exception](concepts/pseudonymization.md#exception-the-bsn-in-the-eudi-and-asi-routes).

### R23: The ADL record is incomplete behind the FSC Inway {#r23}

- **Risk**: The ADL is the authoritative decision record
  ([ADR-0036](decisions/0036-adl-decision-record.md)). Three parts are
  missing:
    - Behind the FSC Inway, the record has its own random trace and no
      transaction ID. The Inway passes neither to the PDP
      ([#369](https://github.com/ICTU/GBO-demo/issues/369)).
    - The record does not name the policy version
      ([REQ-59](requirements/logging-audit.md#req-59)).
    - The record holds only the allow and the reason. It does not hold the
      consent status answer ([F-72](traceability/findings.md#f-72)).
- **Impact**: An auditor finds the record only through the stored request
  header. The auditor cannot replay the decision against a known policy.
- **Follow-up**: Fix the trace headers upstream in open-fsc
  ([ADR-0035](decisions/0035-w3c-trace-context.md)). Record the bundle
  revision in the ADL.
- **Related**: [F-41](traceability/findings-closed.md#f-41),
  [REQ-71](requirements/logging-audit.md#req-71),
  [Q-25](traceability/open-questions.md#q-25).

### R26: The QTSP can read the BSN in the ASI token {#r26}

- **Risk**: ETSI requires the identification data in the access token.
  In the demo, a token claim holds the BSN in readable form
  ([`tokens.go#L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/tokens.go#L29)).
- **Impact**: The QTSP holds the token. It can read a BSN that it is not
  allowed to process
  ([P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)).
- **Follow-up**: Encrypt the identification data for the ASIP
  ([#595](https://github.com/ICTU/GBO-demo/issues/595)). Send the gap to
  ETSI ([E7](traceability/standards-feedback.md#e7)).
- **Related**: [F-86](traceability/findings.md#f-86),
  [REQ-86](requirements/asi.md#req-86),
  [Q-36](traceability/open-questions.md#q-36).

## ASI production gaps

### R27: No national register for QTSP admission {#r27}

- **Risk**: The authorization server admits a QTSP on the entitlement
  `QEAA_Provider` in the national register of relying parties. That
  register and its API do not exist. It is not fixed which identifier
  links the QTSP certificate to its entry. The demo uses a stub register
  file.
- **Impact**: QTSPs cannot be admitted in production. If the register is
  unreachable during a re-check, the demo keeps the client active
  (fail-open). Issued tokens stay valid up to 10 minutes after a
  withdrawal.
- **Follow-up**: [Q-34](traceability/open-questions.md#q-34) (outage
  behavior), [Q-35](traceability/open-questions.md#q-35) (identifier),
  [Q-41](traceability/open-questions.md#q-41) (tokens after withdrawal).
- **Related**: [F-85](traceability/findings.md#f-85),
  [REQ-88](requirements/asi.md#req-88),
  [REQ-89](requirements/asi.md#req-89),
  [E10](traceability/standards-feedback.md#e10).

### R28: No link between the QTSP login and the source login {#r28}

- **Risk**: The QTSP identifies the citizen, and the ASI authorization
  server identifies the citizen again. Nothing links the two. The QR
  route can be completed on another phone.
- **Impact**: A QTSP can attest the data of person B to person A.
- **Follow-up**: Add a check under CIR 2025/1569 art. 9(5). In this
  check, the QTSP sends its identification data for verification. As an
  alternative, the QTSP gives this data to the authorization server as a
  hint ([Q-40](traceability/open-questions.md#q-40)). Send the gap to
  ETSI ([E6](traceability/standards-feedback.md#e6)).
- **Related**: [F-93](traceability/findings.md#f-93),
  [REQ-90](requirements/asi.md#req-90),
  [REQ-102](requirements/asi.md#req-102).

### R29: The NL PID has no place of birth {#r29}

- **Risk**: CIR 2024/2977 makes the place of birth a mandatory PID
  attribute. The NL PID type metadata has no place of birth. As a result,
  the authorization server asks for four of the five mandatory
  attributes.
- **Impact**: If the Netherlands reads "identification data" as the
  mandatory PID attributes, a token from the NL Wallet cannot meet that
  reading. DigiD gives a BSN only
  ([F-88](traceability/findings.md#f-88)).
- **Follow-up**: Ask the NL Wallet team. Fix the minimum identification
  data in the PSA ([Q-36](traceability/open-questions.md#q-36)).
- **Related**: [F-94](traceability/findings.md#f-94),
  [REQ-86](requirements/asi.md#req-86).

### R30: Fuzzy matching without returning a value {#r30}

- **Risk**: The ASIP gives `MatchWithVariation` and never returns the
  stored value. Annex IV of CIR 2026/1735 makes the value optional but
  keeps the fuzzy-matching requirement. The conformance matrix marks
  that requirement `failing`.
- **Impact**: In a literal reading of the annex, the ASIP does not
  conform.
- **Follow-up**: Decide whether the ASIP returns the value on a match
  ([Q-29](traceability/open-questions.md#q-29)). Send the gap to ETSI
  ([E2](traceability/standards-feedback.md#e2)).
- **Related**: [F-92](traceability/findings.md#f-92),
  [REQ-85](requirements/asi.md#req-85),
  [REQ-113](requirements/asi.md#req-113).

## DvTP consent

### R24: The consent proof freezes at consent {#r24}

- **Risk**: BSNk transforms only while the citizen is logged in
  ([BSNK-04](requirements/pseudonymization.md#bsnk-04)). As a result,
  the proof fixes the parties, the key versions, the BSN authorization,
  and the proof form for its whole validity period. The proof has no
  version.
- **Impact**: A new source needs a new consent. A re-keyed source must
  keep its old keys ([AV-09](requirements/admission.md#av-09)).
  A new proof form makes all outstanding proofs fail with
  `CONSENT_CONTEXT_INVALID`.
- **Follow-up**: Give the proof a version. Extend the service catalog
  with OIN, key version, and BSN authorization per party
  ([REQ-82](requirements/pseudonymization.md#req-82),
  [Q-77](traceability/open-questions.md#q-77)).
- **Related**: [F-78](traceability/findings.md#f-78),
  [ADR-0032](decisions/0032-consent-proof.md),
  [the proof freezes at consent](concepts/consent.md#the-proof-freezes-at-consent).

### R31: The backend revokes a revoked consent again {#r31}

- **Risk**: A direct revoke of an expired or already revoked consent
  returns HTTP 200, sets `REVOKED` again, and writes a new LDV record
  ([`main.go#L282-L299`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L282-L299)).
- **Impact**: The status history and the logbook get false entries.
- **Follow-up**: Refuse the revoke with `CONSENT_NOT_REVOCABLE`
  ([REQ-109](requirements/consent.md#req-109),
  [#600](https://github.com/ICTU/GBO-demo/issues/600)).
- **Related**: [F-97](traceability/findings.md#f-97).

### R33: A suspended consumer keeps access {#r33}

- **Risk**: The request policy does not read the admission status of a
  direct consumer. A suspended consumer with an existing contract can
  still send queries under a valid consent.
- **Impact**: Suspension takes effect only at the revocation of the
  contract.
- **Follow-up**: [REQ-110](requirements/admission.md#req-110).
  [Q-53](traceability/open-questions.md#q-53) covers the time until the
  suspension takes effect.
- **Related**: [ADR-0015](decisions/0015-contract-acceptance-by-policy.md).

### R35: The consumer sets the consent validity {#r35}

- **Risk**: The consumer sends the validity period. The default is one
  year, with no upper limit. The citizen cannot change it.
- **Impact**: A proof can live longer than the purpose needs. This makes
  [R4](#r4) and [R24](#r24) worse.
- **Follow-up**: Decide who sets the validity period
  ([Q-13](traceability/open-questions.md#q-13),
  [Q-76](traceability/open-questions.md#q-76)).
- **Related**: [F-11](traceability/findings-closed.md#f-11),
  [REQ-19](requirements/consent.md#req-19).

### R37: BSNk recognition of the consent facility is not settled {#r37}

- **Risk**: Only a recognized party can activate and transform
  ([BSNK-01](requirements/pseudonymization.md#bsnk-01)). It is open
  whether the consent facility can be that party, and in which role. The
  demo assumes route D: the backend derives and activates, and the
  register stores PI and PP.
- **Impact**: Route D works only under one condition: the backend and the
  register are one BSNk participant. The rotation of the reference key
  ([Q-56](traceability/open-questions.md#q-56)) and the protection of
  stored PI and PP ([Q-57](traceability/open-questions.md#q-57)) are open.
- **Follow-up**: [Q-26](traceability/open-questions.md#q-26),
  [Q-49](traceability/open-questions.md#q-49), and
  [ADR-0040](decisions/0040-route-d-citizen-recognition.md) (proposed).
- **Related**: [F-75](traceability/findings.md#f-75),
  [REQ-69](requirements/pseudonymization.md#req-69).

## EUDI issuance

### R36: Attestations are valid 365 days without a change feed {#r36}

- **Risk**: Every attestation type gets a fixed validity of 365 days. GBO
  only queries sources and has no change feed.
- **Impact**: If the source data changes, an issuer must revoke an
  attestation that is valid for 24 hours or more. GBO cannot do that.
- **Follow-up**: Per type, choose short-lived attestations or a change
  feed with revocation
  ([REQ-77](requirements/eudi-issuance.md#req-77)).
- **Related**: [F-82](traceability/findings.md#f-82),
  [AV-12](requirements/admission.md#av-12),
  [AV-13](requirements/admission.md#av-13),
  [ADR-0028](decisions/0028-pubeaa-productization.md).

## Production readiness

### R9: Demo-grade shared services {#r9}

- **Risk**: The shared services are demo grade: the consent register runs
  in memory by default, DigiD is a mock, and the PKI is self-generated.
  The BSNk mock follows the BSNk interface (as JSON), but it encrypts
  nothing. The three demo sources share one OIN and one decryption
  component.
- **Impact**: None of these services carries production trust or
  availability. The demo does not demonstrate unlinkability per source.
- **Follow-up**: [ADR-0023](decisions/0023-identity-convergence.md),
  [ADR-0005](decisions/0005-bsnk-pp.md), a replicated register store
  ([SL-12](traceability/increments.md#sl-12)), and a DigiD connection.
- **Related**: [Q-54](traceability/open-questions.md#q-54),
  [demo mock and production BSNk](concepts/pseudonymization.md#demo-mock-and-production-bsnk).

### R10: The consent register is a dependency of every DvTP decision {#r10}

- **Risk**: For every request, the policy asks for the consent status
  online, without a cache.
- **Impact**: A register outage stops all consent-based traffic (fail
  closed).
- **Follow-up**: Set the availability, latency, and propagation targets
  ([REQ-75](requirements/consent.md#req-75),
  [Q-47](traceability/open-questions.md#q-47)). Replicate the register.
- **Related**: [F-61](traceability/findings-closed.md#f-61),
  [ADR-0032](decisions/0032-consent-proof.md).

### R11: The demo runs one PDP for all providers {#r11}

- **Risk**: The target model has a PAP and a PDP at each bronhouder
  ([ADR-0021](decisions/0021-central-pap-signed-bundles.md)). The demo
  runs one shared PDP.
- **Impact**: The demo does not show policy separation between bronhouders.
- **Follow-up**: Run a PDP per provider in the simulation deployment.
- **Related**: [Q-21](traceability/answered-questions.md#q-21) (answered).

### R12: Policy distribution has no integrity chain and no visible fallback {#r12}

- **Risk**: By default, the PDP loads policies from a bind mount. Bundle
  distribution through the OpenFTV Manager is opt-in. Bundles are not
  signed. Signing is not planned while bundles stay inside one
  organization ([#426](https://github.com/ICTU/GBO-demo/issues/426)).
  The policy store is cumulative, and one broken module stops every
  decision.
- **Impact**: There is no integrity chain from author to runtime. There
  is no visible fallback to the last valid policy set.
- **Follow-up**: Guidelines [RL-01](requirements/authorization.md#rl-01)
  and [RL-05](requirements/authorization.md#rl-05). If a bundle
  crosses an organization boundary, signing becomes a requirement.
- **Related**: [F-09](traceability/findings-closed.md#f-09),
  [F-51](traceability/findings.md#f-51),
  [F-52](traceability/findings.md#f-52),
  [Q-21](traceability/answered-questions.md#q-21).

### R13: The PDP mapper is a patch on OpenFTV {#r13}

- **Risk**: The PDP is built from OpenFTV tag v0.1.0, with the FTV GraphQL
  mapper patched in.
- **Impact**: Upstream changes can break the build. The patch steps fail
  loudly, but the maintenance cost stays.
- **Follow-up**: Contribute the mapper extension point to OpenFTV
  upstream ([ADR-0013](decisions/0013-pdp-request-mapper.md)).
- **Related**: [REQ-42](requirements/authorization.md#req-42).

### R14: New sources need a restart of the issuance server {#r14}

- **Risk**: The issuance server reads its configuration at startup.
- **Impact**: Source activation needs a controlled restart.
- **Follow-up**: Accepted in demo v0.9.0
  ([ADR-0016](decisions/0016-source-owned-metadata.md)). If the issuance
  server supports reload, revisit this decision.
- **Related**: [REQ-64](requirements/sources-identity.md#req-64).

## Governance and standards

### R15: The legal ceiling of the service catalog has no technical counterpart {#r15}

- **Risk**: Rule coverage replaced the catalog artifact. The legally
  anchored ceiling and its governance (the Bureau DvTP process) are not
  defined.
- **Impact**: The legal ceiling of what a consumer can ask for is not
  inspectable on its own.
- **Follow-up**: A legal anchoring decision
  ([ADR-0008](decisions/0008-dienstencatalogus-ceiling.md),
  [ADR-0009](decisions/0009-closed-world-rules.md)). The data-set
  description is one input ([REQ-121](requirements/consent.md#req-121)).
- **Related**: [F-74](traceability/findings.md#f-74).

### R16: Rego instead of ODRL {#r16}

- **Risk**: The PSA lists ODRL for S06. The design uses Rego, and Cedar
  inside the OpenFTV Manager.
- **Impact**: The comply-or-explain duty is open.
- **Follow-up**: Bring the deviation to the standards bodies, in line
  with [D-13](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/). For
  more information, see [Policy lifecycle](concepts/policy-lifecycle.md)
  and [Q-78](traceability/open-questions.md#q-78).

### R17: GraphQL is not a recognized FDS datadienst type {#r17}

- **Risk**: The data access pillar rests on a deviation that no standard
  covers.
- **Follow-up**: [ADR-0025](decisions/0025-graphql-fds-datadienst.md).

### R18: Integrator mandates have no validity and no governance {#r18}

- **Risk**: Three points of the integrator route are open. A mandate has
  no validity period, and the integrator is not in the proof
  ([Q-46](traceability/open-questions.md#q-46)). The upstream `act.sub`
  deviates from RFC 8693. The route itself is built (opt-in) and has three
  parts ([ADR-0034](decisions/0034-integrator-delegation.md)):
    - an FSC delegated grant
    - a mandate per integrator, provider, and rule in the admission
      register
    - a consent that binds the represented party.
- **Impact**: A mandate stays valid until someone removes it. It is not
  set who admits integrators and on which terms
  ([AV-06](requirements/admission.md#av-06)).
- **Follow-up**: Three items are open: mandate validity, the governance
  of admission ([Q-74](traceability/open-questions.md#q-74)), and a
  change log for admissions
  ([REQ-123](requirements/admission.md#req-123)).
- **Related**: [F-73](traceability/findings-closed.md#f-73) (closed),
  [REQ-106](requirements/consent.md#req-106),
  [Q-12](traceability/answered-questions.md#q-12).

### R19: LDV gaps: citizen view, activity register, ASIP {#r19}

- **Risk**: LDV is built: each controller logs its own processings in its
  own logbook ([ADR-0026](decisions/0026-ldv-integration.md)). These
  gaps remain:
    - the citizen view of processings per consent is not built
      ([P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/))
    - the register of processing activities is a stand-in
      ([Q-08](traceability/open-questions.md#q-08))
    - the local `dpl.gbo.*` extension is not agreed
      ([Q-72](traceability/open-questions.md#q-72))
    - the ASIP writes no LDV records
    - no pointer leads from the ADL to the consent logbook
      ([Q-25](traceability/open-questions.md#q-25))
    - no retention, access model, or tamper evidence exists for the ADL
      the logbooks, and the FSC transaction logs
      ([REQ-32](requirements/logging-audit.md#req-32)).
- **Impact**: A citizen cannot see QTSP verifications. A chain read
  stops at a party that does not log under LDV
  ([F-68](traceability/findings.md#f-68)).
- **Follow-up**: The open points of
  [ADR-0026](decisions/0026-ldv-integration.md), and the consumer
  obligation ([AV-02](requirements/admission.md#av-02)).
- **Related**: [REQ-72](requirements/logging-audit.md#req-72),
  [F-64](traceability/findings-closed.md#f-64),
  [SL-50](traceability/increments.md#sl-50).

### R20: Onboarding cost for small bronhouders {#r20}

- **Risk**: The cost to connect a source stays high for small
  organizations.
- **Impact**: There is an adoption risk for gemeenten and small sources.
- **Follow-up**: [ADR-0027](decisions/0027-onboarding-toolkit.md).

## Accepted technical debt

The design accepts the following technical debt on purpose:

- Monetary amounts in attestations are integers, because the pinned
  wallet stack cannot represent non-integral values
  ([ADR-0017](decisions/0017-gbo-simple-v1.md)).
- Attestations have no nested claims
  ([REQ-78](requirements/eudi-issuance.md#req-78)).
- The `unsecured` source transport exists for local development. The
  mount policy excludes it from deployments. The code does not exclude
  it.
- The demo works around OpenFTV upstream quirks and documents them: the
  policy language flag, the missing policy-data APIs, and the broken
  policy DELETE (the demo retires a policy instead).

## Traceability

- Requirements: [REQ-39](requirements/consent.md#req-39),
  [REQ-45](requirements/eudi-issuance.md#req-45),
  [REQ-59](requirements/logging-audit.md#req-59),
  [REQ-60](requirements/logging-audit.md#req-60),
  [REQ-71](requirements/logging-audit.md#req-71),
  [REQ-74](requirements/authorization.md#req-74),
  [REQ-75](requirements/consent.md#req-75),
  [REQ-76](requirements/consent.md#req-76),
  [REQ-77](requirements/eudi-issuance.md#req-77),
  [REQ-81](requirements/pseudonymization.md#req-81),
  [REQ-83](requirements/asi.md#req-83),
  [REQ-86](requirements/asi.md#req-86),
  [REQ-88](requirements/asi.md#req-88),
  [REQ-106](requirements/consent.md#req-106),
  [REQ-109](requirements/consent.md#req-109),
  [REQ-110](requirements/admission.md#req-110)
- Findings: [F-52](traceability/findings.md#f-52) (open),
  [F-54](traceability/findings.md#f-54) (open),
  [F-70](traceability/findings.md#f-70) (open),
  [F-72](traceability/findings.md#f-72) (open),
  [F-78](traceability/findings.md#f-78) (open),
  [F-79](traceability/findings.md#f-79) (open),
  [F-80](traceability/findings.md#f-80) (open),
  [F-85](traceability/findings.md#f-85) (open),
  [F-86](traceability/findings.md#f-86) (open),
  [F-92](traceability/findings.md#f-92) (open),
  [F-93](traceability/findings.md#f-93) (open),
  [F-94](traceability/findings.md#f-94) (open)
- Open questions: [Q-08](traceability/open-questions.md#q-08),
  [Q-13](traceability/open-questions.md#q-13),
  [Q-21](traceability/answered-questions.md#q-21) (answered),
  [Q-29](traceability/open-questions.md#q-29),
  [Q-34](traceability/open-questions.md#q-34),
  [Q-36](traceability/open-questions.md#q-36),
  [Q-40](traceability/open-questions.md#q-40),
  [Q-49](traceability/open-questions.md#q-49),
  [Q-58](traceability/open-questions.md#q-58),
  [Q-75](traceability/open-questions.md#q-75) (all open unless marked)
- Demo increments: [SL-12](traceability/increments.md#sl-12) (planned),
  [SL-25](traceability/increments.md#sl-25) (dropped),
  [SL-28](traceability/increments.md#sl-28) (done),
  [SL-29](traceability/increments.md#sl-29) (done, reversed by PR #370),
  [SL-50](traceability/increments.md#sl-50) (done),
  [SL-51](traceability/increments.md#sl-51) (done)
