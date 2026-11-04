# ADR-0019: FSC transaction ID as the end-to-end correlation key

- Status: superseded by [ADR-0035](0035-w3c-trace-context.md)
- Date: 2026-08-24 (superseded 2026-11-02)
- Satisfies: [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
- Superseded by: [ADR-0035](0035-w3c-trace-context.md)
- Deliberation: [OBSERVABILITY.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/OBSERVABILITY.md), FSC txlog observability ([SL-38](../traceability/increments.md#sl-38))
- Implemented in: changed in gbo-demo ([PR #366](https://github.com/ICTU/GBO-demo/pull/366)). If no `traceparent` arrives, entry components still tie the trace to the transaction ID: [consumerhttp.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/consumerhttp/consumerhttp.go#L166-L182), [eudi-adapter/main.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L363-L368). Txlog viewer: [fsctxlog.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/fsctxlog.go)

## Why superseded

If the two IDs are equal, the design breaks in three cases
([F-67](../traceability/findings-closed.md#f-67)):

- A caller sends its own `traceparent`.
- One processing calls more than one source.
- The request passes an extra FSC hop.

LDV and the ADL require that a component takes over the trace ID
unchanged. FSC-Logging gives every transaction its own ID. Also, FSC
forwards `traceparent` on the data path. Only the AuthZEN call from the
Inway to the PDP drops it ([F-41](../traceability/findings-closed.md#f-41)).

[ADR-0035](0035-w3c-trace-context.md) makes W3C Trace Context the
correlation key and records the transaction ID next to it. One part stays:
an entry component without an incoming `traceparent` can tie its trace to
the transaction ID that it mints. The following sections keep the
original decision as history.

## Context and problem statement

FSC does not propagate W3C trace context across the Inway. As a result,
the trace of a consumer and the records on the provider side carry
unrelated identifiers.

## Decision (superseded)

Consumers generate a UUIDv7. They use it as the `Fsc-Transaction-Id` and
also as the OpenTelemetry trace ID. The PDP records it in every decision
log line. The FSC transaction logs of every hop carry it natively.

## Consequences (at the time)

- One identifier links the consumer request, the policy decision, and the
  audit record of each hop. A deny reason can be traced to the exact
  exchange.
- Debug stores (Jaeger, Loki) keep data only for a short time. The FSC
  txlog stays the authoritative record. For more information, see
  [Logging and traceability](../concepts/logging.md).
- If a later FSC version supports trace-context propagation, GBO can
  change this convention without breaking the txlog linkage.

## Traceability

- Requirements: [REQ-55](../requirements/logging-audit.md#req-55)
- Findings: [F-39](../traceability/findings-closed.md#f-39) (resolved in demo), [F-41](../traceability/findings-closed.md#f-41) (resolved in demo), [F-67](../traceability/findings-closed.md#f-67) (resolved in demo)
- Open questions: none
- Demo increments: [SL-07](../traceability/increments.md#sl-07) (done), [SL-38](../traceability/increments.md#sl-38) (done)
