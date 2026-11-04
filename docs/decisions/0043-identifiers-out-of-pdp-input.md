# ADR-0043: Keep identifiers out of the PDP input instead of masking decision logs

- Status: proposed (waits for demo [#368](https://github.com/ICTU/GBO-demo/issues/368))
- Date: 2026-11-02
- Satisfies: [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
- Deliberation: [REQ-60](../requirements/logging-audit.md#req-60), [F-54](../traceability/findings.md#f-54), and demo [#149](https://github.com/ICTU/GBO-demo/issues/149), [#364](https://github.com/ICTU/GBO-demo/issues/364), [#368](https://github.com/ICTU/GBO-demo/issues/368), [CHANGELOG](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L588-L602)
- Implemented in: not implemented. The plain BSN enters the PDP input at [eudi-adapter source_metadata.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata.go#L273) and [asi-provider graphqlsource/source.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source.go#L94).

## Context and problem statement

Logging must hold no BSN that the processing does not need
([REQ-60](../requirements/logging-audit.md#req-60)). Two decision logs
record the PDP input: the ADL and the console decision log
([ADR-0036](0036-adl-decision-record.md)). The routes differ:

- In the consent route, the PDP input holds a placeholder and no
  identifier ([ADR-0032](0032-consent-proof.md)). This route meets the
  requirement.
- In the EUDI and ASI routes, the query variables hold the plain BSN from
  the PID or the token. As a result, both decision logs hold the BSN.

Masking in the policy engine had no effect
([F-54](../traceability/findings.md#f-54)). The demo then kept the BSN
out through the construction of the input: the request mapper
pseudonymized the BSN through BSNk. The demo removed that step when the
mapper became a pure mapper
([#364](https://github.com/ICTU/GBO-demo/issues/364)). The demo accepts
the BSN in both logs until
[#368](https://github.com/ICTU/GBO-demo/issues/368) decides between
masking and "transform first".

## Proposed decision

The proposal has three parts:

- A component that builds PDP input leaves out or replaces every
  identifying value that the decision does not need.
- If the component cannot do that, the request does not continue.
- Masking in the engine or in the log pipeline is a second line only,
  with a continuous test on the real log output.

## Why proposed, not accepted

In demo v0.9.0, the input side gives no guarantee. If the team picks
masking in #368, [REQ-60](../requirements/logging-audit.md#req-60) must
change, because it says "never rely only on masking".

## Considered options

1. Keep identifiers out of the input (proposed). The PDP never receives
   the value, so no log can hold it.
2. Mask the decision logs. The value still reaches the engine. A change
   in the log shape can leak the value again without notice, as F-54
   showed.
3. Transform the BSN to a pseudonym before the PDP, as the earlier
   mapper did. This option needs a BSNk call in the decision path, and
   no rule reads the result.

## Consequences

- If the proposal is accepted, the EUDI adapter and the ASIP must build
  their PDP input without the BSN. The source still needs the BSN after
  the allow. For this reason, the value must reach the source another
  way, as in the consent route
  ([ADR-0033](0033-gateway-decrypts-after-allow.md)).
- LDV records never hold a BSN. The logbook refuses any record with a
  run of nine digits that passes the BSN checksum (elfproef)
  ([ADR-0026](0026-ldv-integration.md)). This ADR covers the decision
  logs only.
- Until a decision on #368, the BSN in the EUDI and ASI decision logs is
  a known risk ([Risks and technical debt](../risks.md)).

## Traceability

- Requirements: [REQ-60](../requirements/logging-audit.md#req-60), [REQ-71](../requirements/logging-audit.md#req-71), [REQ-20](../requirements/pseudonymization.md#req-20)
- Findings: [F-54](../traceability/findings.md#f-54) (open)
- Open questions: [Q-08](../traceability/open-questions.md#q-08) (open)
- Demo increments: [SL-29](../traceability/increments.md#sl-29) (done)
