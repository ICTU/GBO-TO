# ADR-0034: An integrator connects under FSC delegation, and the consent binds the represented party

- Status: accepted
- Date: 2026-11-02
- Satisfies: [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel), [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Deliberation: [REQ-106](../requirements/consent.md#req-106), [F-20](../traceability/findings-closed.md#f-20), [F-73](../traceability/findings-closed.md#f-73), [Q-12](../traceability/answered-questions.md#q-12), and demo [#379](https://github.com/ICTU/GBO-demo/issues/379), [PR #464](https://github.com/ICTU/GBO-demo/pull/464), [docs/integrator.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/integrator.md)
- Implemented in:
    - [lib.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L62-L72): the acting party and the represented party.
    - [engine.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L246-L267): the mandate check.
    - [dvtp_helper.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvtp_helper.rego#L57-L65): the consent binds the represented party.
    - [autosign.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L113-L125): the delegated grant.
    - [onboarding service.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dvtp-onboarding-register/internal/onboarding/service.go#L50-L58): `integrations` and `acts_for`.
    - [dvtp-onboarding.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml): the PIP pull.

## Context and problem statement

A consumer (dienstverlener) can let a software party, the integrator,
call the source for it. The consent binds a consumer. The policy
compared the `dienstverlener_oin` of the consent with the FSC peer that
calls. An integrator breaks that assumption
([F-73](../traceability/findings-closed.md#f-73)). The integrator calls, but
the citizen gave consent to the consumer.

The integrator acts as processor for the consumer
([Q-12](../traceability/answered-questions.md#q-12),
[AV-06](../requirements/admission.md#av-06)). The integrator
must not get access of its own. It must act only for the consumers that
registered it ([REQ-106](../requirements/consent.md#req-106)).

## Decision

The decision has four parts:

- Transport. The integrator connects over an FSC
  `DelegatedServiceConnection` grant (grant type 3). The consumer is the
  delegator and signs the contract.
- Contract admission. The contract decision of the source admits a
  delegated grant only if the admission register has that integration.
  If not, the decision refuses with `DELEGATION_NOT_REGISTERED`
  ([ADR-0015](0015-contract-acceptance-by-policy.md)).
- Mandate. The admission register records per integrator the consumers
  and the rules that it acts for (`integrations`, pulled into OpenFTV as
  `acts_for`). At request time, every delegated call needs a mandate for
  the represented party and the granting rule:
    - If the mandate is missing, the engine denies with
      `INTEGRATOR_NOT_REGISTERED`.
    - If the register data is missing, the engine denies with
      `INTEGRATOR_REGISTER_UNAVAILABLE`.
    - The engine applies this check to every rule. No rule can leave it
      out.
- Consent binding. The consent binds the represented party. That is the
  FSC delegator, or the calling peer if there is no delegator. The
  consent gives the integrator no mandate.

## Considered options

1. FSC delegation plus a mandate in the admission register (chosen).
2. The integrator calls with its own direct grant. The source then sees
   only the integrator. Either the consent binding fails, or the
   integrator gets access of its own.
3. The integrator in the consent proof. With this option, the citizen
   also consents to the integrator. FR-DvTP v0.9 does not ask any more to
   tell the citizen about the integrator. It stays open whether the proof
   names the integrator ([Q-46](../traceability/open-questions.md#q-46)).
4. No integrator role (the earlier TO). Real consumers use software
   parties, so the design must say how they connect
   ([F-20](../traceability/findings-closed.md#f-20)).

## Consequences

- The integrator gets a separate admission and acts as processor
  ([AV-06](../requirements/admission.md#av-06)).
- In demo v0.9.0, a mandate has no validity period. It ends only when
  the register entry changes.
- The admission register is also a request-time input, in addition to a
  contract-time input. A suspended consumer with a valid contract can
  still query directly. [REQ-110](../requirements/admission.md#req-110)
  covers that gap.
- OpenFSC puts the delegator in `act.sub` and the connecting peer in
  `sub`. That is the reverse of RFC 8693. The demo reads the values as
  OpenFSC writes them. An upstream issue is due.
- The autosign input has no grant data. For this reason, the contract
  decision admits the pair, but not the direction of the delegation. The
  mandate check at request time closes that gap.
- In the demo, the path is opt-in (`make demo-integrator`, peer `…1100`).
- One point is open: can policy read the FSC Peer ID as the OIN of the
  consumer ([Q-68](../traceability/open-questions.md#q-68))?

## Traceability

- Requirements: [REQ-106](../requirements/consent.md#req-106), [REQ-48](../requirements/authorization.md#req-48), [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-110](../requirements/admission.md#req-110), [AV-06](../requirements/admission.md#av-06)
- Findings: [F-20](../traceability/findings-closed.md#f-20) (closed), [F-73](../traceability/findings-closed.md#f-73) (closed)
- Open questions: [Q-12](../traceability/answered-questions.md#q-12) (answered), [Q-46](../traceability/open-questions.md#q-46) (open), [Q-68](../traceability/open-questions.md#q-68) (open)
- Demo increments: none
