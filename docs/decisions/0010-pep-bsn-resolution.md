# ADR-0010: BSN resolution inside the PEP

- Status: superseded by [ADR-0011](0011-sidecar-pseudonym-resolution.md), which [ADR-0033](0033-gateway-decrypts-after-allow.md) supersedes in turn
- Date: 2026-08-24 (ported from reference architecture v0.6.2)
- Satisfies: [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: Reference architecture v0.6.2, decision 4 (archived and unpublished)
- Implemented in: superseded before implementation

## Context and problem statement

After the PDP allows a pseudonymous DvTP request, a component must resolve
the pseudonym to the BSN. The API of the source requires the BSN.

## Decision (superseded)

The PEP intercepts the query of the consumer. After the policy decision,
the PEP resolves `consent_id → PI → BSNk Transform → BSN`. Then it puts the
BSN into the internal query of the source holder (bronhouder).

## Why it was superseded

With this decision, the PEP becomes a middlebox that transforms data.
Also, a component with BSN authorization sits in shared infrastructure.

In the implemented design, the PEP (the FSC Inway) only enforces
decisions. The source owns the identifier resolution. For this design, see
[ADR-0011](0011-sidecar-pseudonym-resolution.md).

## Traceability

- Requirements: [REQ-21](../requirements/pseudonymization.md#req-21), [BSNK-04](../requirements/pseudonymization.md#bsnk-04)
- Findings: [F-30](../traceability/findings-closed.md#f-30) (resolved in demo), [F-37](../traceability/findings-closed.md#f-37) (resolved in demo)
- Open questions: none
- Demo increments: [SL-02](../traceability/increments.md#sl-02) (done)
