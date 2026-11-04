# Component catalog

This catalog is the lowest zoom level of the building block view. It lists
every component of gbo-demo v0.9.0 with its responsibility and a link to
its code. Each block is either part of the target architecture or *demo
scaffolding*. Demo scaffolding makes the demo usable or observable.

To read the design from the top down, start at the
[overview](index.md). It shows GBO Basis and the channels that GBO Basis
feeds, and each block there zooms in to this catalog.

## All components in one view

```mermaid
graph TB
    subgraph CONSUMERS["Consumers (demo scaffolding)"]
        CONS["Consumer backend<br/>Hypotheek-BV, Installatie Register"]
        INTG[Integrator backend]
    end

    subgraph CONSENT["Consent chain (DvTP)"]
        PORTAL["Consent portal<br/>frontend + backend"]
        CREG[Consent register]
    end

    subgraph AUTHZ["Authorization chain"]
        PDP["OpenFTV PDP v0.1.0<br/>FTV GraphQL mapper + OPA/Rego"]
        POL["Policy set<br/>engine, consent PIP, five rules"]
        ADM["Admission register<br/>(Admission register)"]
    end

    subgraph FSCG["FSC group (per organization)"]
        DIR[Directory]
        MGR[Manager]
        OUT[Outway]
        IN["Inway (PEP)"]
        TXLOG[Txlog API]
    end

    subgraph SRC["Source holder (per source: BD, RvIG, LVG)"]
        SIDE["Source gateway<br/>(bron-sidecar)"]
        DEC[Decryption component]
        GQL[GraphQL source API]
        META["Source metadata<br/>/.well-known/gbo"]
    end

    subgraph EUDI["EUDI chain"]
        ADP[EUDI adapter]
        ISS["Issuance server<br/>(nl-wallet)"]
        REC[Source reconciler]
    end

    REG[("Source registry<br/>PostgreSQL")]

    subgraph ASI["ASI chain"]
        ASIP[ASIP]
        AZSP[ASI authorization server]
        WV[Wallet verifier]
    end

    subgraph AUDIT["Audit records"]
        ADL[("ADL<br/>decision records")]
        LDV[("LDV logbooks<br/>per controller")]
    end

    BSNK["BSNk PP<br/>(mock /v2)"]

    CONS --> OUT
    INTG -->|delegated grant| OUT
    PORTAL --> CREG
    PORTAL -->|consent time only| BSNK
    OUT --> IN
    IN -->|AuthZEN| PDP
    MGR -->|AuthZEN contract decision| PDP
    PDP --- POL
    PDP -.->|PIP pull| ADM
    PDP -->|JWKS| CREG
    PDP -->|status over FSC| CREG
    PDP --> ADL
    IN --> SIDE
    SIDE --> DEC
    SIDE --> GQL
    ISS --> ADP
    ADP --> OUT
    REC -->|over FSC| META
    REC --> REG
    ADP --> REG
    ASIP -->|reader role| REG
    ASIP -->|own Outway| OUT
    ASIP -.->|keys via metadata| AZSP
    AZSP --> WV
    SIDE -.-> LDV
    CREG -.-> LDV

--8<-- "mermaid/classes.mmd"
    class CONS,INTG mock
    class PORTAL,CREG dvtp
    class PDP,POL,DIR,MGR,OUT,IN,SIDE,DEC basis
    class ADM,REG,ADL,LDV,TXLOG store
    class GQL,META source
    class ADP,ISS,REC,ASIP,AZSP,WV eudi
    class BSNK ext
```

The demo implements three routes end to end: the DvTP query under
consent, EUDI issuance, and ASI verification for QTSPs. The SDG-OOTS
adapter has no implementation and is not in this view
([ADR-0020](../decisions/0020-as4-bridge-for-oots.md)). The QTSP and the
Discover Interface are external roles. The [context view](../context.md)
shows them.

