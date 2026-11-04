# ADR-0033: The source gateway decrypts its own value after the allow, and only the Inway reaches it

- Status: accepted
- Date: 2026-11-02
- Satisfies: [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering), [S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)
- Supersedes: [ADR-0011](0011-sidecar-pseudonym-resolution.md)
- Deliberation: [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-81](../requirements/pseudonymization.md#req-81), [F-30](../traceability/findings-closed.md#f-30), [F-37](../traceability/findings-closed.md#f-37), [F-79](../traceability/findings.md#f-79), and demo [#364](https://github.com/ICTU/GBO-demo/issues/364), [PR #469](https://github.com/ICTU/GBO-demo/pull/469), [PR #476](https://github.com/ICTU/GBO-demo/pull/476), [PR #477](https://github.com/ICTU/GBO-demo/pull/477), [#473](https://github.com/ICTU/GBO-demo/issues/473)
- Implemented in:
    - [bron-sidecar/main.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/main.go#L185-L189): the gateway acts on the consent proof.
    - [substitution.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution.go#L213-L251): the own value and the recipient check.
    - [decryption.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/decryption/decryption.go#L44-L50): the source keys, with older versions kept.
    - [transport.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/transport.go#L9-L13): only the request shape that the PDP judged.
    - [docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L829-L837): the network isolation.

## Context and problem statement

Under a consent, the query of the consumer names the citizen with a
placeholder ([ADR-0032](0032-consent-proof.md)). The source API needs a
BSN, or the own pseudonym of the source for the citizen. A component
must replace the placeholder, under three conditions:

- Only after the PDP allowed the request
  ([REQ-04](../requirements/authorization.md#req-04)).
- Inside the boundary of the source, with the keys of the source, and
  without a central party in the query path
  ([REQ-21](../requirements/pseudonymization.md#req-21)).
- Without a BSNk call, because BSNk transforms only while the citizen is
  logged in ([BSNK-04](../requirements/pseudonymization.md#bsnk-04)).

A transformation after the decision is a gateway task. It is not a
policy task ([F-37](../traceability/findings-closed.md#f-37)).

## Decision

A gateway that the source owns (`bron-sidecar`) sits between the source
Inway and the source API. The gateway works as follows:

- The evidence decides. If a consent token is present, the subject comes
  from the token. Without a token, the request passes through unchanged
  (PID regime, [ADR-0031](0031-regime-from-evidence.md)). Grant properties
  play no part.
- Only the own value of the source counts. The gateway takes
  `encrypted_subject[<own OIN>]` from the proof: the VI for
  `consent:identity`, and the VP for `consent:pseudonym`. The own
  decryption component of the source reads the value with the keys of
  the source.
- The recipient must match. The decrypted value must name the own OIN of
  the source as recipient, or the gateway does not accept it. The key
  in the proof is not evidence. The value that BSNk signed is the
  evidence.
- Three cases lead to a refusal, and the request then goes no further:
    - A form is missing, for example no VI for a source that is not on
      the BSN authorization list.
    - The value is for another recipient.
    - The query has a literal subject under a consent proof.
- The gateway does not verify the proof again. The PDP verified it on
  the same request, and the gateway runs only after the allow.
- Isolation is the control:
    - Only the source Inways reach the gateway (network
      `source-gateways`).
    - The gateway reaches only what serves the source (network
      `sources`).
    - The gateway publishes no port.
    - The gateway accepts only the request shape that the PDP judged:
      POST, one path, a JSON body, and no query string.

## Considered options

1. The source gateway decrypts after the allow (chosen).
2. BSN resolution in the PEP ([ADR-0010](0010-pep-bsn-resolution.md)).
   The PEP becomes a middlebox that transforms data in shared
   infrastructure, with a BSNk call in the query path.
3. The sidecar calls BSNk Transform per request
   ([ADR-0011](0011-sidecar-pseudonym-resolution.md)). BSNk transforms
   only while the citizen is logged in, and a query comes later.
4. Transformation in the PDP. Policy is not a data pipeline
   ([F-37](../traceability/findings-closed.md#f-37)). With this option, the PDP
   holds BSN authority.
5. The gateway verifies the proof again. This option adds no protection,
   because a consumer holds real proofs. The protection is that no
   request reaches the gateway without the allow of the PDP
   ([F-79](../traceability/findings.md#f-79)).

## Consequences

- The query path has no central party and no BSNk. Only the source holds
  BSN authority, as P-10 requires.
- "After the decision" holds only while nothing other than the Inway
  reaches the gateway ([REQ-81](../requirements/pseudonymization.md#req-81)).
  The compose networks do this. A Kubernetes deployment needs a
  NetworkPolicy or an equivalent. In demo v0.9.0, the Helm chart has no
  such policy.
- A nonce does not bind a value to one consent. That binding is not built
  ([F-79](../traceability/findings.md#f-79)).
- A source keeps the decryption keys of an older key version while
  proofs for that version are valid
  ([AV-09](../requirements/admission.md#av-09)).
- A source must get its keys in advance, as a step of admission
  ([BSNK-09](../requirements/pseudonymization.md#bsnk-09),
  [onboarding keys](../requirements/pseudonymization.md#onboarding-keys),
  [#467](https://github.com/ICTU/GBO-demo/issues/467)).
- The gateway is a processing. It writes LDV records for the decryption
  and the forward ([ADR-0026](0026-ldv-integration.md)).
- In the demo, the three sources share one OIN and one decryption
  component. The mock does not encrypt. Production needs one decryption
  component per source.
- Two parts are not built: a source API that answers on a pseudonym
  ([#474](https://github.com/ICTU/GBO-demo/issues/474)), and a pseudonym
  for the consumer itself ([#478](https://github.com/ICTU/GBO-demo/issues/478),
  [Q-01](../traceability/open-questions.md#q-01)).
- The gateway is separate from the HTTP handler. For this reason, the
  gateway can move into an Inway plugin later.

## Traceability

- Requirements: [REQ-04](../requirements/authorization.md#req-04), [REQ-17](../requirements/authorization.md#req-17), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-80](../requirements/pseudonymization.md#req-80), [REQ-81](../requirements/pseudonymization.md#req-81), [AV-09](../requirements/admission.md#av-09), [BSNK-04](../requirements/pseudonymization.md#bsnk-04), [BSNK-07](../requirements/pseudonymization.md#bsnk-07), [BSNK-08](../requirements/pseudonymization.md#bsnk-08), [BSNK-09](../requirements/pseudonymization.md#bsnk-09)
- Findings: [F-06](../traceability/findings-closed.md#f-06) (closed), [F-30](../traceability/findings-closed.md#f-30) (resolved in demo), [F-37](../traceability/findings-closed.md#f-37) (resolved in demo), [F-79](../traceability/findings.md#f-79) (open)
- Open questions: [Q-01](../traceability/open-questions.md#q-01) (partly answered)
- Demo increments: [SL-02](../traceability/increments.md#sl-02) (done), [SL-22](../traceability/increments.md#sl-22) (done), [SL-51](../traceability/increments.md#sl-51) (done)
