# ADR-0008: Service catalog as a data-driven policy ceiling

- Status: superseded by [ADR-0009](0009-closed-world-rules.md)
- Date: 2026-08-24 (ported from reference architecture v0.6.2)
- Satisfies: [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [GO: dienstencatalogus](https://ictu.github.io/GBO-GO/main/bijlage_begrippenlijst/#begrip-dienstencatalogus)
- Deliberation: Reference architecture v0.6.2, decision 3 (archived and unpublished)
- Implemented in: superseded before implementation

## Context and problem statement

GBO needs a ceiling that applies to all individual consents. The ceiling
limits what a consent screen can ask for and what a query can select.

## Decision (superseded)

GBO keeps a wettelijke service catalog (dienstencatalogus) as a separate register with a
legal anchor. The register maps each scope to its allowed fields
(`data.dienstencatalogus[scope].allowed_fields`). The PDP checks every
query against the catalog. The consent portal (toestemmingsportaal) shows only catalog entries.

## Why it was superseded

A separate catalog is a second authorization source. It can drift away
from the rules that enforce it. The implemented model puts the ceiling
into the rules themselves: the coverage declarations in closed-world rules
are the catalog ([ADR-0009](0009-closed-world-rules.md)).

The question of the legal anchor stays open: a catalog based on an AMvB,
with its own governance.
[Risks and technical debt](../risks.md) tracks this question.

## Traceability

- Requirements: [REQ-08](../requirements/authorization.md#req-08), [REQ-121](../requirements/consent.md#req-121)
- Findings: [F-21](../traceability/findings-closed.md#f-21) (closed), [F-23](../traceability/findings-closed.md#f-23) (closed), [F-38](../traceability/findings-closed.md#f-38) (closed)
- Open questions: none
- Demo increments: [SL-14](../traceability/increments.md#sl-14) (done)
