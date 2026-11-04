# Source and identity requirements

These requirements cover how a source describes its own services and how GBO activates that description. They also cover how the legal identity of a party follows from its certificate. For the design, see [Source onboarding](../concepts/source-onboarding.md) and [Identity and trust](../concepts/identity-trust.md).

This page has the following parts:

- [Source metadata and activation requirements](#source-metadata)
- [Identity, trust and transport requirements](#identity-trust)

## Source metadata and activation requirements {#source-metadata}

These requirements cover how a source publishes its service description,
and how GBO validates and activates that description. [REQ-64](#req-64)
applies to every GBO-delivered component that must know something per
source or per service, in every data flow: EUDI issuance, the ASIP, and
the consent facility (toestemmingsvoorziening) (DvTP). [REQ-65](#req-65) and [REQ-66](#req-66)
describe activation as the issuance route and the shared Source Registry
implement it.

The demo builds the description for two channels. EUDI issuance reads the
`eudi` capability. Since [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592),
the ASIP reads the `asi` capability (schema version 1.1) from the same
Source Registry. In demo v0.9.0, the offer of a source for DvTP is in the
GBO rules. The source does not publish it.

[F-57](../traceability/findings.md#f-57)
and [F-58](../traceability/findings-closed.md#f-58) give the background.
[ADR 0016](../decisions/0016-source-owned-metadata.md) records the
mechanism.

Evidence links to gbo-demo point at tag `v0.9.0`.
### REQ-64: A GBO component works only with the service description the source publishes itself, after validation {#req-64}

> A GBO-delivered component MUST take the service description of a source only from what the source publishes itself. The description covers the data service, the query with declared parameters, the mapping, the attestation schema, the validity per attestation type, and the offer. The component MUST NOT keep that description itself, add to it, or carry it per source in code. This applies to every GBO-delivered component that must know something per source or per service, in every data flow. These data flows are issuance, the ASIP, and the consent facility (the offer of the source per data set). A new service or data set of a source MUST be usable without a code change in such a component.

> Before use, the component MUST validate the description on schema, origin (the publishing party is the source holder (bronhouder) of the certificate set), version, validity window, and binding to the contract for the data service. The runtime MUST work only from a validated, activated version ([REQ-66](#req-66)). Every request that follows from it goes through the PDP of the source ([REQ-44](authorization.md#req-44)). The description MUST name the read API of the logbook of the source, and the chain MUST fill `dpl.read.nextLogbookId` from it.

> If the answer of the source does not fit the published mapping exactly, or holds more than one result, issuance MUST refuse. It MUST NOT pick a result, and it MUST NOT add or convert a value.

| Case | Outcome |
|---|---|
| Valid description, OIN equal to the certificate set, contracts present | candidate activated |
| OIN in the description differs from the certificate set | not activated: `METADATA_INVALID` |
| No contract for the data service the description names | not activated: `DATA_CONTRACT_NOT_FOUND` |
| Query is not exactly one read operation, or unknown mapping profile | not activated: `METADATA_INVALID` |
| Valid for less than one hour, or `expires_at` not after `issued_at` | not activated: `METADATA_INVALID` |
| Issuance request with parameters outside the published offer | refused (HTTP 400) |
| Answer does not fit the mapping (path missing, other datatype, result not a list) | no attestation (HTTP 502): `GBO_SIMPLE_PATH_MISSING`, `GBO_SIMPLE_TYPE_MISMATCH`, `GBO_SIMPLE_RESULT_TYPE` (code) |
| Answer with more than one result | no attestation (HTTP 502): `GBO_SIMPLE_RESULT_AMBIGUOUS` (code) |
| Answer without a result | no attestation (HTTP 404) (code) |
| Source without its own endpoint, where the operator maintains the document | admitted as an exception, visible as unauthenticated transport, lapses after `expires_at` |
| Read API of the logbook in the description | *proposal and not built* |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)
            ("the source holder can in principle add new services through the
            source-specific GBO configuration")
        - [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus)
            ("the source holder manages a source-specific GBO configuration that
            records which data services are available for which data flows, and
            which schemas, mappings and other processing instructions apply",
            "central GBO facilities can consult the configuration relevant to them
            in machine readable form", "the configuration can be validated,
            versioned and traced")
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
            (the source holder records mapping and attestation schema in its GBO
            configuration)
        - [GO](https://ictu.github.io/GBO-GO/main/) ("the mapping happens
            centrally with the settings from the decentral configuration
            component")
        - Implementing Regulation (EU)
            [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj),
            Annex II point 2(b) (verify the identity of the authentic source)
        - [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
        - for the exception:
            [D-13](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
    - **Addressee**: GBO-delivered component: the reconciler and the runtime
        of the EUDI adapter, the ASIP, and the consent facility. Interface
        agreement: the form of the publication and the validation rules. What
        the source holder must publish is in
        [AV-07](admission.md#av-07) and
        [AV-08](admission.md#av-08).
    - **Evidence**: [PR #219](https://github.com/ICTU/GBO-demo/pull/219),
        [PR #224](https://github.com/ICTU/GBO-demo/pull/224),
        [PR #242](https://github.com/ICTU/GBO-demo/pull/242),
        [PR #318](https://github.com/ICTU/GBO-demo/pull/318),
        [PR #463](https://github.com/ICTU/GBO-demo/pull/463),
        [#592](https://github.com/ICTU/GBO-demo/issues/592).
        - Publication at `/.well-known/gbo`:
            [`brp-graphql-server/main.go#L938`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/main.go#L938)
            and
            [`graphql-server/main.go#L360`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/main.go#L360),
            with the document
            [`gbo-source-metadata.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/config/gbo-source-metadata.json).
        - Schema with version 1.0 or 1.1 (1.1 adds `asi`):
            [`gbo-source-metadata-v1.schema.json#L17-L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json#L17-L23).
        - Origin and contract:
            [`source-registry/onboarding/service.go#L403-L413`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L403-L413).
        - Content: one read operation in
            [`source_metadata.go#L130-L141`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata.go#L130-L141).
            The validity window is in
            [`source_metadata_cache.go#L29-L41`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata_cache.go#L29-L41),
            tested in
            [`main_test.go#L628`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main_test.go#L628).
        - Offer:
            [`source_metadata.go#L272-L296`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata.go#L272-L296),
            tested in
            [`main_test.go#L434`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main_test.go#L434).
        - GBO generates the SD-JWT VC Type Metadata from `display` and `claims`:
            [`type_metadata.go#L64`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/type_metadata.go#L64),
            tested in
            [`type_metadata_test.go#L120`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/type_metadata_test.go#L120).
        - The ASIP reads the active release:
            [`asi-provider/main.go#L101`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L101),
            tested in
            [`asi_onboarding_test.go#L152`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/asi_onboarding_test.go#L152).
        - Exception without endpoint:
            [`source-metadata/README.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/source-metadata/README.md)
            and
            [`service.go#L18-L28`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L18-L28),
            [`#L56-L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L56-L66).
    - **Related**: [REQ-44](authorization.md#req-44),
        [REQ-57](eudi-issuance.md#req-57), [REQ-65](#req-65),
        [REQ-66](#req-66), [REQ-67](sources-identity.md#req-67),
        [REQ-72](logging-audit.md#req-72),
        [REQ-77](eudi-issuance.md#req-77), [REQ-78](eudi-issuance.md#req-78),
        [REQ-116](eudi-issuance.md#req-116), [REQ-121](consent.md#req-121),
        [REQ-124](eudi-issuance.md#req-124),
        [F-57](../traceability/findings.md#f-57),
        [F-68](../traceability/findings.md#f-68),
        [F-71](../traceability/findings.md#f-71),
        [F-74](../traceability/findings.md#f-74),
        [Q-14](../traceability/open-questions.md#q-14),
        [Q-19](../traceability/answered-questions.md#q-19),
        [Q-38](../traceability/open-questions.md#q-38),
        [ADR 0016](../decisions/0016-source-owned-metadata.md),
        [ADR 0017](../decisions/0017-gbo-simple-v1.md),
        [ADR 0039](../decisions/0039-asi-source-described-attributes.md).
    - **Notes**:
        - The requirement is built for EUDI issuance and, since #592, for the
            ASIP. The Source Registry is a shared module in
            `services/source-registry`. The ASIP reads the active release every 5
            seconds.
        - The `eudi` capability describes each attestation with `type_id`,
            `type_version`, `offers`, `graphql`, `mapping_profile`, `display`,
            and `claims`. Each claim has one `gbo-simple-v1` rule in `source`, a
            label, and an `sd` value. GBO derives the mapping and generates the
            Type Metadata from it. The schema has no separate `mapping`,
            `attribute_schema`, and `type_metadata` blocks.
        - The `asi` capability maps source fields onto GBO-catalogued attribute
            value schemas with `pointer`, `join`, `const`, and `each`.
            `gbo-simple-v1` applies to the `eudi` capability only
            ([ADR 0039](../decisions/0039-asi-source-described-attributes.md)).
        - For DvTP, the offer of a source is in the GBO rules
            ([`dvt0001.rego#L32-L44`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L32-L44)).
            The source does not publish it. For DvTP, the requirement covers the
            supply side. The legal ceiling per service, and whether a data set is
            mandatory or optional, come from the catalogue (FR-32,
            [F-74](../traceability/findings.md#f-74),
            [REQ-121](consent.md#req-121),
            [Q-45](../traceability/open-questions.md#q-45)).
        - In demo v0.9.0, the origin check is authenticated transport (FSC)
            plus the OIN from the certificate set. The document itself is not
            signed.
        - The exception for a source without an endpoint follows D-13. The
            demo builds the exception as visible (`data_transport_authenticated`)
            and temporary (`expires_at`). The agreement of the source holder is only
            an instruction in the README
            ([AV-08](admission.md#av-08),
            [F-71](../traceability/findings.md#f-71)). The local compose also has
            a source over unsecured HTTP. Deployments do not mount it
            ([`docker-compose.yml#L1868-L1870`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L1868-L1870)).
        - Not built: the logbook read API in the description. In demo v0.9.0,
            the adapter gets it per caller from configuration
            ([`docker-compose.yml#L1819`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L1819),
            [F-68](../traceability/findings.md#f-68)). Also not built: a
            reference to the DCAT-AP-NL description of the data service (S10:
            "refers to managed objects where possible").
        - The content and the interface of the source configuration are an
            open decision of PSA S10. `gbo-source-metadata-v1` is the proposal of
            the demo.
        - The issuance runtime of nl-wallet reads its configuration only at
            start. That is a product property.

### REQ-65: Only an explicit management action takes a source into use, and a valid contract is not enough {#req-65}

> A valid FSC contract MUST NOT be enough to take a source into use or to
> publish its offer in the wallet. Taking a source into use MUST be an
> explicit management action, recorded in configuration apart from the
> contract. A validated service description MUST apply only after a
> separate promotion. A component MUST NOT discover and activate a source
> by itself.

| Case | Outcome |
|---|---|
| Valid metadata contract, no source configuration | nothing activated |
| Source configuration, no metadata contract | source blocked: `METADATA_CONTRACT_NOT_FOUND` |
| Source configuration, no contract for the data service | source blocked: `DATA_CONTRACT_NOT_FOUND` |
| Validated candidate without promotion | not active |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
        ("participation needs a prior admission decision", "the set-up treats
        technical identity and admission status apart from the role and
        authority in a specific interaction") and
        [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the reconciler of the issuance
        facility.
    - **Evidence**: [PR #237](https://github.com/ICTU/GBO-demo/pull/237),
        [PR #247](https://github.com/ICTU/GBO-demo/pull/247).
        - Configuration: one file per source in `sources/configured/`, read in
            [`source_configuration.go#L16-L28`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go#L16-L28).
        - No discovery, tested in
            [`fsc_contract_discovery_test.go#L143`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/fsc_contract_discovery_test.go#L143).
        - Missing contract in
            [`service.go#L346-L349`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L346-L349),
            tested in
            [`fsc_contract_discovery_test.go#L201`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/fsc_contract_discovery_test.go#L201).
        - Promotion as a separate step in
            [`reconcile_command.go#L134-L151`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go#L134-L151).
    - **Related**: [REQ-61](admission.md#req-61), [REQ-64](#req-64),
        [REQ-66](#req-66), [REQ-123](admission.md#req-123),
        [F-58](../traceability/findings-closed.md#f-58),
        [ADR 0016](../decisions/0016-source-owned-metadata.md).
    - **Notes**: design choice: automatic promotion is off by default
        ([`reconcile_command.go#L197`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go#L197)).
        Compose and the Helm example turn it on
        ([`docker-compose.yml#L1865`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L1865)).
        In that case, adding the configuration file is the management action.
        Not built: who is allowed to do that action, and how the admission
        decision is recorded (PSA
        [B-09](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister)).
        The configuration is a file in the repository.

### REQ-66: Source metadata fails closed per source, ages within bounds, and can be rolled back {#req-66}

> Source metadata can fail to validate, fall outside its validity, or fail to refresh within a grace period set in advance. In each of these cases, the metadata MUST fail closed for that source: no issuance follows on that metadata. The failure of one source MUST NOT stop issuance for other sources.

> An activated version MUST be immutable, MUST be activated as a whole, and MUST be possible to roll back to an earlier valid version. A version number MUST identify one content. A candidate with the same version but other content MUST NOT be activated. A candidate with a lower version than the last validated candidate of that source MUST NOT be activated either. Only the explicit management action of [REQ-65](#req-65) can go back to an earlier version.

| Case | Outcome |
|---|---|
| Refresh fails, previous version within grace | source `stale`, and issuance on the previous version |
| Refresh fails, no previous version or grace over | source `blocked` |
| Active version of a source past grace | issuance for that source refused (HTTP 503) |
| Certificate set of one source missing | that source blocked, the others activated |
| One configured source without a valid version | no new release for any source, and the active release stays (*deviates from the requirement, see notes*) |
| One source past grace | offer list for all sources HTTP 503 (*deviates from the requirement*) |
| Roll back to a stored release | active. Automatic promotion does not undo that. |
| Roll back to a release the adapter cannot load | refused |
| Source publishes the same version with other content | not activated (code, no test) |
| Source publishes a lower version than the last validated one | not activated (code, no test) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus)
        ("the configuration can be validated, versioned and traced"). For the
        isolation, the requirement is derived. It serves
        [P-15](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) and
        [D-04](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/). If the
        configuration of one source fails, issuance for other source holders must
        not fail with it.
    - **Addressee**: GBO-delivered component: the reconciler, the release
        register, and the runtime of the issuance facility.
    - **Evidence**: [PR #205](https://github.com/ICTU/GBO-demo/pull/205),
        [PR #276](https://github.com/ICTU/GBO-demo/pull/276),
        [PR #463](https://github.com/ICTU/GBO-demo/pull/463). Not built: the
        test for the version rule
        ([ICTU/GBO-demo#610](https://github.com/ICTU/GBO-demo/issues/610)) and
        the per-source isolation of promotion and offer list
        ([ICTU/GBO-demo#606](https://github.com/ICTU/GBO-demo/issues/606)).
        - Grace in
            [`service.go#L463-L476`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L463-L476),
            tested in
            [`fsc_contract_discovery_test.go#L549`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/fsc_contract_discovery_test.go#L549).
        - Refusal per source in
            [`main.go#L221-L225`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L221-L225).
        - Isolation tested in
            [`service_test.go#L130`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service_test.go#L130).
        - Immutable and atomic in
            [`store.go#L300-L390`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/postgresregistry/store.go#L300-L390),
            tested in
            [`store_test.go#L94`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/postgresregistry/store_test.go#L94)
            and
            [`#L147`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/postgresregistry/store_test.go#L147).
        - Rollback in
            [`source_registry_command.go#L120-L143`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registry_command.go#L120-L143),
            tested in
            [`source_registry_command_test.go#L72`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registry_command_test.go#L72)
            and
            [`registry_test.go#L116`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/registry_test.go#L116).
        - Version rule in
            [`source_registry_backend.go#L163-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registry_backend.go#L163-L175).
    - **Related**: [REQ-64](#req-64), [REQ-65](#req-65),
        [REQ-124](eudi-issuance.md#req-124),
        [F-52](../traceability/findings.md#f-52),
        [F-59](../traceability/findings-closed.md#f-59),
        [ADR 0016](../decisions/0016-source-owned-metadata.md),
        [ADR 0021](../decisions/0021-central-pap-signed-bundles.md).
    - **Notes**:
        - Design choice: fresh for at most 15 minutes, one hour of grace, and
            at least one hour of validity
            ([`source_metadata_cache.go#L10-L14`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata_cache.go#L10-L14)).
            The source states are `pending`, `active`, `stale`, `blocked`, and
            `rollout_required`.
        - Design choice: promotion of a new version needs a valid version of
            every configured source. This way, no source drops out of the release
            without notice
            ([`registry.go#L133-L158`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/registry.go#L133-L158)).
            As a result, new metadata of other sources waits until the failing
            source is repaired, or until the operator removes it from the
            configuration.
        - The offer list `/eudi-offers.json` takes the shortest grace of all
            sources
            ([`source_release_runtime.go#L95-L100`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L95-L100),
            [`#L298-L300`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L298-L300)).
            As a result, the list fails for all sources at the same time. That
            breaks the rule that the failure of one source must not stop issuance
            for other sources (#606).
        - Policy bundles do not have this lifecycle
            ([F-52](../traceability/findings.md#f-52),
            [F-59](../traceability/findings-closed.md#f-59)). PSA S06 asks the same for
            them ("on failure they fall back in a controlled way", "rollback
            procedure").

### Removed numbers

No numbers of this page were removed. The list of all removed numbers is
on the [requirements overview](index.md#removed-numbers).

## Identity, trust and transport requirements {#identity-trust}

These requirements cover how GBO establishes who an organization is, and
how channels reach a source. FSC establishes the identity of the calling
organization on every channel. The legal identity of a source holder (OIN
and name) comes from its certificate. It does not come from configuration
that an operator can fill in. Authorization for each request stays a
separate layer: see [Authorization](authorization.md).

[ADR 0003](../decisions/0003-fsc-connectivity.md) records FSC as the
transport. [ADR 0023](../decisions/0023-identity-convergence.md) records
the certificate roles. Evidence links to gbo-demo point at tag `v0.9.0`.

### REQ-46: Every channel that calls a source on behalf of an external party does so through FSC, with a valid certificate {#req-46}

> Every channel that calls a service of a source holder on behalf of an
> external party MUST do so through FSC. A channel MUST NOT enter the
> service of the source holder, or the authorization for it, directly. FSC
> establishes the identity of the calling organization. The authorization
> for each request (consent, PID binding, legal basis) stays a separate
> layer of the channel. If the certificate of the calling party is expired
> or revoked, the connection MUST be refused. The revocation check MUST
> NOT be disabled.

| Case | Outcome |
|---|---|
| Certificate of the calling party expired | connection refused |
| Certificate of the calling party revoked | connection refused, after the revocation propagates. Time limit: [Q-53](../traceability/open-questions.md#q-53) |
| Revocation check disabled in an Inway, Outway or Manager | not allowed *(proposal: not checked)* |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [GO](https://ictu.github.io/GBO-GO/main/) (FSC as the connectivity
            standard).
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel).
        - FR-34 criterion 3 ("on expiry or revocation of the organization identification means, access to the consent process and the data traffic is blocked immediately").
        - FR-33 criterion 2.
    - **Addressee**: interface agreement for every channel: DvTP, EUDI
        issuance (PuB-EAA), and the Authentic Source Interface.
    - **Evidence**: all three channels call through their own FSC Outway:
        - the service provider (dienstverlener) backend
            ([`main.go#L82`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/main.go#L82))
        - the EUDI adapter
            ([`main.go#L115`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L115))
        - the ASIP
            ([`main.go#L83-L85`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L83-L85))

        Nobody checked the revocation behavior.

    - **Related**: [REQ-61](admission.md#req-61),
        [REQ-74](authorization.md#req-74),
        [REQ-111](consent.md#req-111),
        [Q-53](../traceability/open-questions.md#q-53),
        [Q-60](../traceability/open-questions.md#q-60),
        [ADR 0003](../decisions/0003-fsc-connectivity.md).
    - **Notes**:
        - FSC establishes the organization. That says nothing about what the
            organization is allowed to do in each request. The regime for each
            request follows from the evidence that the request carries
            ([REQ-74](authorization.md#req-74)).
        - open-fsc checks revocation with a CRL cache. An operator can switch
            the check off for each Inway, Outway, and Manager. Without this
            requirement, that switch is a silent configuration choice.
        - The time within which a revocation must take effect is
            [Q-53](../traceability/open-questions.md#q-53).
        - The consent process blocks through the status in the register
            ([REQ-111](consent.md#req-111)), as long as the initiation
            is not bound to the certificate
            ([Q-60](../traceability/open-questions.md#q-60)).

### REQ-67: The legal identity of a source holder comes from its certificate and not from configuration {#req-67}

> A GBO component can put the legal identity of a source holder (OIN and
> organization name) in an attestation or a decision record. The component
> MUST then take it from verified certificate material of that
> source holder. A value that an
> operator can fill in freely MUST NOT be the source for it.

| Case | Outcome |
|---|---|
| Certificate with the OIN in `serialNumber` and exactly one organization name | OIN and name come from the certificate |
| Configured OIN or name differs from the certificate | refused: the certificate set is not loaded |
| Certificate without a 20-digit OIN, or without exactly one organization name | refused |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
            ("organizations and systems use recognized identifiers and certificates",
            "the set-up links the technical identity to the admitted legal organization and role").
        - [PSA F1](https://ictu.github.io/GBO-PSA/main/generieke-functies/#f1-identiteit-vertrouwen).
        - FR-33 and FR-34.
        - [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the source registration of
        the EUDI adapter.
    - **Evidence**: [PR #242](https://github.com/ICTU/GBO-demo/pull/242),
        [PR #247](https://github.com/ICTU/GBO-demo/pull/247),
        [PR #321](https://github.com/ICTU/GBO-demo/pull/321). Code and tests:
        - The derivation is in
            [`development_ca_provider.go#L242-L253`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider.go#L242-L253)
            and
            [`#L280-L288`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider.go#L280-L288),
            tested in
            [`development_ca_provider_test.go#L152`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider_test.go#L152).
        - A set without OIN or name blocks the source:
            [`source-registry/onboarding/service.go#L293-L297`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L293-L297).
        - The organization description goes into the certificate through
            [`onboarding.go#L182`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/onboarding.go#L182).
    - **Related**: [REQ-58](eudi-issuance.md#req-58),
        [REQ-64](sources-identity.md#req-64),
        [F-60](../traceability/findings-closed.md#f-60),
        [Q-06](../traceability/answered-questions.md#q-06),
        [Q-07](../traceability/answered-questions.md#q-07),
        [Q-68](../traceability/open-questions.md#q-68),
        [ADR 0023](../decisions/0023-identity-convergence.md).
    - **Notes**:
        - It is open whether policy can read the Peer ID of a consumer as its
            OIN: [Q-68](../traceability/open-questions.md#q-68).
        - In FSC the Peer ID is the `subject.serialNumber` of the FSC
            certificate. If the peer is the source holder itself, the Peer ID is the
            OIN. One peer can offer services of more than one source holder. So the
            source configuration keeps `provider_peer_id` apart from
            the OIN in the certificate
            ([`source_configuration.go#L35-L44`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go#L35-L44)).
        - The runtime gets leaf material and public CA certificates. It gets no
            CA private keys
            ([`development_ca_provider_test.go#L128`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider_test.go#L128)).
        - Consents are bound to the identity of the consumer. A change of that
            identity makes them unusable
            ([PR #244](https://github.com/ICTU/GBO-demo/pull/244),
            [PR #277](https://github.com/ICTU/GBO-demo/pull/277)).
        - In the default demo onboarding, RvIG is published through the
            Belastingdienst peer with the Belastingdienst OIN. That is a demo
            shortcut, and it does not show one OIN for each source holder. The
            certificate sets still differ for each source.

### Removed numbers

- REQ-01: removed. Organization attributes from a register described FSC
    and OpenFTV behavior that no longer exists.
- REQ-02: merged into [REQ-61](admission.md#req-61) (admission comes from
    a register).
- REQ-03: removed. A verified token before each query described code that
    no longer exists.

The list of all removed numbers is on the
[requirements overview](index.md#removed-numbers).

