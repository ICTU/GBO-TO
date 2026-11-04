# ADR-0035: W3C Trace Context is the correlation key, and the FSC transaction ID is recorded next to it

- Status: accepted
- Date: 2026-11-02
- Satisfies: [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid), [D-08](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Supersedes: [ADR-0019](0019-fsc-transaction-id-tracing.md)
- Deliberation: [REQ-55](../requirements/logging-audit.md#req-55), [F-67](../traceability/findings-closed.md#f-67), [F-41](../traceability/findings-closed.md#f-41), and demo [PR #366](https://github.com/ICTU/GBO-demo/pull/366) ([#365](https://github.com/ICTU/GBO-demo/issues/365)), [PR #329](https://github.com/ICTU/GBO-demo/pull/329)
- Implemented in:
    - [ldv-client/tracecontext.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext.go#L25-L32): the rule and the order.
    - [consent.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L190-L245): the status lookup carries the trace.
    - The entry components [consumerhttp.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/consumerhttp/consumerhttp.go#L166-L182), [eudi-adapter/main.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L363-L368), and [asi-provider tracing.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/tracing/tracing.go#L61-L63).

## Context and problem statement

An auditor must follow one request through the consumer, the PDP, the
source gateway, the source, and the consent register. Three standards
record parts of the request:

- LDV (processing records) and the ADL (decision records) require that a
  component takes the incoming trace ID over unchanged (LDV §3.3.1, W3C
  Trace Context §3.1).
- FSC-Logging gives every FSC transaction its own transaction ID, unique
  per transaction (§3.4.1.1).

[ADR-0019](0019-fsc-transaction-id-tracing.md) used one value for both.
That choice breaks in three cases
([F-67](../traceability/findings-closed.md#f-67)):

- A caller sends its own `traceparent`.
- One processing calls several sources.
- The request takes an extra FSC hop, for example the status lookup of
  the PDP.

FSC forwards `traceparent` on the data path. Only the AuthZEN call of
the Inway to the PDP drops it ([F-39](../traceability/findings-closed.md#f-39),
[F-41](../traceability/findings-closed.md#f-41)).

## Decision

The decision has four parts:

- Every GBO component takes the trace ID unchanged from the incoming
  `traceparent`. If the caller is in the same trace, the component sets
  the span of the caller as parent. The component sends `traceparent`
  and `tracestate` on every outbound call.
- The order of sources is fixed: `traceparent`, then
  `Fsc-Transaction-Id`, then `X-Request-Id`, then the ambient span, and
  then a new trace.
- The `Fsc-Transaction-Id` never replaces an incoming trace. A component
  that starts or receives an FSC transaction records the transaction ID
  next to the trace ID. It records the ID as span attribute
  `gbo.fsc.transaction_id`, and in the ADL as `adl.fsc.transaction_id`.
- If an entry component receives no `traceparent`, it can tie its new
  trace to the UUIDv7 transaction ID that it mints. This part of
  ADR-0019 stays.

## Considered options

1. W3C Trace Context, with the transaction ID next to it (chosen). This
   option follows LDV, ADL, and FSC-Logging at the same time.
2. The transaction ID equals the trace ID
   ([ADR-0019](0019-fsc-transaction-id-tracing.md)).
   [F-67](../traceability/findings-closed.md#f-67) showed that this option
   fails.
3. A custom correlation header. Not chosen: LDV mandates W3C Trace
   Context.

## Consequences

- One processing has one trace ID and several transaction IDs. Logs and
  traces join on equal identifiers. They do not join on time stamps.
- The consent status lookup carries the trace and the transaction ID of
  the request. The LDV record of the register lands in the trace of the
  request.
- Separate units of work keep separate traces. The `consent_id` joins the
  consent issuance and the later query. A trace does not join them
  ([F-16](../traceability/findings-closed.md#f-16)).
- Behind the FSC Inway, the ADL record has its own random trace and no
  `adl.fsc.transaction_id`. The cause is that the Inway sends neither
  header to the PDP. A reader finds the record through the request
  headers stored in it. The fix is upstream in open-fsc
  ([#369](https://github.com/ICTU/GBO-demo/issues/369),
  [ADR-0036](0036-adl-decision-record.md)).
- A private consumer must send trace context and record the transaction
  ID ([AV-01](../requirements/admission.md#av-01)).
- In demo v0.9.0, the operational logs of `bron-sidecar`,
  `eudi-adapter`, and `asi-provider` carry no trace ID.

## Traceability

- Requirements: [REQ-55](../requirements/logging-audit.md#req-55), [REQ-71](../requirements/logging-audit.md#req-71), [REQ-72](../requirements/logging-audit.md#req-72), [AV-01](../requirements/admission.md#av-01)
- Findings: [F-16](../traceability/findings-closed.md#f-16) (closed), [F-39](../traceability/findings-closed.md#f-39) (resolved in demo), [F-40](../traceability/findings-closed.md#f-40) (resolved in demo), [F-41](../traceability/findings-closed.md#f-41) (resolved in demo), [F-67](../traceability/findings-closed.md#f-67) (resolved in demo)
- Open questions: none
- Demo increments: [SL-07](../traceability/increments.md#sl-07) (done), [SL-38](../traceability/increments.md#sl-38) (done), [SL-50](../traceability/increments.md#sl-50) (exploration done, build delivered)
