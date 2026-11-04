# ADR-0040: Citizen recognition and the BSNk participant: route D

- Status: proposed (waits for [Q-49](../traceability/open-questions.md#q-49))
- Date: 2026-11-02
- Satisfies: [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal), [S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering), [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: [Open design choice: how does the register find the citizen again?](../requirements/pseudonymization.md#recognition), [route D](../requirements/pseudonymization.md#route-d), [routes A, B and C](../requirements/pseudonymization.md#routes-abc), [F-75](../traceability/findings.md#f-75), [F-98](../traceability/findings.md#f-98), and demo [PR #469](https://github.com/ICTU/GBO-demo/pull/469)
- Implemented in: demo, provisionally:
    - [subjectref.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/subjectref.go#L38-L42): the HMAC reference.
    - [portal.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L296-L314): one activation per citizen.
    - [polymorphic.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/polymorphic.go#L10-L17): PI and PP stored under the reference.

## Context and problem statement

The toestemmingsvoorziening needs two things from a citizen who logged in:

1. A stable key for its own administration. With this key, the service
   shows and revokes the consents of the citizen without a BSN
   ([REQ-20](../requirements/pseudonymization.md#req-20),
   [REQ-40](../requirements/consent.md#req-40)).
2. A PI and a PP. With these, the service makes the values for the
   parties at a new consent
   ([BSNK-03](../requirements/pseudonymization.md#bsnk-03)).

A stored PI or PP is not a stable key. BSNk gives other values at every
activation, and the service cannot compute these values from a BSN.
Every activation goes into the Inzageregister
([BSNK-10](../requirements/pseudonymization.md#bsnk-10)). Only a
recognized BSNk participant can activate and transform
([BSNK-01](../requirements/pseudonymization.md#bsnk-01)).

Two points are open ([Q-49](../traceability/open-questions.md#q-49)):

- Are the toestemmingsregister and the toestemmingsportaal backend one system?
- Which of them is the BSNk participant?

The working assumption puts the BSNk calls at the register. The demo
puts them at the backend. The TO removed the earlier requirement on this
point (REQ-22) until a decision on Q-49.

## Proposed decision

The proposal is route D, under the working assumption that MijnOverheid
passes the BSN:

- The toestemmingsvoorziening recognizes the citizen by an HMAC of the BSN, with
  a secret, versioned key:
    - The key is in an HSM or KMS.
    - The input has a fixed prefix and nine digits with leading zeros.
    - The result is at least 128 bits.
    - Every record keeps the key version.
- At the first consent, the service activates once at BSNk. It stores PI
  and PP under that reference. At a later consent, the service only lets
  BSNk transform values.
- To show and revoke consents, the service needs no BSNk call.

In the demo, the portal backend derives the reference and activates.
The register stores PI and PP. This split fits only if both are one BSNk
participant (Q-49).

## Considered options

[BSNk preconditions](../requirements/pseudonymization.md#routes-abc)
describes the routes in full. The design weighed four options:

1. Route D: an own pseudonym from the BSN (proposed). BSNk is necessary
   only at the first activation. The route needs the BSN from
   MijnOverheid and a grondslag for the register.
2. [Route A](../requirements/pseudonymization.md#route-a): an own
   pseudonym through BSNk. The service activates and transforms at every
   login, also to show consents. Every login goes into the
   Inzageregister.
3. [Route B](../requirements/pseudonymization.md#route-b): a pseudonym
   through the login. MijnOverheid passes a VP for the register. The
   route depends on DigiD and MijnOverheid.
4. [Route C](../requirements/pseudonymization.md#route-c): a reference
   from MijnOverheid. MijnOverheid must have such a reference and must
   be allowed to pass it on.

## Consequences

- The register stores PI and PP. It stores no BSN and no value per party
  ([REQ-69](../requirements/pseudonymization.md#req-69),
  [REQ-23](../requirements/consent.md#req-23)). This deviates on
  purpose from FR-35, criterion 1
  ([F-98](../traceability/findings.md#f-98)).
- The service processes the BSN briefly at every login, and that needs a
  grondslag. For every BSN, the service can compute whether consents
  exist, without a trace elsewhere.
- The secret key is the whole protection. Without the key, anyone can
  compute every reference back from the small BSN space.
- A new key gives every citizen a new reference. A migration of existing
  records is not built
  ([Q-56](../traceability/open-questions.md#q-56)).
- The toestemmingsvoorziening must become a recognized BSNk participant
  ([F-75](../traceability/findings.md#f-75),
  [Q-26](../traceability/open-questions.md#q-26)).

These points are open:

- [Q-49](../traceability/open-questions.md#q-49): one system, and which
  participant.
- [Q-50](../traceability/open-questions.md#q-50): how the backend gets
  the verified identity.
- [Q-57](../traceability/open-questions.md#q-57): the protection of the
  stored PI and PP.
- [Q-58](../traceability/open-questions.md#q-58): does the register
  authenticate the backend?
- [Q-63](../traceability/open-questions.md#q-63): retention.

When Q-49 has a decision, this ADR becomes accepted, or another route
replaces it.

## Traceability

- Requirements: [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-23](../requirements/consent.md#req-23), [REQ-24](../requirements/consent.md#req-24), [REQ-40](../requirements/consent.md#req-40), [REQ-69](../requirements/pseudonymization.md#req-69), [BSNK-01](../requirements/pseudonymization.md#bsnk-01), [BSNK-02](../requirements/pseudonymization.md#bsnk-02), [BSNK-03](../requirements/pseudonymization.md#bsnk-03), [BSNK-10](../requirements/pseudonymization.md#bsnk-10)
- Findings: [F-75](../traceability/findings.md#f-75) (open), [F-98](../traceability/findings.md#f-98) (open)
- Open questions: [Q-26](../traceability/open-questions.md#q-26) (open), [Q-49](../traceability/open-questions.md#q-49) (open), [Q-50](../traceability/open-questions.md#q-50) (open), [Q-56](../traceability/open-questions.md#q-56) (open), [Q-57](../traceability/open-questions.md#q-57) (open), [Q-58](../traceability/open-questions.md#q-58) (open), [Q-63](../traceability/open-questions.md#q-63) (open)
- Demo increments: [SL-51](../traceability/increments.md#sl-51) (done)
