# ADR-0045: A consent flow starts with a pushed request over FSC and ends with a code that the consumer exchanges over FSC

- Status: accepted
- Date: 2026-11-23
- Satisfies: [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal), [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
- Deliberation: [Q-60](../traceability/answered-questions.md#q-60), [Q-44](../traceability/answered-questions.md#q-44), [Q-61](../traceability/open-questions.md#q-61) sub-question 2, [REQ-37](../requirements/consent.md#req-37), [REQ-111](../requirements/consent.md#req-111), [REQ-119](../requirements/consent.md#req-119), and demo [#427](https://github.com/ICTU/GBO-demo/issues/427), [#648](https://github.com/ICTU/GBO-demo/issues/648)
- Implemented in:
    - [par.go](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/services/consent-portal-backend/consent/par.go): the pushed request and its reference.
    - [initiation.go](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/services/consent-portal-backend/consent/initiation.go): the checks against the registration.
    - [authorize.go](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/services/consent-portal-backend/consent/authorize.go): resolve and decision.
    - [token.go](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/services/consent-portal-backend/consent/token.go): the code and its exchange.
    - [fschttp.go](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/services/consent-portal-backend/fschttp/fschttp.go): `/par` and `/token` as an FSC service.
    - [consentrequest.go](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/services/dienstverlener-backend/consentrequest/consentrequest.go): the consumer side.
    - [consent-flow.md](https://github.com/ICTU/GBO-demo/blob/afcef2065578f902b0f5531d9b18e2bae11fce37/docs/consent-flow.md): the flow, its reason codes and its demo shortcuts.

## Context and problem statement

A consumer sends the citizen to the consent portal to give consent, and
the citizen returns to the consumer with the outcome
([REQ-37](../requirements/consent.md#req-37),
[REQ-119](../requirements/consent.md#req-119)). The name and purpose
that the citizen sees, and the return address, come from the
registration ([REQ-111](../requirements/consent.md#req-111)).

Two questions were open. Must the origin of the request be provable
([Q-60](../traceability/answered-questions.md#q-60))? How does the
consent proof reach the consumer, and which outcomes does the consumer
tell apart ([Q-44](../traceability/answered-questions.md#q-44))? The
earlier design carried the whole request in the URL, through the
browser and the login, and returned the proof in the URL.

## Decision

The flow follows the pattern of OAuth 2.0 with pushed authorization
requests (RFC 9126). The consent facility is the authorization server.

1. The consumer pushes its request over FSC to the consent facility:
   service, data sets, return address, `state`, and a PKCE challenge
   with method S256. The FSC peer identity proves which consumer sent
   it.
2. The consent facility checks the request against the registration
   before any citizen sees it, and answers with a short-lived
   `request_uri`.
3. The browser carries only `client_id` and `request_uri` to the start
   page of the consent portal. Only this reference has to survive the
   login.
4. The portal resolves the reference for the logged-in citizen. The
   first citizen who resolves it is bound to it. One decision spends it.
5. The consent facility decides the return. On a given consent, the
   return address carries a one-time `code` and `state`. On a refusal,
   it carries `error=access_denied` and `state`. On an error, it carries
   `error=server_error` and `state`.
6. The consumer exchanges the code over FSC, with its PKCE verifier, for
   the consent proof. The proof comes back as `access_token` in a token
   response. It never passes through the browser.

The lifetimes of the reference and the code are configuration. The
reference must outlive the login. The code lives briefly.

## Considered options

1. A pushed request over FSC and a code exchange over FSC (chosen).
2. The request as parameters in the URL, as in demo v0.9.0. Nothing
   proves its origin, and the whole request travels through the browser
   and the login.
3. A signed request object in the URL (RFC 9101). The origin is
   provable without an FSC call. But the long request still travels
   through the browser and the login. Every consumer also needs a
   registered signing key.
4. The portal of the consent facility as the OAuth party of another
   organization, which runs the protocol for consumers. The consent
   facility then depends on that organization for its interface.
5. No redirect: the consumer registers the request, and the citizen
   finds it in the portal. Nothing has to survive the login, but the
   citizen leaves the flow of the consumer.

For the proof, the alternative was the proof in the URL fragment of the
return, as in demo v0.9.0. A URL has a limited length, and the proof
holds a value per source.

## Consequences

- The design deviates from a plain OAuth setup in three points. The
  start page belongs to the consent portal, and not to a separate
  authorization endpoint. The consumer authenticates with its FSC peer
  identity, and not with an OAuth client authentication method. The
  token response carries the consent proof as `access_token`.
- The consent facility publishes two FSC services for consumers: the
  pushed request and the token exchange. A consumer needs a server-side
  session to keep `state`, the verifier and the proof
  ([AV-16](../requirements/admission.md#av-16)).
- A code that is used twice is refused, but the consent it gave is not
  revoked. RFC 6749 section 4.1.2 says that the server SHOULD revoke
  the tokens of a reused code. Only the consumer can exchange a code,
  over FSC and with its verifier, so a second use points to an error of
  the consumer. A failed exchange leaves the code usable until it
  expires.
- The consent is recorded at the decision, before the consumer holds
  the proof. A consent can therefore exist that no consumer holds
  ([F-101](../traceability/findings.md#f-101)).
- The confirmation before the return is a time limit
  ([F-102](../traceability/findings.md#f-102)).
- Contract acceptance does not see the service. A party admitted to the
  peer of the consent register can therefore also connect to the consent
  status ([F-100](../traceability/findings.md#f-100)).
- An integrator cannot start the flow yet. [REQ-37](../requirements/consent.md#req-37)
  asks the request to name the integrator. Demo
  [#702](https://github.com/ICTU/GBO-demo/issues/702) adds it.
- The proof is valid for the whole consent. A short-lived proof with
  refresh is demo [#647](https://github.com/ICTU/GBO-demo/issues/647).
- The GO (figure 4) shows the earlier redirect with the request in the
  URL. This decision replaces that step.

## Traceability

- Requirements: [REQ-37](../requirements/consent.md#req-37), [REQ-111](../requirements/consent.md#req-111), [REQ-119](../requirements/consent.md#req-119), [REQ-126](../requirements/consent.md#req-126), [REQ-127](../requirements/consent.md#req-127), [AV-16](../requirements/admission.md#av-16)
- Findings: [F-100](../traceability/findings.md#f-100) (open), [F-101](../traceability/findings.md#f-101) (open), [F-102](../traceability/findings.md#f-102) (open)
- Open questions: [Q-44](../traceability/answered-questions.md#q-44) (answered), [Q-60](../traceability/answered-questions.md#q-60) (answered), [Q-61](../traceability/open-questions.md#q-61) (partly answered)

