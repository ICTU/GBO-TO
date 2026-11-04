# ADR-0036: The ADL is the authoritative record of authorization decisions

- Status: accepted
- Date: 2026-11-02
- Satisfies: [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid), [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
- Deliberation: [REQ-71](../requirements/logging-audit.md#req-71), [F-53](../traceability/findings-closed.md#f-53), [F-63](../traceability/findings-closed.md#f-63), [F-72](../traceability/findings.md#f-72), and demo [PR #337](https://github.com/ICTU/GBO-demo/pull/337), [PR #373](https://github.com/ICTU/GBO-demo/pull/373) ([#332](https://github.com/ICTU/GBO-demo/issues/332))
- Implemented in:
    - [docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L117-L126): the ADL is required in every profile.
    - [adl-reader.sql](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/adl/adl-reader.sql): the SELECT-only reader.
    - [authz.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/authz.rego#L42-L51): what the record carries.
    - [dev-portal-backend/adl.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dev-portal-backend/adl.go#L48-L66): the lookup by transaction ID.

## Context and problem statement

The PDP produces two decision logs:

- The Authorization Decision Log (ADL), which OpenFTV writes to
  Postgres.
- The console decision log of the embedded OPA, which goes to Loki.

The design did not say which log is the audit source
([F-53](../traceability/findings-closed.md#f-53)). The Logius standards family
has three records with three roles
([F-63](../traceability/findings-closed.md#f-63)):

- The ADL for decisions.
- LDV for processings ([ADR-0026](0026-ldv-integration.md)).
- FSC-Logging for transport.

A PDP decision is not a processing, so it is not an LDV record.

## Decision

The decision has four parts:

- An ADL record holds every PDP decision. OpenFTV writes the record to
  the Postgres database `ftv_adl`. The PDP does not start without this
  database, so the ADL runs in every deployment profile.
- The ADL record is the audit source for authorization decisions.
  Contract-acceptance decisions are ADL records too.
- The console decision log of the engine is observability. Nobody cites
  it as the record of a decision.
- A reader gets a SELECT-only database role (`adl_reader`).

## Considered options

1. The ADL as audit source (chosen). It is a standard record with an
   access model.
2. The console decision log as audit source. Not chosen: it is a log
   pipeline that can lose or sample lines, and it has no access model
   ([F-53](../traceability/findings-closed.md#f-53)).
3. Per-field detail in the reason of the record. Not chosen: the Inway
   returns the reason to the consumer
   ([F-72](../traceability/findings.md#f-72)).

## Consequences

- The record carries only `{allow, reason}`. On a deny, the reason is
  the code for the consumer (`FIELD_NOT_PERMITTED`, `ACCESS_DENIED`,
  `COVERAGE_UNVERIFIABLE <subcode>`, and more). The per-field rule codes
  and the step trace are only in the console log
  ([REQ-06](../requirements/authorization.md#req-06)).
- The record has these known gaps:
    - The record does not name the policy version (`policies: 0`,
      [REQ-59](../requirements/logging-audit.md#req-59)).
    - The record does not hold the consent-status answer
      (`adl.core.information`) or the configuration
      ([F-72](../traceability/findings.md#f-72)).
    - Behind the FSC Inway, the record does not hold the trace ID or
      `adl.fsc.transaction_id`
      ([#369](https://github.com/ICTU/GBO-demo/issues/369),
      [ADR-0035](0035-w3c-trace-context.md)). The dev portal finds the
      record through the stored request headers.
    - No pointer leads from the ADL record to the logbook of the consent register (toestemmingsregister) ([Q-25](../traceability/open-questions.md#q-25)).
    - In the EUDI and ASI routes, the record holds the plain BSN
      ([REQ-60](../requirements/logging-audit.md#req-60),
      [ADR-0043](0043-identifiers-out-of-pdp-input.md)).
- A replay of a decision from (input, policy, data) is not possible,
  because the policy fetches the consent status during the evaluation
  ([ADR-0032](0032-consent-proof.md)). A replay needs the
  non-deterministic built-in cache of OPA, and OpenFTV does not enable
  this cache.
- Retention, read access, and tamper evidence are not set
  ([REQ-32](../requirements/logging-audit.md#req-32),
  [Q-08](../traceability/open-questions.md#q-08)).

## Traceability

- Requirements: [REQ-71](../requirements/logging-audit.md#req-71), [REQ-32](../requirements/logging-audit.md#req-32), [REQ-59](../requirements/logging-audit.md#req-59), [REQ-60](../requirements/logging-audit.md#req-60), [REQ-06](../requirements/authorization.md#req-06)
- Findings: [F-07](../traceability/findings-closed.md#f-07) (closed), [F-53](../traceability/findings-closed.md#f-53) (resolved in demo), [F-63](../traceability/findings-closed.md#f-63) (closed), [F-72](../traceability/findings.md#f-72) (open)
- Open questions: [Q-08](../traceability/open-questions.md#q-08) (open), [Q-25](../traceability/open-questions.md#q-25) (open)
- Demo increments: [SL-04](../traceability/increments.md#sl-04) (done), [SL-50](../traceability/increments.md#sl-50) (exploration done, build delivered)
