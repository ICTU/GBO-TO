# ADR-0017: Gbo-simple-v1 as the attestation mapping profile

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: scope `eudi` only, claims model, error contract, gbo-demo v0.9.0)
- Satisfies: [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
- Deliberation: [docs/gbo-simple-v1.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/gbo-simple-v1.md), [REQ-116](../requirements/eudi-issuance.md#req-116)
- Implemented in: [internal/gbosimplev1/profile.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/profile.go), [gbo-simple-v1 schema](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/gbo-simple-v1.schema.json), claims validation in [source_claims.go#L216-L242](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_claims.go#L216-L242), generated Type Metadata in [type_metadata.go#L64](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/type_metadata.go#L64), error codes in [profile.go#L33-L37](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/profile.go#L33-L37), runtime in [main.go#L302-L316](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L302-L316)

## Context and problem statement

Source data must become attestation claims through a mapping. The source
must be able to declare this mapping in its metadata. GBO must be able to
execute the mapping without trusting logic from the source.

The source holder (bronhouder) stays responsible for the attestation content. So GBO must
not add to the content or convert it
([REQ-116](../requirements/eudi-issuance.md#req-116)).

## Decision

GBO defines gbo-simple-v1 under a fixed URN. It is a mapping profile that
is minimal on purpose and fails closed. The profile has these properties:

- It projects one source object to flat claims through RFC 6901 pointers.
- It has six data types and hard limits.
- It has no conversions, filters, joins, defaults, expressions, or I/O.
- Zero source rows give a `no_data` outcome (no credential). More than one
  row is an error.
- Unknown mapping properties are refused.

The profile applies only to the `eudi` capability of the source metadata.
The `asi` capability has its own operations (`pointer`, `join`, `const`,
`each`) against a value schema that GBO keeps
([ADR-0039](0039-asi-source-described-attributes.md)).

### Claims model

A source defines each claim once, in `claims`. Each claim carries these
items:

- its gbo-simple-v1 rule as `source` (`pointer`, `datatype`, optional
  `optional`)
- a `label` for each language
- an optional `description`
- `sd` (`always` by default, `allowed`, or `never`)

GBO derives the mapping from the claims. GBO also generates the SD-JWT VC
Type Metadata from `display` and `claims`. In this metadata,
`schema.required` is exactly the non-optional claims, and every claim gets
`svg_id`. The claim order is the display order in the wallet. Reserved
claim names (`vct`, `iss`, `status`, `cnf`, and others) are refused.

### No partial attestation

If the answer of the source does not fit the mapping, the adapter issues
nothing. This includes the claims that do fit. The adapter gives these
outcomes:

| Case | Outcome |
|---|---|
| A mandatory claim is missing | HTTP 502, `GBO_SIMPLE_PATH_MISSING` |
| A mandatory claim is `null` or has another type | HTTP 502, `GBO_SIMPLE_TYPE_MISMATCH` |
| The result is not a list | HTTP 502, `GBO_SIMPLE_RESULT_TYPE` |
| There is more than one result | HTTP 502, `GBO_SIMPLE_RESULT_AMBIGUOUS` |
| There is no result | HTTP 404 (`no_data`), and the adapter still logs it |
| An optional claim is missing or `null` | The claim is left out, and the rest is issued |

The consumer sees only the HTTP status. The code is in the adapter log.

## Consequences

- Mappings are data. They can be validated against a JSON Schema. They
  have an independent set of conformance fixtures
  ([testdata/cases.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/testdata/cases.json)).
- More expressive needs (derivations, unit conversions) require a later
  version of the profile and not ad-hoc extensions. A source that needs
  another form delivers that form itself.
- A change to claims or display changes the integrity value of the Type
  Metadata. Therefore the change needs a new `type_version`.
- The profile supports `number`, but EUDI onboarding refuses it. The
  reason is that nl-wallet v0.5 cannot show an amount that is not an
  integer. [Risks and technical debt](../risks.md) tracks this.

## Open points

- The profile does not support nested claims (objects and lists) with
  selective disclosure for each element. Only scalar data types pass
  validation ([REQ-78](../requirements/eudi-issuance.md#req-78)).
- In demo v0.9.0, nobody can trace which versions of the mapping, the
  source schema, and the attestation schema an attestation used
  ([REQ-124](../requirements/eudi-issuance.md#req-124)).

## Traceability

- Requirements: [REQ-64](../requirements/sources-identity.md#req-64),
  [REQ-78](../requirements/eudi-issuance.md#req-78),
  [REQ-116](../requirements/eudi-issuance.md#req-116),
  [REQ-124](../requirements/eudi-issuance.md#req-124)
- Open questions: [Q-20](../traceability/answered-questions.md#q-20),
  [Q-38](../traceability/open-questions.md#q-38)
- Demo increments: [SL-46](../traceability/increments.md#sl-46)
