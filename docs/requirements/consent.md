# Consent requirements (DvTP)

These requirements cover the consent of the citizen in the DvTP channel. They cover the consent proof and its lifecycle, and the start of a request. They also cover the roles of portal and register, access and revocation by the citizen, and the data model of the register. For the design, see [Toestemmingsvoorziening](../building-blocks/dvtp/consent-service.md).

This page has the following parts:

- [Consent proof and use](#consent)
- [Consent lifecycle requirements](#consent-lifecycle)
- [Consent initiation and return requirements](#consent-initiation)
- [Role split between toestemmingsregister and toestemmingsportaal (S01/S02)](#consent-roles)
- [Citizen access and revocation requirements](#citizen-access)
- [Toestemmingsregister data model](#consent-register)

## Consent proof and use {#consent}

In the DvTP route (Data via Third Parties), a citizen gives consent to a
private dienstverlener to get data about the citizen from a source. The
requirements on this page cover three topics:

- what a consent covers
- what the citizen sees and confirms
- how the authorization chain checks a consent at every request

The toestemmingsportaal is the portal UI inside MijnOverheid plus the
toestemmingsportaal backend. It records the choice of the citizen. The
toestemmingsregister stores the consent and issues a signed consent proof.
The consumer sends that proof with each request. The PDP of the source
checks the proof itself, and asks the register for the current status over
FSC ([ADR 0032](../decisions/0032-consent-proof.md)). If an integrator
connects, the consent binds the represented party
([ADR 0034](../decisions/0034-integrator-delegation.md)).

The related topic pages are [consent lifecycle](consent.md#consent-lifecycle),
[toestemmingsregister data model](consent.md#consent-register),
[role split S01/S02](consent.md#consent-roles),
[initiation and return](consent.md#consent-initiation),
[citizen access and revocation](consent.md#citizen-access), and
[pseudonymization](pseudonymization.md).

Evidence links to gbo-demo point at tag `v0.9.0`. The linked files did not
change between the review commit `819f3eb` and `v0.9.0`.
### REQ-10: Consent covers a whole data set, and the citizen does not pick fields within a set {#req-10}

> A consent MUST apply to one or more indivisible data sets (scopes). It
> MUST NOT apply to separate fields. The citizen MUST NOT be able to exclude
> fields within a set.

> Under a consent for a set, the PDP MUST allow exactly the fields that the
> service fixes for that set. The PDP MUST NOT allow more fields. The PDP
> MUST NOT allow only a part of them because of a field choice in the
> consent. If a request asks fields of a set without consent, the PDP MUST
> deny it.

| Case | Outcome |
|---|---|
| Consent for the set, and the request asks fields of that set | allowed (code) |
| The request also asks a field that is not part of the set | that field denied: `NO_APPLICABLE_RULE` (code) |
| Consent only for another set | denied: `SCOPE_NOT_ALLOWED`, or `YEAR_NOT_COVERED` for another tax year (code) |
| The citizen switches a set off | no consent for that set. The citizen cannot switch off a part of a set (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-10 criteria 1 and 2, and FR-38 criteria 4 and 5.
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("gegevensscope").
        - [GO, pattern C](https://ictu.github.io/GBO-GO/main/#patroon-c-gegevensverzoek-van-private-dienstverlener-dvtp)
          ("een specifieke gegevensset").
    - **Addressee**: GBO-delivered component: the portal UI, the
      toestemmingsregister, and the reference policy.
    - **Evidence**: [PR #511](https://github.com/ICTU/GBO-demo/pull/511),
      [PR #580](https://github.com/ICTU/GBO-demo/pull/580). Code and tests:
        - The proof carries only scopes
          ([`consent_token.go#L70-L80`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/consent_token.go#L70-L80)).
        - The fields of the set are in
          [`dvt0001.rego#L27-L45`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L27-L45).
          The set check is in
          [`#L61-L96`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L61-L96).
        - The tests are in
          [`engine_test.rego#L210-L220`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L210-L220),
          [`#L265-L270`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L265-L270),
          and
          [`#L288-L294`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L288-L294).
        - The UI has one toggle per set in
          [`ScopeToggle.tsx#L9-L25`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/components/consent/ScopeToggle.tsx#L9-L25).
        - [PR #509](https://github.com/ICTU/GBO-demo/pull/509): a consent for
          another question does not open the root field either
          ([`dvt0001_test.rego#L91-L102`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L91-L102)).
    - **Related**: [REQ-08](authorization.md#req-08), [REQ-12](#req-12),
      [REQ-121](#req-121), [F-03](../traceability/findings-closed.md#f-03),
      [F-17](../traceability/findings-closed.md#f-17),
      [Q-03](../traceability/answered-questions.md#q-03),
      [Q-45](../traceability/open-questions.md#q-45).
    - **Notes**: in the demo, the rule fixes which fields belong to a set. The
      portal UI fixes this again, separately. This information belongs in the
      service catalog
      ([ICTU/GBO-demo#382](https://github.com/ICTU/GBO-demo/issues/382)).
      Whether the design enforces a minimal mandatory set is open:
      [Q-45](../traceability/open-questions.md#q-45). In demo v0.9.0, the
      register and the proof accept a field list per scope
      (`consented_fields`) that no component reads.

### REQ-12: A consent is bound to one consumer, one service, and a named data scope {#req-12}

> Every consent MUST be bound to one consumer (OIN), one service with its
> purpose, and at least one named data set. The portal MUST NOT offer
> consent for a request without a purpose or a data set. The
> toestemmingsregister MUST NOT record a consent without a consumer, a
> service, or a data set. If a consent has no data set or no purpose, the
> toestemmingsportaal backend MUST refuse it with `CONSENT_SCOPE_MISSING`. The
> UI then offers no button.

| Case | Outcome |
|---|---|
| Consumer, purpose, and at least one known set | recorded (code) |
| No consumer | not recorded. The register refuses (code: HTTP 400 `dienstverlener_oin is required`) |
| No set chosen | button disabled. The backend refuses: `CONSENT_SCOPE_MISSING` (not built in the backend in demo v0.9.0) |
| No purpose | refused: `CONSENT_SCOPE_MISSING` (the demo fills in `hypotheek`, which deviates) |
| A set that the portal does not know | no consent question. The citizen sees "Onbekend verzoek" (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-09 criteria 1 and 2.
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("een toestemmingsrecord bevat minimaal … afnemer, dienst, doel,
          gegevensscope").
        - [PSA F2](https://ictu.github.io/GBO-PSA/main/generieke-functies/#f2-toegang-interactie)
          ("toestemming is vrij, specifiek, geïnformeerd …").
        - [GO, pattern C](https://ictu.github.io/GBO-GO/main/#patroon-c-gegevensverzoek-van-private-dienstverlener-dvtp)
          ("een specifiek doel, een specifieke afnemer en een specifieke
          gegevensset").
    - **Addressee**: GBO-delivered component: the portal UI, the toestemmingsportaal
backend, and the toestemmingsregister.
    - **Evidence**: the work to build is
      [ICTU/GBO-demo#601](https://github.com/ICTU/GBO-demo/issues/601). Code and tests:
        - The consumer is mandatory in
          [`main.go#L417-L420`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L417-L420).
        - The UI shows no button without a set in
          [`PortaalConsent.tsx#L164-L171`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L164-L171).
        - The unknown set is in
          [`#L63-L75`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L63-L75).
        - A part is not built: the backend and the register do not check the
          set and the purpose.
    - **Related**: [REQ-10](#req-10), [REQ-37](consent.md#req-37),
      [REQ-68](#req-68), [REQ-106](#req-106),
      [REQ-111](consent.md#req-111),
      [Q-46](../traceability/open-questions.md#q-46),
      [Q-49](../traceability/open-questions.md#q-49),
      [Q-69](../traceability/open-questions.md#q-69).
    - **Notes**:
        - The purpose is in the record but not in the proof, so the PDP does
          not check it.
        - In the demo, the service follows only from the set. The service
          catalog adds a service identifier
          ([ICTU/GBO-demo#382](https://github.com/ICTU/GBO-demo/issues/382)).
        - FR-09 criterion 2 also names the integrator in the record. This
          point is open in [Q-46](../traceability/open-questions.md#q-46).
        - [Q-69](../traceability/open-questions.md#q-69) asks whether the proof
          must bind the purpose, so that the PDP checks it (FR-17 criterion 1).

### REQ-14: After revocation, the chain denies every later request on that consent {#req-14}

> After the citizen revoked a consent, the authorization chain MUST deny
> every later request on that consent. This also applies to a proof that
> was valid before the revocation. The deny MUST work without any action
> by the consumer and without a message to the consumer.

| Case | Outcome |
|---|---|
| Consent revoked, and a request with the proof | denied: `CONSENT_WITHDRAWN` (code) |
| The same proof before and after the revocation | first allowed, then denied. The proof itself does not change (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-23 criterion 3, FR-24, FR-17 criterion 4, and FR-11 criterion 3.
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("de registratie ondersteunt … intrekking", and "de autorisatie
          controleert de actuele status op het moment van de gegevensvraag").
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("het toestemmingsregister verwerkt een intrekking zonder onnodige
          vertraging").
        - [GO](https://ictu.github.io/GBO-GO/main/#toestemming-en-grondslag-als-afdwingbaar-autorisatiemechanisme)
          ("Intrekking heeft direct effect").
    - **Addressee**: GBO-delivered component: the toestemmingsregister and the
      reference policy.
    - **Evidence**: [PR #371](https://github.com/ICTU/GBO-demo/pull/371),
      [PR #390](https://github.com/ICTU/GBO-demo/pull/390). Code and tests:
        - The revocation is in
          [`main.go#L585-L610`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L585-L610).
        - The status check in the policy is in
          [`consent.rego#L270-L280`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L270-L280).
        - The tests are in
          [`consent_test.rego#L197-L205`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L197-L205)
          and
          [`status_test.go#L23-L48`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status_test.go#L23-L48).
    - **Related**: [REQ-38](consent.md#req-38), [REQ-68](#req-68),
      [REQ-75](#req-75), [REQ-109](consent.md#req-109),
      [Q-42](../traceability/open-questions.md#q-42),
      [Q-48](../traceability/open-questions.md#q-48).
    - **Notes**: design choices:
        - A revocation changes only the status in the register. The record
          stays, and the citizen sees it as Ingetrokken (revoked).
        - The revocation does not touch the proof, the FSC contract, or
          sessions at the consumer. The consumer gets no message.
        - The deny follows because the PDP asks the status at every request
          ([REQ-68](#req-68)). [REQ-75](#req-75) sets how fast this must work,
          and whether another mechanism is allowed.
        - The chain does not recall data that the consumer got before the
          revocation (FR-24). For that data, the portal refers the citizen to
          the consumer (FR-25, [REQ-120](consent.md#req-120)).
        - The register does not record when the citizen revoked the consent:
          [Q-48](../traceability/open-questions.md#q-48).

### REQ-68: The PDP decides only on a consent whose origin, binding, and current status it establishes itself {#req-68}

> The consent proof of a request MUST bind at least these items: the
> citizen, the granted sets, the consumer, the authorization service, and
> the validity. The proof MUST bind the citizen as a value per receiving
> party ([REQ-80](pseudonymization.md#req-80)). The consumer is the party to
> whom the citizen gave the consent. The authorization service is the
> service for which the proof is meant.

> Before it allows, the PDP MUST establish itself that the register issued
> the proof, and that the proof is unchanged. It MUST establish that the
> binding is complete. It MUST establish that the consumer is the party on
> whose behalf the request is made. It MUST also establish the current
> status of the consent.

> If the PDP cannot establish one of these points, it MUST deny. The sets,
> the citizen, and the consumer on which the PDP decides MUST come from that
> established proof.

| Case | Outcome |
|---|---|
| Valid proof, consent active, consumer matches | allowed (code) |
| Signature does not verify, unknown key, or another algorithm | denied: `CONSENT_SIGNATURE_INVALID` (code) |
| The PDP cannot get the verification keys | denied: `CONSENT_KEYS_UNAVAILABLE`. The consumer sees `ACCESS_DENIED` (code) |
| Another issuer, another audience, another type, or a mandatory claim is missing | denied: `CONSENT_CONTEXT_INVALID` (code) |
| Consent given to another consumer | denied: `CONSENT_ACTOR_MISMATCH` (code) |
| The register does not know the consent | denied: `CONSENT_NOT_FOUND` (code) |
| The PDP cannot establish the status (time-out, error, unexpected answer) | denied: `CONSENT_STATUS_UNAVAILABLE`. The consumer sees `ACCESS_DENIED` (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          ("de PDP kan relevante informatiebronnen raadplegen …
          toestemmingsregister", and "een PEP weigert standaard bij
          ontbrekende of onbetrouwbare beslisinformatie").
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("de autorisatie controleert de actuele status op het moment van de
          gegevensvraag").
        - FR-17 criterion 1, and FR-26 criteria 1 and 3.
        - [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the toestemmingsregister
      (issuer) and the reference policy (verifier). Interface agreement: the
      form of the proof between consumer and source.
    - **Evidence**: [PR #238](https://github.com/ICTU/GBO-demo/pull/238),
      [PR #371](https://github.com/ICTU/GBO-demo/pull/371),
      [PR #390](https://github.com/ICTU/GBO-demo/pull/390),
      [PR #469](https://github.com/ICTU/GBO-demo/pull/469),
      [PR #477](https://github.com/ICTU/GBO-demo/pull/477). Code and tests:
        - The issuance is in
          [`consent_token.go#L130-L152`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/consent_token.go#L130-L152).
        - The verification is in
          [`consent.rego#L109-L186`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L109-L186).
        - The status check is in
          [`#L270-L280`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L270-L280).
        - The other checks are in
          [`dvt0001.rego#L49-L59`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L49-L59).
        - The tests are in
          [`consent_test.rego#L172-L193`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L172-L193),
          [`#L291-L343`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L291-L343),
          [`#L380-L424`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L380-L424),
          and
          [`dvt0001_test.rego#L84-L87`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L84-L87).
    - **Related**: [REQ-14](#req-14), [REQ-18](authorization.md#req-18),
      [REQ-19](consent.md#req-19),
      [REQ-74](authorization.md#req-74), [REQ-75](#req-75),
      [REQ-76](#req-76), [REQ-79](pseudonymization.md#req-79),
      [REQ-80](pseudonymization.md#req-80),
      [REQ-82](pseudonymization.md#req-82), [REQ-106](#req-106),
      [F-61](../traceability/findings-closed.md#f-61),
      [F-72](../traceability/findings.md#f-72),
      [F-78](../traceability/findings.md#f-78),
      [Q-44](../traceability/open-questions.md#q-44),
      [Q-55](../traceability/open-questions.md#q-55),
      [Q-68](../traceability/open-questions.md#q-68),
      [ADR 0032](../decisions/0032-consent-proof.md).
    - **Notes**: [ADR 0032](../decisions/0032-consent-proof.md) records the
      design choice. The proof is a token that the register signs
      (`gbo-consent+jwt`, ES256). The consumer sends it with each request. The
      demo handles the token as follows:
        - The Rego policy verifies the token itself. The request mapper only
          maps GraphQL.
        - The claims are `consent_id`, `encrypted_subject`, `scopes`,
          `scope_entries`, `dienstverlener_oin`, and `valid_until`, plus
          `iss`, `aud`, `iat`, `nbf`, `exp`, and `jti`.
        - The policy allows 30 s clock skew.
        - The policy keeps the verification keys (JWKS) in a cache for five
          minutes. On an unknown key ID, it gets them again at once, without a
          fallback to old keys.
        - The policy asks the status at every request, without a cache.
        - The policy compares the consumer with the represented party. For an
          integrator, see [REQ-106](#req-106).
          [Q-68](../traceability/open-questions.md#q-68) asks whether the FSC
          Peer ID can count as the OIN.
        - The status is not in the PDP input. For this reason, the PDP puts
          the consent that it got in its answer
          ([F-72](../traceability/findings.md#f-72)).
        - The proof carries no version
          ([F-78](../traceability/findings.md#f-78)).
        - [Q-55](../traceability/open-questions.md#q-55) covers the key
          location and rotation.
        - A pseudonym for the dienstverlener itself is not built
          ([ICTU/GBO-demo#478](https://github.com/ICTU/GBO-demo/issues/478)).

### REQ-75: Consent status is available within a set propagation time, availability, and latency {#req-75}

> The toestemmingsregister MUST deliver the current status of a consent
> within a set maximum propagation time. The propagation time runs from the
> revocation by the citizen to the first deny in the chain. The register
> MUST also meet a set availability and a set latency per query. If the
> status cannot be established in time, the chain MUST deny
> ([REQ-68](#req-68)). The mechanism (query per request, status list, or
> push) MAY be chosen freely, as long as it meets the set values. If a
> mechanism has a propagation time of more than zero, it MUST record that
> time.

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("de autorisatie controleert de actuele status op het moment van de
          gegevensvraag").
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("zonder onnodige vertraging").
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          ("regels voor foutafhandeling, time-outs en fail-safe gedrag").
        - [GO](https://ictu.github.io/GBO-GO/main/#toestemming-en-grondslag-als-afdwingbaar-autorisatiemechanisme)
          ("Intrekking heeft direct effect").
        - FR-11 criterion 3, and FR-17 criterion 4.
    - **Addressee**: GBO-delivered component: the toestemmingsregister and the
      status check in the reference policy.
    - **Evidence**: [PR #371](https://github.com/ICTU/GBO-demo/pull/371),
      [PR #390](https://github.com/ICTU/GBO-demo/pull/390). Code and tests:
        - The query per request is in
          [`consent.rego#L190-L200`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L190-L200)
          and
          [`#L268-L280`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L268-L280).
        - The tests are in
          [`consent_test.rego#L202-L214`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L202-L214)
          and
          [`#L303-L314`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L303-L314).
        - The values are not set.
    - **Related**: [REQ-14](#req-14), [REQ-68](#req-68), [REQ-76](#req-76),
      [F-61](../traceability/findings-closed.md#f-61),
      [F-68](../traceability/findings.md#f-68),
      [Q-05](../traceability/answered-questions.md#q-05),
      [Q-24](../traceability/answered-questions.md#q-24),
      [Q-47](../traceability/open-questions.md#q-47).
    - **Notes**:
        - The management organization sets the values with the owner of the
          register. The volumes are unknown
          ([Q-47](../traceability/open-questions.md#q-47)).
        - The demo asks per request, so the propagation time is zero in
          practice. The demo queries with a 2 s time-out.
        - PR #390 measured the query over FSC once: p50 14.5 ms, maximum 82 ms,
          and about 290 ms for the first query after a start.
        - The mechanism also affects the audit. With a status call per request, the
          LDV records of the register show which sources one processing
          touched (FR-31, [F-68](../traceability/findings.md#f-68)). A status
          list removes that information.

### REQ-76: The register gives consent status only to an authenticated, authorized PDP, over FSC, and records who asked {#req-76}

> The toestemmingsregister MUST give the status of a consent only to an
> authenticated, authorized component. That component is the PDP of a source
> that offers the service for which the consent applies. The query MUST go
> over FSC.

> The register MUST record the verified identity of the caller in its
> processing log ([REQ-72](logging-audit.md#req-72)). Along the same
> path, only the status of the register MUST be reachable.

| Case | Outcome |
|---|---|
| PDP peer with a contract asks the status | status delivered. The peer is the processor in the LDV record (code) |
| Query without an FSC peer | denied: HTTP 401 (code) |
| Another path than the status through the status service (detail, list, revoke) | denied (code) |
| Peer with a contract, but not the PDP of a source of that service | denied. Not built in demo v0.9.0: the demo delivers the status (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("alleen de burger en bevoegde componenten hebben toegang tot
          toestemming", and "gestandaardiseerd PIP-koppelvlak voor
          raadpleging").
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          ("aansluiting van PIP-bronnen").
        - [GO](https://ictu.github.io/GBO-GO/main/) (FSC as the connectivity
          standard).
    - **Addressee**: GBO-delivered component: the toestemmingsregister.
      Interface agreement: the status service over FSC.
    - **Evidence**: [PR #390](https://github.com/ICTU/GBO-demo/pull/390). Code and tests:
        - The status service is in
          [`status.go#L43-L99`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status.go#L43-L99).
        - The query through the Outway is in
          [`consent.rego#L39`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L39).
        - The tests are in
          [`status_test.go#L13-L96`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status_test.go#L13-L96),
          [`ldv_test.go#L204-L207`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/ldv_test.go#L204-L207),
          and
          [`consent_test.rego#L216-L219`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L216-L219).
        - The limit to the PDP of a source of the service is not built
          ([ICTU/GBO-demo#382](https://github.com/ICTU/GBO-demo/issues/382)).
    - **Related**: [REQ-39](consent.md#req-39),
      [REQ-46](sources-identity.md#req-46), [REQ-68](#req-68),
      [REQ-72](logging-audit.md#req-72), [REQ-75](#req-75),
      [F-68](../traceability/findings.md#f-68),
      [Q-23](../traceability/answered-questions.md#q-23),
      [Q-58](../traceability/open-questions.md#q-58).
    - **Notes**:
        - In the demo, the PDP queries through its own Outway (peer `…0800`)
          and the Inway of the register (peer `…0700`, service
          `consent-status`).
        - The register serves the status on its own listener, which serves
          nothing else. In demo v0.9.0, the portal-facing listener does not
          answer status calls.
        - The Manager of the register signs a contract only for peers admitted
          in the admission register (the PDP peer). Thus in the demo, the FSC
          contract is the authorization.
        - The register can check which source belongs to which service only
          with the catalog.
        - The status service trusts the `Fsc-Authorization` header that the
          Inway passes on. For this reason, the status service must be
          reachable only through that Inway. In the demo, a component can also
          reach it directly on the compose network.
        - Every query over FSC is a separate transaction. This counts in the
          choice of mechanism under [REQ-75](#req-75).

### REQ-106: An integrator acts only with a registered mandate, and the consent binds the represented party {#req-106}

> If an integrator calls on behalf of a dienstverlener, the authorization
> decision MUST check the consent against the represented party. It MUST NOT
> check the consent against the party that makes the connection.

> The connecting party MUST have a registered mandate for that
> dienstverlener and that use. If there is no mandate, the request MUST be
> denied. A mandate MUST have a validity. Outside that validity, a request
> MUST be denied as if there is no mandate.

> A contract in which a party connects on behalf of another party MAY come
> into force only if that representation is registered.

| Case | Outcome |
|---|---|
| Consent for dienstverlener X, and integrator registered for X and this rule | allowed |
| Consent given to another dienstverlener | denied: `CONSENT_ACTOR_MISMATCH` |
| Integrator registered only for another rule | denied: `INTEGRATOR_NOT_REGISTERED` |
| Integrator suspended | denied: `INTEGRATOR_NOT_REGISTERED` |
| Mandate not in force at that time, or expired | denied: `INTEGRATOR_NOT_REGISTERED` *(proposal: not built)* |
| The admission register delivers no data | denied: `INTEGRATOR_REGISTER_UNAVAILABLE` |
| Consent given to the integrator itself instead of the dienstverlener | denied: `CONSENT_ACTOR_MISMATCH` |
| No registration of the representation | contract stays proposed: `DELEGATION_NOT_REGISTERED` |
| Dienstverlener suspended, for a delegated contract | contract stays proposed: `PARTY_NOT_ACTIVE` |
| The dienstverlener calls itself, with or without an integrator in the chain | allowed, unchanged |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-18, and FR-37 criteria 3 and 4.
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          ("als een actor namens een andere partij handelt, gebruikt de
          autorisatiebeslissing zowel de handelende actor als de
          vertegenwoordigde partij", and "rol, reikwijdte en geldigheid van de
          bevoegdheid").
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
          ("een technische intermediair voor alleen transport of connectiviteit
          krijgt door die rol geen bevoegdheid om namens een andere partij te
          handelen"). The representation context holds "rol of hoedanigheid,
          reikwijdte en geldigheid".
        - Tightened: the requirement also applies when the contract comes into
          force.
    - **Addressee**: GBO-delivered component: the reference policy for
      requests and contracts, and the admission register with the mandates.
      Interface agreement: the FSC delegation
      (`DelegatedServiceConnectionGrant`). Nothing changes for the consent
      components, because the proof already binds the dienstverlener
      ([REQ-68](#req-68)).
    - **Evidence**: [ICTU/GBO-demo#379](https://github.com/ICTU/GBO-demo/issues/379),
      [PR #464](https://github.com/ICTU/GBO-demo/pull/464). The demo builds
      this as an opt-in path (`make demo-integrator`, documented in
      [`integrator.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/integrator.md)).
      Code and tests:
        - The represented party is in
          [`lib.rego#L55-L72`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L55-L72).
        - The mandate is in
          [`engine.rego#L246-L267`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L246-L267).
        - The contract is in
          [`autosign.rego#L119-L139`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L119-L139).
        - The tests are in
          [`engine_test.rego#L613-L721`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L613-L721),
          [`dvt0001_test.rego#L113-L126`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L113-L126),
          and
          [`autosign_test.rego#L171-L203`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L171-L203).
    - **Related**: [REQ-61](admission.md#req-61), [REQ-68](#req-68),
      [REQ-110](admission.md#req-110), [AV-06](admission.md#av-06),
      [F-56](../traceability/findings-closed.md#f-56),
      [F-73](../traceability/findings-closed.md#f-73),
      [Q-12](../traceability/answered-questions.md#q-12),
      [Q-46](../traceability/open-questions.md#q-46),
      [Q-68](../traceability/open-questions.md#q-68),
      [ADR 0034](../decisions/0034-integrator-delegation.md).
    - **Notes**:
        - The represented party is the FSC delegator. If there is no
          delegator, it is the subject ID of the caller.
        - The mandates are in the admission register and reach the PDP as
          `acts_for`.
        - [Q-46](../traceability/open-questions.md#q-46) asks whether the
          integrator also belongs in the proof, or whether the mandate in the
          register is sufficient.
        - The design does not enforce the processor side of FR-18 (processor
          agreement, no lasting storage) technically. That side is in
          [AV-06](admission.md#av-06).
        - For a contract, the policy sees only the pair, and not who
          represents whom. At every request, the policy does check the
          direction.
        - An integrator is always a processor
          ([AV-06](admission.md#av-06)), so its role needs no
          separate check.

### REQ-107: Consent can be given only after confirmation that the citizen saw the information {#req-107}

> The UI of the toestemmingsportaal MUST make the action "give consent"
> available only after the citizen confirmed that they saw the information
> shown. The confirmation mechanism MUST be accessible according to WCAG
> 2.1 AA. If a request to give consent has no confirmation, the toestemmingsportaal
> backend MUST refuse it, before any processing.

| Case | Outcome |
|---|---|
| Not confirmed | button disabled |
| Confirmed, and at least one scope chosen | button active, consent recorded |
| Confirmation undone again | button disabled again |
| Request to the backend without confirmation, for example directly on the API | refused: `CONFIRMATION_MISSING`. No record, and no activation or transformation at BSNk |
| Keyboard or screen reader only | confirming and giving work |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-08 criteria 1 to 3.
        - FR-09 (dependency: store only after the confirmation of FR-08).
        - [PSA F2](https://ictu.github.io/GBO-PSA/main/generieke-functies/#f2-toegang-interactie)
          ("toestemming is vrij, specifiek, geïnformeerd, ondubbelzinnig en
          aantoonbaar").
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("de interactie voldoet aan toegankelijkheidseisen").
        - Tightened: FR-08 asks to block the button in the UI. This
          requirement also lets the backend enforce it.
    - **Addressee**: GBO-delivered component: the portal UI inside MijnOverheid
      and the toestemmingsportaal backend.
    - **Evidence**: not built:
      [ICTU/GBO-demo#598](https://github.com/ICTU/GBO-demo/issues/598). The
      demo has no confirmation. When the citizen chooses one scope, the button
      becomes active
      ([`PortaalConsent.tsx#L164-L171`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L164-L171)).
    - **Related**: [REQ-12](#req-12), [REQ-24](consent.md#req-24),
      [Q-49](../traceability/open-questions.md#q-49),
      [Q-51](../traceability/open-questions.md#q-51).
    - **Notes**:
        - The requirement chooses no mechanism. FR-08 gives a checkbox, or
          mandatory scrolling with a confirm button, as examples.
        - A separate field with the moment of confirmation is not necessary.
          The backend refuses without confirmation, so every recorded consent
          is confirmed.
        - Whether the register must record *which* information the citizen
          saw is open: [Q-51](../traceability/open-questions.md#q-51).
        - The confirmation comes from the client, as a field in the request.
          The check catches a client that skips the step (a UI error, another
          client). It does not catch a caller that sends the field itself.
        - The design accepts this gap. The identity comes from the login
          ([REQ-24](consent.md#req-24)), so only the citizen can forge
          the field, and only for their own consent.

### REQ-117: Before choosing, the citizen sees in plain language who asks what, for what, and for how long {#req-117}

> Before the choice, the portal UI MUST show the name of the consumer, the
> service with its purpose, and the validity period. Per data set, it MUST
> show the data elements that the consumer gets, and whether the set is
> mandatory or optional. Per element, it MUST show the bronhouder that
> supplies it, without the values.

> The portal UI MUST show that the consumer is an admitted participant. This
> statement MUST be based on the admission that the toestemmingsportaal backend
> establishes in the register ([REQ-111](consent.md#req-111)). The
> portal UI MUST state that the route is voluntary, and which equivalent
> alternative exists.

> The portal UI MUST NOT offer as a choice the form in which a source
> recognizes the citizen (BSN or pseudonym). That form follows from the
> authorization of the source ([REQ-82](pseudonymization.md#req-82)).

> The texts MUST be at language level B1. The legal description MUST stay
> available. The description of sets and elements MUST come from the service
> description that the toestemmingsvoorziening knows. It MUST NOT come from the
> request of the consumer.

| Case | Outcome |
|---|---|
| Request for known sets | consumer, purpose, valid until, and per set the title and description in B1 (code) |
| Data elements per set | per set the elements, without values *(proposal: the demo shows only title and description)* |
| A set with elements of more than one bronhouder | per element the bronhouder *(proposal: not built)* |
| Admitted, active consumer | the screen states that the consumer is admitted *(proposal: not built)* |
| Mandatory and optional sets | the screen shows a mandatory set as mandatory, and the citizen cannot switch it off *(proposal)* |
| Voluntariness and alternative | stated on the screen *(proposal: not built)* |
| The citizen refuses | back to the consumer with `status=denied`, and no consent (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-05 criteria 1 to 5, FR-07 criteria 1 and 2, FR-30 criterion 3,
          and FR-38 criterion 1.
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("de burger ziet in begrijpelijke taal de afnemer, dienst, doel,
          gegevensscope, duur en gevolgen", "de inrichting biedt een
          gelijkwaardig alternatief als wetgeving of beleid dat vereist", and
          "de interface presenteert deze niet als inhoudelijke keuze").
        - [PSA F2](https://ictu.github.io/GBO-PSA/main/generieke-functies/#f2-toegang-interactie)
          ("toestemming is vrij, specifiek, geïnformeerd …").
        - [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the portal UI inside
      MijnOverheid. The toestemmingsportaal backend delivers name and purpose from
      the registration ([REQ-111](consent.md#req-111)).
    - **Evidence**: partly built. Code and tests:
        - The screen is in
          [`PortaalConsent.tsx#L115-L149`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L115-L149).
          The refusal is in
          [`#L100-L106`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L100-L106).
        - The UI shows one set per card in
          [`ScopeToggle.tsx#L9-L25`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/components/consent/ScopeToggle.tsx#L9-L25).
        - The descriptions are in
          [`scopeGroups.ts#L8-L30`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/data/scopeGroups.ts#L8-L30).
        - No test covers what the screen shows.
        - Not built: the elements per set, mandatory or optional, and the
          voluntariness and alternative.
    - **Related**: [REQ-10](#req-10), [REQ-12](#req-12),
      [REQ-19](consent.md#req-19),
      [REQ-37](consent.md#req-37),
      [REQ-82](pseudonymization.md#req-82), [REQ-107](#req-107),
      [REQ-111](consent.md#req-111), [REQ-121](#req-121),
      [REQ-122](#req-122), [F-98](../traceability/findings.md#f-98),
      [Q-13](../traceability/open-questions.md#q-13),
      [Q-45](../traceability/open-questions.md#q-45),
      [Q-76](../traceability/open-questions.md#q-76).
    - **Notes**:
        - Design choice in the demo: the UI fixes the sets and descriptions.
          The elements are in the data (`fields`), but the UI does not show
          them.
        - In the demo, the validity period comes from the request.
        - Who sets the period, and whether the citizen must be able to change
          it (FR-05 criterion 5, FR-11 criterion 1), is open:
          [Q-13](../traceability/open-questions.md#q-13).
        - Whether the period can differ per source is open:
          [Q-76](../traceability/open-questions.md#q-76).
        - FR-05 does not work out which "gevolgen" (consequences, S02) the
          citizen sees.
        - Supervision of voluntariness is an open decision of S02.
        - S02 also calls pseudonymization "transparant voor de burger". The
          GBO team asked the PSA authors whether that means invisible or
          explained ([F-98](../traceability/findings.md#f-98)).
        - A public list of admitted participants (FR-30 criterion 3, "ook voor
          anderen") is a task of the management organization.

### REQ-118: If a service excludes delegation, an authorized representative cannot give consent for it {#req-118}

> This requirement applies to a service whose description excludes
> delegation. For such a service, the portal UI MUST NOT show a consent
> screen to a citizen who logged in on behalf of another person. If a
> consent is given under such a login, the toestemmingsportaal backend MUST
> refuse it with `DELEGATION_NOT_ALLOWED`, before any processing. The
> citizen MUST then get a clear message that no representative can give
> consent for this service. A citizen who logged in with their own means
> MUST be admitted.

> Whether a service excludes delegation MUST come from the service
> description that the toestemmingsvoorziening knows. It MUST NOT come from the
> request of the consumer.

> In two cases, the toestemmingsvoorziening MUST refuse with
> `DELEGATION_NOT_ALLOWED` (fail-closed). In the first case, it cannot
> establish whether the login is on behalf of another person. In the second
> case, the login is on behalf of another person, and the service
> description does not state whether the service excludes delegation.

| Case | Outcome |
|---|---|
| Service excludes delegation, and login on behalf of another person | no consent screen, and a message to the representative. The backend refuses: `DELEGATION_NOT_ALLOWED`. No consent, and no activation or transformation at BSNk |
| Service excludes delegation, and the citizen logs in for themselves | consent screen |
| Service allows delegation, and login with a valid authorization | consent screen. [Q-73](../traceability/open-questions.md#q-73) asks whose consent it then is |
| The toestemmingsvoorziening cannot establish whether the login is on behalf of another person | refused: `DELEGATION_NOT_ALLOWED`, and no consent screen |
| The service does not state whether it excludes delegation, and login on behalf of another person | refused: `DELEGATION_NOT_ALLOWED`, and no consent screen |
| The service does not state whether it excludes delegation, and the citizen logs in for themselves | consent screen |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-02 criteria 2, 3, and 5, with the dependency on FR-32 (the
          setting per service follows from the grondslag).
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          ("als een actor namens een andere partij handelt, gebruikt de
          autorisatiebeslissing zowel de handelende actor als de
          vertegenwoordigde partij").
        - Tightened: FR-02 asks to block access to the screen. This
          requirement also lets the backend enforce it. The backend also
          refuses if the login or the service does not establish it.
    - **Addressee**: GBO-delivered component: the portal UI inside
      MijnOverheid and the toestemmingsportaal backend. MijnOverheid delivers
      whether the login is on behalf of another person
      ([Q-61](../traceability/open-questions.md#q-61) sub-question 7). The
      management organization records the setting per service in the catalog.
    - **Evidence**: not built. The demo has no authorization (machtiging).
    - **Related**: [REQ-24](consent.md#req-24),
      [REQ-40](consent.md#req-40),
      [REQ-119](consent.md#req-119), [REQ-121](#req-121),
      [Q-44](../traceability/open-questions.md#q-44),
      [Q-61](../traceability/open-questions.md#q-61),
      [Q-73](../traceability/open-questions.md#q-73).
    - **Notes**: if MijnOverheid already blocks earlier
      ([Q-61](../traceability/open-questions.md#q-61) sub-question 7), the
      refusal in the backend is still necessary for a client that skips the
      step. [REQ-119](consent.md#req-119) and
      [Q-44](../traceability/open-questions.md#q-44) cover whether the citizen
      returns after the message, and with which outcome.

### REQ-121: Screen, initiation check, and reference policy follow the same data-set description {#req-121}

> The portal UI, the toestemmingsportaal backend, and the reference policy MUST
> take the data sets from the same description of the service. Per set, that
> description holds the data elements with their bronhouder. It also holds
> whether the set is mandatory or optional, and the consumers that are
> allowed to ask for the set.

> An administrator MUST be able to add or change a set without a code change
> in the portal UI or the toestemmingsportaal backend.

| Case | Outcome |
|---|---|
| An administrator adds a set to a service | set usable in initiation and screen, without a new release of UI or backend *(proposal)* |
| The reference policy allows under a set a field that the description does not name, or misses one | a test of the policy set fails *(proposal)* |
| The screen shows for a set an element that the description does not name | a test fails *(proposal)* |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-32 description and criterion 1, and FR-38 criterion 1.
        - FR-21 (description: the same elements as when the citizen gave
          consent).
    - **Addressee**: GBO-delivered component: the portal UI, the toestemmingsportaal
backend, and the reference policy. The content of the description
      is a task of the management organization
      ([Q-62](../traceability/open-questions.md#q-62)).
    - **Evidence**: not built:
      [ICTU/GBO-demo#382](https://github.com/ICTU/GBO-demo/issues/382).
    - **Related**: [REQ-10](#req-10), [REQ-37](consent.md#req-37),
      [REQ-38](consent.md#req-38), [REQ-64](sources-identity.md#req-64),
      [REQ-117](#req-117), [F-74](../traceability/findings.md#f-74),
      [F-98](../traceability/findings.md#f-98),
      [Q-21](../traceability/answered-questions.md#q-21),
      [Q-45](../traceability/open-questions.md#q-45),
      [Q-62](../traceability/open-questions.md#q-62),
      [Q-69](../traceability/open-questions.md#q-69).
    - **Notes**:
        - In the demo, the sets are in the UI
          ([`scopeGroups.ts#L35-L43`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/data/scopeGroups.ts#L35-L43)),
          and the fields are separately in the rule.
        - A source with its own policy
          ([Q-21](../traceability/answered-questions.md#q-21)) is bound to
          [REQ-10](#req-10). This requirement does not bind it.
        - [Q-45](../traceability/open-questions.md#q-45) asks whether the
          design enforces mandatory and optional sets.
        - FR-39 criterion 5 puts the link from catalog to scopes in a central
          policy. Under the decision on
          [Q-21](../traceability/answered-questions.md#q-21), the link belongs in
          the service description ([F-98](../traceability/findings.md#f-98)).

### REQ-122: The citizen gets a confirmation of their choice {#req-122}

> After the citizen gave, refused, or revoked consent, the toestemmingsvoorziening
> MUST give the citizen a confirmation of that choice. After giving, the
> confirmation MUST name the consumer, the service with its purpose, and the
> granted data sets. It MUST also name the valid-until moment. It MUST name
> these items as they are recorded.

> After a revocation, the confirmation MUST name which consent is revoked. A
> confirmation MUST follow only a choice that is recorded. If recording
> fails, the citizen MUST be told so and see no confirmation.

| Case | Outcome |
|---|---|
| Consent given and recorded | confirmation with consumer, service, purpose, sets, and valid until. Then the return ([REQ-119](consent.md#req-119)) |
| The citizen refuses | confirmation that no consent was given. Return with the outcome refusal |
| Consent revoked | confirmation of the revocation (FR-23, step C-10a) |
| Recording or revoking fails | error message. No confirmation, and no return as successful |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("de burger ontvangt een bevestiging van de gemaakte keuze").
        - FR-23 with step C-10a, and FR-14.
    - **Addressee**: GBO-delivered component: the portal UI inside
      MijnOverheid and the toestemmingsportaal backend.
    - **Evidence**: not checked.
    - **Related**: [REQ-107](#req-107), [REQ-109](consent.md#req-109),
      [REQ-117](#req-117), [REQ-119](consent.md#req-119),
      [REQ-120](consent.md#req-120),
      [Q-43](../traceability/open-questions.md#q-43),
      [Q-44](../traceability/open-questions.md#q-44),
      [Q-61](../traceability/open-questions.md#q-61).
    - **Notes**:
        - The requirement chooses no form. The possible forms are these:
            - a screen before the return
            - a message in MijnOverheid
            - an entry in the overview to which the citizen can go directly
            - a combination of these forms
        - FR-14 asks for an automatic return. A screen before the return must
          fit with that ([Q-61](../traceability/open-questions.md#q-61)
          sub-question 2).
        - [Q-43](../traceability/open-questions.md#q-43) asks whether the
          register records a refusal. The confirmation to the citizen is
          separate from that question.

### Removed numbers

- REQ-13 (status check per request against the toestemmingsregister as PIP): removed. The successors are [REQ-68](#req-68) and [REQ-18](authorization.md#req-18).
- REQ-15 (no BSN in the consumer request): merged into [REQ-79](pseudonymization.md#req-79).

## Consent lifecycle requirements {#consent-lifecycle}

A consent has a limited validity. The lifecycle requirement covers the
validity of a consent and its repeated use within that validity. The
statuses that a citizen sees (Actief, Verlopen, Ingetrokken) and
revocation are in [citizen access and revocation](consent.md#citizen-access) and
[REQ-14](consent.md#req-14).

In the demo, the toestemmingsregister sets an absolute valid-until moment
when it records the consent. It writes that moment into the consent proof
as both `valid_until` and the expiry time `exp`. The PDP checks it at
every request. A consumer can use a consent again and again within its
validity. Single use is not built
([SL-01b](../traceability/increments.md#sl-01b) is blocked). Who sets the
validity period is open again
([Q-13](../traceability/open-questions.md#q-13)).

### REQ-19: A consent has a finite validity, and after that the PDP denies {#req-19}

> Every consent MUST have a finite valid-until moment. The PDP MUST check
> that moment at every request and deny a request after that moment.
> Within the validity, the consent MUST be usable repeatedly. If the
> valid-until moment is missing or cannot be read, the PDP MUST deny.

| Case | Outcome |
|---|---|
| Within the validity | allowed (code) |
| Second request within the validity | allowed (design FR-11 criterion 2, code: no reuse check) |
| After the valid-until moment, within 30 s clock skew | denied: `CONSENT_EXPIRED` (code) |
| More than 30 s after the valid-until moment | denied: `CONSENT_TOKEN_EXPIRED` (code) |
| Valid-until missing, or different from the expiry time of the proof | denied: `CONSENT_CONTEXT_INVALID` (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design. FR-11 criteria 2 and 3, FR-17 criteria 1 and 4, and
      [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
      ("geldigheidsduur", "de registratie ondersteunt … verloop").
    - **Addressee**: GBO-delivered component: the toestemmingsregister (sets
      the moment) and the reference policy (checks it).
    - **Evidence**: [PR #238](https://github.com/ICTU/GBO-demo/pull/238),
      [PR #371](https://github.com/ICTU/GBO-demo/pull/371). Code and tests:
        - The moment is in
          [`main.go#L421-L424`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L421-L424)
          and
          [`consent_token.go#L142`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/consent_token.go#L142).
        - The check is in
          [`dvtp_helper.rego#L46-L48`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvtp_helper.rego#L46-L48)
          and
          [`consent.rego#L124`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L124).
        - The tests are in
          [`consent_test.rego#L347-L358`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L347-L358),
          [`#L400-L402`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L400-L402),
          and
          [`dvt0001_test.rego#L76-L78`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L76-L78).
    - **Related**: [REQ-68](consent.md#req-68),
      [REQ-117](consent.md#req-117),
      [F-04](../traceability/findings-closed.md#f-04),
      [F-11](../traceability/findings-closed.md#f-11),
      [Q-04](../traceability/answered-questions.md#q-04),
      [Q-13](../traceability/open-questions.md#q-13),
      [Q-42](../traceability/open-questions.md#q-42),
      [Q-76](../traceability/open-questions.md#q-76).
    - **Notes**:
        - FR-11 criterion 1 lets the default period for each service come from
          the catalog. It also lets the citizen change the period within
          bounds. It is open whether the citizen must be able to do that
          ([Q-13](../traceability/open-questions.md#q-13)). This requirement
          does not demand it.
        - [Q-76](../traceability/open-questions.md#q-76) asks whether the
          validity can differ for each source.
        - In the demo, the consumer chooses the period with
          `validity_seconds`. The default is one year, with no upper bound
          ([ICTU/GBO-demo#382](https://github.com/ICTU/GBO-demo/issues/382)
          point 5,
          [ICTU/GBO-demo#380](https://github.com/ICTU/GBO-demo/issues/380)).
        - Design choice: the expiry time of the proof is the valid-until
          moment, with 30 s clock skew. So expiry gives two reason codes,
          depending on the moment: `CONSENT_EXPIRED` within the skew, and
          `CONSENT_TOKEN_EXPIRED` after it. The design accepts that.
        - FR-11 criterion 2 also asks to record when a consumer first fetched
          data: [Q-42](../traceability/open-questions.md#q-42).

## Consent initiation and return requirements {#consent-initiation}

A consent starts at the consumer. The consumer sends the citizen to the
toestemmingsportaal with a request that names who asks what. After the
choice, the portal sends the citizen back to the consumer with the
outcome. The requirements cover that request, the data that the portal
takes from the registration instead of the request, and the return.

In the demo, the consumer sends the context as query parameters: consumer
OIN, scopes, purpose, and return address. The portal keeps the context in
the browser session during the mock login. It refuses a scope that it
cannot describe, and shows only the requested scopes. On success, the
proof goes back in the URL fragment. On refusal, the return carries
`status=denied`. In demo v0.9.0, the toestemmingsportaal backend does not check
the request ([ICTU/GBO-demo#427](https://github.com/ICTU/GBO-demo/issues/427)).

### REQ-37: A consent request names the consumer, the service, the requested data sets, and the return address {#req-37}

> A request of a consumer for consent MUST name at least the consumer, the
> service, the requested data sets, and the return address. If an
> integrator acts on behalf of the consumer, the request MUST also name
> the integrator. These data MUST still be available after the citizen
> logged in. If an item is missing, the citizen MUST NOT see a consent
> screen. The same applies if the request asks for a data set that the
> toestemmingsvoorziening does not know.

> The toestemmingsportaal backend MUST refuse such a request:
> `INITIATION_INCOMPLETE` if a mandatory item is missing, `UNKNOWN_SCOPE`
> for an unknown data set. A data set can be known to the toestemmingsvoorziening,
> but not belong to that service according to the service description. It
> can also be known but not recorded for this consumer. In both cases, the
> toestemmingsportaal backend MUST refuse the request with
> `SCOPE_NOT_REGISTERED`, before the citizen sees a consent screen.

> The name and purpose of the consumer MAY be missing. They come from the
> registration ([REQ-111](#req-111)).

| Case | Outcome |
|---|---|
| Complete request, known data sets | after the login, the consent screen with this context at once *(from code)* |
| One of the mandatory items is missing | refused: `INITIATION_INCOMPLETE`, no consent screen (demo: only the UI, "Geen sessie") |
| Unknown data set | refused: `UNKNOWN_SCOPE`, no consent screen (demo: only the UI, "Onbekend verzoek", [PR #435](https://github.com/ICTU/GBO-demo/pull/435)) |
| Known data set that does not belong to the requested service, or is not recorded for this consumer | refused: `SCOPE_NOT_REGISTERED`, no consent screen *(not built)* |
| Request on behalf of a consumer through an integrator | the request also names the integrator *(proposal from FR-12 criterion 2: not built)* |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-12 criterion 2.
        - FR-13 criterion 1, with its rationale (scope ID and return address).
        - FR-14 criterion 1.
        - FR-10 description ("binnen het wettelijke plafond van de dienstencatalogus").
        - FR-17 criterion 2, FR-32 criterion 2, and FR-38 criterion 5.
    - **Addressee**: interface agreement: the initiation koppelvlak between
      consumer and toestemmingsvoorziening. GBO-delivered component: the portal UI
      inside MijnOverheid, which shows no consent screen.
    - **Evidence**: partly, only in the UI. Code and tests:
        - The mandatory fields are in
          [`useRedirectContext.ts#L29-L41`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/hooks/useRedirectContext.ts#L29-L41).
        - The refusal is in
          [`PortaalConsent.tsx#L49-L75`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L49-L75).
        - A test of the unknown data set is in
          [`scopeGroups.test.mjs#L16`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/tests/scopeGroups.test.mjs#L16).
        - The consumer mocks build the request in
          [`buildPortalUrl.ts#L69-L80`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/dienstverlener-mock/src/lib/buildPortalUrl.ts#L69-L80).
        - The backend checks nothing.
          [ICTU/GBO-demo#427](https://github.com/ICTU/GBO-demo/issues/427)
          adds that check.
    - **Related**: [REQ-10](consent.md#req-10), [REQ-106](consent.md#req-106),
      [REQ-111](#req-111), [REQ-121](consent.md#req-121),
      [Q-44](../traceability/open-questions.md#q-44),
      [Q-45](../traceability/open-questions.md#q-45),
      [Q-60](../traceability/open-questions.md#q-60),
      [Q-61](../traceability/open-questions.md#q-61).
    - **Notes**:
        - The form of the request is open: query parameters, a signed request,
          or a reference to a request sent in advance. How the request
          survives the login at MijnOverheid is also open:
          [Q-60](../traceability/open-questions.md#q-60),
          [Q-61](../traceability/open-questions.md#q-61) sub-questions 2 and 4.
        - Name and purpose come from the registration ([REQ-111](#req-111)).
          The demo also demands them in the request.
        - The demo knows the data sets from a fixed list in the UI
          ([`scopeGroups.ts#L35-L43`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/data/scopeGroups.ts#L35-L43))
          and does not take them from the service catalog.
        - In the demo, the service does not get into the consent. The register
          receives the purpose as `use_case`
          ([`PortaalConsent.tsx#L82-L87`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L82-L87)).
        - `SCOPE_NOT_REGISTERED` is a reason of its own next to
          `UNKNOWN_SCOPE`. With it, the consumer can tell "this set does not
          exist" from "you are not allowed to ask this set for this service".
        - The PDP of the source does not repeat this check. The proof binds
          only sets that the backend allowed. [REQ-10](consent.md#req-10)
          limits what the PDP allows under a set.

### REQ-111: What the citizen sees about the consumer, and the return address, come from the registration and not from the request {#req-111}

> Before it shows a consent screen, the toestemmingsportaal backend MUST take
> the name of the consumer and the purpose from the registration. It MUST
> check that the consumer is admitted and active for the requested
> service. It MUST check the return address against the addresses recorded
> for that consumer in the admission register. The backend MUST refuse a
> request that fails these checks before the citizen sees a consent
> screen. The same applies to a request with a name or purpose that
> differs from the registration.

| Case | Outcome |
|---|---|
| Active consumer, registered return address | consent screen, with name and purpose from the registration |
| Name or purpose in the request differs from the registration | refused: `INITIATION_MISMATCH` |
| Consumer suspended or not admitted | refused: `PARTY_NOT_ACTIVE` |
| Consumer active, but not admitted for this service | refused (no decision on the reason), no consent screen *(not built)* |
| Return address not registered for that consumer | refused: `RETURN_URL_NOT_REGISTERED`, no return to that address |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-14 criterion 1, with its rationale (protection against open
          redirects).
        - FR-34, FR-12, and FR-16 criterion 2 ("bevoegd is voor de gevraagde dienst en gegevens").
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
          ("vertrouwensankers en deelnemersstatus zijn machineleesbaar controleerbaar").
        - Tightened: the requirement fixes which data come from the
          registration. Provable origin of the request is out of scope.
    - **Addressee**: GBO-delivered component: the toestemmingsportaal backend.
      Management organization: the return addresses in the admission
register.
    - **Evidence**: not built:
      [ICTU/GBO-demo#427](https://github.com/ICTU/GBO-demo/issues/427). The
      portal reads consumer, name, scope, and return address from the URL
      ([`useRedirectContext.ts#L29-L38`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/hooks/useRedirectContext.ts#L29-L38)).
      Only the frontend checks the address, against a fixed list of origins.
    - **Related**: [REQ-37](#req-37), [REQ-61](admission.md#req-61),
      [REQ-110](admission.md#req-110), [REQ-117](consent.md#req-117),
      [REQ-119](#req-119), [Q-44](../traceability/open-questions.md#q-44),
      [Q-53](../traceability/open-questions.md#q-53),
      [Q-59](../traceability/open-questions.md#q-59),
      [Q-60](../traceability/open-questions.md#q-60),
      [Q-69](../traceability/open-questions.md#q-69).
    - **Notes**:
        - With these checks, a forged request can lead only to a consent to
          the real consumer, with the right name. The return also goes only to
          the address of that consumer.
        - It is open whether it must also be provable that the consumer made
          the request (FR-34 criterion 1):
          [Q-60](../traceability/open-questions.md#q-60).
        - The return addresses are in the admission register and not in the
          service catalog. They belong to the consumer, and the admission is
          already there ([REQ-61](admission.md#req-61)).
        - The check for each service needs an admission register that knows,
          for each consumer, the services for which it is admitted (FR-30,
          FR-32). [REQ-61](admission.md#req-61) records the admission for each
          bronhouder.
        - [Q-69](../traceability/open-questions.md#q-69) asks whether the PDP
          also checks this at the request to the source.

### REQ-119: After every outcome the citizen returns to the consumer with that outcome {#req-119}

> When the consent process ends, the toestemmingsvoorziening MUST return the
> citizen automatically to the registered return address of the consumer
> ([REQ-111](#req-111)). This applies to every outcome, also after a
> refusal or an error. The return MUST name the outcome. For any outcome
> other than a given consent, the toestemmingsvoorziening MUST NOT record a
> consent. If the toestemmingsvoorziening cannot establish the return address, it
> MUST NOT return the citizen.

| Case | Outcome |
|---|---|
| The citizen gives consent | back with the outcome success. The proof reaches the consumer as [Q-44](../traceability/open-questions.md#q-44) decides |
| The citizen refuses | back with the outcome refusal (demo: `status=denied`, code) |
| The consent cannot be recorded (for example no value for a source, [REQ-82](pseudonymization.md#req-82), or the register does not answer) | back with the outcome error, no consent |
| Refused by [REQ-118](consent.md#req-118) (delegation) | back with an outcome. Refusal or error: [Q-44](../traceability/open-questions.md#q-44) |
| Consumer or return address cannot be established ([REQ-111](#req-111)) | no return. What the citizen sees: no decision |
| The citizen closes the window or the session expires | no return ([Q-43](../traceability/open-questions.md#q-43), [Q-44](../traceability/open-questions.md#q-44)) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design. FR-14 criteria 2 ("ongeacht de uitkomst (succes, weigering of fout)") and 3.
    - **Addressee**: GBO-delivered component: the portal UI inside
      MijnOverheid and the toestemmingsportaal backend. Interface agreement: the
      outcome values in the return.
    - **Evidence**: partly. A refusal returns with `status=denied`
      ([`PortaalConsent.tsx#L100-L106`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L100-L106)).
      A success returns with the proof in the URL fragment
      (`PortaalBevestiging.tsx`). "Annuleren" (cancel) does not return
      ([`PortaalConsent.tsx#L108`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L108)).
      The return after an error is not checked.
    - **Related**: [REQ-37](#req-37), [REQ-82](pseudonymization.md#req-82),
      [REQ-111](#req-111), [REQ-117](consent.md#req-117),
      [REQ-118](consent.md#req-118), [REQ-122](consent.md#req-122),
      [Q-43](../traceability/open-questions.md#q-43),
      [Q-44](../traceability/open-questions.md#q-44).
    - **Notes**:
        - These points are open in
          [Q-44](../traceability/open-questions.md#q-44) (partly answered):
            - which outcomes the consumer tells apart, and what they are
              called
            - how the proof arrives on success: through the browser, or
              through a code that the consumer exchanges
            - whether the consumer gets the allowed sets back separately
        - "Aborted" is not an outcome.

## Role split between toestemmingsregister and toestemmingsportaal (S01/S02) {#consent-roles}

The PSA splits the consent function into two capabilities:
[S01 consent registration](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
(the toestemmingsregister) and
[S02 toestemmingsportaal](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
(the toestemmingsportaal: the portal UI inside MijnOverheid and the toestemmingsportaal
backend). The requirements for this split keep the BSN out of the
register, and fix where the citizen identity comes from.

In the demo, the toestemmingsportaal backend receives the BSN from the
validated portal token. It derives a reference to the citizen (an HMAC of
the BSN). On the first consent, it asks BSNk for values. It sends only the
reference and the encrypted values to the register. The register stores
the polymorphic values under the reference. It is open whether register
and backend stay two systems, and which of them is the BSNk participant
([Q-49](../traceability/open-questions.md#q-49),
[ADR 0040](../decisions/0040-route-d-citizen-recognition.md), proposed).

### REQ-23: The toestemmingsregister gets no BSN, not even temporarily {#req-23}

> A request to the toestemmingsregister MUST NOT contain a BSN. The same
> applies to every answer of the register and to every data item that it
> stores, also temporarily while it handles a request.

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
          ("het register bevat geen BSN als een pseudonieme identificatie volstaat").
        - [PSA S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering)
          ("alleen componenten en organisaties met een geldige grondslag verwerken het BSN").
        - FR-35 criterion 1.
        - Tightened: the BSN is also not in a request or an answer, so that
          the BSN stays limited to one component.
    - **Addressee**: GBO-delivered component: the toestemmingsregister, and
      the toestemmingsportaal backend that calls it.
    - **Evidence**: [PR #148](https://github.com/ICTU/GBO-demo/pull/148),
      [PR #469](https://github.com/ICTU/GBO-demo/pull/469). Code and tests:
        - A test of the creation of a consent and of keeping the polymorphic
          values is in
          [`portal_test.go#L348`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal_test.go#L348).
        - The adapter to the register has no method that takes a BSN
          ([`register.go#L1-L10`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/register/register.go#L1-L10)).
        - The stored model has no BSN
          ([`main.go#L33-L46`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L33-L46)).
        - Overview and revocation send only the reference or the consent ID
          ([`register.go#L60-L63`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/register/register.go#L60-L63)).
          There is no test of its own for that.
    - **Related**: [REQ-20](pseudonymization.md#req-20),
      [REQ-39](consent.md#req-39),
      [REQ-69](pseudonymization.md#req-69),
      [Q-49](../traceability/open-questions.md#q-49),
      [Q-56](../traceability/open-questions.md#q-56).
    - **Notes**:
        - The register knows the citizen under a reference that the toestemmingsportaal
backend derives from the BSN. Under that reference, the
          register keeps the polymorphic values of the first activation
          ([REQ-69](pseudonymization.md#req-69)). It receives the encrypted
          values for each party only to sign the proof.
        - It is open who makes the reference from the BSN. The demo does it in
          the backend. The working assumption
          ([route D](pseudonymization.md#route-d)) puts it in the register.
        - If the design follows the working assumption, or if register and
          backend become one system, this requirement does not apply in this
          form: [Q-49](../traceability/open-questions.md#q-49). The requirement
          applies to the register as long as it is a component of its own.

### REQ-24: The citizen identity comes from the authentication service assertion at the required assurance level and not from client input {#req-24}

> The toestemmingsportaal backend MUST take the identity of the citizen from the
> validated assertion of the authentication service. The backend MUST NOT
> use a BSN that the client sends as input as the identity. The toestemmingsportaal
> backend MUST accept only an assertion that states the assurance
> level of the authentication. The assertion can state a level lower than
> the set minimum, or no level. If so, the backend MUST show no personal
> data and no consent options. It MUST also record or revoke nothing.

| Case | Outcome |
|---|---|
| Assertion at the minimum level or higher | identity accepted |
| Assertion at a level lower than the minimum, or without a level | refused (no decision on the reason). Nothing shown, recorded, or revoked *(proposal: not built)* |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-01 criterion 2 ("op het door de overheid vereiste minimale betrouwbaarheidsniveau").
        - [P-05](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("de authenticatie heeft een passend betrouwbaarheidsniveau").
    - **Addressee**: GBO-delivered component: the toestemmingsportaal backend.
    - **Evidence**: [PR #148](https://github.com/ICTU/GBO-demo/pull/148). Code and tests:
        - The backend takes the BSN from the validated token, and refuses a
          request without one
          ([`portalhttp.go#L138-L147`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/portalhttp/portalhttp.go#L138-L147)).
        - The creation of a consent sends a token and no BSN
          ([`portalClient.ts#L20-L25`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/api/portalClient.ts#L20-L25)).
        - No automated test covers the refusal.
    - **Related**: [REQ-38](consent.md#req-38),
      [REQ-40](consent.md#req-40),
      [REQ-107](consent.md#req-107), [REQ-118](consent.md#req-118),
      [BSNK-04](pseudonymization.md#bsnk-04),
      [Q-50](../traceability/open-questions.md#q-50),
      [Q-59](../traceability/open-questions.md#q-59).
    - **Notes**:
        - The demo simulates the login. With a mock login, the backend signs a
          token with the BSN itself and also validates it
          ([`auth.go#L12-L24`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/portalhttp/auth.go#L12-L24)).
          That says nothing about the assurance level.
        - It is not known whether a token of the authentication service is
          available inside MijnOverheid. So the requirement prescribes no
          token. It prescribes only that the identity comes from the validated
          assertion and not from client input.
        - The working assumption is that MijnOverheid passes on the BSN after
          the login ([BSNk preconditions](pseudonymization.md#bsnk-preconditions)). How
          MijnOverheid does that decides how the backend checks this
          requirement: [Q-50](../traceability/open-questions.md#q-50).
        - The government sets the minimum level (FR-01 criterion 2), and GBO
          does not. Whether the MijnOverheid assertion states the level
          belongs to [Q-50](../traceability/open-questions.md#q-50).
        - BSNk also requires a login at the requested level before a
          transformation ([BSNK-04](pseudonymization.md#bsnk-04)).

### Removed numbers

- REQ-22 (the pseudonymization action belongs in S02): removed, pending [Q-49](../traceability/open-questions.md#q-49), watch item for [ADR 0040](../decisions/0040-route-d-citizen-recognition.md).
- REQ-35 (citizen ownership check on revocation): merged into [REQ-40](consent.md#req-40).

## Citizen access and revocation requirements {#citizen-access}

A citizen can see the consents that they gave and revoke them in the
toestemmingsportaal inside MijnOverheid (FR-20, FR-22, FR-23). The
requirements for this function cover these topics:

- the overview of consents
- the components that can reach the register for the overview
- ownership
- export
- revocation
- the notice about the rights of the citizen at the consumer

In the demo, the toestemmingsportaal backend derives the reference to the
citizen (an HMAC of the BSN) from the validated portal token. The backend
asks the register for the consents under that reference. It shows them as
Actief (active), Verlopen (expired), or Ingetrokken (revoked). On a
revocation, the backend checks ownership and asks the register to set the
status to revoked. The record stays.

Viewing and revoking do not call BSNk. The authorization chain denies the
next request on a revoked consent with `CONSENT_WITHDRAWN`
([REQ-14](consent.md#req-14)). The status names follow
[F-97](../traceability/findings.md#f-97). The status Opgehaald (retrieved)
waits for [Q-42](../traceability/open-questions.md#q-42).

### REQ-38: A logged-in citizen can view consents with status and revoke them {#req-38}

> The toestemmingsportaal backend MUST let a citizen with a verified identity
> ([REQ-24](consent.md#req-24)) view their consents and revoke a
> consent. The overview MUST order the consents by the moment of granting.
> It MUST hold the active consents, and the recently expired or revoked
> consents. For each consent, the overview MUST show the consumer, the
> purpose, the data sets, the validity, and the status. The data sets MUST
> show the same data elements as the consent screen showed before, without
> values.
>
> If the citizen has no verified identity, the backend MUST show
> nothing and change nothing. The status MUST follow from the register and
> the validity, on the same grounds on which the authorization chain
> denies.

| Case | Outcome |
|---|---|
| Logged in, overview | the own consents, each with the status Actief, Verlopen, or Ingetrokken *(from code)* |
| Validity passed | Verlopen *(from code)* |
| Revoked, also if the validity passed later | Ingetrokken *(from code)* |
| Logged in, revoke an own active consent | Ingetrokken *(from code)* |
| Detail of a consent | for each set, the same data elements as on the consent screen, without values *(proposal: not built)* |
| Not logged in, or invalid assertion | refused, nothing shown or changed *(from code: HTTP 401)* |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - FR-20: the description ("een chronologisch overzicht") and criteria 1
          and 2.
        - FR-21: criterion 3 and the description ("dezelfde data-elementen als getoond tijdens het geven van de toestemming, zonder de feitelijke waarden").
        - FR-22 criteria 1 and 2, FR-23 criterion 2, and FR-01 criterion 3.
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          (provision "inzage- en intrekkingsfunctie").
        - [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the toestemmingsportaal backend. The
      portal UI inside MijnOverheid shows the result.
    - **Evidence**: [PR #148](https://github.com/ICTU/GBO-demo/pull/148),
      [PR #469](https://github.com/ICTU/GBO-demo/pull/469). Code and tests:
        - The routes are in
          [`portalhttp.go#L322-L357`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/portalhttp/portalhttp.go#L322-L357).
        - The refusal without an assertion is in
          [`#L138-L147`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/portalhttp/portalhttp.go#L138-L147).
          No test covers this refusal.
        - The status is in
          [`consent.go#L135-L146`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/consent.go#L135-L146),
          tested in
          [`portal_test.go#L276`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal_test.go#L276).
    - **Related**: [REQ-24](consent.md#req-24), [REQ-40](#req-40),
      [REQ-108](#req-108), [REQ-109](#req-109),
      [REQ-111](consent.md#req-111),
      [REQ-117](consent.md#req-117), [REQ-120](#req-120),
      [REQ-121](consent.md#req-121),
      [F-19](../traceability/findings.md#f-19),
      [Q-25](../traceability/open-questions.md#q-25),
      [Q-42](../traceability/open-questions.md#q-42),
      [Q-53](../traceability/open-questions.md#q-53),
      [Q-61](../traceability/open-questions.md#q-61),
      [Q-63](../traceability/open-questions.md#q-63).
    - **Notes**:
        - The status Opgehaald follows after
          [Q-42](../traceability/open-questions.md#q-42). The processings for
          each consent (FR-20 criterion 2) follow after
          [Q-25](../traceability/open-questions.md#q-25).
        - The length of "recently" depends on the retention period:
          [Q-63](../traceability/open-questions.md#q-63).
        - The form of the link between the UI inside MijnOverheid and the
          backend is open:
          [Q-61](../traceability/open-questions.md#q-61) sub-question 1.
        - Design choice: the demo has no separate route for one consent. The UI
          filters the overview.
        - In the demo, the name of the consumer comes from a fixed list in the
          UI
          ([`onderwerpMap.ts#L14-L21`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/data/onderwerpMap.ts#L14-L21)).
          As on the consent screen, the name must come from the registration.
        - [Q-53](../traceability/open-questions.md#q-53) asks whether the
          overview shows a consent of a suspended consumer differently from
          Actief.

### REQ-39: Only the consent backend can create, query, and revoke the consents of a citizen in the register {#req-39}

> The toestemmingsregister MUST allow only the toestemmingsportaal backend to
> create, query, and revoke the consents of a citizen. The register MUST
> also allow only that backend to read and keep the values that the
> register keeps for that citizen. A portal UI, a citizen, or another
> component MUST NOT be able to call the register for these actions
> directly.

| Case | Outcome |
|---|---|
| The toestemmingsportaal backend creates, queries, or revokes | allowed |
| The portal UI or the browser calls the register directly | not reachable *(proposal, reachable in the demo)* |
| The PDP of a source asks for the status | only through the entry for the status ([REQ-76](consent.md#req-76)), no other actions *(from code)* |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
      ("alleen de burger en bevoegde componenten hebben toegang tot toestemming", provision "interface voor het toestemmingsportaal").
      Tightened: the citizen has access only through the toestemmingsportaal
      backend, because only that backend checks ownership
      ([REQ-40](#req-40)).
    - **Addressee**: GBO-delivered component: the toestemmingsregister and the
      deployment that it runs in.
    - **Evidence**: partly. Code and tests:
        - The UI talks only to the backend
          ([`nginx.conf#L7-L8`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/nginx.conf#L7-L8),
          [`vite.config.ts#L12-L17`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/vite.config.ts#L12-L17)).
        - The status query has its own entry that serves nothing else
          ([`status.go#L13-L26`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/status.go#L13-L26),
          [PR #390](https://github.com/ICTU/GBO-demo/pull/390)).
        - Not enforced: the register publishes a host port, allows every
          origin, and does not authenticate
          ([`docker-compose.yml#L718-L719`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L718-L719),
          [`main.go#L301-L305`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L301-L305)).
    - **Related**: [REQ-23](consent.md#req-23), [REQ-40](#req-40),
      [REQ-76](consent.md#req-76),
      [Q-49](../traceability/open-questions.md#q-49),
      [Q-57](../traceability/open-questions.md#q-57),
      [Q-58](../traceability/open-questions.md#q-58).
    - **Notes**:
        - It is open whether the register authenticates the backend, or whether
          network isolation is enough:
          [Q-58](../traceability/open-questions.md#q-58).
        - If the register and the backend become one system
          ([Q-49](../traceability/open-questions.md#q-49)), this limit becomes
          a boundary inside that system.
        - The public keys for the proof are public and are out of scope here.
        - The register refuses an overview without a citizen reference
          ([`main.go#L486-L502`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L486-L502)).
          This limits an overview to one citizen, but the register does not
          check who asks.

### REQ-40: A citizen sees and revokes only their own consents {#req-40}

> At every overview, every view of one consent, and every revocation, the
> toestemmingsportaal backend MUST determine the citizen from the verified
> identity ([REQ-24](consent.md#req-24)). It MUST show or change only
> the consents of that citizen. The backend MUST NOT use a reference to a
> citizen that the request carries. The backend MUST refuse a revocation of
> the consent of another citizen before the register changes anything. The
> consent of another citizen and an unknown consent MUST get the same
> outcome: not found (`CONSENT_NOT_FOUND`). Then the answer does not reveal
> whether a consent exists.

| Case | Outcome |
|---|---|
| Overview | only the consents of this citizen *(from code)* |
| Revoke an own consent | revoked *(from code)* |
| Revoke the consent of another citizen | refused: `CONSENT_NOT_FOUND` (HTTP 404), consent unchanged (demo: 403 `consent_not_owned_by_caller`) |
| Revoke an unknown consent | refused: `CONSENT_NOT_FOUND` (HTTP 404) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
      ("alleen de burger en bevoegde componenten hebben toegang tot toestemming"),
      tightened: the citizen has access only to their own consents. Also
      FR-20 criterion 1 and FR-23.
    - **Addressee**: GBO-delivered component: the toestemmingsportaal backend.
    - **Evidence**: to build:
      [ICTU/GBO-demo#602](https://github.com/ICTU/GBO-demo/issues/602). The
      demo has this evidence:
        - [PR #238](https://github.com/ICTU/GBO-demo/pull/238) and
          [PR #469](https://github.com/ICTU/GBO-demo/pull/469).
        - The overview is in
          [`portal.go#L249-L266`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L249-L266),
          tested in
          [`portal_test.go#L327`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal_test.go#L327).
        - The revocation is in
          [`portal.go#L268-L293`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L268-L293),
          tested in
          [`portal_test.go#L232`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal_test.go#L232),
          [`#L250`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal_test.go#L250),
          and
          [`#L266`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal_test.go#L266).
        - The refusal reason is in
          [`portalhttp.go#L167-L169`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/portalhttp/portalhttp.go#L167-L169).
    - **Related**: [REQ-24](consent.md#req-24), [REQ-38](#req-38),
      [REQ-39](#req-39), [REQ-109](#req-109),
      [Q-49](../traceability/open-questions.md#q-49),
      [Q-56](../traceability/open-questions.md#q-56),
      [ADR 0040](../decisions/0040-route-d-citizen-recognition.md).
    - **Notes**:
        - Design choice: the backend recognizes the citizen by an HMAC of the
          BSN under its own key
          ([route D](pseudonymization.md#route-d), working assumption). The
          backend asks BSNk nothing for this.
        - A new key makes existing consents impossible to find until a
          migration of these consents:
          [Q-56](../traceability/open-questions.md#q-56).
        - The ownership check is in the backend, because the register does not
          see who calls. So the register must accept calls only from the
          backend ([REQ-39](#req-39)).
        - The demo has no route for one consent. If such a route comes, the
          same check applies.

### REQ-108: The citizen can export the overview of consents {#req-108}

> After login, the citizen MUST be able to export the overview of their
> consents. The export MUST contain the same consents and data as the
> overview, and MUST NOT contain the BSN or the name of the citizen.

| Case | Outcome |
|---|---|
| A logged-in citizen exports | a file with all consents of the overview (active, and recently expired or revoked): consumer, service, sets, valid until, and status |
| A citizen without consents | empty export, no error |
| Not logged in | no export |
| Content | only consents of this citizen, no BSN, and no name |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design. FR-20 criterion 3, FR-01,
      [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
      (access), and
      [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
      Tightened: the export contains no BSN or name of the citizen.
    - **Addressee**: GBO-delivered component: the portal UI inside
      MijnOverheid, and the toestemmingsportaal backend if it makes the export. The
      requirement does not fix where the export happens.
    - **Evidence**: not built. The demo has no export. The demo issue follows
      after [Q-52](../traceability/open-questions.md#q-52).
    - **Related**: [REQ-40](#req-40),
      [Q-25](../traceability/open-questions.md#q-25),
      [Q-27](../traceability/open-questions.md#q-27),
      [Q-52](../traceability/open-questions.md#q-52).
    - **Notes**: the format follows from
      [Q-52](../traceability/open-questions.md#q-52). The processings for each
      consent (FR-20 criterion 2) belong in the export after a decision on
      where they come from ([Q-25](../traceability/open-questions.md#q-25),
      [Q-27](../traceability/open-questions.md#q-27)). Until that decision, the
      export contains only the consents.

### REQ-109: Revocation is possible only for a valid consent {#req-109}

> The UI of the toestemmingsportaal MUST offer the action "revoke" only for
> a consent with the status Actief or Opgehaald. It MUST NOT offer it for
> Verlopen or Ingetrokken. The toestemmingsportaal backend MUST refuse a
> revocation of an expired or already revoked consent. It MUST NOT change
> the status or make a new registration then.

| Case | Outcome |
|---|---|
| Actief | button visible, Ingetrokken after the citizen approves |
| Opgehaald (still valid) | button visible, Ingetrokken after the citizen approves (to build after [Q-42](../traceability/open-questions.md#q-42)) |
| Verlopen | no button. The backend refuses a direct request: `CONSENT_NOT_REVOCABLE`. The status stays Verlopen |
| Already revoked | no button. The backend refuses a direct request: `CONSENT_NOT_REVOCABLE`. No new registration |
| The consent of another citizen | refused, as in demo v0.9.0 ([REQ-40](#req-40)) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design. FR-23 criterion 1, FR-24 criterion 1,
      [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)
      (the registration supports revocation and expiry), and
      [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal).
      Tightened: the FRs put the button in the UI. This requirement also makes
      the backend enforce the rule.
    - **Addressee**: GBO-delivered component: the portal UI inside MijnOverheid
      and the toestemmingsportaal backend.
    - **Evidence**: partly. The backend check is in
      [ICTU/GBO-demo#600](https://github.com/ICTU/GBO-demo/issues/600). The UI
      shows the button only for the status `active`
      ([`MijnToestemmingenDetail.tsx#L127`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/MijnToestemmingenDetail.tsx#L127)).
      The backend checks only ownership. It sets an expired or revoked consent
      to `REVOKED` again, with a new LDV record
      ([`portal.go#L269`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L269),
      [`main.go#L282`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L282)).
    - **Related**: [REQ-14](consent.md#req-14), [REQ-40](#req-40),
      [F-97](../traceability/findings.md#f-97),
      [Q-42](../traceability/open-questions.md#q-42).
    - **Notes**: the words Actief, Opgehaald, Verlopen, and Ingetrokken are the
      names of statuses here, chosen in
      [F-97](../traceability/findings.md#f-97). Their form on screen follows
      the text guideline. The backend refuses a second revocation and does not
      accept it silently. So a double click gets a message.

### REQ-120: For every consent and after every revocation, the portal points the citizen to their rights at the consumer {#req-120}

> The portal UI MUST show a notice in the detail view of every consent and
> after every revocation. The notice MUST state that data already given to
> the consumer stays with the consumer. It MUST state that the citizen can
> use their GDPR rights there, such as erasure. It MUST also give the
> contact details of the consumer for that purpose. The toestemmingsportaal backend MUST take those
> contact details from the registration of the consumer and not from the
> request of the consumer.

| Case | Outcome |
|---|---|
| The citizen opens the detail view of a consent | text about GDPR rights, with the contact details from the registration *(proposal: not built)* |
| The citizen revokes a consent | the message after the revocation states that data already given stays with the consumer, with the contact details *(proposal: not built)* |
| No data fetched yet under the consent | the notice still shows. The requirement does not depend on [Q-42](../traceability/open-questions.md#q-42) |
| Consumer without registered contact details | does not occur for an admitted consumer: no admission without these details ([AV-14](admission.md#av-14)) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design. FR-25 criteria 1 and 2, FR-23, and FR-24
      (description: data already delivered falls under the GDPR responsibility
      of the consumer). Tightened: FR-25 applies the notice only to the case in
      which revocation is no longer possible. According to FR-24, that case
      does not exist ([F-98](../traceability/findings.md#f-98)). So the notice
      is always in the detail view and after a revocation.
    - **Addressee**: GBO-delivered component: the portal UI inside
      MijnOverheid and the toestemmingsportaal backend. The management organization
      records the contact details at admission.
    - **Evidence**: not built.
    - **Related**: [REQ-14](consent.md#req-14), [REQ-38](#req-38),
      [REQ-109](#req-109), [REQ-111](consent.md#req-111),
      [REQ-122](consent.md#req-122), [AV-14](admission.md#av-14),
      [F-98](../traceability/findings.md#f-98),
      [Q-62](../traceability/open-questions.md#q-62).
    - **Notes**: sub-question 2 of
      [Q-62](../traceability/open-questions.md#q-62) covers where the contact
      details are kept and how they reach the portal.

### Removed numbers

- REQ-41 (revocation is a change of the consent record, with no token invalidation and no change at the consumer): merged into [REQ-14](consent.md#req-14).

## Toestemmingsregister data model {#consent-register}

The toestemmingsregister must keep certain data for production. The data
model follows from the requirements. It is no requirement with its own
number: every data item refers to the requirement or functional
requirement that it follows from. Where an open question decides the
model, the table marks an open place.

The model says what the register knows. It does not say in which tables or
which product. It is open whether the register and the toestemmingsportaal
backend (S01 and S02) are one system or two:
[Q-49](../traceability/open-questions.md#q-49).

State: November 2, 2026. Demo: the schema of the demo
([`postgres_store.go#L15-L60`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/postgres_store.go#L15-L60))
covers the core. Where the schema deviates, the item says so. The compose
default runs the register in memory.

The PostgreSQL store is optional
([SL-12](../traceability/increments.md#sl-12) is planned). With a
persistent store, the register needs a fixed signing key
(`CONSENT_SIGNING_KEY_PATH`), so that proofs stay valid after a restart
([Q-55](../traceability/open-questions.md#q-55)).

### Citizen

The register keeps two data items about the citizen:

| Data item | Content | Basis |
|---|---|---|
| Reference to the citizen | An HMAC of the BSN under a secret key of the portal, with the key version in it. No BSN. | [REQ-20](pseudonymization.md#req-20), [route D](pseudonymization.md#route-d) |
| Polymorphic values | PI and PP of the first activation, under the reference. Once for each citizen. After that, only transformation. | [REQ-69](pseudonymization.md#req-69) |

The register does not keep the BSN. It also does not keep the encrypted
identity (VI) and the encrypted pseudonym (VP) for each receiving party.
It signs those into the proof and forgets them
([REQ-69](pseudonymization.md#req-69),
[REQ-80](pseudonymization.md#req-80)).

### Consent

The register keeps these data items for each consent:

| Data item | Content | Basis |
|---|---|---|
| Consent ID | Own ID of the register. It is in the proof and is the key for the status query. | [REQ-68](consent.md#req-68) |
| Citizen | The reference to the citizen. | [REQ-20](pseudonymization.md#req-20) |
| Consumer | OIN of the dienstverlener to whom the citizen gave the consent. For an integrator, the represented party. | [REQ-12](consent.md#req-12), [REQ-106](consent.md#req-106) |
| Use case | The service from the catalog for which the consent applies. | [REQ-12](consent.md#req-12), FR-32 |
| Scope per source | For each source: the scope and the fields for which the citizen gave consent. One representation. A flat list of scopes can be derived from it. | [REQ-12](consent.md#req-12) |
| Created | Moment of granting. | FR-22 |
| Valid until | Absolute moment. The register keeps only the result. Where the period comes from (a default period for each service, bounds, and whether the citizen changes it) is open: [Q-13](../traceability/open-questions.md#q-13). | FR-05, FR-11, FR-32, [REQ-19](consent.md#req-19) |
| Status | Active or revoked. An expired consent follows from "valid until". | FR-22, FR-24, [REQ-68](consent.md#req-68) |

The demo deviates from this model in three places:

- Scopes are in the schema twice: as a flat list and as scope per source.
  Production needs only the scope per source.
- The consumer chooses the validity period (`validity_seconds`). The
  default is one year, and the citizen cannot change anything:
  [ICTU/GBO-demo#380](https://github.com/ICTU/GBO-demo/issues/380).
- The purpose comes from the redirect of the consumer. The register
  stores it as `use_case`, default `hypotheek`.

### Log of processings

Every change produces an LDV record
([REQ-72](logging-audit.md#req-72)). The demo writes that record
through an outbox in the same transaction as the change. So there is no
consent without a log record. That is a choice of the demo and is no
requirement.

### Open places

Open questions decide these places in the model:

| Place | What the model needs when the question is answered | Question |
|---|---|---|
| Retrieved | Whether and when a consumer used a consent, and how the register learns that. | [Q-42](../traceability/open-questions.md#q-42) |
| Validity period | Whether the register records only the result, or also the default period and a change by the citizen. | [Q-13](../traceability/open-questions.md#q-13) |
| Validity per source | One valid-until for each consent, as in demo v0.9.0, or a valid-until for each source within the consent. | [Q-76](../traceability/open-questions.md#q-76) |
| Change | Whether a consent can change. If so, whether the record changes or a new record replaces the old one. | [Q-77](../traceability/open-questions.md#q-77) |
| Authorized representative | In whose name a consent given by a representative is, and whether the register records the representative with it. | [Q-73](../traceability/open-questions.md#q-73) |
| Refusal | A record of the refusal, a count for each consumer, or nothing in the register. | [Q-43](../traceability/open-questions.md#q-43) |
| Mandatory set | Whether the register records for each consent which fields were mandatory, or whether this comes from the catalog. | [Q-45](../traceability/open-questions.md#q-45) |
| Integrator | With option (a), a field for the integrator with the consent. With option (b), nothing in the register: the mandate is in the admission register. | [Q-46](../traceability/open-questions.md#q-46) |
| Volumes | Size and load. This decides storage and indexes, and does not change the data. | [Q-47](../traceability/open-questions.md#q-47) |
| Moment of revocation | A field with the consent, or only in the LDV log. | [Q-48](../traceability/open-questions.md#q-48) |
| Proof of the interaction | PSA S01 asks for it in the record. The record that the citizen saw the information follows from [REQ-107](consent.md#req-107). It is open whether the register records the version of the information shown. | [Q-51](../traceability/open-questions.md#q-51) |
| Retention periods | How long expired and revoked consents, PI and PP, and references stay. | [Q-63](../traceability/open-questions.md#q-63) |
| Storage durability | Which durability and recovery requirements apply to the register storage. | [Q-54](../traceability/open-questions.md#q-54) |
| S01 and S02 | Whether the polymorphic values and the consents are with one participant. A polymorphic value does not leave the party that requested it ([BSNK-03](pseudonymization.md#bsnk-03)). | [Q-49](../traceability/open-questions.md#q-49) |

