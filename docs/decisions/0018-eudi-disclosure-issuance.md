# ADR-0018: EUDI issuance through disclosure-based OpenID4VCI on the nl-wallet stack

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: no flow or subject identifier type, PID verification and the callback gap, gbo-demo v0.9.0)
- Satisfies: [P-06](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [GO: PuB-EAA-uitgifte](https://ictu.github.io/GBO-GO/main/#uitgifte-van-attestaties-voor-de-eudi-wallet-pubeaa-uitgifte)
- Deliberation: Reference architecture v0.6.2, PuB-EAA Provider (archived and unpublished), [REQ-45](../requirements/eudi-issuance.md#req-45), [SL-25](../traceability/increments.md#sl-25), demo constraints in [AGENTS.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/AGENTS.md)
- Implemented in: [services/eudi-adapter](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-adapter), [services/eudi-issuance-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/eudi-issuance-server) (nl-wallet v0.5.0), PID trust anchors in [issuance_server.toml.example#L3-L9](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/config/issuance_server.toml.example#L3-L9), adapter route in [source_release_runtime.go#L69](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L69)

## Context and problem statement

Citizens must receive attestations from government sources into their
EUDI wallet. The reference architecture called this function the shared
PuB-EAA Provider. The protocol stack and the identification mechanism were
open.

PSA v1 treats the wallet as a hook
([P-06](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). The
demo proves the route, but the route is outside the v1 scope of the PSA.

## Decision

GBO realizes the issuance function on the open-source nl-wallet issuance
server (pinned version), with disclosure-based issuance. The issuance has
five steps:

1. The wallet discloses its PID over OpenID4VP. The issuance server
   verifies the disclosure against its PID trust anchors.
2. The issuance server calls the GBO EUDI adapter
   (`POST /attestations/{sourceID}/{typeID}`). The adapter reads the BSN
   from the disclosed PID.
3. The adapter gets the source data over FSC through the standard PEP-PDP
   chain. It uses the query from the source metadata
   ([ADR-0016](0016-source-owned-metadata.md)). The adapter is a channel
   adapter, and the PDP of the source decides
   ([REQ-44](../requirements/authorization.md#req-44)).
4. The request carries no consent proof. So the PDP evaluates it under the
   PID regime ([ADR-0031](0031-regime-from-evidence.md)). Grants carry no
   `flow` or `subject_id_type` property.
5. The adapter projects the answer with gbo-simple-v1
   ([ADR-0017](0017-gbo-simple-v1.md)). The server issues the credential
   as `dc+sd-jwt` with immutable type metadata. It uses the certificate
   set of the source holder (bronhouder) ([ADR-0016](0016-source-owned-metadata.md)).

## Consequences

- Issuance is a full GBO route. It uses the same source API and the
  same authorization chain as DvTP. The source carries no logic that is
  specific to the wallet.
- The issuance policy enforces three things:
    - the presence of a PID
    - an actor allowlist (`designated_issuers`)
    - limits for each type (EUD0001, EUD0002)

    These checks replace the abstract `subject.bsn == resource.bsn` rule
    of the reference architecture.

- The issuance server verifies the PID. The demo removed a separate check
  in the adapter ([SL-25](../traceability/increments.md#sl-25)). The demo
  does not test this verification independently.
- The main gap is the callback from the issuance server to the adapter.
  The adapter route has no caller authentication. Any caller that reaches
  the adapter can post any BSN. The adapter then calls the source as the
  designated issuer peer, and the PDP allows the request. Nothing binds the
  BSN in the query to a verified disclosure
  ([REQ-45](../requirements/eudi-issuance.md#req-45),
  [ICTU/GBO-demo#133](https://github.com/ICTU/GBO-demo/issues/133)).
  [Risks and technical debt](../risks.md) tracks this gap.
- In addition to the PID providers, the PID trust list holds the GBO
  development CA and the issuer CA of every source.
- The BSN from the PID stays in the PDP input and is in both decision logs
  ([REQ-60](../requirements/logging-audit.md#req-60),
  [ADR-0043](0043-identifiers-out-of-pdp-input.md)).
- The validity is 365 days for every type. Each type has one status list.
  For the productization, see [ADR-0028](0028-pubeaa-productization.md).

## Open points

The following points are open:

- Trust in the callback and positive PID evidence
  ([Q-18](../traceability/open-questions.md#q-18),
  [REQ-45](../requirements/eudi-issuance.md#req-45)). Two solutions meet
  REQ-45:
    - The adapter verifies the SD-JWT itself.
    - The issuance server authenticates the callback and delivers signed
      evidence.

    Both solutions also need the binding of the disclosure to the request.
    The PID trust list must hold only PID-provider anchors. A revocation
    check of the PID is a recommendation (SHOULD). The legal status of a
    BSN from a PID is part of Q-18.

- Attestations about a related person. They follow a relation that the
  source declares, starting from the verified requester
  ([REQ-57](../requirements/eudi-issuance.md#req-57),
  [F-47](../traceability/findings.md#f-47),
  [Q-14](../traceability/open-questions.md#q-14)). The demo uses a source
  view. The alternative is filter arguments that the policy requires with
  fixed values
  ([ICTU/GBO-demo#425](https://github.com/ICTU/GBO-demo/issues/425)).
- Validity and revocation for each type. The source holder sets them. If an
  attestation is valid for more than 24 hours and the source data changes,
  the attestation must be revoked. GBO has no change feed
  ([REQ-77](../requirements/eudi-issuance.md#req-77),
  [F-82](../traceability/findings.md#f-82)).

## Traceability

- Requirements: [REQ-44](../requirements/authorization.md#req-44),
  [REQ-45](../requirements/eudi-issuance.md#req-45),
  [REQ-57](../requirements/eudi-issuance.md#req-57),
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-60](../requirements/logging-audit.md#req-60),
  [REQ-74](../requirements/authorization.md#req-74),
  [REQ-77](../requirements/eudi-issuance.md#req-77)
- Findings: [F-47](../traceability/findings.md#f-47) (open),
  [F-70](../traceability/findings.md#f-70) (open),
  [F-82](../traceability/findings.md#f-82) (open),
  [F-83](../traceability/findings.md#f-83) (open)
- Open questions: [Q-14](../traceability/open-questions.md#q-14),
  [Q-18](../traceability/open-questions.md#q-18)
- Demo increments: [SL-19](../traceability/increments.md#sl-19),
  [SL-25](../traceability/increments.md#sl-25),
  [SL-26](../traceability/increments.md#sl-26),
  [SL-29](../traceability/increments.md#sl-29),
  [SL-43](../traceability/increments.md#sl-43)
