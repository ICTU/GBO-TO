# ADR-0020: AS4 bridge for SDG-OOTS

- Status: accepted (not implemented in gbo-demo v0.9.0)
- Date: 2026-08-24 (ported from the reference architecture)
- Satisfies: [S08](https://ictu.github.io/GBO-PSA/main/capabilities/#s08-oots-adapter), [GO patroon B](https://ictu.github.io/GBO-GO/main/#patroon-b-grensoverschrijdend-verzoek-via-oots), SDG-verordening (EU 2018/1724)
- Deliberation: Reference architecture v0.6.2, decision 7 and OOTS bridge (archived and unpublished)
- Implemented in: not implemented. gbo-demo v0.9.0 has no implementation.

## Context and problem statement

The Single Digital Gateway Regulation requires cross-border evidence
exchange through the Once-Only Technical System (OOTS). OOTS uses
eDelivery AS4 transport, OOTS-EDM payloads, and SMP discovery. This is an
EU obligation, so GBO has no architectural choice here.

## Decision

GBO builds an OOTS-adapter at its edge. The adapter has three parts:

- A Domibus access point receives AS4 messages.
- An OOTS-EDM adapter maps evidence requests.
- An FSC translator forwards the requests to source holders (bronhouders) over the standard
  FSC and PEP-PDP chain.

The source holder sees a normal FSC request. AS4 exists only at the edge, in
line with the national Basisinrichting OOTS.

## Consequences

- Source holders serve cross-border requests without work that is specific
  to OOTS.
- The mapping of evidence types depends on canonical semantic models
  ([ADR-0024](0024-canonical-semantic-models.md)).
- The route needs a legal-basis policy path in the Gov-to-Gov style.
  This path is not implemented either.
  [Risks and technical debt](../risks.md) tracks both gaps.

## Traceability

- Open questions: [Q-79](../traceability/open-questions.md#q-79)
