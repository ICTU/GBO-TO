# Source onboarding

A GBO component must know, for each source, which data service to call,
with which query, and what to do with the answer. That knowledge comes
from the source itself, and GBO takes a source into use in a fixed set of
steps. The decisions are
[ADR-0016](../decisions/0016-source-owned-metadata.md) (mechanism),
[ADR-0017](../decisions/0017-gbo-simple-v1.md) (mapping profile for
attestations), and
[ADR-0039](../decisions/0039-asi-source-described-attributes.md)
(attributes for the ASIP). For the requirements, see
[Source metadata and activation](../requirements/sources-identity.md#source-metadata).
For the components, see the [building block view](../building-blocks/components.md).
For the step-by-step flow, see
[Admission and activation](../runtime/admission.md).

The behavior on this page is the behavior of gbo-demo v0.9.0
([docs/source-onboarding.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/source-onboarding.md),
[docs/source-metadata-cache.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/source-metadata-cache.md)).

## Why the source owns its description

The bronhouder keeps control of its data
([P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). It
can add services through its source-specific GBO configuration
([S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)).
Central GBO facilities read the part of this configuration that they
need. They read it in machine-readable form, validated and versioned
([S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus)).

As a result, a GBO component takes the service description of a source
only from what the source publishes itself
([REQ-64](../requirements/sources-identity.md#req-64),
[F-57](../traceability/findings.md#f-57)):

- The component does not keep the description, add to it, or carry it per
  source in code.
- A new service or attestation type needs no code change in GBO.
- The source does not publish its GraphQL schema. It publishes the queries
  and mappings that it takes responsibility for.

Before this mechanism, every new source, attestation type, or tax year
was a change in GBO code or in a GBO catalog file. With this mechanism,
the adapter parameters come from the source
([Q-19](../traceability/answered-questions.md#q-19)). In GO terms, the
document is the service catalog that the bronhouder manages. The
validation rules of the reconciler are the common profile.

The mechanism (publish, validate, activate, roll back) is a GBO design
decision. The document format `gbo-source-metadata-v1` is the proposal of
the demo for the open PSA S10 decision. It is not a final interface
agreement.

Three inputs together describe a source. Each input has a different
owner:

| Item | Owner | Where |
|---|---|---|
| `source_id`, transport, metadata location, FSC Peer ID | GBO operator | source configuration file (`sources/configured/<source_id>.yaml`) |
| Legal OIN, organization name, issuer name and logo | bronhouder, through its certificate | certificate set under the key `source_id` ([Identity and trust](identity-trust.md)) |
| Access to the metadata and data services | bronhouder and GBO, by agreement | FSC contracts and grant hashes |
| Data service, query, parameters, offers, display, claims, attributes | bronhouder | the source document at `/.well-known/gbo` |
| Shape of an ASI attribute value (`value_schema`) | GBO, until the EU catalog of attributes exists | [`schemas/asi-attributes.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json) |
| SD-JWT VC Type Metadata | GBO generates it from the document | Source Registry |
| Candidates, states, releases, active pointer | GBO | Source Registry (PostgreSQL) |

## Lifecycle

```mermaid
flowchart LR
    A[1 Configure<br/>source file] --> B[2 Discover<br/>FSC contracts]
    B --> C[3 Fetch or read<br/>the document]
    C --> D[4 Validate]
    D --> E[5 Candidate<br/>rollout_required]
    E --> F[6 Promote]
    F --> G[7 Immutable<br/>release]
    G --> H[8 Active<br/>pointer]
    H --> I[9 Runtime<br/>reload]
    D -- invalid --> X[source stale<br/>or blocked]

--8<-- "mermaid/classes.mmd"
    class A,B,C,D,E,F,I,X basis
    class G,H store
```

Onboarding goes through nine steps:

1. Configure: the operator adds one file per source in
   `sources/configured/`. The file name is the stable `source_id`. The file
   names the transport, the location of the metadata, and the FSC Peer ID
   of the provider
   ([`source_configuration.go#L16-L28`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go#L16-L28)).
   It does not name the OIN or the organization name. These come from the
   certificate set.
2. Discover the contracts: for the `fsc` transport, the reconciler looks
   in the existing FSC contracts. There it finds the metadata contract and
   the data contract of the configured peer. It does not discover sources: a contract
   without a source file activates nothing.
3. Fetch or read: only the reconciler fetches source metadata. It uses
   `ETag` and `If-None-Match`. A `304` only extends freshness. The
   reconciler validates every `200` in full. The runtime never fetches
   metadata.
4. Validate: the reconciler validates schema, origin, version, validity
   window, query, mapping, offers, claims, and the binding to the data
   contract. The `source_oin` in the document must equal the OIN in the
   certificate set
   ([`source-registry/onboarding/service.go#L403-L413`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L403-L413)).
5. Candidate: a valid result becomes a complete candidate with state
   `rollout_required`. This candidate is not active. An invalid result
   does not replace the last complete candidate.
6. Promote: an operator promotes a complete candidate set. In the demo,
   the reconciler can do this itself (`--auto-promote`). Promotion is a
   separate step
   ([`reconcile_command.go#L134-L151`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go#L134-L151)).
7. Immutable release: promotion writes one release from the complete
   candidate set. The SHA-256 of the content identifies the release. A
   release never changes
   ([`postgresregistry/store.go#L300-L390`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/postgresregistry/store.go#L300-L390)).
8. Active pointer: in the same database transaction, promotion sets the
   singleton `active_release_id`. If a promotion fails, the previous
   release stays active.
9. Runtime reload: the readers poll the active pointer with a read-only
   role. They build the new release in memory and swap it atomically. The
   nl-wallet issuance server reads its configuration only at startup. So a
   new release needs a controlled restart of that server.

Four readers use the active release:

| Reader | What it derives | Reload |
|---|---|---|
| EUDI adapter | source snapshot (source, query, mapping, FSC grant, validity window), Type Metadata, offer catalog `/eudi-offers.json` | live, by polling |
| Issuance init container | `issuance_server.toml`: offers, disclosure, certificates, trust anchors | at a restart of the issuance server |
| ASIP | per data service: query, attribute mapping, legal name of the authentic source, discovery records | live, every 5 seconds ([`asi-provider/main.go#L101`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L101)) |
| Developer portal and landing page | the offers that a citizen can start, from the adapter | live |

The Source Registry is a shared module,
[`services/source-registry`](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry)
(`onboarding`, `postgresregistry`, `asisnapshot`). The reconciler writes to
it with the writer role. The adapter, the issuance init container, and the
ASIP read it with the reader role. The reconciler has no Kubernetes API
rights. It reads certificates and contracts and writes only to the
registry.

## Transports

A source has two legs: the metadata leg and the data leg. Each leg selects
its own transport
([`service.go#L18-L28`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L18-L28)):

| Transport | Metadata leg | Data leg | Authenticated |
|---|---|---|---|
| `fsc` | fixed path `/.well-known/gbo` through a separate FSC metadata service | the data service named in the document, under its contract | yes |
| `unsecured` | an absolute HTTP or HTTPS URL, with no FSC headers and no redirects | an absolute URL | no |
| `file` | a document in the metadata directory of the operator (`--metadata-dir`). The path cannot leave that directory | not possible: a file cannot answer a query | no |

Five rules apply when the two legs combine transports:

- If no `data_access` block is present, the data leg uses the metadata
  transport.
- `fsc` metadata with `unsecured` data is refused.
- `file` metadata needs an explicit `data_access`.
- If both legs use `fsc`, the two services must differ.
- `provider_peer_id` is on the leg that speaks FSC, never on both.

The registry reports both legs separately, as `transport_authenticated`
and `data_transport_authenticated`
([`service.go#L56-L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L56-L66)).
A single flag hides an FSC-authenticated data call whose description came
over an unauthenticated channel. The party that controls the document
decides the query, the mapping, and the wallet claims.

The intended form is `fsc` on both legs. The other combinations are for
an onboarding phase:

- `file` is for a source that publishes no `/.well-known/gbo`. The
  operator then keeps the description of the product of another party.
  This is an exception under
  [D-13](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/). The
  transport flag makes the exception visible, and `expires_at` makes it
  temporary.

    The exception is admissible only with recorded agreement of the
    bronhouder ([AV-08](../requirements/admission.md#av-08),
    [F-71](../traceability/findings.md#f-71)). The demo does not record
    this agreement. The need for agreement is only an instruction in
    [`source-metadata/README.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/source-metadata/README.md).

- `unsecured` is for local demonstrations. Only the local compose file
  mounts that source (`sources/local-demo/`). Deployments use only
  `sources/configured/`.

Four bounds stay in place with every transport:

- The Peer ID comes from the GBO configuration.
- The grant hash pins the contract.
- The reconciler compares the OIN with the certificate.
- Promotion is a separate step.

The trust model for each transport is an open point in demo issue
[#221](https://github.com/ICTU/GBO-demo/issues/221).

## Contract and activation {#a-valid-contract-is-not-activation}

A valid FSC contract does not take a source into use. It also does not
put the offer of the source in the wallet
([REQ-65](../requirements/sources-identity.md#req-65),
[F-58](../traceability/findings-closed.md#f-58)). Transport and mandate are two
decisions with two owners. If a contract alone activates a source,
admission becomes automatic again through a back door
([F-55](../traceability/findings-closed.md#f-55)). Each situation has a fixed
result:

| Situation | Result |
|---|---|
| Valid metadata contract, no source file | nothing happens |
| Source file, no metadata contract | source `blocked`: `METADATA_CONTRACT_NOT_FOUND` |
| Source file, no contract for the data service | source `blocked`: `DATA_CONTRACT_NOT_FOUND` |
| FSC Manager unreachable | source `blocked`: `FSC_MANAGER_UNAVAILABLE` |
| Validated candidate without promotion | not active |

The reason codes are in
[`service.go#L141-L152`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L141-L152).
Automatic promotion is off by default
([`reconcile_command.go#L197`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go#L197)).
Compose and the Helm example turn it on for the demo. Then the source file
is the management action. Demo v0.9.0 does not build two things: control
over who can do that action, and a record of the admission decision
(PSA B-09 in the
[besluitregister](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister),
[REQ-123](../requirements/admission.md#req-123)).

## Versions, freshness and isolation

Source metadata fails closed for each source and ages within fixed
bounds. An operator can roll it back
([REQ-66](../requirements/sources-identity.md#req-66)). The mechanism has
five parts:

- Freshness: a successful check is fresh for at most 15 minutes. After
  that, it is stale for at most one hour. At acceptance, a document must
  be valid for at least one more hour
  ([`source_metadata_cache.go#L10-L14`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata_cache.go#L10-L14)).
  The issuance route shows `X-GBO-Metadata-Cache: fresh|stale`.
- States per source: each source has one of five application states.
  Kubernetes conditions are a separate thing.
    - `pending`: the check started.
    - `rollout_required`: a complete candidate waits.
    - `active`: the source is in use.
    - `stale`: the refresh fails, and the previous snapshot is within
      grace.
    - `blocked`: no usable snapshot exists, or the grace is over.
- Per-source refusal: if a source is past its grace, only the requests
  for that source get HTTP 503.
- Version rule: activation refuses a lower version than the last
  validated candidate. It also refuses the same version with other
  content
  ([`source_registry_backend.go#L163-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registry_backend.go#L163-L175)).
  The rule has no test
  ([#610](https://github.com/ICTU/GBO-demo/issues/610)).
- Rollback: an operator activates a stored release with
  `activate-source-release --release-id`. The command refuses a release
  that the adapter cannot load. An auto-promoter respects the rollback
  until new candidate content arrives.

Demo v0.9.0 has two deviations from the isolation rule
([#606](https://github.com/ICTU/GBO-demo/issues/606)):

- Promotion needs a valid version of every configured source
  ([`registry.go#L133-L158`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/registry.go#L133-L158)).
  The aim of this design is that no source leaves the wallet offer
  without notice. As a side effect, one broken source freezes new
  releases for all sources.
- The offer list `/eudi-offers.json` takes the shortest grace of all
  sources
  ([`source_release_runtime.go#L95-L100`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L95-L100)).
  So the list fails for all sources at the same time.

Source releases have the lifecycle that policy bundles lack: validation
before activation, bounded staleness, atomic promotion, and rollback
([F-59](../traceability/findings-closed.md#f-59)). For the policy side, see
[Policy lifecycle](policy-lifecycle.md) and
[ADR-0021](../decisions/0021-central-pap-signed-bundles.md).

## A certificate set per source

Every source has its own certificate set for issuance: issuer, reader
(access), and status-list certificates. GBO never shares a set between
sources and never substitutes one
([REQ-58](../requirements/eudi-issuance.md#req-58)). The issuer name and
the purpose that the wallet shows are bound to the signing and reader
certificates. A fallback to the set of another source made the wallet
show the wrong issuer ([F-50](../traceability/findings-closed.md#f-50)).

If material is missing, onboarding fails hard for that source only:

| Situation | Result |
|---|---|
| No set for the `source_id` | source `blocked`: `CERTIFICATE_SET_NOT_FOUND` |
| Set without OIN or organization name | source `blocked`: `CERTIFICATE_SET_INVALID` |
| Mounted material differs from the active release | GBO generates no issuance configuration ([`issuance_release.go#L113-L116`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_release.go#L113-L116)) |
| Two sources behind one FSC peer | each source has its own set |

The reconciler gets only public leaf certificates and public CA
certificates. Only the issuance init container gets the private keys of
the leaf certificates. Provisioning is a separate privileged command. For
where these certificates come from and how they map to EUDI trust roles,
see [Identity and trust](identity-trust.md).

## The source document

The document is JSON, validated against
[`gbo-source-metadata-v1.schema.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json).
The format is closed: validation refuses unknown fields. The envelope has
these fields:

| Field | Meaning |
|---|---|
| `schema_version` | `1.0` or `1.1`. Version 1.1 adds the `asi` capability ([`#L17-L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json#L17-L23)) |
| `source_oin` | 20-digit OIN. It must equal the OIN in the certificate set |
| `version` | Numeric version. One version identifies one content |
| `issued_at`, `expires_at` | Validity window. At acceptance, at least one hour must remain |
| `capabilities.eudi` | attestations for EUDI issuance |
| `capabilities.asi` | attributes for verification through the ASIP (1.1 only) |

### The `eudi` capability: claims once, Type Metadata generated

Each attestation has `type_id`, `type_version`, `offers`, `graphql`,
`mapping_profile`, `display`, and `claims`. Four of these fields hold
structured content:

- `offers` are the concrete wallet offers, each with fixed parameters (for
  example `jaar: 2024`). A request with parameters outside the published
  offers is refused with HTTP 400.
- `graphql` holds `service_reference`, `endpoint`, one read operation in
  `document`, `subject_variable`, declared `parameters`, and
  `result_pointer`.
- `display` is keyed by language. It holds a name, a description, a
  `summary` with `{{claim}}` placeholders, and rendering.
- `claims` defines each claim once. A claim has one `gbo-simple-v1` rule
  in `source` (`pointer`, `datatype`, optional `optional`), a `label`, an
  optional `description`, and `sd` (`always` by default, `allowed`, or
  `never`).

Earlier versions had separate `mapping`, `attribute_schema`, and
`type_metadata` blocks. The format removed them. GBO derives the mapping
from `claims`. It generates the SD-JWT VC Type Metadata from `display` and
`claims`
([`type_metadata.go#L64`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/type_metadata.go#L64)).
Each Type Metadata field has a fixed origin in the document:

| Type Metadata | Derived from |
|---|---|
| `name`, `description` | the first language in `display` |
| `display[]` | `display`, with `lang` from the key |
| `claims[].path`, `svg_id` | the claim name |
| `claims[].display[]` | `label` and `description` |
| `claims[].sd` | `sd` |
| `schema.properties` | `source.datatype` (`date` becomes a string with `format: date`) |
| `schema.required` | every claim without `optional: true`, plus `vct` and `vct#integrity` |

Because the schema comes from the same rules as the projection, a source
cannot publish a schema that differs from what the mapping fills. Five
validation rules apply to the claims
([`source_claims.go#L216-L242`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_claims.go#L216-L242)):

- A `summary` placeholder must be a claim name.
- Validation refuses reserved names (`vct`, `vct#integrity`, `iss`,
  `status`, `cnf`, `iat`, `nbf`, `exp`, `sub`,
  `attestation_qualification`).
- The order of the claims is the order in which the wallet shows them.
- Validation refuses the datatype `number` for EUDI, because nl-wallet
  v0.5 cannot show a non-integral value.
- Only scalar datatypes pass. GBO does not support nested claims
  ([REQ-78](../requirements/eudi-issuance.md#req-78)).

The VCT of a type version is `/types/{source-id}/{type-id}/v{type-version}`.
The value `vct#integrity` covers the exact bytes that GBO serves at that
URL. A change to claims or display changes those bytes, so the change
needs a new `type_version`. GBO never deletes published type versions
automatically.

For how an answer of the source becomes an attestation, and for the error
codes if the answer does not fit, see
[ADR-0017](../decisions/0017-gbo-simple-v1.md)
([REQ-116](../requirements/eudi-issuance.md#req-116)).

### The `asi` capability (schema 1.1)

From schema 1.1 on, a source can also describe the attributes that it
offers for verification through the ASIP
([ADR-0039](../decisions/0039-asi-source-described-attributes.md),
[Q-38](../traceability/open-questions.md#q-38)). The `asi` capability has
three parts:

- `authentic_source`: the legal name and the country. The ASIP uses them
  in responses and discovery records
  ([REQ-94](../requirements/asi.md#req-94)).
- `graphql`: one query that ends in only `...Selected`, the subject
  variable, and the result pointer. For each request, the ASIP replaces
  `...Selected` with the fields of the requested attributes
  ([REQ-92](../requirements/asi.md#req-92)).
- `attributes`: for each attribute, an `identifier`, an optional type
  condition `on`, and `fields`. Each member of the value has exactly one
  operation:

    | Operation | Meaning |
    |---|---|
    | `pointer` | copy a field |
    | `join` with `separator` | concatenate two or more fields, without empty parts |
    | `const` | a fixed value of the member type |
    | `each` with `pointer` | for each element of a list, the field at `pointer` |

The `identifier` must exist in the attribute catalog of GBO,
[`schemas/asi-attributes.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json).
The catalog gives a `value_schema` for each identifier. The identifiers
are placeholders until the EU catalog of attributes exists
([Q-31](../traceability/open-questions.md#q-31)).

The profile `gbo-simple-v1` applies only to the `eudi` capability. The `asi`
capability composes values, because a source cannot always deliver a
catalog value with a copy. For example, a house number is three BRP
fields. The BRP document shows this composition
([`brp-graphql-server/config/gbo-source-metadata.json#L204`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/config/gbo-source-metadata.json#L204)).

Onboarding applies six rules to `asi`
([`source_registration.go#L396-L406`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registration.go#L396-L406)):

- If `asi` has an error, onboarding refuses the whole source, also if
  `eudi` is valid. The active release stays.
- The `asi` query uses the same data service as the attestations: one
  document, one data service.
- Onboarding also refuses a document with only `asi`, because onboarding
  requires the issuance certificate sets.
- If the reconciler cannot read the catalog, it refuses only the sources
  with `asi`.
- A source with `asi` gets release snapshot version 4.0. A source without
  `asi` stays at 3.0.
- Onboarding validates only the form. It does not validate the GraphQL
  schema of the source, or whether the policy of the source allows the
  selection. A difference becomes visible at the first request.

If the description is absent, has no `asi`, or is stale, the ASIP answers
503 for verify, retrieve, and discovery
([REQ-93](../requirements/asi.md#req-93)). If no registry is available,
the ASIP can read a release file (`asi-provider write-release-file`).

## Connection conditions for bronhouders

GBO asks three things of a bronhouder, as candidate connection
conditions:

- The bronhouder publishes a machine-readable, versioned description for
  each data service at the fixed location. The description includes the
  read API of the logbook of the bronhouder
  ([AV-07](../requirements/admission.md#av-07)).
- If the bronhouder has no endpoint of its own, it agrees provably with
  the description that the operator keeps
  ([AV-08](../requirements/admission.md#av-08)).
- The bronhouder provides a certificate set that carries its OIN and
  organization name ([REQ-67](../requirements/sources-identity.md#req-67)).

## Open points

Seven points are open:

- The document is not signed. The origin depends on the authenticated
  transport plus the OIN from the certificate set.
- The description lacks three items: the read API of the logbook of the
  source, a reference to the DCAT-AP-NL description, and central
  findability ([F-57](../traceability/findings.md#f-57),
  [F-68](../traceability/findings.md#f-68),
  [AV-07](../requirements/admission.md#av-07)). Without the
  read API, a caller cannot fill `dpl.read.nextLogbookId` from the
  description.
- DvTP does not use the description. The DvTP offer of a source is in the
  GBO rules. DvTP scope comes from the demand side. EUDI scope comes from
  the supply side ([F-74](../traceability/findings.md#f-74)).
- Traceability of versions: no record shows which versions of the
  mapping, the source schema, and the attestation schema an attestation
  used ([REQ-124](../requirements/eudi-issuance.md#req-124)).
- Key custody: the central issuance server holds the private keys of the
  issuer and status-list certificates of every source
  ([Q-17](../traceability/open-questions.md#q-17)).
- ASI resource list: in demo v0.9.0, the ASI authorization server takes
  its data services from configuration. It does not use the descriptions
  ([#592](https://github.com/ICTU/GBO-demo/issues/592)).
- Scale: how many sources the ASIP must connect, and how fast, is open
  ([Q-38](../traceability/open-questions.md#q-38), sub-question 1).

## Traceability

- Requirements: [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-64](../requirements/sources-identity.md#req-64),
  [REQ-65](../requirements/sources-identity.md#req-65),
  [REQ-66](../requirements/sources-identity.md#req-66),
  [REQ-67](../requirements/sources-identity.md#req-67),
  [REQ-78](../requirements/eudi-issuance.md#req-78),
  [REQ-92](../requirements/asi.md#req-92),
  [REQ-93](../requirements/asi.md#req-93),
  [REQ-94](../requirements/asi.md#req-94),
  [REQ-116](../requirements/eudi-issuance.md#req-116),
  [REQ-123](../requirements/admission.md#req-123),
  [REQ-124](../requirements/eudi-issuance.md#req-124),
  [AV-07](../requirements/admission.md#av-07),
  [AV-08](../requirements/admission.md#av-08)
- Findings: [F-50](../traceability/findings-closed.md#f-50) (closed),
  [F-55](../traceability/findings-closed.md#f-55) (closed),
  [F-57](../traceability/findings.md#f-57) (open),
  [F-58](../traceability/findings-closed.md#f-58) (closed),
  [F-59](../traceability/findings-closed.md#f-59) (closed),
  [F-68](../traceability/findings.md#f-68) (open),
  [F-71](../traceability/findings.md#f-71) (open),
  [F-74](../traceability/findings.md#f-74) (open)
- Open questions: [Q-17](../traceability/open-questions.md#q-17) (open),
  [Q-19](../traceability/answered-questions.md#q-19) (answered),
  [Q-31](../traceability/open-questions.md#q-31) (open),
  [Q-38](../traceability/open-questions.md#q-38) (partly answered)
- Demo increments: [SL-32](../traceability/increments.md#sl-32) (done),
  [SL-46](../traceability/increments.md#sl-46) (done),
  [SL-49](../traceability/increments.md#sl-49) (done)
- Decisions: [ADR-0016](../decisions/0016-source-owned-metadata.md),
  [ADR-0017](../decisions/0017-gbo-simple-v1.md),
  [ADR-0039](../decisions/0039-asi-source-described-attributes.md)
