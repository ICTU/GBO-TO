# ADR-0046: A source registers each delivery under a consent at a data usage index, and the register reads it back from the source's logbook

- Status: accepted
- Date: 2026-11-23
- Satisfies: [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid), [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: [Q-42](../traceability/answered-questions.md#q-42), [F-19](../traceability/findings.md#f-19), [F-68](../traceability/findings.md#f-68), [ADR-0026](0026-ldv-integration.md), and demo [#686](https://github.com/ICTU/GBO-demo/issues/686), [#687](https://github.com/ICTU/GBO-demo/issues/687), [#689](https://github.com/ICTU/GBO-demo/issues/689), [PR #704](https://github.com/ICTU/GBO-demo/pull/704), [PR #705](https://github.com/ICTU/GBO-demo/pull/705), [PR #706](https://github.com/ICTU/GBO-demo/pull/706), [PR #707](https://github.com/ICTU/GBO-demo/pull/707)
- Implemented in:
    - [services/data-usage-index](https://github.com/ICTU/GBO-demo/blob/088eb2b07393b0f136247a6e109d78f568c282ae/services/data-usage-index/README.md): the index, with one FSC service to register and one to look up.
    - [bron-sidecar/main.go](https://github.com/ICTU/GBO-demo/blob/088eb2b07393b0f136247a6e109d78f568c282ae/services/bron-sidecar/main.go#L170-L240): the reference implementation at the source, which registers and records a delivery.
    - [ldv-logboek](https://github.com/ICTU/GBO-demo/blob/088eb2b07393b0f136247a6e109d78f568c282ae/services/ldv-logboek/README.md#the-read-api-for-the-consent-register-over-fsc-686): the delivery logbooks and their read API over FSC.
    - [authz.rego](https://github.com/ICTU/GBO-demo/blob/088eb2b07393b0f136247a6e109d78f568c282ae/policies/authz.rego#L31-L79): the rule `LDV_READ_FSC` in the PDP of the source.
    - [uses/uses.go](https://github.com/ICTU/GBO-demo/blob/088eb2b07393b0f136247a6e109d78f568c282ae/services/consent-register/uses/uses.go): the register looks up, reads back and shows the uses.

## Context and problem statement

FR-11 and FR-22 (FR-DvTP v0.9) ask the consent register to show whether
and when data was retrieved under a consent. The register cannot see a
delivery. The source delivers to the consumer, and the register only
answers the status lookup of the PDP of the source
([Q-42](../traceability/answered-questions.md#q-42)).

Each controller logs its own processing in its own LDV logbook
([ADR-0026](0026-ldv-integration.md)). The delivery is therefore in the
logbook of the source. Nothing tells the register which logbook holds a
delivery under a given consent, or under which trace. LDV has no
standard place for the consent ID in a record
([Q-72](../traceability/open-questions.md#q-72)).

The LDV report on the TransparantieApp describes a "trace index" for a
comparable problem. That index points to the logbooks that hold traces
for a person.

## Decision

The decision has six parts:

1. A source that delivers data under a consent registers each delivery
   at the data usage index. A registration holds the logbook ID, the
   trace ID of the delivery, the type of legal basis (`consent`) and
   the consent ID. It holds no personal data and nothing that the source
   delivered.
2. The source records the delivery in its own LDV logbook, under the
   same trace ID. The record names the data subject in the pseudonym
   space of the source, and not the consent. The logbook offers the LDV
   read extension to the consent register over FSC.
3. The index publishes two FSC services under the peer of the consent
   register. Sources get a connection to register. Only the consent
   register gets a connection to look up, and it looks up by consent.
   The citizen reaches the uses through the register.
4. The register reads each registered trace back from the logbook of
   the source, through the read extension. The PDP of the source allows
   this read only for the peer of the register, and only with exactly
   one trace ID. The answer holds no data subject and no resource.
5. A use is a registration for which the logbook of the source holds a
   record. A registration without a record gives no use. If the register cannot reach the index or a logbook, it tells the
   citizen that the list is incomplete. It does not show an empty list.
6. The obligation lies with the source
   ([AV-17](../requirements/admission.md#av-17)). GBO offers the source
   gateway (bron-sidecar) as a reference implementation. A source can also build the same behavior itself.

This decision does not settle four points:

- What counts as a use, for example an answer without data
  ([Q-87](../traceability/open-questions.md#q-87)).
- What a source does when it cannot register or record a delivery
  ([Q-86](../traceability/open-questions.md#q-86)).
- Which person key the index needs for a general overview per citizen
  ([Q-88](../traceability/open-questions.md#q-88)).
- How long the index and the delivery logbooks keep their entries
  ([Q-08](../traceability/open-questions.md#q-08)).

## Considered options

1. An index of pointers, checked against the logbook of the source
   (chosen).
2. The status lookup at the register as the index (Q-42 option A, the
   proposal in [F-68](../traceability/findings.md#f-68)). The register
   sees the lookup itself, and the source builds nothing. But a lookup
   is not a delivery: the PDP can deny after it, or the source can
   fail. It also works only while the PDP looks up the status for every
   request ([REQ-75](../requirements/consent.md#req-75)).
3. A message from the source to the register after each delivery
   (Q-42 option B). This option is exact. But the register then keeps a
   list of deliveries, nothing in the logbook of the source backs the message, and the interface serves only consent. The index can also
   take deliveries on another legal basis, such as an issuance to an
   EUDI wallet or an OOTS request.
4. Derive the uses from the LDV chain (Q-42 option C). The chain starts
   at the consumer, and LDV does not bind the consumer
   ([F-68](../traceability/findings.md#f-68)). The register also needs the consent ID in the log records, outside the
   LDV core
   ([Q-72](../traceability/open-questions.md#q-72)).
5. The model of the TransparantieApp: an index by person pseudonym. The
   app of the citizen reads each logbook with a token that the index
   issues. This model needs a person key and a pseudonym service
   ([Q-88](../traceability/open-questions.md#q-88)). A view per consent
   needs only the consent ID, which the register already has.

## Consequences

- The index holds no personal data, but it links a consent ID to the
  logbooks and traces of its deliveries. Only the register can look it up.
- The consent ID stays outside the LDV record. The link between a
  delivery and its consent lives in the index. A view per consent
  therefore does not need a `dpl.gbo.*` attribute
  ([Q-72](../traceability/open-questions.md#q-72)).
- The register keeps no "retrieved" field. It derives the uses each
  time the citizen asks ([F-19](../traceability/findings.md#f-19)).
- The overview depends on the sources. A source that cannot answer
  makes the overview incomplete, and the register says so. The read
  extension has no paging. The demo cuts an answer off at 500 records
  and marks it in a local header
  ([F-103](../traceability/findings.md#f-103)).
- The register finds uses by trace. If a consumer uses one trace ID
  under two consents, each delivery shows as a use of both. A span ID in the registration fixes this.
- The index links a delivery to its source and its consent. This
  answers part of [F-68](../traceability/findings.md#f-68) for DvTP: the
  step from the source to the register. It does not answer the pointer
  from the decision at the source to the logbook of the register
  ([Q-25](../traceability/open-questions.md#q-25)).
- In the demo, the source gateway registers first and records second,
  so a record exists only for a delivery that the index accepted. It
  withholds the data if either step fails, and it uses no outbox. This
  deviates from part 4 of [ADR-0026](0026-ldv-integration.md). Whether
  that deviation stays is [Q-86](../traceability/open-questions.md#q-86).
- The name allows legal bases other than consent. Today the index
  accepts only `consent`.

## Traceability

- Requirements: [REQ-40](../requirements/consent.md#req-40), [REQ-72](../requirements/logging-audit.md#req-72), [REQ-75](../requirements/consent.md#req-75), [REQ-76](../requirements/consent.md#req-76), [AV-17](../requirements/admission.md#av-17)
- Findings: [F-19](../traceability/findings.md#f-19) (open), [F-68](../traceability/findings.md#f-68) (open), [F-103](../traceability/findings.md#f-103) (open)
- Open questions: [Q-08](../traceability/open-questions.md#q-08) (open), [Q-25](../traceability/open-questions.md#q-25) (open), [Q-42](../traceability/answered-questions.md#q-42) (answered), [Q-72](../traceability/open-questions.md#q-72) (open), [Q-86](../traceability/open-questions.md#q-86) (open), [Q-87](../traceability/open-questions.md#q-87) (open), [Q-88](../traceability/open-questions.md#q-88) (open)
