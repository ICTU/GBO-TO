# ADR-0032: The consent proof: signed, a value per source, a placeholder in the query, status online over FSC, verified in policy

- Status: accepted
- Date: 2026-11-02
- Satisfies: [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), [S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering), [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Supersedes: [ADR-0007](0007-consent-signed-token.md)
- Deliberation: [REQ-68](../requirements/consent.md#req-68), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-80](../requirements/pseudonymization.md#req-80), [F-44](../traceability/findings-closed.md#f-44), [F-61](../traceability/findings-closed.md#f-61), and demo [PR #238](https://github.com/ICTU/GBO-demo/pull/238), [PR #371](https://github.com/ICTU/GBO-demo/pull/371) ([#330](https://github.com/ICTU/GBO-demo/issues/330)), [PR #390](https://github.com/ICTU/GBO-demo/pull/390), [PR #469](https://github.com/ICTU/GBO-demo/pull/469), [#383](https://github.com/ICTU/GBO-demo/issues/383), [#473](https://github.com/ICTU/GBO-demo/issues/473)
- Implemented in:
    - [consent_token.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/consent_token.go#L20-L36): the proof.
    - [consent.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego): the verification and the status check in policy.
    - [status.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status.go): the status listener behind the register Inway.
    - [lib.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L43-L53): the placeholders.
    - [docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L141-L142): the status call over the PDP Outway.

## Context and problem statement

In DvTP, the consent of the citizen is the access basis. The PDP at the
source must establish three facts itself
([REQ-68](../requirements/consent.md#req-68)):

- The consent comes from the consent register (toestemmingsregister) and is unchanged.
- The consent is bound to this consumer, this data set, and this
  citizen.
- The consent is valid at the time of the request, also after a
  revocation one second before.

The consumer must not hold a citizen identifier
([REQ-20](../requirements/pseudonymization.md#req-20)). The consumer
also must not choose the subject of its question
([REQ-79](../requirements/pseudonymization.md#req-79)). BSNk transforms
values only while the citizen is logged in
([BSNK-04](../requirements/pseudonymization.md#bsnk-04)). For this
reason, the register must make every value that a source needs at
consent time. These values travel with the proof.

## Decision

### The proof

When the citizen gives consent, the consent register signs a JWT
with these properties:

- The algorithm is ES256. The header has `typ=gbo-consent+jwt` and
  `kid`. The public keys are in the JWKS of the register.
- The claims are `consent_id`, `scopes`, `scope_entries` (per source),
  `dienstverlener_oin`, `valid_until`, `iss`, `aud` (default
  `gbo:dvtp:pdp`), `iat`, `nbf`, `exp` (equal to `valid_until`), and
  `jti`. The `dienstverlener_oin` is the represented party
  ([ADR-0034](0034-integrator-delegation.md)).
- The `encrypted_subject` claim holds a `pseudonym` (VP) per source OIN.
  If the source is on the BSN authorization list, it also holds an
  `identity` (VI) for that source. Each value carries its
  `key_set_version`. Only that source can read the value
  ([REQ-80](../requirements/pseudonymization.md#req-80)).

The proof holds no PI and no BSN. If a proof has no pseudonym for every
party, the register refuses it.

### The consumer

The consumer sends the proof unchanged in `X-GBO-Consent-Token`
([AV-05](../requirements/admission.md#av-05)). In its query,
the consumer names the citizen only with a placeholder:

- `consent:identity` for a BSN API.
- `consent:pseudonym` for a source-pseudonym API.

Each rule lists the placeholders that it accepts. If the query has a
literal value, or a placeholder without a verified proof, the PDP denies
(`CONSTRAINT_MISMATCH`).

### The PDP policy verifies the proof itself

The request mapper only maps ([ADR-0013](0013-pdp-request-mapper.md)).
`consent.rego` does these steps per evaluation:

1. It verifies the ES256 signature against the JWKS of the register. The
   policy caches the JWKS for 300 seconds. On an unknown `kid`, the
   policy fetches the JWKS again.
2. It verifies the claims in Rego, with 30 seconds of clock skew.
3. Only after that, it asks the status of this `consent_id`. This call uses
   no cache and a 2-second timeout. It goes over FSC, through the Outway
   of the PDP, to the Inway of the register (FSC service
   `consent-status`).

Keys can be five minutes old. The status cannot be old. Every failure
maps to its own reason code:

- `CONSENT_SIGNATURE_INVALID`
- `CONSENT_TOKEN_EXPIRED`
- `CONSENT_KEYS_UNAVAILABLE`
- `CONSENT_CONTEXT_INVALID`
- `CONSENT_NOT_FOUND`
- `CONSENT_STATUS_UNAVAILABLE`
- `CONSENT_WITHDRAWN`

The policy ignores a `pip.consent` in the input.

### After an allow

After an allow, the source gateway takes its own value from the proof.
The gateway decrypts the value with its own keys and replaces the
placeholder ([ADR-0033](0033-gateway-decrypts-after-allow.md)).

## Considered options

1. A signed proof, with the status online (chosen).
2. Only a consent ID, and the PDP looks up the content at the register
   ([ADR-0006](0006-consent-register-as-pip.md)). The register becomes
   the only source of the evidence. The consumer presents nothing that
   the PDP can verify.
3. A status list that the PDP fetches periodically. A revocation takes
   effect only after the next fetch.
   [REQ-14](../requirements/consent.md#req-14) needs a deny on the next
   request.
4. A verifiable credential or presentation. This is a wallet format for
   a server-to-server proof. It adds a holder role that the consumer
   does not have.
5. A PI in the query, and a BSNk call at the PEP or the source
   ([ADR-0010](0010-pep-bsn-resolution.md),
   [ADR-0007](0007-consent-signed-token.md)). The PI belongs to the
   requester only ([BSNK-03](../requirements/pseudonymization.md#bsnk-03)).
   BSNk transforms only while the citizen is logged in
   ([BSNK-04](../requirements/pseudonymization.md#bsnk-04)).
6. Consent verification in the Go request mapper (the earlier demo). FTV
   puts attribute retrieval inside the PDP. With verification in the
   mapper, the decision rests on facts that the policy did not establish
   ([REQ-18](../requirements/authorization.md#req-18)).

## Consequences

- Freshness is asymmetric on purpose
  ([F-61](../traceability/findings-closed.md#f-61)). The basis travels as a
  proof. The status stays online, so the register is a dependency on
  every request ([REQ-75](../requirements/consent.md#req-75)). The values
  for latency and availability are open
  ([Q-47](../traceability/open-questions.md#q-47)).
- The status check is a processing at the register. The register
  answers only an FSC peer that its Inway authenticated. The register
  logs that peer as the processor
  ([REQ-76](../requirements/consent.md#req-76)). Any connected peer can
  still ask the status of any consent whose ID it holds. A restriction
  to the own PDP of the source is not built in demo v0.9.0.
- A replay from (input, policy, data) is not possible. The policy
  fetches the status during the evaluation. The engine copies the
  resolved consent into its response for the console log. The ADL
  carries only `{allow, reason}` ([F-72](../traceability/findings.md#f-72),
  [ADR-0036](0036-adl-decision-record.md)).
- The PDP verifies that the subject comes from the proof. The PDP does
  not verify who the subject is ([F-77](../traceability/findings.md#f-77)).
  One request names one subject. No policy can depend on the identity of
  the subject.
- The proof freezes at consent ([F-78](../traceability/findings.md#f-78)).
  The parties, key versions, BSN authorization, and proof form stay fixed
  for its validity period. The proof has no version. If a source is
  added or gets new keys later, it needs a new consent, or it keeps its
  old keys ([AV-09](../requirements/admission.md#av-09)).
- The proof is a bearer token. The actor binding stops use by another
  consumer, but it does not stop replay by the same consumer. Production
  needs a shorter validity and a proof-of-possession binding to the FSC
  identity ([Risks and technical debt](../risks.md)).
- The consumer holds no citizen identifier
  ([F-76](../traceability/findings.md#f-76)). What the consumer records
  about "this person" hangs on the consent ID. A pseudonym for the
  consumer itself is not built
  ([#478](https://github.com/ICTU/GBO-demo/issues/478)).

These points are open:

- Where does the signing key live, and how does it rotate
  ([Q-55](../traceability/open-questions.md#q-55))?
- Does the proof bind the purpose
  ([Q-69](../traceability/open-questions.md#q-69))?
- Is the integrator in the proof
  ([Q-46](../traceability/open-questions.md#q-46))?
- Who sets the validity period
  ([Q-13](../traceability/open-questions.md#q-13))?

The design came in three steps:

1. A consent PIP through a PEP pre-fetch
   ([SL-08](../traceability/increments.md#sl-08)).
2. A signed, actor-bound proof
   ([SL-47](../traceability/increments.md#sl-47)).
3. An encrypted value per source and a placeholder
   ([SL-51](../traceability/increments.md#sl-51)).

## Traceability

- Requirements: [REQ-68](../requirements/consent.md#req-68), [REQ-75](../requirements/consent.md#req-75), [REQ-76](../requirements/consent.md#req-76), [REQ-14](../requirements/consent.md#req-14), [REQ-18](../requirements/authorization.md#req-18), [REQ-19](../requirements/consent.md#req-19), [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-80](../requirements/pseudonymization.md#req-80), [REQ-82](../requirements/pseudonymization.md#req-82), [AV-05](../requirements/admission.md#av-05), [BSNK-03](../requirements/pseudonymization.md#bsnk-03), [BSNK-04](../requirements/pseudonymization.md#bsnk-04)
- Findings: [F-44](../traceability/findings-closed.md#f-44) (resolved in demo), [F-61](../traceability/findings-closed.md#f-61) (closed), [F-72](../traceability/findings.md#f-72) (open), [F-76](../traceability/findings.md#f-76) (open), [F-77](../traceability/findings.md#f-77) (open), [F-78](../traceability/findings.md#f-78) (open)
- Open questions: [Q-05](../traceability/answered-questions.md#q-05) (answered), [Q-13](../traceability/open-questions.md#q-13) (open), [Q-46](../traceability/open-questions.md#q-46) (open), [Q-47](../traceability/open-questions.md#q-47) (open), [Q-55](../traceability/open-questions.md#q-55) (open), [Q-69](../traceability/open-questions.md#q-69) (open)
- Demo increments: [SL-08](../traceability/increments.md#sl-08) (done), [SL-23](../traceability/increments.md#sl-23) (done), [SL-47](../traceability/increments.md#sl-47) (done), [SL-51](../traceability/increments.md#sl-51) (done)
