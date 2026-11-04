# ADR-0026: Each controller logs its own processing in an LDV logbook

- Status: accepted
- Date: 2026-08-24, proposed as "Logboek Dataverwerkingen integration". Rewritten and accepted on 2026-11-02.
- Satisfies: [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
- Deliberation: reference architecture v0.6.2, gap 5 "traceability correlation" (archived and unpublished), [REQ-72](../requirements/logging-audit.md#req-72), [F-64](../traceability/findings-closed.md#f-64), [F-65](../traceability/findings-closed.md#f-65), [F-68](../traceability/findings.md#f-68), [F-69](../traceability/findings-closed.md#f-69), and demo [PR #303](https://github.com/ICTU/GBO-demo/pull/303) ([#302](https://github.com/ICTU/GBO-demo/issues/302)), [PR #366](https://github.com/ICTU/GBO-demo/pull/366), [docs/ldv/README.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/ldv/README.md)
- Implemented in:
    - [services/ldv-logboek](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/README.md): the logbook stand-in, one instance per controller.
    - [services/ldv-client](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client): the shared client ([outbox.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/outbox.go#L17-L25)).
    - [validate.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/validate.go): the BSN refusal.
    - [docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L410-L598): the seven logbooks.

## Context and problem statement

A citizen and an auditor must be able to see which organization
processed which personal data, and why. The decision log records
decisions. It does not record processings, because a PDP decision is not
a processing ([F-63](../traceability/findings-closed.md#f-63)). The gap is at
the processing itself ([F-64](../traceability/findings-closed.md#f-64)):

- The consent status lookup at the register.
- The decryption at the source gateway.
- The query at the source.

The Logius standard Logboek Dataverwerkingen (LDV, v1.0.0) records each
processing in the logbook of its controller (Verantwoordelijke). Only
trace metadata crosses an organization boundary.

## Decision

The decision has four parts:

- Every component that GBO delivers and that processes personal data
  writes one LDV record per processing and per data subject. The record
  goes to the logbook of the controller of that component
  ([REQ-72](../requirements/logging-audit.md#req-72)).
- The record carries these values:
    - The trace context, as [ADR-0035](0035-w3c-trace-context.md)
      decides.
    - The data subject in the pseudonym space of that controller, with
      an explicit `data_subject_id_type`. The data subject is never a
      BSN.
    - A versioned, resolvable `processing_activity_id`.
    - `dpl.read.nextLogbookId`, if the processing calls another party.
    - The FSC peer that the Inway verified, if the component is a
      processor on a lookup over FSC
      ([REQ-76](../requirements/consent.md#req-76)).
- GBO ships the client. Each controller owns its logbook (P-10).
- A component stores the record durably in a local outbox before the
  processing delivers. If the logbook is down, the record arrives later.
  The outage never loses the record, and it does not fail the request.

## Considered options

1. A logbook per controller, written by a shared client (chosen).
2. One central GBO logbook. Not chosen: LDV keeps records at each
   controller, and only trace metadata crosses a boundary.
3. OpenTelemetry spans, relabeled as LDV records. Not chosen: spans are
   sampled, and their delivery is not acknowledged
   ([REQ-32](../requirements/logging-audit.md#req-32)).
4. A failed request when the logbook is down (the first demo version).
   The outbox replaced this option, because a withheld response does not
   undo a processing that already happened.

## Consequences

- The demo runs one `ldv-logboek` image as seven logbooks:
  Belastingdienst, BRP, consent (register and portal), EUDI adapter,
  consumer (Hypotheek-BV and the integrator), LVG, and Installatie
  Register. Twelve components write to them.
- The decryption at the source gateway is a processing at the source.
  Each logbook uses its own pseudonym space. As a result, a pseudonym
  does not travel between the logbooks of different controllers
  ([F-69](../traceability/findings-closed.md#f-69)).
- LDV records never hold a BSN. The logbook refuses any record with a
  run of nine digits that passes the elfproef.
- A reader follows a chain forward from the start logbooks through
  `nextLogbookId`. In DvTP the chain starts at the consumer, and LDV does
  not bind the consumer ([F-68](../traceability/findings.md#f-68),
  [AV-02](../requirements/admission.md#av-02)).
- The consumer has no citizen identifier, so it logs under the consent
  ID ([Q-27](../traceability/open-questions.md#q-27)).
- Citizen access works per controller, through the read extension of
  each logbook ([F-65](../traceability/findings-closed.md#f-65)). A view of the
  processings per consent is not built in demo v0.9.0.

These points are open:

- The register of processing activities is a stand-in without legal
  status. Retention and read access are open
  ([Q-08](../traceability/open-questions.md#q-08)).
- Components write a local `dpl.gbo.*` extension that nobody ratified
  ([Q-72](../traceability/open-questions.md#q-72)).
- No pointer leads from the decision at the source to the logbook of the
  consent register (toestemmingsregister) ([Q-25](../traceability/open-questions.md#q-25)).
- In demo v0.9.0, the ASIP writes no LDV records.
- Production needs WORM storage, hash chaining, or a notary for the
  logbooks ([REQ-32](../requirements/logging-audit.md#req-32)).

## Traceability

- Requirements: [REQ-72](../requirements/logging-audit.md#req-72), [REQ-32](../requirements/logging-audit.md#req-32), [REQ-55](../requirements/logging-audit.md#req-55), [REQ-60](../requirements/logging-audit.md#req-60), [REQ-76](../requirements/consent.md#req-76), [AV-02](../requirements/admission.md#av-02)
- Findings: [F-07](../traceability/findings-closed.md#f-07) (closed), [F-63](../traceability/findings-closed.md#f-63) (closed), [F-64](../traceability/findings-closed.md#f-64) (resolved in demo), [F-65](../traceability/findings-closed.md#f-65) (closed), [F-68](../traceability/findings.md#f-68) (open), [F-69](../traceability/findings-closed.md#f-69) (resolved in demo)
- Open questions: [Q-08](../traceability/open-questions.md#q-08) (open), [Q-24](../traceability/answered-questions.md#q-24) (closed), [Q-25](../traceability/open-questions.md#q-25) (open), [Q-27](../traceability/open-questions.md#q-27) (open), [Q-72](../traceability/open-questions.md#q-72) (open)
- Demo increments: [SL-50](../traceability/increments.md#sl-50) (exploration done, build delivered)
