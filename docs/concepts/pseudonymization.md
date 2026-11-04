# Pseudonymization

Private consumers must not process the BSN
([P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). In
DvTP, they still request data about one citizen from government sources.
For this, GBO uses the BSNk PP polymorphic pseudonym scheme. GBO calls BSNk
only at consent time ([ADR-0005](../decisions/0005-bsnk-pp.md)). In the
consent route, the consumer holds no identifier of the citizen: no BSN and
no pseudonym ([REQ-20](../requirements/pseudonymization.md#req-20)). After
the PDP allows the request, only the source turns its own value back into
the BSN ([ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)).

Pseudonymization realizes capability
[S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering).
For the BSNk rules that shape this design, see
[BSNk preconditions](../requirements/pseudonymization.md#bsnk-preconditions). For the consent
proof that carries the values, see [Consent](consent.md).

## Identifiers

Each identifier of the citizen or the consent has its own maker and holder:

| Identifier | What it is | Made by | Held by |
|---|---|---|---|
| BSN | The citizen service number | DigiD login, or PID disclosure (EUDI, ASI) | The portal backend during the login. The source, inside its own boundary |
| PI, PP | Polymorphic identity and polymorphic pseudonym. Only the requester can get them transformed ([BSNK-03](../requirements/pseudonymization.md#bsnk-03)) | BSNk Activate, once per citizen | The portal backend. The register stores them under `subject_ref` ([REQ-69](../requirements/pseudonymization.md#req-69)) |
| VI (encrypted identity) | A value for one recipient OIN and key version. It decrypts to the BSN. It exists only for a recipient on the BSN authorization list ([BSNK-06](../requirements/pseudonymization.md#bsnk-06)) | BSNk Transform, at consent | Inside the consent proof, `encrypted_subject[<OIN>].identity` |
| VP (encrypted pseudonym) | A value for one recipient OIN and key version. It decrypts to the own pseudonym of that recipient for the citizen. Every recipient gets one | BSNk Transform, at consent | Inside the consent proof, `encrypted_subject[<OIN>].pseudonym` |
| Placeholder | `consent:identity` or `consent:pseudonym`: the name of the subject in a consent-based query | Fixed values ([`lib.rego#L43-L53`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L43-L53)) | The consumer query and the PDP input. The source gateway replaces it |
| `subject_ref` | HMAC of the BSN with the secret, versioned key of the portal | Portal backend ([`subjectref.go#L38-L42`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/subjectref.go#L38-L42)) | Portal backend and register: the key to the consents of the citizen |
| `consent_id` | The consent record | Consent register (toestemmingsregister) | Consumer: its only handle on "this person" |

PI and PP belong to the portal. VI and VP belong to their recipient. No
other party can read them. In the demo, every party can read them because
the mock does not encrypt. For more information, see
[Demo mock and production BSNk](#demo-mock-and-production-bsnk).

## Where each identifier lives

```mermaid
flowchart LR
    subgraph PORTAL[Consent portal backend]
        B1[BSN from login]
        REF[subject_ref = HMAC]
    end
    BSNK[BSNk]
    subgraph CR[Consent register]
        PP[PI + PP under subject_ref]
        PROOF[Signed proof:<br/>VI/VP per source]
    end
    subgraph CONS[Consumer]
        CID[consent_id + proof<br/>placeholder in query]
    end
    subgraph PDP[PDP of the source]
        P1[placeholder only]
    end
    subgraph SRC[Source boundary]
        GW[Source gateway]
        DEC[Decryption component]
        B2[BSN]
    end
    B1 --> REF
    B1 -->|first consent only| BSNK
    BSNK -->|PI + PP| PP
    PP -->|transform at consent| BSNK
    BSNK -->|VI, VP| PROOF
    PROOF --> CID
    CID -->|FSC| P1
    P1 -->|allow| GW
    GW -->|own VI| DEC
    DEC --> B2

--8<-- "mermaid/classes.mmd"
    class B1,REF,PROOF dvtp
    class BSNK,CID ext
    class PP store
    class P1,GW,DEC basis
    class B2 source
    style PORTAL fill:#F4F5F7,stroke:#E28F80
    style CR fill:#F4F5F7,stroke:#E28F80
    style CONS fill:#F4F5F7,stroke:#D1D5DB
    style PDP fill:#F4F5F7,stroke:#16A34A
    style SRC fill:#FFFFFF,stroke:#6F94B8,stroke-dasharray:4 3
```

## Values made at consent time

BSNk transforms values only while the citizen is logged in
([BSNK-04](../requirements/pseudonymization.md#bsnk-04)). A query comes
later. As a result, the portal makes every value that a source needs while
the citizen gives consent
([`portal.go#L119-L192`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L119-L192)).
The portal does these steps:

1. It derives `subject_ref` from the BSN.
2. It looks up PI and PP under `subject_ref` in the register. At the first
   consent of this citizen, it activates the BSN once at BSNk and stores PI
   and PP ([`portal.go#L296-L314`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L296-L314)).
3. It reads the BSN authorization list from a copy. The copy is at most
   `BSN_AUTHORISATION_LIST_MAX_AGE` old (default 1 hour).
4. It transforms PP to a VP for every source. It transforms PI to a VI for
   every source on the list
   ([`portal.go#L197-L224`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L197-L224)).
   Each BSNk request names at most four parties
   ([BSNK-05](../requirements/pseudonymization.md#bsnk-05),
   [`bsnk.go#L102-L115`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/bsnk/bsnk.go#L102-L115)).
5. It sends the values to the register. The register signs them into the
   proof and does not store them.

For each source, the portal must know the OIN, the key version, and the BSN
authorization ([REQ-82](../requirements/pseudonymization.md#req-82)). In
the demo, this is configuration: `CONSENT_SOURCES=<OIN>@<key set version>`
([`docker-compose.yml#L1005`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L1005)).
If no source is configured, the portal gives no consent. A service
catalogue that carries these facts is not built
([#382](https://github.com/ICTU/GBO-demo/issues/382)).

The portal makes all
values at consent, so the proof freezes. For more information, see
[Consent](consent.md#the-proof-freezes-at-consent)
([F-78](../traceability/findings.md#f-78)).

## Citizen recognition: route D

To show and revoke the consents of a citizen without a BSN, the consent facility (toestemmingsvoorziening) needs a stable key. A stored PI or PP is not a stable key, because
BSNk gives other values at every activation. The proposed solution is route
D ([ADR-0040](../decisions/0040-route-d-citizen-recognition.md), proposed,
[route D](../requirements/pseudonymization.md#route-d)). Route D works as
follows:

- The service recognizes the citizen by an HMAC of the BSN, with a
  secret, versioned key. Every record keeps the key version.
- The service activates once and stores PI and PP under that reference.
- To show or revoke consents, the service does not call BSNk.

The register stores PI and PP, but no BSN and no per-party value
([REQ-69](../requirements/pseudonymization.md#req-69),
[REQ-23](../requirements/consent.md#req-23)). This is an intentional
deviation from FR-35, criterion 1 ([F-98](../traceability/findings.md#f-98)).
For the other routes, see
[BSNk preconditions](../requirements/pseudonymization.md#routes-abc).

Route D has these open points:

- Are the register and the portal backend one BSNk participant
  ([Q-49](../traceability/open-questions.md#q-49))? In the demo, the
  backend activates and the register stores.
- A changed HMAC key gives every citizen a different reference. Then the
  service does not show older consents. Migration is not built
  ([Q-56](../traceability/open-questions.md#q-56)).
- The protection of the stored PI and PP is open
  ([Q-57](../traceability/open-questions.md#q-57)). Retention is also open
  ([Q-63](../traceability/open-questions.md#q-63)).

## Where the boundary is enforced

The BSN is in three places only. All three places are inside the
government:

1. Portal backend, at login: the backend derives `subject_ref`. At the
   first consent, it sends the BSN to BSNk. After that step, no component
   holds a BSN, because the draft consent has no field for one
   ([`portal.go#L116-L118`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L116-L118)).
   It is open how the backend inside MijnOverheid gets the verified
   identity ([Q-50](../traceability/open-questions.md#q-50)).
2. BSNk, at activation: BSNk records every activation in its
   Inzageregister ([BSNK-10](../requirements/pseudonymization.md#bsnk-10)).
3. The source, after the allow: the source gateway takes the value for its
   own OIN from the proof. The decryption component of the source reads the
   value with the keys of the source. The gateway accepts the result only
   if the value names the OIN of the source as recipient
   ([`substitution.go#L213-L251`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution.go#L213-L251),
   [REQ-80](../requirements/pseudonymization.md#req-80)). Then the gateway
   replaces the placeholder. BSNk is not in the query path
   ([REQ-21](../requirements/pseudonymization.md#req-21)).

The register never gets a BSN, not even for a short time
([REQ-23](../requirements/consent.md#req-23)). The consumer never
gets a BSN in the proof or in the response.

Like the PDP, the gateway acts on the evidence. If the request carries a
consent token, the gateway takes the subject from the token. If the request
has no consent token, the gateway passes it through unchanged (PID regime).
The gateway reads no grant property. The value for the requested form can
be missing, for example no VI for a source that is not on the list. In that
case, the gateway does not forward the request.

### Network isolation is the control

The gateway does not verify the proof again
([`substitution.go#L105-L107`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution.go#L105-L107)).
A second check adds nothing, because a consumer holds real proofs. The
rule "after the decision" holds only while the Inway is the only component
that reaches the gateway
([REQ-81](../requirements/pseudonymization.md#req-81),
[F-79](../traceability/findings.md#f-79)).

In the demo, the gateways publish no port. They are on two networks only:

- `source-gateways`, shared with the source Inways.
- `sources`, shared with the source services, the decryption component,
  and the logbooks
  ([`docker-compose.yml#L829-L836`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L829-L836)).

No consumer is on either network. Outside Docker Compose, this isolation
needs a Kubernetes NetworkPolicy or an equivalent control. The Helm chart
in demo v0.9.0 has no NetworkPolicy. A nonce that binds a value to one
consent, as a second line, is not built. For the zones, see
[Deployment](../deployment.md).

## Subject binding

Under a consent, the PDP does not compare identifiers. The query names the
subject with a placeholder. The source can fill in only the subject from
the proof ([REQ-79](../requirements/pseudonymization.md#req-79),
[F-77](../traceability/findings.md#f-77)). For the rule, see
[Authorization](authorization.md#constraints-inside-the-query).
Subject binding has these consequences:

- No policy at the PDP can depend on who the citizen is.
- One request names one subject. A question about two persons does not
  fit. This needs a design decision.
- Substitution works only on variables. If the query text holds a literal
  placeholder, the placeholder passes the PDP. The gateway does not replace
  it, and the query finds nobody.
- The PDP input and the decision logs have no identifier. They do hold the
  proof with the encrypted values.

## The consumer has no identifier

The consumer reads only `consent_id` and `scopes` from the proof
([F-76](../traceability/findings.md#f-76)). This goes further than the
"BSN-free" rule of P-04, because the consumer is free of all identifiers.
This has three effects:

- Logging: the consumer logbook names the data subject by the consent ID,
  with subject type `consent-id`
  ([`logbook.go#L20-L22`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/logbook/logbook.go#L20-L22)).
  In the logbook, one citizen with two consents is two data subjects. It is
  open whether this fits LDV ([Q-27](../traceability/open-questions.md#q-27)).
- Access requests: a citizen can ask the consumer what it processed. The
  consumer can find the citizen only through the consents of the citizen.
- Recognition: through GBO, the consumer cannot tell that two consents are
  from the same person. This is data minimization, and a design choice.

With its own VP, the consumer has a pseudonym to log under. This option is
in the design and not built
([#478](https://github.com/ICTU/GBO-demo/issues/478),
[Q-01](../traceability/open-questions.md#q-01)). A source API that answers
on a pseudonym is also not built. No demo rule accepts
`consent:pseudonym` ([#474](https://github.com/ICTU/GBO-demo/issues/474)).

## Exception: the BSN in the EUDI and ASI routes

The EUDI adapter and the ASIP put the plain BSN from the PID or the token
into the query variables. As a result, the BSN is in the PDP input and in
both decision logs: the ADL and the console log
([`source_metadata.go#L273`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata.go#L273),
[`source.go#L94`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source.go#L94)).
The PDP does not call BSNk. This is a known violation of
[REQ-60](../requirements/logging-audit.md#req-60). The demo accepts it
until [#368](https://github.com/ICTU/GBO-demo/issues/368) decides between
masking and "transform first"
([CHANGELOG](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L588-L602)).

The proposed decision keeps identifiers out of the PDP input and uses
masking only as a second line
([ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md), proposed).
Earlier, masking in the policy engine had no effect
([F-54](../traceability/findings.md#f-54)). LDV records never hold a BSN,
because the logbook refuses one ([Logging](logging.md)).

## Demo mock and production BSNk

The demo uses `bsnk-mock`
([README](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bsnk-mock/README.md)).
The mock follows the BSNk interface (`/v2/activate`, `/v2/transform`,
`/v2/bsn-authorisation-list`, and more), but as JSON instead of SOAP. The
mock enforces these rules:

- Only the requester can use the PI.
- The BSN authorization list applies.
- A request names at most four parties.
- The mock reads values per key version.

The mock and production BSNk differ in these properties:

| Property | Demo | Production |
|---|---|---|
| Encryption | None: any party that holds a PI or VI can read the BSN | Encrypted values, unlinkable between parties |
| Values | Stable by default. Random with `RANDOMIZE_VALUES=true`, as real BSNk | Different at every request |
| Interface | JSON over HTTP | SOAP with PKIoverheid ([BSNK-11](../requirements/pseudonymization.md#bsnk-11)) |
| Who can activate | Not checked: the mock takes the requester from the request | Only a recognized participant ([BSNK-01](../requirements/pseudonymization.md#bsnk-01), [F-75](../traceability/findings.md#f-75), [Q-26](../traceability/open-questions.md#q-26)) |
| Activation input | The BSN. The mock does not check it against a population register | The BSN and check data ([BSNK-02](../requirements/pseudonymization.md#bsnk-02)) |
| Recipient keys | Demo keys in the gateway image | Per recipient through an Access Service or Key Requester ([BSNK-09](../requirements/pseudonymization.md#bsnk-09), [#467](https://github.com/ICTU/GBO-demo/issues/467)) |
| Key versions | The mock accepts any key set version | A value belongs to one key version. The source keeps older keys while proofs for them are valid ([BSNK-08](../requirements/pseudonymization.md#bsnk-08), [AV-09](../requirements/admission.md#av-09)) |
| Decryption component | One, shared by the three demo sources, which also share one OIN | One per source, each with its own OIN ([BSNK-07](../requirements/pseudonymization.md#bsnk-07)) |

The same image, started with `DECRYPTION_COMPONENT_ONLY=true`, is the
decryption component of the sources
([`docker-compose.yml#L773-L786`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L773-L786)).
The mock does not encrypt and the sources share one OIN. As a result, the
demo does not show unlinkability between parties. For the certificates and
keys per party at onboarding, see
[BSNk preconditions](../requirements/pseudonymization.md#onboarding-keys).

## Traceability

- Requirements: [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-23](../requirements/consent.md#req-23), [REQ-60](../requirements/logging-audit.md#req-60), [REQ-69](../requirements/pseudonymization.md#req-69), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-80](../requirements/pseudonymization.md#req-80), [REQ-81](../requirements/pseudonymization.md#req-81), [REQ-82](../requirements/pseudonymization.md#req-82), [AV-09](../requirements/admission.md#av-09), [BSNK-01](../requirements/pseudonymization.md#bsnk-01), [BSNK-02](../requirements/pseudonymization.md#bsnk-02), [BSNK-03](../requirements/pseudonymization.md#bsnk-03), [BSNK-04](../requirements/pseudonymization.md#bsnk-04), [BSNK-05](../requirements/pseudonymization.md#bsnk-05), [BSNK-06](../requirements/pseudonymization.md#bsnk-06), [BSNK-07](../requirements/pseudonymization.md#bsnk-07), [BSNK-08](../requirements/pseudonymization.md#bsnk-08), [BSNK-09](../requirements/pseudonymization.md#bsnk-09), [BSNK-10](../requirements/pseudonymization.md#bsnk-10), [BSNK-11](../requirements/pseudonymization.md#bsnk-11)
- Findings: [F-30](../traceability/findings-closed.md#f-30) (resolved in demo), [F-54](../traceability/findings.md#f-54) (open), [F-75](../traceability/findings.md#f-75) (open), [F-76](../traceability/findings.md#f-76) (open), [F-77](../traceability/findings.md#f-77) (open), [F-78](../traceability/findings.md#f-78) (open), [F-79](../traceability/findings.md#f-79) (open), [F-98](../traceability/findings.md#f-98) (open)
- Open questions: [Q-01](../traceability/open-questions.md#q-01) (partly answered), [Q-26](../traceability/open-questions.md#q-26) (open), [Q-27](../traceability/open-questions.md#q-27) (open), [Q-49](../traceability/open-questions.md#q-49) (open), [Q-50](../traceability/open-questions.md#q-50) (open), [Q-56](../traceability/open-questions.md#q-56) (open), [Q-57](../traceability/open-questions.md#q-57) (open), [Q-63](../traceability/open-questions.md#q-63) (open)
- Demo increments: [SL-02](../traceability/increments.md#sl-02) (done), [SL-22](../traceability/increments.md#sl-22) (done), [SL-29](../traceability/increments.md#sl-29) (done), [SL-51](../traceability/increments.md#sl-51) (done)
