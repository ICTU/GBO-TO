# ADR-0009: Closed-world per-field rules: the rule is the catalog

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: plain-Rego rules bound by regime and service)
- Satisfies: [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Supersedes: [ADR-0008](0008-dienstencatalogus-ceiling.md)
- Deliberation: [engine.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego) (design notes in comments), [REQ-48](../requirements/authorization.md#req-48), [REQ-97](../requirements/authorization.md#req-97), [F-90](../traceability/findings-closed.md#f-90), demo commit [`80af776`](https://github.com/ICTU/GBO-demo/commit/80af776) (rules as plain Rego), [PR #527](https://github.com/ICTU/GBO-demo/pull/527) (service binding)
- Implemented in: [policies/gbo](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo): [engine.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L168-L192) (regime and service binding), [lib.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L1-L7) (reads the request only), [rules/](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules), [engine_test.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L497-L501) (every rule names its services)

## Context and problem statement

For each requested field, the PDP must decide whether an authorization basis
covers the field. The PDP must do this without a separate catalog, because
a catalog can drift away from enforcement.

A field key (`ParentType.field`) is unique only within one schema. Two
services can share a key: `Query.ingeschrevenPersoon` is in both `bri` and
`brp` ([F-90](../traceability/findings-closed.md#f-90)).

## Decision

Each rule is plain Rego. A rule declares these items:

- `rule_id`, `regime` (`consent` or `pid`), and `services` (the FSC
  services that the rule applies to)
- `covers_fields` and `covers_types`: the fields that the rule can grant
- its reasons to refuse: `deny` for the whole request and `deny_field[i]`
  for one field

If a rule gives no reason, it grants the field. Each rule checks the actor
and the scope itself ([REQ-48](../requirements/authorization.md#req-48)).
`lib.rego` only reads the request. It holds no checks.

The engine binds rules to fields in four steps:

1. Only the rules of the active regime bind
   ([ADR-0031](0031-regime-from-evidence.md)).
2. Only the rules that serve the FSC service of the request bind. The
   service is the `service_name` from the FSC access token. The Manager of
   the source signed this token
   ([REQ-97](../requirements/authorization.md#req-97)).
3. A field binds to the rules that name its key. An argument-free leaf
   outside the root types also binds to the rules that cover its parent
   type.
4. For each field, the first bound rule without reasons grants the field.

The rule set is a closed world:

- If no rule covers a field, the PDP denies the field with
  `NO_APPLICABLE_RULE`.
- If the PDP cannot make the decision for a field, it refuses the field
  as `RULE_NOT_EVALUABLE`. The request then fails as a configuration
  error.
- If the field list of a request is uncertain, the PDP denies the whole
  request ([REQ-17](../requirements/authorization.md#req-17),
  [ADR-0013](0013-pdp-request-mapper.md)).

The demo has five rules, as the following table shows:

| Rule | Regime | Service | Grants |
|---|---|---|---|
| DVT0001 | consent | `bri` | Income declaration fields under consent |
| LVG0001 | consent | `lvg` | Ownership check at the LVG, scope `lvg:vbo:eigendom` |
| EUD0001 | pid | `bri` | Inkomensverklaring to the wallet, years 2024 and 2025 |
| EUD0002 | pid | `brp` | Akte van overlijden to the wallet |
| ASI0001 | pid | `brp` | BRP fields for the ASIP |

## Consequences

- One artifact defines what is allowed and why. A new access decision
  needs a new rule file with tests.
- A test requires every rule to name its services. A rule for one service
  cannot grant a field of another service with the same key.
- Consent per year works because each scope covers one year
  (`bd:ib:2025`). Also, the year selector must travel inside the query. If
  the filter is missing, the request fails closed.
- Reasons have two layers
  ([REQ-06](../requirements/authorization.md#req-06)):
    - The consumer and the ADL get only a client code, such as
      `FIELD_NOT_PERMITTED`.
    - The rule codes for each field go only to the console decision log
      for the operator, in a fixed order.

    For more information, see [Authorization](../concepts/authorization.md).

- The service catalog (dienstencatalogus) with a legal anchor from
  [ADR-0008](0008-dienstencatalogus-ceiling.md) stays an open governance
  question. [Risks and technical debt](../risks.md) tracks it.
- gbo-demo v0.9.0 has no test that makes sure that every rule checks the
  actor itself ([#604](https://github.com/ICTU/GBO-demo/issues/604)).

## Traceability

- Requirements: [REQ-48](../requirements/authorization.md#req-48), [REQ-97](../requirements/authorization.md#req-97), [REQ-17](../requirements/authorization.md#req-17), [REQ-06](../requirements/authorization.md#req-06), [REQ-74](../requirements/authorization.md#req-74), [REQ-08](../requirements/authorization.md#req-08)
- Findings: [F-21](../traceability/findings-closed.md#f-21) (closed), [F-23](../traceability/findings-closed.md#f-23) (closed), [F-90](../traceability/findings-closed.md#f-90) (resolved in demo)
- Open questions: [Q-14](../traceability/open-questions.md#q-14) (open)
- Demo increments: [SL-03b](../traceability/increments.md#sl-03b) (done), [SL-13](../traceability/increments.md#sl-13) (done), [SL-33](../traceability/increments.md#sl-33) (done)