The status lookup is one edge in the diagram. It runs from the PDP's own
Outway to the register's Inway, as the FSC service `consent-status`. The
dotted LDV edges stand for every component that writes processing records
([Level 2: logging and audit](#level-2-logging-and-audit)).

## Level 2: authorization chain

The authorization chain has the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| OpenFTV PDP | Decides every data request and every FSC contract submission. The build uses OpenFTV tag `v0.1.0` and patches in the GBO FTV GraphQL mapper. If a patch step changes nothing, the build fails. The PDP offers AuthZEN 1.0 at `POST /authzen/v1/evaluation` over HTTPS. It writes one ADL record per evaluation. It does not start without the ADL database. | [services/openftv-pdp](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/openftv-pdp), [Dockerfile](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/Dockerfile#L9) |
| FTV GraphQL mapper | Implements the mapping function of the FTV GraphQL profile (`ftv-graphql/0.1`). It parses the raw body and resolves parent types from the bundled schema of the FSC service in the access token. It returns the field list with arguments as the source executes them, or `COVERAGE_UNVERIFIABLE` with a subcode. It accepts only queries. For any other operation it returns `OPERATION_NOT_SUPPORTED`. It applies fixed limits: body 1 MiB, depth 64, and 1000 field records. It verifies no token, reads no flow, and calls no external service. | [services/ftv-graphql-mapper](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/ftv-graphql-mapper), [limits](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper.go#L252-L268), [OpenFTV adapter](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go) |
| Bundled schemas and pins | One directive-free schema per FSC service (`bri`, `brp`, `lvg`). The policy bundle pins the digest of each schema. The policy denies an evaluation against another schema (`SCHEMA_MISMATCH`). A CI job compares the bundled schemas with the source schemas. | [schemas/pdp-mirror](https://github.com/ICTU/GBO-demo/tree/v0.9.0/schemas/pdp-mirror), [graphql_schemas.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/graphql_schemas.rego), [check-schema-drift.sh](https://github.com/ICTU/GBO-demo/blob/v0.9.0/scripts/check-schema-drift.sh) |
| Policy entrypoint | Allows the source-metadata fetch for two known peers, on the two metadata services only. It sends every other request to the rule engine. It passes only `allow` and the consumer's reason code to OpenFTV. | [policies/authz.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/authz.rego) |
| Rule engine | Selects the regime from the evidence. If the request carries a consent token, the regime is consent. Without a token, the regime is PID. The engine binds a field to the rules of that regime that serve the FSC service and name the field key. It denies a field that no rule covers (`NO_APPLICABLE_RULE`). The first bound rule without a reason grants the field. The engine checks the integrator mandate on every delegated call. It returns a coarse reason code to the consumer and keeps the per-field codes for the operator. | [policies/gbo/engine.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L173-L192) |
| Request reader | Reads the field list, the arguments, the caller, the represented party, and the time from the input. It does no checks. | [policies/gbo/lib.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego) |
| Consent PIP | Verifies the consent token in policy: ES256 signature, issuer, audience, type, validity with 30 s skew, and required claims. It fetches the JWKS directly from the register and caches it for 300 s. It fetches the status for each evaluation over FSC, through the PDP's Outway. The status fetch has no cache and a 2 s timeout. Every failure has its own reason code. The engine copies the resolved consent into its response. | [policies/gbo/consent.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego) |
| Authorization rules | Five plain-Rego rules, listed in the next table. Each rule names its regime, its FSC services, and its fields. It also states its own reasons to deny. | [policies/gbo/rules](https://github.com/ICTU/GBO-demo/tree/v0.9.0/policies/gbo/rules) |
| Contract acceptance policy | Decides whether a provider's FSC Manager signs a submitted contract. It accepts grant types service connection and delegated service connection. It applies eight ordered refusal codes, from `NOT_AN_AUTOSIGN_REQUEST` to `DELEGATION_NOT_REGISTERED`. It keeps a missing register (`ADMISSION_REGISTER_UNAVAILABLE`) apart from a missing entry (`PARTY_NOT_IN_REGISTRY`). | [policies/fsc/autosign.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L167-L174) |
| Admission register | Holds the admitted participants: source holders (bronhouders), GBO system participants (EDI issuer, PDP, ASIP), and consumers. Each entry has `active` and `allowed_source_peer_ids`. The register also holds integrator mandates (`integrations`) and serves them as `acts_for`. OpenFTV pulls it every 5 s over a network that only the PDP shares. The register deactivates an entry and never deletes it. It keeps no change log ([REQ-123](../requirements/admission.md#req-123)). It is a SQLite database with an admin UI. | [services/dvtp-onboarding-register](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/dvtp-onboarding-register), [PIP pull](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml) |

The PID regime has no positive evidence of its own. A request without a
consent token enters it ([F-70](../traceability/findings.md#f-70)). For this
reason, the PID rules admit only named actors. These actor lists must stay
apart from the consent consumers. The five rules grant these fields:

| Rule | Regime | Services | What it grants | Own deny reasons | File |
|---|---|---|---|---|---|
| DVT0001 | consent | `bri` | Income declaration fields under consent | consent codes, `SCOPE_NOT_ALLOWED`, `CONSTRAINT_MISMATCH`, `YEAR_NOT_COVERED` | [dvt0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego) |
| LVG0001 | consent | `lvg` | Ownership check at LVG, scope `lvg:vbo:eigendom` | consent codes, `SCOPE_NOT_ALLOWED`, `CONSTRAINT_MISMATCH` | [lvg0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/lvg0001.rego) |
| EUD0001 | pid | `bri` | Inkomensverklaring to the wallet, years 2024 and 2025 | `PID_NOT_PRESENT`, `ACTOR_NOT_ALLOWED`, `YEAR_NOT_ALLOWED` | [eud0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0001.rego) |
| EUD0002 | pid | `brp` | Akte van overlijden to the wallet | `PID_NOT_PRESENT`, `ACTOR_NOT_ALLOWED` | [eud0002.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0002.rego) |
| ASI0001 | pid | `brp` | BRP fields behind the ASI attributes, for the ASIP peer `…1200` only | `PID_NOT_PRESENT`, `ACTOR_NOT_ALLOWED` | [asi0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego) |

The EUDI rules share one actor list, `designated_issuers`
([eudi_helper.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eudi_helper.rego#L16-L20)).
The consent rules share the consent checks in
[dvtp_helper.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvtp_helper.rego).

### Rule shape

A rule is plain Rego. It declares what it covers and states its reasons to
deny. If a rule has no deny reason for a field, it grants that field.
`box2Inkomen` and `box3Inkomen` are not in `covers_fields`, so the engine
denies them under consent. This excerpt from
[DVT0001](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L13-L80)
shows the shape of a rule:

```rego
rule_id := "DVT0001"
regime := "consent"
services := {"bri"}

covers_types := {"Bedrag"}
covers_fields := {
	"Query.ingeschrevenPersoon",
	"IngeschrevenPersoon.heeftBelastingjaarAangifte",
	"AangifteIH.verzamelinkomen",
	"AangifteIH.box1Inkomen",
	# ... scalar fields of the declaration
}

deny contains helper.consent_invalid_reason if not helper.consent_verified
deny contains "CONSENT_WITHDRAWN" if not helper.consent_active
deny contains "CONSENT_ACTOR_MISMATCH" if not helper.consent_given_to_caller
deny contains "SCOPE_NOT_ALLOWED" if not income_scope_granted

# The subject must be the identity placeholder, not a literal BSN.
deny_field[i] contains "CONSTRAINT_MISMATCH" if {
	some i, f in lib.fields
	lib.key(f) == "Query.ingeschrevenPersoon"
	not helper.names_consent_citizen(f, "bsn", {lib.identity_placeholder})
}
```

[Authorization](../concepts/authorization.md) explains regime selection, rule
binding, and the two layers of reason codes. The decisions are in
[ADR-0002](../decisions/0002-opa-rego-authzen.md),
[ADR-0009](../decisions/0009-closed-world-rules.md),
[ADR-0013](../decisions/0013-pdp-request-mapper.md),
[ADR-0015](../decisions/0015-contract-acceptance-by-policy.md), and
[ADR-0031](../decisions/0031-regime-from-evidence.md).

## Level 2: consent chain

The consent chain has the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| Consent portal (toestemmingsportaal) frontend | The citizen UI. It has a DigiD login (mock), one toggle per data set, a consent overview, and revocation. It shows only the requested data sets and refuses a data set that it cannot describe. It checks the return origin against an allowlist. It returns the consent proof in the URL fragment, or `status=denied`. | [toestemmingsportaal-frontend](https://github.com/ICTU/GBO-demo/tree/v0.9.0/toestemmingsportaal-frontend) |
| Consent portal backend | Keeps the BSN away from the register and the consumer. The type system enforces this boundary, and the backend never sends a BSN to the register. It derives `subject_ref` as a keyed HMAC of the BSN, with a key version. It activates a citizen at BSNk once and stores PI and PP in the register. At each consent, it reads the BSN authorization list and has BSNk transform the values. Every configured source gets a VP. Only a source on the list also gets a VI. | [services/consent-portal-backend](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/consent-portal-backend), [portal.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go), [subjectref.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/subjectref.go) |
| Consent register (toestemmingsregister) | Stores consent records: `subject_ref`, consumer, scopes, scope entries per source, purpose (`use_case`), validity, and status. It also stores the portal's PI and PP per `subject_ref` (route D, [ADR-0040](../decisions/0040-route-d-citizen-recognition.md)). It stores no BSN, no VI, and no VP. It signs the consent proof and serves the JWKS. A separate listener serves only the status, published as the FSC service `consent-status`. By default, the register keeps its data in memory. If it uses Postgres, it requires a persistent signing key. | [services/consent-register](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/consent-register), [status.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status.go), [polymorphic.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/polymorphic.go) |
| Consent proof | ES256 JWT, type `gbo-consent+jwt`. Claims: `consent_id`, `encrypted_subject`, `scopes`, `scope_entries`, `dienstverlener_oin`, `valid_until` (equal to `exp`), `iss`, `aud`, `iat`, `nbf`, `jti`. `encrypted_subject` holds a `pseudonym` per source OIN. For a source on the BSN authorization list, it also holds an `identity`. Each value has a `key_set_version`. `dienstverlener_oin` holds the consumer's FSC Peer ID ([Q-68](../traceability/open-questions.md#q-68)). The PDP denies a token in the old form with `pi`. | [consent_token.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/consent_token.go#L22-L80) |

The consumer holds no citizen identifier. Its query names the subject with
the placeholder `consent:identity` or `consent:pseudonym`. The source
gateway replaces the placeholder after the allow decision (see the next
section).
[Consent](../concepts/consent.md) explains the record and its lifecycle.
[Pseudonymization](../concepts/pseudonymization.md) explains the values. The
decision is [ADR-0032](../decisions/0032-consent-proof.md).

## Level 2: source holder {#level-2-bronhouder}

The source holder runs the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| GraphQL source API | The query endpoint of the source. Sources identify a citizen by BSN. The demo has three sources. Service `bri` is a Belastingdienst profile with income declarations per year. Service `brp` is a BRP profile with the persoonslijst and the akte van overlijden view. Service `lvg` is an LVG mock for the LVG pilot (`vbo(bsn, vboId) { vboId }`). | [graphql-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/graphql-server), [brp-graphql-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/brp-graphql-server), [lvg-graphql-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/lvg-graphql-server) |
| Source gateway (bron-sidecar) | Source-owned gateway between the Inway and the API, one instance per source. Its behavior depends on the presence of a consent token. With a token, it takes the value for its own OIN from `encrypted_subject` and has the decryption component read it. It checks that the value names its own OIN. Then it replaces the placeholder. It refuses a literal subject under a token. Without a token, it passes the request through. It accepts only the transport shape the PDP judged: `POST`, one path, no query string. | [services/bron-sidecar](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/bron-sidecar), [substitution](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution.go), [transport.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/transport.go) |
| Decryption component | Reads a VI or VP with the source's own keys. It calls no other service, so there is no BSNk call at query time. The demo uses the `bsnk-mock` image with only the decryption endpoints. The three demo sources share one instance and one OIN. Production needs one instance per source. | [decryption.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/decryption/decryption.go), [bsnk-mock README](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bsnk-mock/README.md) |
| Source metadata endpoint | Serves the source-owned description at `/.well-known/gbo` over a separate FSC metadata service. | [source_metadata.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/source_metadata.go), [BD document](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/config/gbo-source-metadata.json) |

Only the source Inways can reach the source gateway. Because of this
network isolation, every request at the gateway comes after a PDP
decision. For this reason, the gateway does not verify the token again
([ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md),
[F-79](../traceability/findings.md#f-79)). The
[deployment view](../deployment.md#deployment-units-and-network-zones) shows the
networks.

### Source metadata document

A source describes its own products in one JSON document. It serves the
document at `/.well-known/gbo`. For a source without an endpoint, an
operator supplies it through the `file` transport. GBO validates the
document against
[gbo-source-metadata-v1](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json)
(`urn:gov:nl:gbo:schema:gbo-source-metadata:1`).

GBO holds no catalog of sources, years, or schemas. This document is the
catalog, and the source owns it ([ADR-0016](../decisions/0016-source-owned-metadata.md)). The document
format is a proposal for the open PSA decision on S10.

The document has the following fields:

| Field | Content |
|---|---|
| `schema_version` | `1.0` or `1.1`. Version 1.1 adds `capabilities.asi`. |
| `source_oin`, `version`, `issued_at`, `expires_at` | Envelope. `source_oin` must match the OIN in the certificate set. `version` must increase. GBO refuses a validity of less than one hour. |
| `capabilities.eudi` | `version` and `attestations[]`, one entry per attestation type. |
| `type_id`, `type_version` | Identity of the attestation type. With the source ID they form the VCT path `/types/{source-id}/{type-id}/v{n}`. |
| `offers[]` | Products a wallet can request: `id`, `label`, `description` and fixed `parameters` (for example `{"jaar": 2025}`). |
| `graphql` | The source-owned query plan: `service_reference` (the FSC data service), `endpoint`, `document` (exactly one read operation), `subject_variable`, typed `parameters`, and `result_pointer` (RFC 6901). |
| `mapping_profile` | `gbo-simple-v1` ([ADR-0017](../decisions/0017-gbo-simple-v1.md)). It applies to the `eudi` capability only. |
| `display` | Per language: `name`, `description`, a `summary` with `{{claim}}` placeholders, and `rendering`. |
| `claims` | Per claim: `source` (one gbo-simple-v1 rule: `pointer`, `datatype`, optional `optional`), `label`, optional `description`, and `sd` (`always` by default, `allowed` or `never`). The claim order is the display order in the wallet. |
| `capabilities.asi` | `version`, `authentic_source` (`legal_name`, `country`), a `graphql` block with one `...Selected` fragment, and `attributes[]`. Each attribute has an `identifier`, an optional type condition `on`, and `fields` built with `pointer`, `join`, `const` or `each` ([ADR-0039](../decisions/0039-asi-source-described-attributes.md)). |

GBO generates the SD-JWT VC Type Metadata from `display` and `claims`. It
publishes the Type Metadata immutably per version, with `vct#integrity`.
A change to `claims` or `display` therefore needs a new `type_version`. The
schema has no `unit`. The reconciler refuses reserved claim names (`vct`,
`iss`, `status`, `cnf`) and nested objects
([REQ-78](../requirements/eudi-issuance.md#req-78)).

The adapter puts the BSN from the PID into `$bsn` and the year of the offer
into `$jaar`. It reads the result at `result_pointer` and copies each
`source.pointer` into its claim. This shortened excerpt from the
[Belastingdienst document](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/config/gbo-source-metadata.json)
(version 2.4.0) shows how the query plan and the claims relate:

```json
{
  "type_id": "inkomensverklaring",
  "type_version": "2.4",
  "offers": [
    {"id": "inkomensverklaring_2025", "label": "Inkomensverklaring 2025",
     "description": "Inkomensverklaring over belastingjaar 2025",
     "parameters": {"jaar": 2025}}
  ],
  "graphql": {
    "service_reference": "bri",
    "endpoint": "/graphql",
    "document": "query Inkomensverklaring($bsn: BSN!, $jaar: Int!) { ... }",
    "subject_variable": "bsn",
    "parameters": {"jaar": {"type": "integer", "required": true}},
    "result_pointer": "/data/ingeschrevenPersoon/heeftBelastingjaarAangifte"
  },
  "mapping_profile": "gbo-simple-v1",
  "display": {
    "nl-NL": {"name": "Inkomensverklaring",
              "summary": "€{{verzamelinkomen}} ({{belastingjaar}})"}
  },
  "claims": {
    "belastingjaar": {"source": {"pointer": "/belastingjaar", "datatype": "gYear"},
                      "label": {"nl-NL": "Belastingjaar"}},
    "verzamelinkomen": {"source": {"pointer": "/verzamelinkomen/waarde", "datatype": "integer"},
                        "label": {"nl-NL": "Verzamelinkomen"}}
  }
}
```

The
[BRP document](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/config/gbo-source-metadata.json)
(version 2.6.0, schema 1.1) also publishes the `asi` capability. This
excerpt shows two of its attributes:

```json
{
  "version": "1.0",
  "authentic_source": {"legal_name": "Basisregistratie Personen (mock)", "country": "NL"},
  "graphql": {
    "service_reference": "brp",
    "endpoint": "/graphql",
    "document": "query Asi($bsn: BSN!) { ingeschrevenPersoon(bsn: $bsn) { ...Selected } }",
    "subject_variable": "bsn",
    "result_pointer": "/data/ingeschrevenPersoon"
  },
  "attributes": [
    {"identifier": "https://gbo.example/attributes/family_name/1",
     "fields": {"family_name": {"join": ["/voorvoegsel", "/geslachtsnaam"], "separator": " "}}},
    {"identifier": "https://gbo.example/attributes/nationality/1",
     "fields": {"nationalities": {"each": "/heeftNationaliteit", "pointer": "/nationaliteit"}}}
  ]
}
```

By design, the document leaves out three things:

- The GraphQL schema. The PDP keeps its own bundled copy. It authorizes
  the source's query plan field by field, like any other query.
- Access decisions. The EUD and ASI rules decide which fields a channel
  can receive. The mapping of the source has no part in that decision.
- The `value_schema` of an ASI attribute. GBO keeps it per attribute
  identifier in
  [schemas/asi-attributes.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json)
  until an EU catalog of attributes exists.

Provenance rests on the authenticated FSC transport and the OIN in the
certificate set. The source does not sign the document. The document also
has no reference to an LDV read API or a DCAT-AP-NL entry
([F-57](../traceability/findings.md#f-57), [AV-07](../requirements/admission.md#av-07)).

### Source configuration on the GBO side

The GBO configuration per source is small: one YAML file, named after the
`source_id`. The file names where the description comes from and how GBO
reaches the data. This is
[sources/configured/belastingdienst.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/sources/configured/belastingdienst.yaml):

```yaml
metadata_endpoint:
  transport: fsc
  provider_peer_id: "99999999900000000200"
  service_reference: gbo-metadata-bd
```

An optional `data_access` block (`transport`, `provider_peer_id`) gives the
data leg a different transport than the metadata leg. The `file` transport
is an exception for a source without its own endpoint. In that case, the
operator takes over the description. GBO does not record the agreement of
the source holder
([F-71](../traceability/findings.md#f-71), [AV-08](../requirements/admission.md#av-08)).

The legal identity of the source comes from the certificate set with the
same `source_id`. The OIN comes from the certificate's `serialNumber`, and
the name comes from its `O`. GBO refuses a configured value that differs
([REQ-67](../requirements/sources-identity.md#req-67)). The configuration holds
the FSC Peer ID apart from the OIN. The data service and the grant hash
come from the source document and the FSC contracts in force. They never
come from this file.

A valid FSC contract activates nothing. A source becomes active only after
three steps: it is configured, its candidate is valid, and an operator
promotes a release ([REQ-65](../requirements/sources-identity.md#req-65)). If
a precondition is missing, the reconciler reports
`METADATA_CONTRACT_NOT_FOUND`, `DATA_CONTRACT_NOT_FOUND`, or
`FSC_MANAGER_UNAVAILABLE`. [Source onboarding](../concepts/source-onboarding.md)
and [admission and activation](../runtime/admission.md) explain the lifecycle.

In demo v0.9.0, the RvIG source
([rvig.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/sources/configured/rvig.yaml))
uses the Belastingdienst peer `…0200` and the OIN of the Belastingdienst.
This is a demo shortcut. The demo therefore does not show one OIN per
source holder.

### Source schema and the PDP copy

The source owns its schema. The PDP holds a directive-free copy per FSC
service to resolve parent types. The year selector is in the query, so the
PDP can enforce consent per year. This excerpt from the
[BD copy](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/pdp-mirror/bd.graphql)
shows the DvTP part:

```graphql
type IngeschrevenPersoon {
  bsn: BSN!
  heeftBelastingjaarAangifte(belastingjaren: [Int!]): [BelastingjaarAangifte!]
}

type Query {
  ingeschrevenPersoon(bsn: BSN!): IngeschrevenPersoon
}
```

The BRP source adds a flat view for the akte van overlijden. The selection
of the deceased partner from the marriage history is a security-sensitive
invariant. The source holds this selection and its tests. The policy does
not contain it
([REQ-57](../requirements/eudi-issuance.md#req-57),
[F-47](../traceability/findings.md#f-47)). For the view, see the
[BRP copy](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/pdp-mirror/eudi/brp.graphql)
and
[EUD0002](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0002.rego):

```graphql
type Query {
  ingeschrevenPersoon(bsn: BSN!): IngeschrevenPersoon
  akteVanOverlijden(bsn: BSN!): [AkteVanOverlijden!]!
}
```

## Level 2: FSC group

The FSC group `fsc-demo` runs OpenFSC v2.4.0. The
[deployment view](../deployment.md#fsc-peers) lists the peers. The group has
the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| Directory | The registry of the group. It signs service publications automatically. It signs nothing else. | [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml) |
| Manager (per organization) | Issues access tokens for contracted connections. The token carries the signed `service_name`, which binds the PDP rules to a service. The provider Managers of BD, BRP, and the consent register decide contract acceptance through the PDP (AuthZEN autosign). | [bd-manager](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L701-L702) |
| Inway (per provider) | `bd-inway` and `brp-inway` are the PEP. Their AuthZEN plugin sends every request with its body to the PDP before the request reaches the source gateway. `cr-inway` has no AuthZEN hook. Behind `cr-inway`, the contract authorizes `consent-status`, and the register reads the calling peer from the `Fsc-Authorization` token. | [bd-inway](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L773-L775), [cr-inway](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L1117) |
| Outway (per consumer) | Opens mTLS connections to Inways under a grant hash. Grant links give each contracted service a path: `/bri`, `/brp`, `/lvg`, `/consent-status`. | [seed-bri-contract.sh](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/scripts/seed-bri-contract.sh) |
| Grants | Service-connection grants carry no properties. The demo removed `flow` in [PR #363](https://github.com/ICTU/GBO-demo/pull/363) and `subject_id_type` in [#473](https://github.com/ICTU/GBO-demo/issues/473). The regime follows from the evidence on the request ([ADR-0031](../decisions/0031-regime-from-evidence.md)). | [seed-bri-contract.sh](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/scripts/seed-bri-contract.sh#L60-L71) |
| Delegated grants | An integrator connects under a `DelegatedServiceConnectionGrant`. The integrator, the represented consumer and the provider sign it. The provider's Manager admits it only for a registered integration ([ADR-0034](../decisions/0034-integrator-delegation.md)). | [seed-bri-delegation-int.sh](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/scripts/seed-bri-delegation-int.sh) |
| Consent-status service | The register peer `…0700` publishes `consent-status`. The PDP peer `…0800` connects to it with grant link `/consent-status`. The register's Manager signs the connection only for peers in the admission register. | [fsc-seed-consent-status](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L647-L668) |
| ASIP peer | The ASIP peer `…1200` has an Outway only. It holds a contract for `brp` on `…0200` with grant link `/brp`. | [fsc-seed-asip](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L711-L729) |
| Txlog API (per peer) | Records each transport transaction (FSC-Logging). It is the authoritative transport record. The ADL records the decisions, and the LDV logbooks record the processings. | [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml) |

## Level 2: EUDI chain

The EUDI chain has the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| EUDI adapter | The bridge between the issuance server and the FSC chain. The issuance server calls `POST /attestations/{sourceID}/{typeID}`. The adapter takes the BSN from the disclosed PID and builds the query from the source's published `graphql` block. It calls the source through the EDI Outway with `Fsc-Grant-Hash` and `traceparent`. It projects the answer into claims through gbo-simple-v1. It writes two LDV records per issuance: one for the BSN read and one for the assembly of the attestation. It fetches source data per request and stores none ([REQ-11](../requirements/authorization.md#req-11)). | [services/eudi-adapter](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-adapter), [routes](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L65-L95), [ldv_issuance.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/ldv_issuance.go) |
| Adapter callback and public endpoints | The callback route has no caller authentication ([REQ-45](../requirements/eudi-issuance.md#req-45), [#133](https://github.com/ICTU/GBO-demo/issues/133)). The same listener serves `GET /eudi-offers.json` (the offer catalog for the frontends) and `GET /types/...` (Type Metadata). | [source_release_runtime.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L69-L95) |
| Issuance error contract | The adapter returns 400 for offer parameters outside the offer, or for a PID without a BSN. It returns 404 if there is no result. If a result does not fit the claims, it returns 502 with `GBO_SIMPLE_PATH_MISSING`, `GBO_SIMPLE_TYPE_MISMATCH`, `GBO_SIMPLE_RESULT_TYPE`, or `GBO_SIMPLE_RESULT_AMBIGUOUS`. It never issues a partial attestation ([REQ-116](../requirements/eudi-issuance.md#req-116)). | [internal/gbosimplev1](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-adapter/internal/gbosimplev1) |
| Issuance server | The nl-wallet issuance server (v0.5.0). It does OpenID4VP disclosure and OpenID4VCI issuance (`dc+sd-jwt`). It verifies the PID disclosure against `issuer_trust_anchors`. That list also holds non-PID anchors: the development issuer CA and the issuer CA of every source. An attestation is valid for 365 days. Each type has one status list ([REQ-77](../requirements/eudi-issuance.md#req-77)). A second use case, `qtsp-attestation`, issues the reference QTSP's test statement. An init step writes the server configuration from the active release. | [services/eudi-issuance-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-issuance-server), [issuance_config.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go), [qtsp_issuance.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/qtsp_issuance.go) |
| Source reconciler | Reconciles the configured sources to a desired state. It discovers the FSC contracts. It fetches the source document over FSC, or reads the file for the `file` transport. It validates the document, and it validates the `asi` capability against the attribute catalog. Then it writes candidates and statuses. Promotion creates an immutable release and activates it. The `--auto-promote` flag is for the demo only. | [reconcile_command.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go), [source_configuration.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go) |
| Source registry | A shared Go module with a PostgreSQL store. The store holds candidates, statuses, immutable releases (content-addressed by SHA-256), and one active-release pointer. It has a writer role and a read-only role. The readers are the adapter, the issuance init step, and the ASIP. The states are `pending`, `active`, `stale`, `blocked`, and `rollout_required`. A source is fresh for 15 min and then has a stale grace period of 1 h ([REQ-66](../requirements/sources-identity.md#req-66)). | [services/source-registry](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry), [source_metadata_cache.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata_cache.go#L10-L14) |
| Release runtime | Polls the active-release pointer in the adapter. If the release changes, it rebuilds the attestation bindings. If an error occurs, it keeps the previous snapshot. | [source_release_runtime.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go) |
| gbo-simple-v1 profile | A minimal mapping profile that fails closed. It maps one source object to flat claims through RFC 6901 pointers. It allows only scalar data types, with no conversions or expressions. | [profile](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-adapter/internal/gbosimplev1), [docs/gbo-simple-v1.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/gbo-simple-v1.md) |
| Certificate set (per source) | Issuer, reader, and status-list leaf certificates per source. Sources never share them. A separate privileged command mints the leaves under pre-provisioned CAs. It never mints a CA. Missing or incomplete material blocks only that source (`CERTIFICATE_SET_NOT_FOUND`, `CERTIFICATE_SET_INVALID`) ([REQ-58](../requirements/eudi-issuance.md#req-58)). | [development_ca_provider.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider.go) |

The issuance route runs under the PID regime: it carries no consent token.
The BSN from the PID is in the PDP input and in both decision logs
([REQ-60](../requirements/logging-audit.md#req-60),
[ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md)). The decision is
[ADR-0018](../decisions/0018-eudi-disclosure-issuance.md).

## Level 2: ASI chain

The ASI chain implements the Authentic Source Interface of ETSI TS 119 478,
clause 6.1 ([ADR-0037](../decisions/0037-asi-oauth-front-door.md)). The chain
is demo grade. It uses a stub register, development certificates, and a
DigiD mock. It has the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| ASIP | Offers clause 6.1.1 verify and 6.1.2 retrieve per data service at `/<ds>/authsrc-api`. It first verifies the DPoP-bound token. It takes the BSN only from the token ([REQ-87](../requirements/asi.md#req-87)). It derives one GraphQL query per request from the source's `asi` description and sends it through its own Outway ([REQ-92](../requirements/asi.md#req-92)). For each attribute, it answers `Match`, `NoMatch`, `MatchWithVariation`, or `Unknown`. It never returns a source value ([REQ-85](../requirements/asi.md#req-85)). It seals every 200 response with a detached JWS in `X-JWS-Signature` ([REQ-83](../requirements/asi.md#req-83)). | [services/asi-provider](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-provider), [seal.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/seal/seal.go) |
| Data services | One per authentic source, each with its own base URL, contract, discovery records and token audience ([ADR-0038](../decisions/0038-asi-data-service-per-source.md)). The demo has one: `brp`, source `rvig`. | [config/dataservices.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/config/dataservices.json) |
| Source description (`asi` capability) | The source maps its fields onto GBO attribute identifiers. The ASIP reads the active release every 5 s with the reader role. If no current description is available, the data service answers 503. | [services/asi-mapping](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-mapping), [services/source-registry](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry), [schemas/asi-attributes.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json) |
| Authorization server | Clause 6.1.3. It registers a QTSP with RFC 7591 and a software statement sealed by the QTSP certificate. It verifies the chain and the entitlement `QEAA_Provider` in the register ([REQ-88](../requirements/asi.md#req-88)). It checks the entitlement again every hour ([REQ-89](../requirements/asi.md#req-89)). It runs the code flow with PKCE S256 and `private_key_jwt`. It issues DPoP-bound RFC 9068 tokens (10 min) for exactly one `resource` ([REQ-95](../requirements/asi.md#req-95)). The request page shows who asks for which data at which source ([REQ-91](../requirements/asi.md#req-91)). The login is the approval ([REQ-90](../requirements/asi.md#req-90)). The token carries the BSN and `acr`/`amr` ([REQ-86](../requirements/asi.md#req-86)). | [services/asi-authorization-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server) |
| Register stub | Stands in for the national register of relying parties. The server reads it at every lookup. | [testdata/register.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/testdata/register.json) |
| Wallet verifier | The nl-wallet `verification_server` (v0.5.0). It runs the OpenID4VP PID disclosure for the authorization server (use case `asi-login`, BSN required, [REQ-102](../requirements/asi.md#req-102)). As a demo shortcut it also serves the reference QTSP (`qtsp-login`, no BSN). | [services/asi-wallet-verifier](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-wallet-verifier) |
| DigiD mock (ASI) | A stub means of identification. It accepts nine digits and returns only a BSN. | [internal/digidmock](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server/internal/digidmock) |
| Rule ASI0001 | Grants the ASIP peer the BRP fields behind the attributes, on `brp` only. It does not verify the token or the QTSP. | [asi0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego) |
| Discover Interface (stub) | External role. It answers `retrieve` from the ASIP's `dataService` records ([REQ-99](../requirements/asi.md#req-99)). For `search`, it returns 501. | [services/asi-discovery-stub](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-discovery-stub) |
| Reference QTSP | External role, demo scaffolding. It discovers, registers, gets a token, verifies or retrieves, and accepts a result only with a valid seal. Then it issues a test statement, marked "not qualified", to the wallet. | [services/qtsp-reference](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/qtsp-reference) |
| Conformance matrix | Gives each ETSI requirement ID a status and named tests. If an ID or a test is missing, a CI job fails. | [conformance](https://github.com/ICTU/GBO-demo/tree/v0.9.0/conformance) |

### Trust boundary

The QTSP is not an FSC participant
([F-87](../traceability/findings.md#f-87)). It is an OAuth client of the
authorization server. Its certificate and its register entitlement admit
it. It has no FSC contract.

The ASIP is an FSC consumer peer of its own. For the PDP, the actor is the
ASIP, never the QTSP or the citizen. The ASIP passes nothing about the
QTSP into the chain. In demo v0.9.0, the ASIP writes no LDV records.

[ASI verification](../runtime/asi-verification.md) shows the flow. The
[ASI requirements](../requirements/asi.md#asi-profile) give the profile per
ETSI clause.

## Level 2: logging and audit

GBO keeps three authoritative records, one per Logius standard
([ADR-0036](../decisions/0036-adl-decision-record.md),
[ADR-0026](../decisions/0026-ldv-integration.md)). One W3C trace ID joins
them. The records store the FSC transaction ID next to it
([ADR-0035](../decisions/0035-w3c-trace-context.md)).
[Logging](../concepts/logging.md) explains the model. The logging and audit
chain has the following components:

| Component | Responsibility | Implementation |
|---|---|---|
| Authorization Decision Log (ADL) | The authoritative record of each PDP decision, contract decisions included. OpenFTV writes it to Postgres `ftv_adl`. Readers get a SELECT-only role. It holds the request and `{allow, reason}`. It has no policy version ([REQ-59](../requirements/logging-audit.md#req-59)) and no consent-status answer ([F-72](../traceability/findings.md#f-72)). For decisions behind the Inway, it has no trace ID and no transaction ID ([#369](https://github.com/ICTU/GBO-demo/issues/369)). | [docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L117-L125), [adl-reader.sql](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/adl/adl-reader.sql) |
| LDV logbook | Demo stand-in for the logbook of each controller (Verantwoordelijke), one instance per controller. It accepts one record per processing (`POST /logboek/records`) and serves the read extension (`POST /data-processing-operations`). It keeps a versioned stand-in register of processing activities. It refuses any record with an elfproef-valid run of nine digits. It uses SQLite with `synchronous = FULL`. Write and read take separate tokens. | [services/ldv-logboek](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/ldv-logboek) |
| LDV client | A shared Go module. In production, GBO ships this module to chain participants. It does not ship the logbook. The client takes the trace from `traceparent`. It writes records and waits for the logbook to acknowledge them. It derives the subject in the controller's own pseudonym space. It sets `nextLogbookId` on outbound calls. A local durable outbox stores each record before delivery. As a result, a logbook outage delays records but does not fail requests. | [services/ldv-client](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/ldv-client), [outbox.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/outbox.go) |
| FSC txlog | Authoritative transport record per peer (see FSC group). | [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml) |
| Observability stack | OpenTelemetry collector, Jaeger, Promtail, Loki and Grafana. The engine's console decision log goes to Loki. These stores are for debugging only. They have no audit function. | [otel/collector-config.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/otel/collector-config.yaml), [OBSERVABILITY.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/OBSERVABILITY.md) |

The demo runs seven logbooks. Each controller logs its own processings
([REQ-72](../requirements/logging-audit.md#req-72)):

| Logbook | Controller | Writers |
|---|---|---|
| `logboek-bd` | Belastingdienst | `graphql-server`, `bron-sidecar` |
| `logboek-brp` | RvIG | `brp-graphql-server`, `brp-sidecar` |
| `logboek-lvg` | LVG | `lvg-graphql-server`, `lvg-sidecar` |
| `logboek-toestemming` | GBO consent facility (toestemmingsvoorziening) | `consent-register`, `consent-portal-backend` |
| `logboek-eudi-adapter` | GBO issuance facility | `eudi-adapter` |
| `logboek-afnemer` | Hypotheek-BV (consumer) | `dienstverlener-backend`, `integrator-backend` |
| `logboek-ir` | Installatie Register (consumer) | `ir-backend` |

The register logs each status lookup with the verified FSC peer of the PDP
as processor ([REQ-76](../requirements/consent.md#req-76)). The ASIP writes no
records. The consumer logbooks follow candidate condition
[AV-02](../requirements/admission.md#av-02).

## Level 2: shared services and mocks

The demo has the following shared services and mocks:

| Component | Responsibility | Implementation |
|---|---|---|
| BSNk PP mock | Follows the BSNk interface as JSON instead of SOAP: `/v2/activate`, `/v2/transform`, `/v2/provide-dv-keys`, `/v2/bsn-authorisation-list`, and `/v2/scheme-keys`. It enforces the rules of BSNk. A PI or PP belongs to its requester. A transformation has at most four parties. Only a party on the BSN authorization list gets an identity. It does not encrypt: anyone who holds a value can read it. Only the portal backend calls it, at consent time. | [services/bsnk-mock](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/bsnk-mock), [README](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bsnk-mock/README.md) |
| DigiD mocks | The consent portal has a DigiD login page. The user types a test BSN, and the portal backend signs a portal token with it. The ASI authorization server has its own stub (see the ASI chain). Demo scaffolding. | [DigiDAuth.tsx](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/DigiDAuth.tsx), [portalhttp](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/consent-portal-backend/portalhttp) |
| Consumer backend and frontend | Mock consumer Hypotheek-BV (peer `…0300`). It starts the consent flow, receives the proof and sends the DvTP query with the placeholder. `QUERY_KIND` selects the source (`bd` or `lvg`) and its placeholder. It writes its own LDV records. Demo scaffolding. | [services/dienstverlener-backend](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/dienstverlener-backend), [dienstverlener-mock](https://github.com/ICTU/GBO-demo/tree/v0.9.0/dienstverlener-mock) |
| Installatie Register (LVG pilot) | `keyper-mock` is the IR/Keyper frontend. It has the installer request, the owner approval, and the installer data. `ir-backend` is the consumer backend with `QUERY_KIND=lvg` on its own peer `…1000`. Under one consent, IR calls LVG again at each installer access. IR holds the second consent (citizen to installer). GBO does not hold it. Demo scaffolding. | [keyper-mock](https://github.com/ICTU/GBO-demo/tree/v0.9.0/keyper-mock), [docs/lvg-ir.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/lvg-ir.md) |
| Integrator backend | Consumer backend on the integrator peer `…1100`. It calls `bri` for Hypotheek-BV under a delegated grant. It is opt-in: run `make demo-integrator`. Demo scaffolding. | [docs/integrator.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/integrator.md) |
| Developer portal and backend | A cockpit for engineers. It shows the live flow from the trace event stream and a scenario library. It shows the ADL decision next to the engine detail, the LDV chain, the FSC txlogs, and an ASI tab. Rule metadata comes from a generated `rules.json`. Demo scaffolding. | [developer-portal](https://github.com/ICTU/GBO-demo/tree/v0.9.0/developer-portal), [services/dev-portal-backend](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/dev-portal-backend) |
| OpenFTV Manager, UI, Keycloak | Opt-in policy administration point. It keeps the policies in Postgres and makes a tagged bundle that the PDP pulls. For more information, see [policy lifecycle](../concepts/policy-lifecycle.md). | [services/openftv-manager](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/openftv-manager), [services/openftv-manager-ui](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/openftv-manager-ui) |
| Landing page | Public explainer with links to the demo UIs. Demo scaffolding. | [landing-page](https://github.com/ICTU/GBO-demo/tree/v0.9.0/landing-page) |

The demo removed the old sector PIP
([#378](https://github.com/ICTU/GBO-demo/issues/378)). Admission runs
through the admission register and the contract decision. The decision in
[ADR-0022](../decisions/0022-sector-grants.md) is deferred.

## Traceability

- Requirements: [REQ-04](../requirements/authorization.md#req-04),
  [REQ-11](../requirements/authorization.md#req-11),
  [REQ-17](../requirements/authorization.md#req-17),
  [REQ-21](../requirements/pseudonymization.md#req-21),
  [REQ-42](../requirements/authorization.md#req-42),
  [REQ-45](../requirements/eudi-issuance.md#req-45),
  [REQ-48](../requirements/authorization.md#req-48),
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-61](../requirements/admission.md#req-61),
  [REQ-62](../requirements/admission.md#req-62),
  [REQ-64](../requirements/sources-identity.md#req-64),
  [REQ-65](../requirements/sources-identity.md#req-65),
  [REQ-66](../requirements/sources-identity.md#req-66),
  [REQ-67](../requirements/sources-identity.md#req-67),
  [REQ-68](../requirements/consent.md#req-68),
  [REQ-69](../requirements/pseudonymization.md#req-69),
  [REQ-71](../requirements/logging-audit.md#req-71),
  [REQ-72](../requirements/logging-audit.md#req-72),
  [REQ-74](../requirements/authorization.md#req-74),
  [REQ-79](../requirements/pseudonymization.md#req-79),
  [REQ-80](../requirements/pseudonymization.md#req-80),
  [REQ-81](../requirements/pseudonymization.md#req-81),
  [REQ-83](../requirements/asi.md#req-83),
  [REQ-86](../requirements/asi.md#req-86) to [REQ-92](../requirements/asi.md#req-92),
  [REQ-97](../requirements/authorization.md#req-97),
  [REQ-106](../requirements/consent.md#req-106),
  [REQ-116](../requirements/eudi-issuance.md#req-116),
  [REQ-123](../requirements/admission.md#req-123)
- Findings: [F-47](../traceability/findings.md#f-47) (open),
  [F-57](../traceability/findings.md#f-57) (open),
  [F-70](../traceability/findings.md#f-70) (open),
  [F-71](../traceability/findings.md#f-71) (open),
  [F-72](../traceability/findings.md#f-72) (open),
  [F-79](../traceability/findings.md#f-79) (open),
  [F-87](../traceability/findings.md#f-87) (open),
  [F-90](../traceability/findings-closed.md#f-90) (resolved in demo)
- Open questions: [Q-34](../traceability/open-questions.md#q-34),
  [Q-38](../traceability/open-questions.md#q-38),
  [Q-68](../traceability/open-questions.md#q-68)
- Demo increments: [SL-11](../traceability/increments.md#sl-11),
  [SL-16](../traceability/increments.md#sl-16),
  [SL-22](../traceability/increments.md#sl-22),
  [SL-28](../traceability/increments.md#sl-28),
  [SL-44](../traceability/increments.md#sl-44),
  [SL-45](../traceability/increments.md#sl-45),
  [SL-46](../traceability/increments.md#sl-46),
  [SL-47](../traceability/increments.md#sl-47),
  [SL-50](../traceability/increments.md#sl-50),
  [SL-51](../traceability/increments.md#sl-51)
