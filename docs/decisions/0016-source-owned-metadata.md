# ADR-0016: Source-owned metadata and reconciliation-based onboarding

- Status: accepted (mechanism). The document format is a proposal for PSA S10.
- Date: 2026-08-24 (updated 2026-09-07 for the source registry and split transports in gbo-demo v0.6.11, and updated 2026-11-02 for the claims model, schema 1.1 with `asi`, the shared registry, activation, and certificate sets in gbo-demo v0.9.0)
- Satisfies: [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-04](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), [S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting), [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
- Deliberation: [F-57](../traceability/findings.md#f-57), [F-58](../traceability/findings-closed.md#f-58), [SL-46](../traceability/increments.md#sl-46), [docs/source-onboarding.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/source-onboarding.md), [docs/source-metadata-cache.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/source-metadata-cache.md)
- Implemented in: [eudi-adapter reconcile command](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go), [source registry backend](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registry_backend.go), shared registry module [services/source-registry](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry) (`onboarding`, `postgresregistry`, `asisnapshot`), [gbo-source-metadata-v1 schema](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json), certificate set per source in [issuance_config.go#L159-L180](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L159-L180), ASIP reader in [asi-provider/main.go#L101](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L101)

## Context and problem statement

To connect a source, GBO must not need code on the GBO side or a central
catalog of source capabilities. The source owns its schema, its queries,
and its attestation definitions
([REQ-64](../requirements/sources-identity.md#req-64)). Also, a valid
transport contract alone must not be enough to take a source into use
([F-58](../traceability/findings-closed.md#f-58)).

PSA S10 leaves the content and the interface of the source-specific GBO
configuration open. The following mechanism (publish, validate, activate,
roll back) is a GBO design decision. The document format
`gbo-source-metadata-v1` is the proposal of the demo for that open S10
decision. It is not a final interface agreement.

## Decision

### Publication

Each source publishes its own machine-readable metadata at
`/.well-known/gbo`. The metadata is versioned, expires, and is validated
against a schema. The GBO configuration names only where to fetch it.
Identity comes from certificates. Access comes from FSC contracts.

The document holds capabilities for each channel:

- `eudi` (schema 1.0 and 1.1): for each attestation, `type_id`,
  `type_version`, `offers`, `graphql`, `mapping_profile`, `display` (per
  language), and `claims`. Each claim has one `gbo-simple-v1` rule in
  `source`, a `label`, an optional `description`, and `sd`. GBO generates
  the SD-JWT VC Type Metadata from `display` and `claims`
  ([ADR-0017](0017-gbo-simple-v1.md)). The document has no separate
  `mapping`, `attribute_schema`, and `type_metadata` blocks any more.
- `asi` (schema 1.1 only): the attributes that a source offers to the
  ASIP ([ADR-0039](0039-asi-source-described-attributes.md)).

For more information about the structure, see
[Source onboarding](../concepts/source-onboarding.md).

### Validation into a registry

A reconciler validates the fetched metadata into candidate records in a
PostgreSQL source registry. It validates the schema, the origin, the
version, the validity window, and the binding to the data contract. The
`source_oin` must equal the OIN in the certificate set. If it does not,
the result is `METADATA_INVALID`.

The registry is a shared module (`services/source-registry`). The EUDI
adapter writes it. The adapter, the issuance configuration step, and the
ASIP read it.

### Activation as a separate management action

Activation is a separate management action
([REQ-65](../requirements/sources-identity.md#req-65)). A valid FSC
contract activates nothing. A source becomes active only through an
explicit source configuration file, a validated candidate, and a
promotion.

If a configured source has no contracts, it is blocked with
`METADATA_CONTRACT_NOT_FOUND` or `DATA_CONTRACT_NOT_FOUND`. If the FSC
Manager is unreachable, the result is `FSC_MANAGER_UNAVAILABLE`. Automatic
promotion is off by default. Compose and the Helm example turn it on for
the demo.

### Releases

Promotion creates one immutable release from the complete candidate set.
It activates the release in the same transaction. The SHA-256 of the
content document identifies the release.

These products derive from the active release:

- the adapter activation snapshot
- immutable type metadata
- the issuance-server configuration (an init step writes it)
- the offer catalog
- the description of each data service for the ASIP

The runtime path never fetches metadata. The adapter and the ASIP poll the
active release through a read-only database role.

### Lifecycle per source

The lifecycle rules are in
[REQ-66](../requirements/sources-identity.md#req-66). Metadata is fresh for
15 minutes at most and has one hour of stale grace. It must be valid for
at least one hour.

The source states are `pending`, `active`, `stale`, `blocked`, and
`rollout_required`. If a source is past its grace, it gets HTTP 503. This
applies to that source only. A lower version is not activated. The same
version with other content is not activated either.

### Certificate set per source (fail-hard)

Issuance keeps one certificate set for each bronhouder
([REQ-58](../requirements/eudi-issuance.md#req-58)). The set holds the
issuer, reader (access), and status-list certificates. Issuance never
shares or substitutes a set.

The checks fail hard:

- If a set is missing, the source is blocked with
  `CERTIFICATE_SET_NOT_FOUND`.
- If a set has no OIN or organization name, the result is
  `CERTIFICATE_SET_INVALID`.
- If the mounted material differs from the active release, the
  configuration generation is blocked.

If two sources are behind one FSC peer, each source gets its own set. The
certificate binds the issuer identity and the purpose. So a shared set
shows the wrong issuer ([F-50](../traceability/findings-closed.md#f-50)).

### Transports

The two legs of a source choose their transport independently:

- The metadata leg (`metadata_endpoint`) is `fsc`, `unsecured`, or
  `file`. The `file` transport reads a document that an operator manages
  from a confined directory. It is for sources that publish no endpoint.
- The data leg (`data_access`) is `fsc` or `unsecured`. If `data_access`
  is omitted, the data leg inherits the metadata transport.

FSC metadata with unsecured data is refused. With `file` metadata, an
explicit `data_access` is required. Both legs report their authentication
status separately (`transport_authenticated`,
`data_transport_authenticated`).

## Consequences

- To onboard a source, an operator needs only configuration and
  contracts. There is no GBO catalog of sources, years, or schemas to
  maintain.
- Version rollbacks, byte drift, and expired metadata are refused. If
  metadata is unavailable, issuance fails closed (HTTP 503).
- Published versions of type metadata are immutable (`vct#integrity`
  covers the exact bytes). They are never deleted automatically. A change
  to claims or display needs a new `type_version`.
- An operator can roll back with `activate-source-release --release-id`.
  An auto-promoter that watches the registry keeps that choice while the
  candidate set stays the same.
- Two deviations from REQ-66 remain
  ([ICTU/GBO-demo#606](https://github.com/ICTU/GBO-demo/issues/606)):
    - Promotion needs a valid version of every configured source. So one
      broken source stops new releases for all sources.
    - The offer list `/eudi-offers.json` takes the shortest grace of all
      sources and fails for all sources at once.
- The version rule has no test
  ([ICTU/GBO-demo#610](https://github.com/ICTU/GBO-demo/issues/610)).
- The origin depends on the authenticated transport and the OIN from the
  certificate set. The document itself is not signed.
- With the `file` transport, the operator maintains the description
  instead of the source. This is a D-13 exception.
  `data_transport_authenticated` makes the exception visible, and
  `expires_at` makes it temporary. The exception needs recorded consent of
  the bronhouder
  ([AV-08](../requirements/admission.md#av-08),
  [F-71](../traceability/findings.md#f-71)). The demo does not record that
  consent.
- If the GraphQL service of a source is already on FSC, the source can be
  onboarded before it publishes `/.well-known/gbo`. The data call stays
  bound to the contract.
- The central issuance server holds the private keys of the issuer and
  status-list certificates of every source. There is no decision on
  whether that is allowed
  ([Q-17](../traceability/open-questions.md#q-17)).
- The issuance server reads its configuration only at startup. A new
  release needs a controlled restart (state `rollout_required`).

## Open points

The following points are open:

- The description does not contain the read API of the logbook of the
  source, a reference to the DCAT-AP-NL description, or central
  findability ([F-57](../traceability/findings.md#f-57),
  [F-68](../traceability/findings.md#f-68),
  [AV-07](../requirements/admission.md#av-07)).
- In demo v0.9.0, DvTP does not use the description. The DvTP offer of a
  source is in the GBO rules. The DvTP scope comes from the demand side
  ([F-74](../traceability/findings.md#f-74)).
- Who can do the activation action, and how the admission decision is
  recorded (PSA B-09 in the
  [decision register](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister)).
- The final form of the source configuration. This is the open PSA S10
  decision.

## Traceability

- Requirements: [REQ-64](../requirements/sources-identity.md#req-64),
  [REQ-65](../requirements/sources-identity.md#req-65),
  [REQ-66](../requirements/sources-identity.md#req-66),
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-67](../requirements/sources-identity.md#req-67),
  [AV-07](../requirements/admission.md#av-07),
  [AV-08](../requirements/admission.md#av-08)
- Findings: [F-50](../traceability/findings-closed.md#f-50) (closed),
  [F-57](../traceability/findings.md#f-57) (open),
  [F-58](../traceability/findings-closed.md#f-58) (closed),
  [F-59](../traceability/findings-closed.md#f-59) (closed),
  [F-68](../traceability/findings.md#f-68) (open),
  [F-71](../traceability/findings.md#f-71) (open),
  [F-74](../traceability/findings.md#f-74) (open)
- Open questions: [Q-17](../traceability/open-questions.md#q-17),
  [Q-19](../traceability/answered-questions.md#q-19),
  [Q-38](../traceability/open-questions.md#q-38)
- Demo increments: [SL-46](../traceability/increments.md#sl-46)
