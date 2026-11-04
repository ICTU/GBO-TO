# ADR-0024: Canonical semantic models per bronhouder

- Status: proposed
- Date: 2026-08-24
- Satisfies: [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), [D-14](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [GO F4](https://ictu.github.io/GBO-GO/main/#f4-semantiek-eenheid-van-taal)
- Deliberation: reference architecture v0.6.2, gap 3 (archived and unpublished)
- Implemented in: partially. The GraphQL schemas of the sources come from the [gbo-semantiek source profiles](https://github.com/ICTU/gbo-semantiek). No route serializations other than SD-JWT VC exist.

## Context and problem statement

The same data must appear in three forms:

- GraphQL responses (DvTP).
- Attestation claims (EUDI).
- OOTS-EDM evidence (cross-border).

If no canonical model per source exists, every route grows its own
mapping.

## Proposed decision

The source profile GraphQL schema is the canonical model per source. The
GBO-Semantiek track maintains this schema. GBO generates or defines the
route serializations from it:

- Attestation attribute schemas and type metadata. The sources already
  publish these, as [ADR-0016](0016-source-owned-metadata.md) decides.
- OOTS-EDM evidence-type mappings for
  [ADR-0020](0020-as4-bridge-for-oots.md).

## Open points

These points are open:

- The governance between the schemas of the bronhouders and the central
  semantics track.
- The mapping coverage for the evidence types of the OOTS Semantic
  Repository.
- Is gbo-simple-v1 ([ADR-0017](0017-gbo-simple-v1.md)) sufficient as the
  projection language for richer models?

## Traceability

- Requirements: [REQ-124](../requirements/eudi-issuance.md#req-124)
- Open questions: [Q-79](../traceability/open-questions.md#q-79)
