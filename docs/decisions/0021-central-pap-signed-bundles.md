# ADR-0021: Policy management and distribution per bronhouder

- Status: accepted
- Date: 2026-08-24 (proposed as "Policy distribution through a central PAP with signed bundles", rewritten and accepted 2026-11-02)
- Satisfies: [S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie), [D-01](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: Reference architecture v0.6.2, gap 1 "authorization policy lifecycle" (archived and unpublished), [Q-21](../traceability/answered-questions.md#q-21) (answered October 28, 2026), [F-09](../traceability/findings-closed.md#f-09), [F-51](../traceability/findings.md#f-51), [F-52](../traceability/findings.md#f-52), demo [#426](https://github.com/ICTU/GBO-demo/issues/426) (bundle signing, closed as not planned), [PR #337](https://github.com/ICTU/GBO-demo/pull/337)
- Implemented in: opt-in Manager profile: [bundles/gbo-pdp.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/bundles/gbo-pdp.yaml), [authz/pdp-bundle.cedar](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/authz/pdp-bundle.cedar), [scripts/seed-openftv-manager.py](https://github.com/ICTU/GBO-demo/blob/v0.9.0/scripts/seed-openftv-manager.py#L116) (retire, never delete), and validation in [Makefile](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L92-L117) (`policy-check`, `policy-test`)

## Context and problem statement

Each bronhouder runs its own PDP
([ADR-0004](0004-federated-authorization.md)). Someone must write the
policy for that PDP, publish it, and deliver it to the PDP with integrity.
The earlier proposal put a central PAP at GBO: a central registry, signed
bundles, and governance in the GBO standards bodies.

[Q-21](../traceability/answered-questions.md#q-21) asked who can manage and
publish the policy of a bronhouder. The answer is that policy
management stays with each bronhouder. The policy belongs to the source
(P-10). Bundle signing inside one organization is not planned
([#426](https://github.com/ICTU/GBO-demo/issues/426)).

## Decision

- The PAP and the PDP are at each bronhouder. The bronhouder
  writes, approves, and publishes its own policy. GBO has no central PAP.
- GBO supplies guidance and no service. The guidance is a reference
  policy set, the engine choice ([ADR-0002](0002-opa-rego-authzen.md)),
  and the guidelines [RL-01](../requirements/authorization.md#rl-01)
  to [RL-05](../requirements/authorization.md#rl-05):
    - Deliver policy as a versioned bundle, and do not bake it into the
      PDP (RL-01).
    - Authorize the management API with its own policy set, and deny on
      an empty store (RL-02).
    - Separate writing from publishing. Publish with a non-personal,
      short-lived identity (RL-03).
    - Withdraw policy instead of deleting it. Reconcile the deployed set
      with version control (RL-04).
    - Validate a bundle before activation, and fall back visibly to the
      last valid set (RL-05).
- A bundle is signed only when it crosses an organization boundary.
  Inside one organization, signing is not planned. If a bronhouder lets
  another organization build or host its bundles, signing and
  verification become a requirement.

## Considered options

This decision compared three options:

1. Policy management per bronhouder (chosen). This option fits P-10
   and the federated PDP. Each bronhouder carries the governance cost.
2. A central PAP with signed bundles (the earlier proposal). This option
   gives one place to author and approve policy. But it puts the policy
   of the bronhouder under another organization, and it needs signing
   across that boundary.
3. Policy baked into the PDP image. This option has no lifecycle: no
   version, no withdrawal, and no validation before activation
   ([F-09](../traceability/findings-closed.md#f-09)).

## Consequences

- This decision closes the design gap of
  [F-09](../traceability/findings-closed.md#f-09): signing is required only
  across an organization boundary. The guidelines and their adoption
  remain.
- The demo shows the guidelines with the OpenFTV Manager (opt-in,
  `make demo-manager`):
    - The bundle `gbo-pdp` is tagged and has a version. The PDP pulls it
      at start.
    - Seeding withdraws stale policies and never deletes them.
    - A Cedar policy limits the pull of the PDP to one bundle and to GET.
    - By default, the PDP loads `./policies` from a mount.
- Push distribution does not work. The PDP authorizes its own management
  endpoints with the decision policy. That policy denies everything that
  is not a data request ([F-51](../traceability/findings.md#f-51)). So the
  PDP pulls instead.
- The policy store is cumulative and cannot delete. One duplicate or
  broken module stops every decision
  ([F-52](../traceability/findings.md#f-52)). Before every PDP start,
  `make policy-check` refuses non-Rego files and duplicate file names, and
  compiles the set. A visible fallback to the last valid set is not built
  (RL-05).
- The ADL does not record the policy version that made the decision
  ([REQ-59](../requirements/logging-audit.md#req-59)).
- The PSA mentions ODRL. This mention stays a deviation
  ([Risks and technical debt](../risks.md)).

## Traceability

- Requirements: [RL-01](../requirements/authorization.md#rl-01), [RL-02](../requirements/authorization.md#rl-02), [RL-03](../requirements/authorization.md#rl-03), [RL-04](../requirements/authorization.md#rl-04), [RL-05](../requirements/authorization.md#rl-05), [REQ-59](../requirements/logging-audit.md#req-59)
- Findings: [F-09](../traceability/findings-closed.md#f-09) (closed by this ADR), [F-51](../traceability/findings.md#f-51) (open), [F-52](../traceability/findings.md#f-52) (open), [F-59](../traceability/findings-closed.md#f-59) (closed)
- Open questions: [Q-21](../traceability/answered-questions.md#q-21) (answered)
- Demo increments: [SL-44](../traceability/increments.md#sl-44) (done)
