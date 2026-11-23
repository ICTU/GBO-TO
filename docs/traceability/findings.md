# Findings

A finding records what the demo build showed about the design. A finding
is one of these four types:

- An implicit requirement.
- An assumption that the build made visible.
- A gap.
- An error in a source.

Each finding records four items:

- Its trigger: a [demo increment](increments.md) or a demo PR.
- The observation.
- Why the observation matters for the GO, the PSA, or the FR-DvTP.
- Where it landed: a [requirement](../requirements/index.md), an
  [architecture decision](../decisions/index.md), a risk, or an
  [open question](open-questions.md).

A finding has one of these status values:

- open: the design has no answer to the finding.
- closed: the design or a review answered the finding.
- resolved in demo: the demo changed, and the finding no longer applies.
- superseded.
- premise lapsed.

Finding numbers are never reused. F-01, F-05, F-10, F-12, F-13, F-33, and
F-48 do not exist.

Each open finding is a
[GitHub issue](https://github.com/ICTU/GBO-TO/issues?q=is%3Aissue+label%3Afinding)
with the label `finding`. The issue holds the evidence, the impact, the
proposal and the links, and the discussion until the design answers the
finding. This page keeps the number, the status and a short summary of
each open finding, so that links from other pages keep working. When
the design answers a finding, the entry moves to the
[closed findings](findings-closed.md), and the issue closes.

For the open findings per PSA theme, see
[Summary for the PSA](#summary-for-the-psa).

### F-19: The register does not record the consent-use event ("first used"), so the FR-22 usage status cannot be shown {#f-19}

- **Status**: open

The consent detail page shows when the citizen gave a consent, when a
service provider (dienstverlener) first used it, and when it ended. The
consent register (toestemmingsregister) keeps only the start and end dates, so the demo
cannot show the first use. FR-11 and FR-22 require that the register
itself records whether and when data was first retrieved. The open point
is how the register learns of a successful delivery at the source. Three
options exist: the first status lookup by a PDP, a report from the
source after delivery, or derivation from the LDV chain.

Evidence, impact, proposal and links: [issue #89](https://github.com/ICTU/GBO-TO/issues/89).

### F-47: Wallet credential where the subject of the claim differs from the discloser {#f-47}

- **Status**: open

In the death certificate case, a surviving partner discloses her own PID
and gets a credential about her deceased partner. The source decides
which marriage and partner apply, and the PDP sees only the output
fields, so policy cannot check the relation. The PSA assumes that a
citizen gets credentials about himself or herself only. The proposal is
that the source publishes the relation as filter arguments in its
schema, and policy requires fixed values for them. What a filter cannot
express stays a tested property of the source, marked in its service
description.

Evidence, impact, proposal and links: [issue #90](https://github.com/ICTU/GBO-TO/issues/90).

### F-51: The PDP protects its own management endpoints with the decision policy {#f-51}

- **Status**: open

The PDP protects its own management endpoints with the policy that
decides on requests for citizen data. That policy refuses everything
except GBO data requests, so a push of policy bundles from the PAP
fails. The demo therefore lets the PDP pull its bundles at start-up,
which meets the PSA. The weak point is in the implementation: every rule
that allows management sits in the policy for citizen data. The proposal
is a separate authorization path for management, as a guideline for
bronhouders, because each source keeps its own PAP and PDP.

Evidence, impact, proposal and links: [issue #91](https://github.com/ICTU/GBO-TO/issues/91).

### F-52: The policy store is cumulative and cannot delete, and one duplicate package breaks every decision {#f-52}

- **Status**: open

The PDP compiles all its policies as one set. In the demo, one stale
policy with a duplicate package name made every request fail with a
server error instead of a deny. The policy store also cannot delete a
policy, so an operator can only retire it. Faults of the same class came
back three times, for example a policy that did not compile but showed
as loaded. The proposal is to validate a policy set before activation
and to fall back visibly to the last valid set, as the PSA asks.

Evidence, impact, proposal and links: [issue #92](https://github.com/ICTU/GBO-TO/issues/92).

### F-54: Log masking in the policy engine is inert, so the BSN-free decision log depended on input construction {#f-54}

- **Status**: open

The policy engine loads a masking rule for its decision log but never
applies it, so BSN values reached the log in clear text. The demo then
replaced the BSN with a pseudonym in the PDP input, until it removed
that step on purpose. In demo v0.9.0, the EUDI and ASI routes put the
plain BSN in the PDP input and in the logs. The proposal keeps
identifiers out of the PDP input when the input is built. Masking stays
allowed only as a second line, with a continuous test on real log
output.

Evidence, impact, proposal and links: [issue #88](https://github.com/ICTU/GBO-TO/issues/88).

### F-57: The source owns its service description, and GBO validates and activates it {#f-57}

- **Status**: open

Each source publishes one service description that names its data
service, query, parameters, mapping, attestation schema, and offer. GBO
finds the source through its valid contracts, validates the description,
and activates it in one step. The issuance configuration and the offers
in the frontend come from this description, so a source can join without
a change in GBO code. For the EUDI branch, this design gives the GO
service catalogue a concrete form, which the bronhouder manages with a
common profile. Three points stay open: a link to the DCAT-AP-NL
description, central findability, and a conflict with the wish for no
fixed DvTP queries.

Evidence, impact, proposal and links: [issue #93](https://github.com/ICTU/GBO-TO/issues/93).

### F-68: A chain read goes forward only, and in DvTP the chain starts at a party that LDV does not bind {#f-68}

- **Status**: open

A chain read in LDV starts at the party that started the processing and
follows pointers forward to each next logbook. In DvTP, a private
consumer starts the processing, and LDV does not bind that party, so
nobody knows which sources one processing touched. The PDP at the source
also writes only decision records, so no record at the source points to
the consent logbook. The proposal uses the consent register as an
index: every retrieval leads to a status lookup there, and the register
logs each lookup. The step from the source to the register is open with
Logius.

Evidence, impact, proposal and links: [issue #94](https://github.com/ICTU/GBO-TO/issues/94).

### F-70: The regime follows from the proof, but only consent is positive proof: the PID regime comes from not sending something {#f-70}

- **Status**: open

The PDP picks the rules from the evidence in a request. A consent proof
is positive evidence: it is signed, and the PDP checks it. The PID regime
has no evidence of its own. A request ends up there because it carries no
consent proof. So the only guard on that regime is a short list of
callers, and the adapter does not check who calls it. The design needs a
verified PID as positive evidence for this regime.

Evidence, impact, proposal and links: [issue #95](https://github.com/ICTU/GBO-TO/issues/95).

### F-71: A source without its own metadata endpoint: the operator takes over its service description {#f-71}

- **Status**: open

Some sources publish only their data service and no service description
of their own. For such a source, the demo lets the operator keep the
description in a directory. The operator then decides the query, the
mapping, and the wallet claims for the product of another party. Four
bounds stay in place, among them the pinned contract and the check of
the OIN against the certificate. The design allows this only as an
exception, with the recorded agreement of the bronhouder as first
condition, and that condition is not built.

Evidence, impact, proposal and links: [issue #96](https://github.com/ICTU/GBO-TO/issues/96).

### F-72: The decision record can carry only what the consumer also gets to see {#f-72}

- **Status**: open

The ADL is the audit record of every decision. It stores the answer that
the PDP gives to the consumer, and nothing else. That answer is
deliberately coarse, so the ADL is coarse too: it holds no reason per
field and no consent status. A supervisor can therefore reconstruct only
what the consumer was allowed to know, and nobody can replay a decision
from the record.

Evidence, impact, proposal and links: [issue #97](https://github.com/ICTU/GBO-TO/issues/97).

### F-74: DvTP scope comes from the demand side, EUDI scope from the supply side, and the intersection is what is technically allowed {#f-74}

- **Status**: open

For EUDI, the source publishes its offer, and GBO validates and
activates it. For DvTP, FR-32 describes a statutory service catalogue
that sets a legal ceiling per use case, from the demand side. What a
DvTP consumer can request is the intersection of the source offer and
that ceiling, and no GO, PSA, or FR text names it. In the demo, the DvTP
scopes are spread over policy, portal, and field map. The proposal is
one DvTP catalogue as the single source for scopes, fields, and portal
text, with a check of the intersection at activation.

Evidence, impact, proposal and links: [issue #98](https://github.com/ICTU/GBO-TO/issues/98).

### F-75: The BSNk design fits the specification, but the consent facility can fetch the values only as a recognized party {#f-75}

- **Status**: open

BSNk polymorphic pseudonymization is mandatory for DvTP. A check against
the BSNk specifications showed that the design fits on five points and
keeps BSNk out of the request path. One point does not fit: only a
recognized BSNk party can activate and transform values. The citizen
logs in at MijnOverheid before the sources are known, so the login
cannot deliver the values. The remaining work is administrative and
legal: the consent facility (toestemmingsvoorziening) must become a recognized party, and someone
must decide who the BSNk participant is.

Evidence, impact, proposal and links: [issue #99](https://github.com/ICTU/GBO-TO/issues/99).

### F-76: The consumer has no citizen identifier, so what it records about "this person" depends on the consent {#f-76}

- **Status**: open

The service provider never learns who the citizen is. It holds a consent
proof and names the citizen with a placeholder. This goes further than
"no BSN for private parties", and it has side effects. The service provider
logs under the consent ID, so one citizen with two consents is two
people in its logbook. It cannot tell that two consents come from the
same person, and it can answer a request for access only through the
consents.

Evidence, impact, proposal and links: [issue #100](https://github.com/ICTU/GBO-TO/issues/100).

### F-77: The PDP checks that the subject comes from the proof, and no longer who the subject is {#f-77}

- **Status**: open

The PDP used to compare the citizen in the query with the citizen in the
consent. Now the query carries a placeholder, and the proof carries a
value that the PDP cannot read. The PDP checks only that the citizen
comes from the proof. A rule can therefore never depend on a property of
the citizen, and one request can be about one citizen only.

Evidence, impact, proposal and links: [issue #101](https://github.com/ICTU/GBO-TO/issues/101).

### F-78: The proof freezes at consent: parties, key versions, and proof form are fixed for the whole validity period {#f-78}

- **Status**: open

At consent, the portal makes an encrypted value for each source, with
the OIN and the key version of that source. The consent proof therefore
fixes the parties, the key versions, the BSN authorization, and the
proof form for its whole validity period. An added party needs another
consent from the citizen. A changed OIN or proof form can break
outstanding proofs, and a consent can be valid for months. The proposal
adds the OIN, the key version, and the BSN authorization per party to
the service catalogue, and gives the proof a version.

Evidence, impact, proposal and links: [issue #102](https://github.com/ICTU/GBO-TO/issues/102).

### F-79: "After the decision" holds only if nothing but the Inway reaches the source gateway {#f-79}

- **Status**: open (the demo fixes it for Docker Compose. The roll-out outside Compose and the nonce are open.)

The source gateway decrypts the citizen from the consent proof and does
not check the proof again. That is safe only when every request at the
gateway has passed the PDP first. In an early demo version a consumer
was able to reach the gateway directly and skip the PDP. The demo now isolates
the gateway on its own networks. Every production deployment needs the
same isolation, and a nonce can bind a value to one consent as a second
guard.

Evidence, impact, proposal and links: [issue #103](https://github.com/ICTU/GBO-TO/issues/103).

### F-80: Since 2026 the ASI has a statutory interface and a seal obligation, but the authorization part stays a free choice {#f-80}

- **Status**: open

Since August 2026, EU law requires an authentic source interface (ASI)
for the verification of attributes. From January 1, 2027, the interface
must follow ETSI TS 119 478, and the source or a designated intermediary
must seal every result. The ETSI part on authorization is not
designated, so the member state chooses how the citizen is identified
and how the request is authorized. The GO and the PSA do not say that
verification is a legal obligation or that every result needs a seal.
The demo seals results with a development certificate, and who seals, in
which format, and who is the intermediary stay open.

Evidence, impact, proposal and links: [issue #104](https://github.com/ICTU/GBO-TO/issues/104).

### F-81: Since August 2026 PuB-EAA issuance falls under the same standard as QEAA issuance, with designation, registration, and its own certificate profile {#f-81}

- **Status**: open (the demo is not checked against it)

Since August 2026, EU law puts PuB-EAA issuance under the same standard
as QEAA issuance. The issuer is the bronhouder itself or a public sector
body that the member state designates. The issuer needs a qualified seal
certificate with a fixed profile, a notification by the member state,
and a registration as relying party. For GBO, this probably means one
notification per bronhouder, with GBO as the party that issues on its
behalf. The demo is not checked against the standard, and none of the acts in this reading says
who designates the issuer or who supervises.

Evidence, impact, proposal and links: [issue #105](https://github.com/ICTU/GBO-TO/issues/105).

### F-82: An issuer must track changes in the source, but GBO only supports queries {#f-82}

- **Status**: open

The ARF requires that a provider revokes an attestation when an
attribute value in the source changes. The rule applies to revocable
attestations that are valid for 24 hours or more. GBO supports only
queries, and in the demo the source sends no change notifications. A
provider of long-lived attestations therefore needs a notification
stream from the source. The proposal is a choice per attestation type:
short-lived attestations that the provider issues again often, or
long-lived attestations with change notifications from the source.

Evidence, impact, proposal and links: [issue #106](https://github.com/ICTU/GBO-TO/issues/106).

### F-83: Approval in the wallet is not a legal basis, so the EUDI route and DvTP consent cannot lean on each other {#f-83}

- **Status**: open

The ARF states that approval in the wallet is never a lawful ground for
processing by the relying party. In DvTP, the consent of the citizen is
the legal basis for delivery to a private party. In the EUDI route, the
citizen chooses only what to present. A consumer that uses both routes
therefore needs its own legal basis for the wallet route. The proposal
separates the terms in the GO and the PSA: consent is a registered,
revocable legal basis, and approval is a choice per presentation.

Evidence, impact, proposal and links: [issue #107](https://github.com/ICTU/GBO-TO/issues/107).

### F-84: ETSI leaves the security profile of the ASI authorization server open, and conflicts on two points with the norms it refers to {#f-84}

- **Status**: open

ETSI leaves the security profile of the ASI authorization server largely
open. It gives a choice for client authentication and for token binding,
and it only asks to take the FAPI 2.0 profile into account. On two
points, ETSI conflicts with the norms that it refers to: pushed
authorization requests and the RS256 algorithm. A QTSP that verifies at
several ASI providers must therefore implement a different profile for
each authorization server. The proposal is one fixed profile for Dutch
ASI providers in the PSA, and a report of the two conflicts to ETSI.

Evidence, impact, proposal and links: [issue #108](https://github.com/ICTU/GBO-TO/issues/108).

### F-85: The admission of QTSPs depends on a register and a certificate profile that do not exist {#f-85}

- **Status**: open

Before an ASI authorization server admits a QTSP, it looks up the right
of the QTSP in the national register of relying parties. That register
and its API do not exist. No text says which identifier links the QTSP
certificate to its register entry, and ETSI does not say what happens
when the register is unreachable. The demo uses a stub register and test
certificates, and it keeps a client active when the register is
unreachable. The proposal fixes the link between certificate and entry
and the behavior during an outage.

Evidence, impact, proposal and links: [issue #109](https://github.com/ICTU/GBO-TO/issues/109).

### F-86: ETSI requires the identification data in the token, and without encryption the QTSP reads the BSN {#f-86}

- **Status**: open

ETSI requires that the access token of the ASI carries the
identification data of the citizen, and it rejects token introspection.
The QTSP holds that token. In the demo, the token carries the BSN in
readable form, together with the name, birth date, and nationality.
Without encryption, the QTSP therefore processes the BSN, while the DvTP
route never sends a readable BSN as a field. The proposal is that only
the ASI provider can read the identification data, for example through a
claim that is encrypted for the provider.

Evidence, impact, proposal and links: [issue #87](https://github.com/ICTU/GBO-TO/issues/87).

### F-87: In the ASI route the QTSP is not an FSC participant, and the generic chain starts behind the ASIP {#f-87}

- **Status**: open

The earlier design assumed that a QTSP verifies through FSC as an OIN
holder. Under the designated ETSI route, the QTSP talks to the ASI
provider over HTTP as an OAuth client, and FSC has no part in admission.
The generic GBO chain starts behind the ASI provider, which is the actor
towards the source. The source sees neither the QTSP nor the citizen,
and the citizen cannot see QTSP verifications in any logbook. Open
points are which data about the QTSP the provider passes into the chain,
and how the source gets proof of the citizen.

Evidence, impact, proposal and links: [issue #110](https://github.com/ICTU/GBO-TO/issues/110).

### F-88: An identification means must deliver the mandatory identification data, or the data must come from elsewhere {#f-88}

- **Status**: open

ETSI requires the mandatory identification data of the citizen in the
ASI token. The wallet PID delivers these data except the place of birth,
but DigiD delivers only a BSN. If the Netherlands accepts such a means,
the authorization server fetches the other data from the BRP, or the
token holds only the BSN. The first option makes the server a BRP
consumer, and the second needs a reading of "required identification
data". The proposal is to record in the PSA which identification means
the server accepts and which data the token carries for each means.

Evidence, impact, proposal and links: [issue #111](https://github.com/ICTU/GBO-TO/issues/111).

### F-89: ETSI lets a response name one authentic source, so an ASIP for several sources offers one data service per source {#f-89}

- **Status**: open

In ETSI, a response of the ASI can name only one authentic source. GBO
builds one ASI provider for several sources, so one verify request with
attributes from two sources does not fit one response. The demo
therefore offers one data service per source, each with its own
contract, catalogue entry, and token audience. A token is valid for one
data service, so attributes from two sources need two authorizations and
two citizen interactions. The proposal records this layout in the PSA
and reports the gap to ETSI.

Evidence, impact, proposal and links: [issue #112](https://github.com/ICTU/GBO-TO/issues/112).

### F-91: ETSI requires the authorization-server metadata in the contract, but gives no field for it {#f-91}

- **Status**: open

ETSI requires that the contract of an ASI data service names the
metadata of its OAuth authorization server. The OpenAPI format has no
field for that metadata: its OAuth fields hold single URLs, and its
OpenID field points to another kind of server. The demo uses its own
extension field with the standard metadata URL. Without a fixed field,
each ASI provider picks its own way, and a QTSP in several member states
must learn each way. The proposal is to ask ETSI and, until ETSI
answers, to describe the demo extension in the PSA as the Dutch choice.

Evidence, impact, proposal and links: [issue #113](https://github.com/ICTU/GBO-TO/issues/113).

### F-92: Annex IV of CIR 2026/1735 makes the value optional, but keeps the requirement for fuzzy matching {#f-92}

- **Status**: open

An EU implementing act makes the attribute value optional in a positive
ASI result. It keeps an ETSI rule that an ASI provider with fuzzy
matching must return the stored value. The demo does fuzzy matching and
returns no value, so a literal reading says that the demo does not meet
that rule. If the rule stays, a Dutch ASI provider must choose: return
the stored value on a fuzzy match, or do no fuzzy matching. The proposal
adds this choice to the open question whether the ASI returns the value,
and reports the point to ETSI.

Evidence, impact, proposal and links: [issue #114](https://github.com/ICTU/GBO-TO/issues/114).

### F-93: Nothing links the citizen who logs in at the QTSP to the citizen who logs in at the source's authorization server {#f-93}

- **Status**: open

The QTSP identifies the citizen to whom it issues an attestation, and
the authorization server of the source identifies the citizen again for
the token. Nothing links these two identifications. A QTSP can therefore
issue an attestation with the data of person B to person A, for example
when B scans the QR code. The QTSP cannot compare the two itself,
because it must not receive the BSN and the token is opaque to it. The
proposal is a Dutch check: the QTSP sends its own identification data in
the request or to the authorization server for comparison.

Evidence, impact, proposal and links: [issue #115](https://github.com/ICTU/GBO-TO/issues/115).

### F-94: The NL PID has no place of birth, while the implementing regulation makes it mandatory {#f-94}

- **Status**: open

EU law makes five PID attributes mandatory, among them the place of
birth. The NL Wallet PID has no place of birth, so the authorization
server asks for four of the five attributes plus the BSN. If the
Netherlands reads "required identification data" as the mandatory PID
attributes, a token from the NL Wallet cannot meet the requirement. The
check covered only the metadata of the development environment, so the
content of the production PID is unknown. The proposal asks the NL
Wallet team about a place of birth, and records in the PSA the minimum
data in the token.

Evidence, impact, proposal and links: [issue #116](https://github.com/ICTU/GBO-TO/issues/116).

### F-95: ETSI binds an ASI token only per operation, so a binding per attribute needs its own extension {#f-95}

- **Status**: open

ETSI defines only the scopes verify and retrieve for an ASI token, so a
token covers an operation and names no attributes. The citizen then
approves an operation, and the approval does not name the requested
data. The demo binds the token to attributes with an extension type of
its own, and makes this binding optional. Only parties that know the
type can use the binding, and a QTSP from another member state does not
know it. If the open question decides so, the PSA records the binding as
the Dutch choice, and the type goes to ETSI.

Evidence, impact, proposal and links: [issue #117](https://github.com/ICTU/GBO-TO/issues/117).

### F-96: ETSI does not name RFC 9207, so a QTSP that verifies at several ASIPs has no defense against mix-up {#f-96}

- **Status**: open

An OAuth client that talks to more than one authorization server needs a
defense against mix-up attacks. RFC 9700 prefers the issuer parameter in
the authorization response, and FAPI 2.0 requires the server to return
it. ETSI only asks to take both into account, and the demo does not
return the parameter. A QTSP talks to one authorization server per ASI
provider, which is exactly the case where RFC 9700 makes the defense
mandatory. The proposal is that a Dutch ASI authorization server returns
the issuer parameter and that the QTSP checks it.

Evidence, impact, proposal and links: [issue #118](https://github.com/ICTU/GBO-TO/issues/118).

### F-97: FR-22 to FR-24 name the same statuses with different words, and the rationale of FR-23 contradicts its criteria {#f-97}

- **Status**: open

FR-22 to FR-24 of FR-DvTP use different words for the same consent
statuses. One rationale uses "Openstaand" (pending) next to "Actief"
(active). A revoked consent is "Geannuleerd" (cancelled) in one place and
"ingetrokken" (revoked) in another. The rationale of FR-23 allows
revocation only while the status is "Open", but its criteria also allow
it after retrieval. Builders and reviewers therefore get two readings of
one rule. The proposal is one set of terms, with "Ingetrokken" for a
revoked consent, and a rationale that matches the criteria.

Evidence, impact, proposal and links: [issue #119](https://github.com/ICTU/GBO-TO/issues/119).

### F-98: FR-DvTP v0.9 contradicts decisions and its own criteria on four points, and PSA S02 is ambiguous on one point {#f-98}

- **Status**: open

FR-DvTP v0.9 conflicts with decisions or with its own criteria on four
points, and the PSA is ambiguous on one point. FR-39 and FR-26 put
policy and a first check at a central place, while the decisions keep
PAP and PDP at each bronhouder. FR-25 assumes that revocation ends at
retrieval, and FR-35 describes register contents that differ from the
chosen design. The PSA calls pseudonymization "transparent" to the
citizen, which can mean invisible or explained. The FR-DvTP owner must
make four changes and the PSA authors must fix the meaning, so that
builders do not get two conflicting sources.

Evidence, impact, proposal and links: [issue #120](https://github.com/ICTU/GBO-TO/issues/120).

### F-100: FSC contract acceptance does not see the service, so admission to a peer opens all its services {#f-100}

- **Status**: open

Contract acceptance decides which organisation connects to which source
peer, but not to which service, because the Manager sends the decision
no service name. A party admitted to a peer can get a contract for every
service that peer publishes. Service providers admitted to the consent
register's peer to push consent requests can also connect to the consent
status. The proposal checks the service on every call, at the Inway of
each peer. For DvTP data, a consent covers only the data sets registered
for the service.

Evidence, impact, proposal and links: [issue #125](https://github.com/ICTU/GBO-TO/issues/125).

## Summary for the PSA

The demo shows that the generic chain works end to end for three routes: DvTP, EUDI issuance, and the Authentic Source Interface (ASI). The following sections group the open findings per theme (state of November 2, 2026) and name what the PSA must decide.

An earlier version of this summary named six open design knots. All six are closed: [F-02](findings-closed.md#f-02), [F-03](findings-closed.md#f-03), [F-04](findings-closed.md#f-04), [F-06](findings-closed.md#f-06), [F-07](findings-closed.md#f-07), and [F-08](findings-closed.md#f-08). The requirements and ADRs cover PDP placement, consent atomicity, the consent lifecycle, the fourth validation point, LDV, and mTLS on FSC.

In total, 34 findings are open. The review of September 21, 2026 closed 28 of 39 findings and kept 11 open. After that review, 24 findings were added, and the demo resolves one of them. [F-54](#f-54) is open again, and [ADR-0021](../decisions/0021-central-pap-signed-bundles.md) closed [F-09](findings-closed.md#f-09).

### Policy management

- **Closed**: [F-09](findings-closed.md#f-09) (signing only across an organization boundary, [ADR-0021](../decisions/0021-central-pap-signed-bundles.md)).
- **Open**: [F-51](#f-51) (management endpoints behind the decision policy), [F-52](#f-52) (cumulative store), and [F-98](#f-98) (FR-39 still describes a central policy authority).
- **Decided**: policy management stays at each source. PAP and PDP sit at the bronhouder ([Q-21](answered-questions.md#q-21)). [RL-01 to RL-05](../requirements/authorization.md#policy-management) are guidelines for bronhouders.
- **PSA to decide**: whether bundle signing is required when a bundle crosses an organization boundary ([ADR-0021](../decisions/0021-central-pap-signed-bundles.md)).

### Consent and its lifecycle

- **Open**: [F-19](#f-19) (no "retrieved" status), [F-74](#f-74) (scope is the intersection of legal ceiling and source offer), [F-78](#f-78) (the proof freezes at consent), and [F-97](#f-97) and [F-98](#f-98) (FR-DvTP contradictions).
- **Decided**: the legal basis travels as a signed proof. The status is checked online and fails closed ([F-61](findings-closed.md#f-61), [ADR-0032](../decisions/0032-consent-proof.md)). An integrator connects under FSC delegation, and the consent binds the represented party ([F-73](findings-closed.md#f-73), [ADR-0034](../decisions/0034-integrator-delegation.md)).
- **PSA to decide**:
    1. When a consent counts as retrieved, and how the register learns it ([Q-42](open-questions.md#q-42)).
    2. A DvTP catalogue per FR-32 as the single source for scopes, with an intersection check at activation (B-03, [REQ-121](../requirements/consent.md#req-121)).
    3. A version for the proof, and how long an old version stays valid ([REQ-82](../requirements/pseudonymization.md#req-82)).
    4. What "transparent" means in S02 ([F-98](#f-98)).

### Authorization regime

- **Open**: [F-70](#f-70). The regime follows from the proof ([ADR-0031](../decisions/0031-regime-from-evidence.md)), but only consent is positive proof. The PID regime rests on an actor list and an unverified BSN.
- **PSA to decide**: what the evidence for the EUDI legal basis is ([REQ-45](../requirements/eudi-issuance.md#req-45), [Q-18](open-questions.md#q-18)). The demo resolves the binding of rules to services ([F-90](findings-closed.md#f-90)), and this binding is a proposal for S05.

### Pseudonymization and BSNk

- **Open**: [F-75](#f-75) (the consent facility must be a recognized BSNk party), [F-76](#f-76) (the consumer has no citizen identifier), [F-77](#f-77) (one subject per request), and [F-79](#f-79) (only the Inway reaches the source gateway, with the roll-out outside Compose and the nonce open).
- **Decided in the TO**: the source gateway decrypts its own value after the allow ([ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)). Route D for citizen recognition is proposed ([ADR-0040](../decisions/0040-route-d-citizen-recognition.md)).
- **PSA to decide**:
    1. Recognition of the consent facility at BSNk, and who the BSNk participant is ([Q-26](open-questions.md#q-26), [Q-49](open-questions.md#q-49)).
    2. Whether the consumer gets a pseudonym (VP), with its effects on logging, access, and recognition ([Q-01](open-questions.md#q-01)).
    3. Queries about more than one person.

### Admission and service descriptions

- **Open**: [F-57](#f-57) (the source owns its description, but the DCAT-AP-NL reference and central findability are missing), [F-71](#f-71) (an operator takes over a description, and the recorded agreement of the bronhouder is not built), and [F-100](#f-100) (contract acceptance does not see the service).
- **Decided**: admission is a register entry instead of a policy rule ([F-55](findings-closed.md#f-55)).
- **PSA to decide**: accept or reject the role split "the source publishes, GBO validates and activates" (S10), and decide where central findability lives.

### Audit and logging

- **Open**: [F-54](#f-54) (BSN in both decision logs on the EUDI and ASI routes), [F-68](#f-68) (no route from the ADL at the source to the consent logbook), [F-72](#f-72) (the ADL lacks policy version, consent status answer, and configuration), and [F-76](#f-76) (what the consumer logs under).
- **Decided**: three standards give three records. ADL is for decisions ([ADR-0036](../decisions/0036-adl-decision-record.md)), LDV is per controller ([ADR-0026](../decisions/0026-ldv-integration.md)), and FSC-Logging is for transport. W3C Trace Context is the correlation key ([ADR-0035](../decisions/0035-w3c-trace-context.md)). The register index covers the chain start ([F-68](#f-68) point 1).
- **PSA to decide**: keep identifiers out of the PDP input instead of masking logs ([ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md), proposed). The questions to Logius ([Q-25](open-questions.md#q-25), [Q-27](open-questions.md#q-27)) and to OpenFTV (fill the ADL fields) need an owner.

### EUDI issuance

- **Open**: [F-47](#f-47) (attestation about a related person), [F-81](#f-81) (designation, TS 119 471, and the certificate profile), [F-82](#f-82) (an issuer must track source changes), and [F-83](#f-83) (wallet approval is no legal basis).
- **PSA to decide**:
    1. Who designates the PuB-EAA issuer and who supervises ([Q-28](open-questions.md#q-28)). Add art. 3(46) and TS 119 471 to B-13.
    2. Per attestation type: short-lived, or long-lived with a change notification stream from the source.
    3. Separate the terms "consent" (DvTP) and "approval" (wallet) in the GO and the PSA.
    - The relation in a related-person attestation is enforced through schema filters instead of source code ([REQ-57](../requirements/eudi-issuance.md#req-57)).

### Authentic Source Interface

- **Open**: [F-80](#f-80), [F-84](#f-84) to [F-89](#f-89), and [F-91](#f-91) to [F-96](#f-96).
- **Decided in the TO**: the ASI is an OAuth front door per ETSI TS 119 478 clause 6.1, and the QTSP is not an FSC participant ([ADR-0037](../decisions/0037-asi-oauth-front-door.md)). Each source has one data service, with one token per data service ([ADR-0038](../decisions/0038-asi-data-service-per-source.md)). The source describes its ASI attributes ([ADR-0039](../decisions/0039-asi-source-described-attributes.md)). Two ADRs are proposed: the seal format ([ADR-0041](../decisions/0041-asi-seal-format.md)) and the optional per-attribute binding ([ADR-0042](../decisions/0042-asi-attribute-token-binding.md)).
- **PSA to decide** (S11, B-14): Annex IV and the seal duty apply from January 1, 2027. The PSA must decide five points:
    1. The role of GBO and the designated intermediary ([Q-37](open-questions.md#q-37), [Q-28](open-questions.md#q-28)), and who holds the qualified seal certificate ([Q-17](open-questions.md#q-17), [Q-32](open-questions.md#q-32)).
    2. One security profile for Dutch authorization servers, including `iss` per RFC 9207 ([Q-66](open-questions.md#q-66), [F-84](#f-84), [F-96](#f-96)).
    3. The accepted identification means, and identification data in the token that only the ASIP can read ([Q-36](open-questions.md#q-36), [F-86](#f-86), [F-88](#f-88), [F-94](#f-94)).
    4. A check that links the QTSP login to the login at the authorization server ([Q-40](open-questions.md#q-40), [F-93](#f-93)), and per-attribute binding under art. 9(5) ([Q-33](open-questions.md#q-33)).
    5. Whether the ASI returns the value on a match, and fuzzy matching ([Q-29](open-questions.md#q-29), [F-92](#f-92)). Also the register and the certificate link for QTSP admission ([Q-34](open-questions.md#q-34), [Q-35](open-questions.md#q-35)).
    - The specification gaps go to ETSI ESI: [E1 to E10](standards-feedback.md). The sender is not decided.

### Source texts

- **Open**: [F-97](#f-97) and [F-98](#f-98). The owner of FR-DvTP makes FR-22 to FR-26, FR-35, and FR-39 match the decisions. The PSA authors fix the meaning of "transparent" in S02.
