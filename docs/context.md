# Context and scope

The GBO technical system connects to external actors and systems. This
chapter lists every interface (koppelvlak) on the system boundary and between GBO
components. It covers the technical context only. The
[GO solution direction](https://ictu.github.io/GBO-GO/main/#2-voorgestelde-oplossingsrichting)
and the
[PSA solution direction](https://ictu.github.io/GBO-PSA/main/oplossingsrichting/)
give the business context: which parties exchange which data, and why.

## Technical context

GBO has the same shape as in the
[Globaal Ontwerp](https://ictu.github.io/GBO-GO/main/#overzicht-voorgestelde-oplossing):
external parties use one of the channels, and every channel reaches the
source through GBO Basis. The following figure shows who is on the other
side of each interface in gbo-demo v0.9.0. Dashed blocks are designed but
not built. Click a block to zoom in.

```mermaid
flowchart TB
  subgraph ext["External parties"]
    direction LR
    gov["Government consumer"]
    dv["Private consumer<br/>or integrator"]
    cit(["Citizen<br/>browser + DigiD"])
    wallet["EUDI wallet<br/>NL Wallet app"]
    qtsp["QTSP"]
    eu["EU procedure portal"]
  end
  subgraph ch["GBO channels"]
    direction LR
    tv("Consent facility<br/>portal + register")
    pub("PuB-EAA provider<br/>adapter + issuance server")
    asi("ASI provider<br/>authorization server + ASIP")
    oots("OOTS adapter")
  end
  subgraph svc["External services"]
    direction LR
    bsnk["BSNk PP<br/>Logius"]
    rrp["Register of<br/>relying parties"]
    dip["Discover Interface"]
  end
  subgraph basis["GBO Basis at the source"]
    direction LR
    pep("FSC Inway = PEP<br/>+ PDP")
    src[("Source holder: source<br/>gateway + GraphQL API")]
  end

  gov ~~~ dv ~~~ cit ~~~ wallet ~~~ qtsp ~~~ eu
  tv ~~~ pub ~~~ asi ~~~ oots
  bsnk ~~~ rrp ~~~ dip
  cit -- "HTTPS: consent" --> tv
  dv -- "redirect" --> tv
  wallet -- "OpenID4VP, OpenID4VCI" --> pub
  wallet -- "OpenID4VP: login" --> asi
  qtsp -- "OAuth, verify, retrieve" --> asi
  eu -. "AS4" .-> oots
  dv == "FSC: query + consent proof" ==> pep
  gov -. "FSC" .-> pep
  pub -- "FSC" --> pep
  asi -- "FSC" --> pep
  oots -. "FSC" .-> pep
  tv <-. "consent status, FSC" .- pep
  pep == "after allow" ==> src
  tv -- "at consent only" --> bsnk
  asi -- "entitlement" --> rrp
  qtsp -. "discover" .-> dip

--8<-- "mermaid/classes.mmd"
  class cit source
  class dv,wallet,qtsp,bsnk,rrp,dip ext
  class eu,gov,oots planned
  class tv dvtp
  class pub,asi eudi
  class pep basis
  class src source
  class tv,pub,asi,oots,pep,src zoom
  style ext fill:#F4F5F7,stroke:#D1D5DB
  style ch fill:#F4F5F7,stroke:#D1D5DB
  style basis fill:#F0FDF4,stroke:#16A34A
  style svc fill:#F4F5F7,stroke:#D1D5DB
  click tv "../building-blocks/dvtp/consent-service/" "Toestemmingsvoorziening"
  click pub "../building-blocks/eudi/pubeaa/" "PuB-EAA provider"
  click asi "../building-blocks/eudi/asi/" "ASI provider"
  click oots "../building-blocks/oots/" "OOTS channel"
  click pep "../building-blocks/gbo-basis/" "GBO Basis"
  click src "../building-blocks/gbo-basis/source-access/" "Source access"
```

*Figure 1: The system context. Thick lines: the path of a data request.
Dashed: designed, not built.*
{: .caption }

Inside the boundary, the PDP is the hub. It reads two registers, writes
the decision record, and decides on contracts as well as on requests:

```mermaid
flowchart LR
  subgraph fsc["FSC at the source"]
    direction TB
    inw("FSC Inway<br/>PEP")
    mgr("FSC Manager<br/>contracts")
  end
  pdp("OpenFTV PDP<br/>OPA/Rego")
  subgraph reg["Registers and records"]
    direction TB
    adm[("Admission register")]
    tr[("Consent register")]
    adl[("ADL<br/>decision records")]
  end
  subgraph src["At the source holder"]
    direction TB
    gw("Source gateway")
    dec("Decryption<br/>component")
    ldv[("LDV logbook")]
  end
  subgraph eudi["EUDI components"]
    direction TB
    adp("EUDI adapter<br/>+ reconciler")
    sreg[("Source registry")]
    asip("ASIP")
  end

  inw -- "AuthZEN: request" --> pdp
  mgr -- "AuthZEN: contract" --> pdp
  adm -. "PIP pull, every 5 s" .-> pdp
  pdp -- "keys (JWKS) + status over FSC" --> tr
  pdp --> adl
  inw -- "after allow" --> gw
  gw --> dec
  gw -.-> ldv
  adp -- "writes releases" --> sreg
  asip -- "reads releases" --> sreg

--8<-- "mermaid/classes.mmd"
  class inw,mgr,pdp,gw,dec basis
  class adm,adl,ldv,sreg store
  class tr dvtp
  class adp,asip eudi
  class pdp,tr,sreg,adl zoom
  style fsc fill:#F0FDF4,stroke:#16A34A
  style reg fill:#F4F5F7,stroke:#D1D5DB
  style src fill:#FFFFFF,stroke:#6F94B8,stroke-dasharray:4 3
  style eudi fill:#FFF7ED,stroke:#EA580C
  click pdp "../building-blocks/gbo-basis/authorization/" "Authorization"
  click tr "../building-blocks/dvtp/consent-service/" "Toestemmingsvoorziening"
  click sreg "../building-blocks/gbo-basis/source-configuration/" "Source configuration"
  click adl "../building-blocks/gbo-basis/records/" "Records"
```

*Figure 2: The interfaces between GBO components.*
{: .caption }

The [interface inventory](#koppelvlak-inventory) lists every interface
with its protocol and code. The
[building block view](building-blocks/index.md) zooms in per channel.

Four points in these diagrams are easy to misread:

- Only the portal backend calls BSNk, at consent time. Neither the PDP nor
  the source gateway calls BSNk. The source reads its own value with
  its own decryption component
  ([ADR-0033](decisions/0033-gateway-decrypts-after-allow.md)).
- The PDP gets the consent status over FSC: from its own Outway (peer
  `…0800`) to the register's Inway (peer `…0700`). Only the public keys
  come directly from the register
  ([ADR-0032](decisions/0032-consent-proof.md)).
- The QTSP is not an FSC participant. It is an OAuth client of the ASI
  authorization server and calls the ASIP over HTTPS. The ASIP is the FSC
  participant toward the source
  ([F-87](traceability/findings.md#f-87),
  [ADR-0037](decisions/0037-asi-oauth-front-door.md)).
- The ASI has four roles. GBO provides the ASIP and the authorization
  server. The Discover Interface and the QTSP are external. For these two
  roles, the demo has a stub and a reference client. It is open who
  operates the ASIP and the authorization server
  ([Q-37](traceability/open-questions.md#q-37)).

## Interface inventory {#koppelvlak-inventory}

Every interface has a row in one of the tables in the following sections.
A row gives the standard that the interface follows and its implementation
in gbo-demo. Rows marked *designed* are not built in demo v0.9.0. Paths in
the last column are relative to
[gbo-demo v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0).

### DvTP consent

The DvTP consent chain uses these interfaces:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| Consent initiation | Consumer → consent portal (toestemmingsportaal), and back | HTTPS redirect with consumer, scopes, purpose, and return URL. The return carries the consent proof in the URL fragment, or `status=denied` ([REQ-37](requirements/consent.md#req-37), [REQ-119](requirements/consent.md#req-119)). | [toestemmingsportaal-frontend](https://github.com/ICTU/GBO-demo/tree/v0.9.0/toestemmingsportaal-frontend) |
| Citizen login | Citizen ↔ consent portal | DigiD (mock): the citizen types a test BSN, and the backend signs a portal token with the BSN in `sub`. Real DigiD gives the identity in an assertion ([REQ-24](requirements/consent.md#req-24)). | [portalhttp](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/consent-portal-backend/portalhttp) |
| Consent registration | Portal backend ↔ consent register (toestemmingsregister) | REST: `POST /consents`, `GET /consents?subject_ref=…`, `GET` and `DELETE /consents/{id}`, `GET` and `PUT /subjects/{ref}/polymorphic`. No BSN crosses this interface ([REQ-23](requirements/consent.md#req-23), [REQ-39](requirements/consent.md#req-39)). | [consent-register/main.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L350-L376) |
| BSNk PP | Portal backend → BSNk | `/v2/activate`, `/v2/transform`, and `/v2/bsn-authorisation-list`. The mock follows the BSNk interface as JSON and does not encrypt. Production BSNk uses SOAP with PKIoverheid ([BSNK-11](requirements/pseudonymization.md#bsnk-11)). | [bsnk-mock](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bsnk-mock/README.md) |
| Consent proof | Consumer → Inway → PDP and source gateway | Signed JWT `gbo-consent+jwt` (ES256) in the `X-GBO-Consent-Token` header, with `encrypted_subject` per source. The query names the subject with the placeholder `consent:identity` or `consent:pseudonym` ([REQ-79](requirements/pseudonymization.md#req-79), [AV-05](requirements/admission.md#av-05)). | [consent_token.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/consent_token.go) |
| Consent keys | PDP → consent register | `GET /.well-known/jwks.json`, cached for 300 s | [consent.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego) |
| Consent status | PDP Outway (`…0800`) → register Inway (`…0700`) | FSC service `consent-status`: `GET /consents/{id}/status` on a status-only listener, with no cache and a 2 s timeout. The register refuses a call without an FSC peer ([REQ-76](requirements/consent.md#req-76)). | [status.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status.go), [Makefile](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L647-L668) |

### Authorization and FSC

The authorization chain and the FSC group use these interfaces:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| Data request | Consumer Outway ↔ source holder (bronhouder) Inway | FSC (OpenFSC v2.4.0): mTLS, access token, and grant hash. Grants carry no properties. | [fsc-infra](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml) |
| Delegated data request | Integrator Outway ↔ source holder Inway | FSC `DelegatedServiceConnectionGrant`, signed by the integrator, the represented consumer, and the provider ([REQ-106](requirements/consent.md#req-106)) | [seed-bri-delegation-int.sh](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/scripts/seed-bri-delegation-int.sh) |
| Authorization | Inway (PEP) ↔ PDP | OpenID AuthZEN 1.0, `POST /authzen/v1/evaluation` over HTTPS. The Inway passes the raw body, and the PDP maps it per the FTV GraphQL profile ([REQ-42](requirements/authorization.md#req-42)). | [openftv-pdp](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/openftv-pdp) |
| Contract decision | Provider Manager → PDP | AuthZEN autosign request for each submitted contract ([REQ-62](requirements/admission.md#req-62)) | [autosign.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego) |
| Participant admission | PDP ← admission register | OpenFTV PIP pull, `GET /internal/openftv/participants`, every 5 s, on a network that only the PDP shares ([REQ-61](requirements/admission.md#req-61)) | [dvtp-onboarding.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml) |

### Source holder {#bronhouder}

The source holder uses these interfaces:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| GraphQL source API | Source gateway ↔ source | GraphQL over HTTP, `POST /graphql`. Only the Inway can reach the gateway ([REQ-81](requirements/pseudonymization.md#req-81)). | [graphql-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/graphql-server), [brp-graphql-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/brp-graphql-server), [lvg-graphql-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/lvg-graphql-server) |
| Source decryption | Source gateway → decryption component of the source | `POST /signed-encrypted-identity` and `POST /signed-encrypted-pseudonym`. The component calls no other service ([REQ-21](requirements/pseudonymization.md#req-21)). | [decryption.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/decryption/decryption.go) |
| Source metadata | Reconciler ← source | `GET /.well-known/gbo` over a separate FSC metadata service, per `gbo-source-metadata` 1.0 or 1.1 ([REQ-64](requirements/sources-identity.md#req-64)) | [schema](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json), [source_metadata.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/source_metadata.go) |

### EUDI issuance

EUDI issuance uses these interfaces:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| Wallet issuance | EUDI wallet ↔ issuance server | OpenID4VCI with OpenID4VP disclosure, SD-JWT VC (`dc+sd-jwt`) | [eudi-issuance-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-issuance-server) (nl-wallet v0.5.0) |
| Attestation data | Issuance server → EUDI adapter | `POST /attestations/{source_id}/{type_id}` over public HTTPS. In demo v0.9.0, this route has no caller authentication ([REQ-45](requirements/eudi-issuance.md#req-45), [#133](https://github.com/ICTU/GBO-demo/issues/133)). | [source_release_runtime.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L69) |
| Offer catalog | Frontends ← EUDI adapter | `GET /eudi-offers.json`. If a source is stale, the adapter returns 503. | [source_release_runtime.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L95) |
| Type metadata | Wallet ecosystem ← EUDI adapter | `GET /types/{source-id}/{type-id}/v{n}`, immutable, `vct#integrity` | [type_metadata.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/type_metadata.go) |
| Source registry | EUDI adapter, issuance init step, ASIP ← source registry | PostgreSQL, read-only role on releases and the active pointer | [source-registry](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry) |
| QTSP test statement | Issuance server → reference QTSP | Callback on a secret path over CA-pinned HTTPS (use case `qtsp-attestation`). Demo scaffolding. | [qtsp_issuance.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/qtsp_issuance.go) |

### Authentic Source Interface

The Authentic Source Interface uses these interfaces:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| ASI discovery | QTSP ↔ Discover Interface, and Discover Interface ← ASIP records | ETSI TS 119 478 clause 5.3 and Annex A. `dataService` records (clause 5.3.3) at `/<ds>/dataservices` ([REQ-99](requirements/asi.md#req-99)). | [asi-discovery-stub](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-discovery-stub) (stub), [asi-provider](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-provider) |
| ASI contract | QTSP ← ASIP | ETSI Annex B OpenAPI with completions. `x-oauth-authorization-server` names the authorization server ([REQ-100](requirements/asi.md#req-100)). | [asi-provider/openapi](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-provider/openapi) |
| ASI server metadata | QTSP, ASIP ← authorization server | RFC 8414 metadata and JWKS | [asi-authorization-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server) |
| QTSP registration | QTSP → authorization server | RFC 7591 `POST /register` with a software statement sealed by the QTSP certificate (`x5c`, `registryURI`) ([REQ-88](requirements/asi.md#req-88)) | [asi-authorization-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server) |
| Entitlement lookup | Authorization server → register of relying parties | Lookup on `registryURI` for the entitlement `QEAA_Provider` (CIR 2025/848). The demo reads a stub file ([F-85](traceability/findings.md#f-85)). | [register.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/testdata/register.json) |
| ASI authorization | Citizen browser ↔ authorization server ↔ QTSP | OAuth 2.0 code flow, PKCE S256, RFC 8707 `resource` (exactly one data service), optional RFC 9396 `authorization_details` ([REQ-90](requirements/asi.md#req-90), [REQ-95](requirements/asi.md#req-95)) | [asi-authorization-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server) |
| Citizen identification | Wallet ↔ wallet verifier ↔ authorization server | OpenID4VP, PID `urn:eudi:pid:nl:1`. A DigiD mock is the second means ([REQ-102](requirements/asi.md#req-102)). | [asi-wallet-verifier](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-wallet-verifier), [digidmock](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server/internal/digidmock) |
| ASI token | Authorization server → QTSP → ASIP | RFC 9068 JWT (ES256), DPoP (RFC 9449), `private_key_jwt` ([REQ-86](requirements/asi.md#req-86), [REQ-87](requirements/asi.md#req-87)) | [accesstoken](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-provider/internal/accesstoken) |
| ASI verify and retrieve | QTSP ↔ ASIP | ETSI TS 119 478 clauses 6.1.1 and 6.1.2 at `/<ds>/authsrc-api/verify` and `/retrieve`. Errors follow RFC 9457. The seal is in `X-JWS-Signature` (detached JWS) ([REQ-83](requirements/asi.md#req-83), [REQ-112](requirements/asi.md#req-112)). | [handler.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L99-L105) |
| ASIP source query | ASIP Outway (`…1200`) ↔ provider Inway | FSC and AuthZEN (rule ASI0001). One GraphQL query per request. | [graphqlsource](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-provider/internal/graphqlsource) |
| ASI source description | Reconciler ← source, and ASIP ← source registry | `gbo-source-metadata` 1.1, capability `asi`. The ASIP reads a release snapshot. | [asi-mapping](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-mapping), [source-registry](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry) |

### Logging and audit

Logging and audit use these interfaces:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| Decision records | PDP → ADL, and reader → ADL | Logius ADL in Postgres `ftv_adl`. Readers use a SELECT-only role ([REQ-71](requirements/logging-audit.md#req-71)). | [adl-reader.sql](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/adl/adl-reader.sql), [adl.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/adl.go) |
| Processing records | Component → logbook of its controller | LDV v1.0.0 write, `POST /logboek/records`, over HTTPS with JSON and a bearer write token ([REQ-72](requirements/logging-audit.md#req-72)) | [ldv-client](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/ldv-client) |
| Processing-record read | Auditor, portal → logbook | LDV read extension, `POST /data-processing-operations` on trace ID, processing activity, or data subject. A read is possible with a read token only. | [ldv-logboek](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/ldv-logboek) |
| Transaction logs | Auditors ← txlog of each peer | FSC txlog API, `GET /v1/logs` over mTLS. The demo reads the txlog API inside each organization. Access in production is an open question ([F-42](traceability/findings-closed.md#f-42), [Q-08](traceability/open-questions.md#q-08)). | [fsctxlog.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/fsctxlog.go) |
| Trace context | Every component → next hop | W3C `traceparent`. `Fsc-Transaction-Id` is recorded next to it ([REQ-55](requirements/logging-audit.md#req-55)). | [tracecontext.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext.go) |
| Telemetry | All services → collector | OpenTelemetry OTLP | [collector-config.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/otel/collector-config.yaml) |

### Designed

Two interfaces are designed but not built in demo v0.9.0:

| Interface | Between | Protocol and standard | Implemented in |
|---|---|---|---|
| OOTS evidence exchange | EU access points ↔ OOTS adapter | AS4/eDelivery and OOTS-EDM. This interface is *designed*. For more information, see [ADR-0020](decisions/0020-as4-bridge-for-oots.md) and [Q-79](traceability/open-questions.md#q-79). | — |
| Government data request | Government consumer ↔ source holder Inway | FSC with its own positive evidence. This interface is *designed*. For more information, see [design-level scenarios](runtime/design-level.md). | — |

## Scope

The demo implements three routes end to end, at demo grade:

1. The DvTP query under consent, with an integrator variant and the LVG
   pilot as a second consumer and source.
2. EUDI issuance of PuB-EAA attestations.
3. ASI verification and retrieval for QTSPs (ETSI TS 119 478 clause 6.1).

Two routes are design-level: SDG-OOTS and Gov-to-Gov. The
[runtime view](runtime/index.md) has a scenario for each.

This design covers the following parts of the system:

- the authorization chain: PEP, PDP, PIPs, policies, and contract decisions
- the consent chain: portal, register, consent proof, and status service
- pseudonymization at consent time and decryption at the source
- the FSC group configuration and the admission register
- EUDI issuance, source onboarding, and the source registry
- the Authentic Source Interface: ASIP, authorization server, and discovery
  records
- logging, audit, and observability

The following parts are out of scope:

- the internal architecture of source holder systems behind the GraphQL API
- the EUDI wallet, DigiD, and BSNk themselves
- the QTSP, the Discover Interface, and the national register of relying
  parties
- the relying-party side of wallet presentations, which touches no GBO
  infrastructure
- the EU OOTS common services

The developer tooling of the demo is scaffolding: the developer portal,
the consumer mocks, `keyper-mock`, and the reference QTSP. This tooling is
outside the target architecture. The [deployment view](deployment.md) marks
each unit as target architecture or scaffolding.

## Traceability

- Requirements: [REQ-21](requirements/pseudonymization.md#req-21),
  [REQ-23](requirements/consent.md#req-23),
  [REQ-24](requirements/consent.md#req-24),
  [REQ-37](requirements/consent.md#req-37),
  [REQ-42](requirements/authorization.md#req-42),
  [REQ-45](requirements/eudi-issuance.md#req-45),
  [REQ-55](requirements/logging-audit.md#req-55),
  [REQ-61](requirements/admission.md#req-61),
  [REQ-64](requirements/sources-identity.md#req-64),
  [REQ-71](requirements/logging-audit.md#req-71),
  [REQ-72](requirements/logging-audit.md#req-72),
  [REQ-76](requirements/consent.md#req-76),
  [REQ-79](requirements/pseudonymization.md#req-79),
  [REQ-81](requirements/pseudonymization.md#req-81),
  [REQ-83](requirements/asi.md#req-83),
  [REQ-86](requirements/asi.md#req-86) to [REQ-88](requirements/asi.md#req-88),
  [REQ-99](requirements/asi.md#req-99),
  [REQ-100](requirements/asi.md#req-100),
  [REQ-102](requirements/asi.md#req-102),
  [REQ-106](requirements/consent.md#req-106),
  [REQ-112](requirements/asi.md#req-112),
  [BSNK-11](requirements/pseudonymization.md#bsnk-11),
  [AV-05](requirements/admission.md#av-05)
- Findings: [F-42](traceability/findings-closed.md#f-42) (closed),
  [F-85](traceability/findings.md#f-85) (open),
  [F-87](traceability/findings.md#f-87) (open)
- Open questions: [Q-08](traceability/open-questions.md#q-08),
  [Q-37](traceability/open-questions.md#q-37),
  [Q-79](traceability/open-questions.md#q-79)
- Demo increments: [SL-26](traceability/increments.md#sl-26),
  [SL-28](traceability/increments.md#sl-28),
  [SL-42](traceability/increments.md#sl-42),
  [SL-47](traceability/increments.md#sl-47),
  [SL-51](traceability/increments.md#sl-51)
