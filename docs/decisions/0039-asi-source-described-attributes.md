# ADR-0039: ASI attributes described by the source (`asi` capability in source metadata)

- Status: accepted, partly implemented. In demo v0.9.0, the authorization server takes its resource list from configuration ([ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592) is open).
- Date: 2026-11-02
- Satisfies: [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), [S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: [Q-38](../traceability/open-questions.md#q-38), and demo [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592) steps 1 to 5, up to [PR #624](https://github.com/ICTU/GBO-demo/pull/624)
- Implemented in:
    - `asiCapability` in [gbo-source-metadata-v1.schema.json#L95](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-source-metadata-v1.schema.json#L95).
    - The attribute catalogue [schemas/asi-attributes.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json).
    - The mapping module [services/asi-mapping](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-mapping).
    - The validation by the reconciler in [source_registration.go#L396-L406](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_registration.go#L396-L406).
    - The release snapshot in [services/source-registry/asisnapshot](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/source-registry/asisnapshot).
    - The query per request in [verification/service.go#L238-L268](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L238-L268) and [plan.go#L22-L35](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-mapping/plan.go#L22-L35).
    - The BRP description in [gbo-source-metadata.json#L204](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/config/gbo-source-metadata.json#L204).
    - The rules in [docs/source-onboarding.md#L391-L487](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/source-onboarding.md#L391-L487).

## Context and problem statement

Per data service, the ASIP must know three things:

- Which attributes the source offers.
- Which source fields make each attribute.
- How to ask for these fields.

The first demo ASIP had this knowledge in code, as a BRP adapter. That
breaks [REQ-64](../requirements/sources-identity.md#req-64): a GBO
component works only with the description that the source publishes
itself. With the adapter, a new source needs a code change in the ASIP.

[Q-38](../traceability/open-questions.md#q-38) named three options: code,
GBO configuration, or a description that the source publishes. On
October 27, the direction became the third option, with a "copy only"
mapping. ETSI expects attribute identifiers and value schemas from the EU
catalogue of attributes. That catalogue did not exist on November 2,
2026.

This ADR extends [ADR-0016](0016-source-owned-metadata.md) from EUDI
issuance to the ASIP.

## Decision

The decision has seven parts:

1. The source describes its attributes. Source metadata schema 1.1 adds
   the capability `asi` next to `eudi`. The capability holds these
   parts:
    - `authentic_source`: the legal name and country, used in responses
      and discovery records.
    - `graphql`: one query document that ends in `...Selected`, the
      subject variable, and the result pointer.
    - `attributes`: per attribute identifier, the source fields per
      member of the value.
2. GBO keeps the shape of each value. GBO keeps a `value_schema` per
   attribute identifier in `schemas/asi-attributes.json`, until the EU
   catalogue of attributes provides it. The identifiers are provisional.
   The value schemas use only `type`, `properties`, `required`, `items`,
   and `format`.
3. The source composes values with four operations. Each member of a
   value has exactly one operation:
    - `pointer`: copy a field.
    - `join` with `separator`: concatenate fields.
    - `const`: a fixed value.
    - `each` with `pointer`: per list element.

    Pointers are RFC 6901 JSON Pointers over GraphQL field names. This
    part deviates from the "copy only" direction of October 27. A source
    cannot always deliver a catalogue value with a copy only. An example
    is a house number made of three BRP fields.

4. `gbo-simple-v1` stays for the `eudi` capability only
   ([ADR-0017](0017-gbo-simple-v1.md)). The two capabilities have
   different targets. The `eudi` target is wallet claims that the source
   defines. The `asi` target is values that the catalogue of GBO
   defines.
5. The reconciler validates, and the ASIP reads the active release. The
   reconciler validates `asi` against the catalogue, as part of the
   source metadata ([ADR-0016](0016-source-owned-metadata.md)). If `asi`
   is invalid, the reconciler refuses the whole source. The ASIP reads
   the active release from the source registry every 5 seconds, with the
   reader role.
6. One query per request. The ASIP replaces `...Selected` with only the
   fields of the requested attributes and fragments
   ([REQ-92](../requirements/asi.md#req-92)). If the description does not
   name an attribute, the ASIP answers 404 and does not ask the source.
7. Fuzzy matching follows the value schema. A string with a `format`,
   such as a date, matches exactly or does not match. Only strings
   without a `format` get `MatchWithVariation`
   ([REQ-113](../requirements/asi.md#req-113)).

## Consequences

- A new source for the ASIP needs a description and a configured data
  service. It needs no code. The discovery records and the legal name of
  the source follow the description without a restart.
- If no current description exists (absent, without `asi`, or stale),
  the ASIP answers 503 for verify, retrieve, and discovery
  ([REQ-93](../requirements/asi.md#req-93)).
- A source with `asi` gets release snapshot version 4.0. A source
  without `asi` stays at 3.0. Onboarding still refuses a document with
  only `asi`, because onboarding requires the issuance certificate sets.
- Onboarding validates the form only. It does not validate against the
  GraphQL schema of the source. It also does not check whether the
  policy of the source allows the selection. A difference shows at the
  first request. A demo test holds the BRP description against rule
  ASI0001.
- The ASIP still normalizes a code without a `format`, such as a
  nationality or a postal code. For codes, demo v0.9.0 does not meet
  [REQ-113](../requirements/asi.md#req-113)
  ([Q-70](../traceability/open-questions.md#q-70)).
- The shape of name and address is provisional
  ([Q-71](../traceability/open-questions.md#q-71)).

## Open points

These points are open:

- The authorization server takes its data services from
  `AZSP_RESOURCES`
  ([main.go#L105](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L105)),
  and not from the descriptions. This is the open part of
  [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592).
- The identifiers and value schemas move to the EU catalogue of
  attributes when it exists
  ([Q-31](../traceability/open-questions.md#q-31)).
- Which normalization applies per kind of value
  ([Q-70](../traceability/open-questions.md#q-70))?
- The document format is part of the open PSA S10 decision on the
  source-specific configuration
  ([ADR-0016](0016-source-owned-metadata.md)).

## Traceability

- Requirements: [REQ-64](../requirements/sources-identity.md#req-64),
  [REQ-84](../requirements/asi.md#req-84),
  [REQ-92](../requirements/asi.md#req-92),
  [REQ-93](../requirements/asi.md#req-93),
  [REQ-94](../requirements/asi.md#req-94),
  [REQ-113](../requirements/asi.md#req-113),
  [REQ-115](../requirements/asi.md#req-115)
- Findings: [F-57](../traceability/findings.md#f-57) (open)
- Open questions: [Q-31](../traceability/open-questions.md#q-31),
  [Q-38](../traceability/open-questions.md#q-38),
  [Q-70](../traceability/open-questions.md#q-70),
  [Q-71](../traceability/open-questions.md#q-71)
- Demo increments: [SL-28](../traceability/increments.md#sl-28),
  [SL-46](../traceability/increments.md#sl-46)
