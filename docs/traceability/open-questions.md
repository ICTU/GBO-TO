# Open questions

An open question is a question that the demo cannot answer. It needs a
decision by the PSA, by a system forum (G5, Logius, the standards bodies),
a legal assessment, or a choice by the team. The demo and this TO use the
working assumption until the forum decides the question. An architecture
decision that waits for a question has the status *proposed* in the
[decision log](../decisions/index.md).

Each open question is a
[GitHub issue](https://github.com/ICTU/GBO-TO/issues?q=is%3Aissue+label%3Aquestion)
with the label `question`. The issue holds the forum, the options, the
working assumption and the links, and the discussion until the decision.
This page keeps the number, the status and a short summary of each
question, so that links from other pages keep working. When the forum
decides a question, the answer goes into the TO (a requirement, a
decision or the [answered questions](answered-questions.md)), and the
issue closes.

A question has one of four status values: *open*, *partly answered*,
*answered*, or *closed*. The register never reuses a question number. A
renumbered question keeps a history line with its old number.

### Q-01: Which pseudonym form does the system use? {#q-01}

- **Status**: partly answered

PSA P-04 asks that a consumer without a statutory power gets a citizen
identity that nobody can link outside its context. It is a legal question whether a private
consumer without a public task can connect to BSNk as a recipient. It is
also open whether an encrypted identity that the consumer cannot decrypt
counts as a processing of the BSN. The answer decides how the consumer
logs the citizen, gives access, and recognizes one citizen across
consents. The working assumption is that the consumer gets no pseudonym,
and the consent proof carries an encrypted value per source that each
source decrypts itself.

Forum, options, working assumption and links: [issue #21](https://github.com/ICTU/GBO-TO/issues/21).

### Q-08: What belongs in the LDV (processing log), and who holds the retention duty? {#q-08}

- **Status**: open

GBO builds and runs three components: the consent register (toestemmingsregister), the EUDI
adapter, and the issuance server. Each component records its own
processings in an LDV logbook, and the PDP records every decision in the
ADL. Nobody decided how
long these records stay, or who can read them. That is a legal and
supervision decision, and retention is harder because an ADL record
needs its sources to stay available. In the working assumption, the demo
keeps separate stores and a read-only role for the ADL, without a
retention policy or tamper evidence.

Forum, options, working assumption and links: [issue #22](https://github.com/ICTU/GBO-TO/issues/22).

### Q-13: Who sets the validity period of a consent? {#q-13}

- **Status**: open

The functional requirements give each service a default validity period
from the service catalog and let the citizen adjust it within bounds. It
is open whether the citizen really must be able to change the period,
and within which bounds. The choice is a policy and UX question under
the GDPR, which the demo can show but cannot decide. The demo deviates
from the requirements: the consumer sends the end date, and the citizen
cannot change the period. Without an end date, the consent register
uses one year.

Forum, options, working assumption and links: [issue #23](https://github.com/ICTU/GBO-TO/issues/23).

### Q-14: Query enforcement model: how does the PDP model fields, recursion, and arguments? {#q-14}

- **Status**: open

The PSA speaks of pre-registered, selective data requests, and the GO
says that the service catalog holds the permitted requests per
application. The question is whether queries are fixed per application,
or whether a consumer can write its own queries within a schema that the
source publishes. The answer decides how rich the catalog gets and how
close GBO stays to iWlz (the data exchange of the Dutch Long-term Care Act). The working assumption rejects fixed queries
for DvTP, so the consumer writes its own query and the PDP decides every
field against an allowlist. If the field list is uncertain, the PDP
denies the request.

Forum, options, working assumption and links: [issue #24](https://github.com/ICTU/GBO-TO/issues/24).

### Q-17: EUDI issuance architecture: who owns the issuance server and the adapter? {#q-17}

- **Status**: open

GBO offers a central, optional facility that issues attestations for the
EUDI Wallet, and each bronhouder stays responsible for its
attestations. Can the facility hold the seal key of a bronhouder, or
must it call a signing facility under control of the bronhouder? It
is also open who holds the qualified seal certificate, which names the
authentic source, and the status-list certificate. Key custody and
certificate holding are legal and governance decisions. As a working
assumption, the demo uses one issuance server, a certificate set per
source, and keys in files, which decides nothing for production.

Forum, options, working assumption and links: [issue #25](https://github.com/ICTU/GBO-TO/issues/25).

### Q-18: EUDI flow security: phishing, certificate management, data processing in the adapter, PID verification {#q-18}

- **Status**: open

Can a bronhouder identify a citizen with a BSN from a verified EUDI
Wallet PID, with the legal status of a BSN from DigiD? If so, the chain
must show how the verified disclosure binds to the source query. This is
a national legal question, because eIDAS does not name the BSN and the
member state decides on the number. In the working assumption, the
issuance server verifies the PID but passes only plain attributes to the
adapter, without an authenticated callback. So nothing in the chain
binds the BSN of the source query to a verified PID.

Forum, options, working assumption and links: [issue #26](https://github.com/ICTU/GBO-TO/issues/26).

### Q-25: How can a reader find the step from the decision at the source to the consent log? {#q-25}

- **Status**: open

If the PDP of a source checks a consent status, the consent register
logs that check in its own LDV logbook. The PDP writes only an ADL
decision record, and the ADL has no field that points to another LDV
logbook. A reader who follows the standard links therefore cannot get
from the decision to the consent log. The question is how the ADL record
can point there, and the answer needs Logius or a design choice. The
working assumption accepts the gap: an auditor finds the register record
by a search on the trace ID.

Forum, options, working assumption and links: [issue #27](https://github.com/ICTU/GBO-TO/issues/27).

### Q-26: Can the consent facility become a recognized BSNk party, and in which role? {#q-26}

- **Status**: open

In the design, the consent facility fetches an encrypted identity or
pseudonym per party from BSNk. BSNk serves only recognized parties, such
as means issuers and authorization services, and a consent facility is
none of these. The minister of BZK decides on recognition and its role.
Several practical points are open too, such as how the service
recognizes a citizen at a later login and how it gets the
Autorisatielijst BSN. The working assumption is that MijnOverheid passes
the BSN, and the service derives its own pseudonym under which it stores
the encrypted values.

Forum, options, working assumption and links: [issue #28](https://github.com/ICTU/GBO-TO/issues/28).

### Q-27: Under what does a consumer without an identifier name the data subject in its processing log? {#q-27}

- **Status**: open

The consent proof carries the citizen only in values that sources can
read, so the consumer has no identifier for its LDV processing log. It
is open whether LDV accepts a reference to the legal basis as the data
subject. It is also open whether citizen access through the consents
meets the GDPR. In the working assumption, the consumer logs under the
consent ID. That ID is no pseudonym, so one citizen with two consents
shows as two data subjects.

Forum, options, working assumption and links: [issue #29](https://github.com/ICTU/GBO-TO/issues/29).

### Q-28: Who designates the PuB-EAA issuer and the ASI intermediary of the Netherlands, and who supervises? {#q-28}

- **Status**: open

A bronhouder can issue a PuB-EAA itself, or a public body that the
member state designates issues it on behalf of bronhouders. For
verification of attributes by QTSPs, the law also names a designated
intermediary. The question is whether the Netherlands designates GBO or
the management organization for one or both roles, and who supervises
PuB-EAA issuance. In the working assumption, the bronhouder is the
PuB-EAA provider and GBO runs the technical issuance facility. For
verification, the demo acts as the designated intermediary, but nobody
designated it.

Forum, options, working assumption and links: [issue #30](https://github.com/ICTU/GBO-TO/issues/30).

### Q-29: Is there a legal basis to verify attributes for private QTSPs, and does the ASI return the value on a match? {#q-29}

- **Status**: open

eIDAS lets a QTSP verify attributes at a source in accordance with Union
or national law, so the regulation creates no legal basis itself. From
January 1, 2027, the ASI can return the stored value on a match with
variation, which is more than a yes or no. An ETSI requirement makes
that value mandatory for fuzzy matching, which contradicts the optional
rule. It is open which Dutch legal basis applies, and whether the GBO
ASI does fuzzy matching and returns the value. In the working
assumption, the demo reports a match with variation but never returns
the stored value.

Forum, options, working assumption and links: [issue #31](https://github.com/ICTU/GBO-TO/issues/31).

### Q-30: On which trust list are PuB-EAA issuers: LoTE or the trusted lists? {#q-30}

- **Status**: open

Wallets and relying parties check the seal of a GBO attestation against
a trust list, and that list also goes into the attestation schema. The
EUDI specifications disagree on which list holds PuB-EAA issuers: a List
of Trusted Entities or the trusted lists. It is also open who manages
that list for the Netherlands. No decision exists, so a TO page that
names one list describes an assumption.

Forum, options, working assumption and links: [issue #32](https://github.com/ICTU/GBO-TO/issues/32).

### Q-31: Who registers the Dutch verification points in the catalogue of attributes? {#q-31}

- **Status**: open

The member state asks the EU to include its verification points in the
catalogue of attributes, which tells a QTSP how to use them. Each record
can carry a national code that tells Dutch sources apart if more than
one source delivers the same attribute. The question is who registers
the Dutch attributes and verification points, and who sets that national
coding scheme. Both are assignments that BZK makes. In the working
assumption, the demo has a local discovery stub and registers nothing in
the EU catalogue.

Forum, options, working assumption and links: [issue #33](https://github.com/ICTU/GBO-TO/issues/33).

### Q-32: In which format does an ASIP seal the verification result, so a QTSP can validate every ASIP the same way? {#q-32}

- **Status**: open

From January 1, 2027, every ASI verification result carries a seal, but
no rule fixes its format. A QTSP that verifies in several member states
must then implement the format of each ASIP separately. The question is
whether ETSI or an implementing act will fix a seal profile, or else
whether the Netherlands fixes one format for its ASIPs. In the working
assumption, the demo seals the response body with a detached JWS in a
header. That format is a demo choice, and the reference QTSP had to
implement it.

Forum, options, working assumption and links: [issue #34](https://github.com/ICTU/GBO-TO/issues/34).

### Q-33: Does the Netherlands impose per-attribute authorization for ASI requests under art. 9(5)? {#q-33}

- **Status**: open

Under the ETSI standard, a QTSP gets a token per operation, and that
token is valid for every attribute while it lasts. The implementing
regulation lets a member state add controls, such as a binding of the
token to the attributes that the citizen came for. Such a binding limits
what a QTSP can request, but a QTSP that implements only ETSI fails on
it. The question is whether the Netherlands imposes this authorization
per attribute. In the working assumption, the binding is optional on
request of the QTSP, and a setting in the demo makes it mandatory.

Forum, options, working assumption and links: [issue #35](https://github.com/ICTU/GBO-TO/issues/35).

### Q-34: What happens to admitted QTSPs if the register is unreachable during a re-check, and how often is it checked? {#q-34}

- **Status**: open

The authorization server of the ASI checks the right of each registered
QTSP again at regular intervals in the register of relying parties. No
source says how often, or what happens when the register is unreachable.
With fail-open, a QTSP whose right was revoked during an outage stays
active, and with fail-closed, all QTSPs lose access. That trade-off
between availability and timely exclusion is a management and risk
choice. The working assumption is fail-open with a check every hour, and
the server refuses a new registration while the register is unreachable.

Forum, options, working assumption and links: [issue #36](https://github.com/ICTU/GBO-TO/issues/36).

### Q-35: Which identifier links a QTSP's access certificate to its register entry? {#q-35}

- **Status**: open

A QTSP registers at the ASI with a statement that it seals with its
certificate and that points to its entry in the register. The
authorization server must check that the entry belongs to the
certificate holder, so that no QTSP can present the entry of another.
Candidate identifiers are the EUID, the organization identifier with the
KvK number, and the OIN. The question is which identifier the
certificate and the entry share, and who sets it. In the working
assumption, the organization identifier of the certificate must equal
one of the identifiers of the entry.

Forum, options, working assumption and links: [issue #37](https://github.com/ICTU/GBO-TO/issues/37).

### Q-36: Which identification means does a Dutch ASI authorization server accept, and where does the identification data come from? {#q-36}

- **Status**: open

The ASI authorization server must identify the citizen, with the EUDI
Wallet or another procedure under the ETSI identity proofing standard.
It is open whether a Dutch server accepts the wallet, DigiD, or both.
DigiD gives only a BSN, so it is also open whether the server can fetch
the missing data from the BRP. In the working assumption, the demo
accepts both, and the token carries more data after a wallet login than
after DigiD. The demo refuses an identification without a BSN, which
excludes foreign PIDs, but it accepts a PID with unknown or revoked
status.

Forum, options, working assumption and links: [issue #38](https://github.com/ICTU/GBO-TO/issues/38).

### Q-37: What is GBO's role in the ASI: designated intermediary, technical supplier to bronhouders, or authentic source itself? {#q-37}

- **Status**: open

GBO builds one ASIP for several authentic sources, and the law allows an
ASIP to be the source itself or a designated intermediary. The question
is whether GBO becomes that designated intermediary, stays a technical
supplier to each bronhouder, or becomes an authentic source itself.
The role decides who seals the result and who answers for the
correctness of the data. The working assumption is the intermediary
model, which the GBO team saw as likely on October 14, 2026. The demo
names an authentic source for every data service and uses one seal for
all of them.

Forum, options, working assumption and links: [issue #39](https://github.com/ICTU/GBO-TO/issues/39).

### Q-38: How does an authentic source connect to the ASIP: by code, by configuration, or by a description it publishes itself? {#q-38}

- **Status**: partly answered

The ASIP must turn a verification request into a query on the source.
One part is answered: the bronhouder manages the link between an
attribute and its own schema, in the metadata that it publishes. The
demo builds this: the ASIP derives one query per request from that
description, and the code adapter for the BRP is removed. Still open is
how many sources must connect and how fast, which is a management
choice. The GBO team estimates that code fits fewer than about ten
sources, and configuration or a published description fits tens of sources.

Forum, options, working assumption and links: [issue #40](https://github.com/ICTU/GBO-TO/issues/40).

### Q-39: How does a data service contract name the authorization server, so a QTSP finds every ASIP the same way? {#q-39}

- **Status**: open

A QTSP finds a data service through the Discover Interface, and the
record points to an OpenAPI contract. The ETSI standard requires that
this contract names the OAuth authorization server, but OpenAPI has no
field for it. The question is whether ETSI will fix a way, or whether
the Netherlands sets one for its ASIPs. Without one shared way, a QTSP
cannot find every ASIP the same way. In the working assumption, the demo
uses its own extension in the security scheme, which no QTSP outside the
demo knows.

Forum, options, working assumption and links: [issue #41](https://github.com/ICTU/GBO-TO/issues/41).

### Q-40: Must the citizen logging in at the QTSP provably be the same as the one logging in at the source's authorization server, and who checks? {#q-40}

- **Status**: open

The QTSP and the authorization server of the source each identify the
citizen, and no specification links the two identifications. The
question is whether the Netherlands requires that both are the same
person. If so, the source side can check it in the verification request,
or the authorization server can check it at login. It is also open
whether the QTSP can rely on the identification by the authorization
server. In the working assumption, the reference QTSP identifies the
citizen itself with wallet data and no BSN, but the check itself is not
built.

Forum, options, working assumption and links: [issue #42](https://github.com/ICTU/GBO-TO/issues/42).

### Q-41: What happens to the tokens of a QTSP whose right is revoked? {#q-41}

- **Status**: open

The authorization server checks the right of each QTSP again at
intervals, but the ETSI standard says nothing about tokens that it
already issued. The ASIP validates a token itself and does not ask the
authorization server. The question is whether a QTSP can use its token
after revocation until it expires, or whether the ASIP must learn of the
revocation. How fast a revocation takes effect is a management and risk
choice. In the working assumption, the server deactivates the client,
and issued tokens stay valid until they expire, at most 10 minutes.

Forum, options, working assumption and links: [issue #43](https://github.com/ICTU/GBO-TO/issues/43).

### Q-42: When is a consent "retrieved", and how does the register learn that? {#q-42}

- **Status**: open

The functional requirements ask the consent register to record
whether and when a source first retrieved data under a consent. The
register cannot see a delivery, so the question is how it learns of one.
It is also open whether retrieved means a delivery or a use of the
consent. Each option changes what a source must build, from nothing to
an extra interface (koppelvlak) to the register. In the working assumption, the demo
shows no retrieved status, only Active, Expired, and Revoked.

Forum, options, working assumption and links: [issue #44](https://github.com/ICTU/GBO-TO/issues/44).

### Q-43: For what purpose is a citizen's refusal recorded, and in which form? {#q-43}

- **Status**: partly answered

The functional requirements say that a refusal is recorded, but not
where, what, or for whom. The purpose decides the form: a refusal in the
citizen overview, a count per consumer as an abuse signal, or only a log
line. A record under the citizen is personal data and needs a retention
period. One point is answered: closing the window is no refusal, and
nothing happens then. In the working assumption, the demo returns the
citizen to the consumer with a denied status and records nothing.

Forum, options, working assumption and links: [issue #45](https://github.com/ICTU/GBO-TO/issues/45).

### Q-44: What does the return redirect give back to the consumer, and how does the consent proof reach it? {#q-44}

- **Status**: partly answered

After every outcome, the consent portal (toestemmingsportaal) sends the citizen back to a
registered address of the consumer. On success, the signed consent proof
tells the consumer what is allowed, and on refusal or error a separate
outcome is necessary. It is open which outcomes the consumer must tell
apart, and whether the proof travels through the browser or as an
exchange code. One point is answered: an abort is no outcome, because a
citizen who closes the window does not return. In the working
assumption, the demo puts the proof in the URL fragment of the return
redirect.

Forum, options, working assumption and links: [issue #46](https://github.com/ICTU/GBO-TO/issues/46).

### Q-45: Does the consent facility enforce the minimal mandatory set, and who decides which sets are mandatory? {#q-45}

- **Status**: open

The functional requirements keep the minimal mandatory set always on,
but no source says whether the consent facility enforces it. It is also
open who decides which sets are mandatory, and what happens when a
consent lacks the mandatory set. The choice affects the service catalog
and the initiation request of the consumer. If the consent facility
enforces the set, both the UI and the backend enforce it. The demo has
no mandatory set and enforces none.

Forum, options, working assumption and links: [issue #47](https://github.com/ICTU/GBO-TO/issues/47).

### Q-46: Is the integrator in the consent proof, or only in the register? {#q-46}

- **Status**: open

An integrator acts on behalf of a consumer, with a mandate in the
admission register. The question is whether the consent proof must also
name the integrator, or whether that mandate is enough. With the
integrator in the proof, only that integrator can use it, but a change
of integrator makes running consents unusable. With only the mandate,
every registered integrator of that consumer can use the proof. In the
working assumption, the proof binds the consumer, and the PDP denies an
integrator without a mandate.

Forum, options, working assumption and links: [issue #48](https://github.com/ICTU/GBO-TO/issues/48).

### Q-47: Which volumes must the chain handle, at start and later? {#q-47}

- **Status**: open

The chain needs volume figures for the consent register, the status
query, and the BSNk link, at start and after a few years. The figures
are citizens with a consent, new consents per day, and status queries
per second at average and peak. They matter because every request does
an online status query at the register without a cache, and every
consent costs a BSNk transformation per source. Who supplies the
estimate is open, and no figures exist. One demo measurement of the
status query gave 14.5 ms at the median and 82 ms at most.

Forum, options, working assumption and links: [issue #49](https://github.com/ICTU/GBO-TO/issues/49).

### Q-48: Does the register record when a consent was revoked? {#q-48}

- **Status**: open

The functional requirements ask for status insight for the citizen and
for a revocation that takes effect immediately. The question is whether
the consent register keeps the moment of revocation with the
consent, or whether the LDV log is enough. With the moment in the
register, the overview and the status query can show it, and otherwise
the portal must read the log. It is a choice about access and evidence.
In the working assumption, the register keeps only active or revoked,
and the moment is in the LDV record of the change.

Forum, options, working assumption and links: [issue #50](https://github.com/ICTU/GBO-TO/issues/50).

### Q-49: Are the consent register and the consent portal backend one system, and who is the BSNk participant? {#q-49}

- **Status**: open

The PSA describes the consent register and the consent portal
as capabilities and leaves their setup open. The question is whether the
register and the portal backend become one system or two, and which
party is the BSNk participant. The answer matters because a polymorphic
value must not leave the party that requested it. With two systems at
different parties, the register cannot store those values, and citizen
recognition needs another route. In the working assumption, the portal
backend requests the values at BSNk and the register stores them, under
one participant.

Forum, options, working assumption and links: [issue #51](https://github.com/ICTU/GBO-TO/issues/51).

### Q-50: How does the consent portal backend inside MijnOverheid get the verified citizen identity? {#q-50}

- **Status**: open

The citizen logs in at MijnOverheid, and the backend of the
consent portal runs inside it. The question is which evidence of
that login MijnOverheid can give to the backend, and how the backend
checks it. This matters because the backend must take the citizen
identity from a validated login assertion and never from client input.
MijnOverheid can pass a signed token, pass the BSN over an authenticated
channel, or pass the BSN encrypted for BSNk. Until someone decides, the
demo backend makes its own portal token after a mock login.

Forum, options, working assumption and links: [issue #52](https://github.com/ICTU/GBO-TO/issues/52).

### Q-51: Must it be provable which information the citizen saw when giving consent? {#q-51}

- **Status**: open

When a citizen gives consent, the portal backend requires an
acknowledgment that the citizen saw the information. The question is
whether it must also be provable afterwards what that information was,
and where that evidence is kept. This matters because consent must be
informed and provable, and the GDPR requires that the controller can
show the consent. The existence of a consent proves the acknowledgment,
but it does not show the text. The demo records nothing extra, so in
effect only a versioned catalog can show what the citizen saw, and
nobody has decided this.

Forum, options, working assumption and links: [issue #53](https://github.com/ICTU/GBO-TO/issues/53).

### Q-52: In which format does the citizen export the overview of consents? {#q-52}

- **Status**: open

The citizen can export the overview of consents. The question is which
format the export uses, and whether GBO follows what MijnOverheid uses
for export elsewhere. The requirement says "csv or pdf", which can mean
both formats or only one of them. The content is fixed: what the
overview shows, without the BSN or the name of the citizen. The demo has
no export, so there is no working assumption for the format.

Forum, options, working assumption and links: [issue #54](https://github.com/ICTU/GBO-TO/issues/54).

### Q-53: Within which time and by which mechanism does suspension of a consumer take effect? {#q-53}

- **Status**: open

When a consumer is suspended or terminated, it must lose its access in
time. The question is how fast that happens, by which mechanism, and who
revokes its FSC contract: the source or the management organization. An
expired or revoked consumer certificate must block access immediately,
but FSC checks revocation through a cache. It is also open whether the
citizen overview must show a consent at a suspended consumer as
something other than Active. In the demo, a suspended party gets no new
FSC contract, but it can still send requests with an existing contract.

Forum, options, working assumption and links: [issue #55](https://github.com/ICTU/GBO-TO/issues/55).

### Q-54: Which durability and recovery requirements apply to the register storage? {#q-54}

- **Status**: open

The consent register is the only place that holds the consents and
the polymorphic values of a citizen. The question is which storage RINIS
offers, and which requirements apply for durability, acceptable loss,
recovery time and consistency after recovery. This matters because the
source denies when a consent is lost, while the consumer still holds a
valid consent proof. The demo register runs on Postgres when a database
is set, and in memory otherwise. If RINIS offers Postgres as a platform
service, Postgres is the obvious choice.

Forum, options, working assumption and links: [issue #56](https://github.com/ICTU/GBO-TO/issues/56).

### Q-55: Where is the signing key of the consent proof, and how is it rotated and retired? {#q-55}

- **Status**: open

The consent register signs every consent proof, and the PDPs of the
sources verify it with a public key. The question is where the signing
key is stored, how it rotates, and how it is revoked after a leak. It is
also open how the PDPs get the public keys. This matters because whoever
has the key can make proofs for every citizen and every consumer. With a
persistent store, the demo requires a fixed key from a file.

Forum, options, working assumption and links: [issue #57](https://github.com/ICTU/GBO-TO/issues/57).

### Q-56: How do citizen references follow a rotation of the portal HMAC key? {#q-56}

- **Status**: open

The consent portal recognizes a citizen by an HMAC of the BSN under
a secret key, and the register stores consents under that reference.
With a new key, the same BSN gives a different reference, so the portal
no longer finds the existing consents. The register cannot move them
itself, because it sees no BSN. The question is how often the key
rotates and how existing consents stay findable after a rotation. The
design uses one key and the demo has no migration, so a new key hides
older consents.

Forum, options, working assumption and links: [issue #58](https://github.com/ICTU/GBO-TO/issues/58).

### Q-57: Which protection do the stored polymorphic values get? {#q-57}

- **Status**: open

For each citizen, the consent register keeps the polymorphic
identity and pseudonym of the first activation. From these values, BSNk
makes an encrypted identity or an encrypted pseudonym for every party.
As a result, a party that has the values and can call the portal can
have values made for every source. The question is which protection the
values get: encryption with a key outside the database, access control
only, or both. The demo stores them unencrypted, in a table of their
own.

Forum, options, working assumption and links: [issue #59](https://github.com/ICTU/GBO-TO/issues/59).

### Q-58: Must the register authenticate the consent portal backend, or is network isolation enough? {#q-58}

- **Status**: open

The consent portal backend is the only caller that creates, reads
and revokes consents in the consent register. The question is
whether the register must authenticate that backend, for example with
mTLS or over FSC, or whether network isolation is enough. This matters
because a party that reaches the register directly can create or revoke
consents for every citizen. Network isolation alone requires that the
register and the backend run at one participant, in one environment. The
demo uses network isolation only, and the status query of the PDP has
its own listener over FSC.

Forum, options, working assumption and links: [issue #60](https://github.com/ICTU/GBO-TO/issues/60).

### Q-59: Which security requirements apply to the portal UI inside MijnOverheid? {#q-59}

- **Status**: open

GBO builds the UI of the consent portal inside MijnOverheid. The
question is which security requirements apply to that UI, and which of
them MijnOverheid already imposes. Examples are a content security
policy, session management and protection against open redirects. The
return to the consumer is a redirect, so the portal must check the
return address. In the demo, only the frontend checks that address,
against a fixed list of origins.

Forum, options, working assumption and links: [issue #61](https://github.com/ICTU/GBO-TO/issues/61).

### Q-60: If name, purpose, return address, and status come from the registration, must the origin of the initiation request be provable? {#q-60}

- **Status**: open

The functional requirements say that the initiation request of a
consumer must provably come from that service provider. The portal backend
takes name, purpose and return address from the registration, so a
forged request only gives a consent for the real consumer. A third party
can still start a request for a consumer that asked for nothing. The
question is whether that risk is acceptable, or whether the consumer
must sign the request or send it in advance over FSC. The demo passes
the context as query parameters, and its backend does not do these
checks.

Forum, options, working assumption and links: [issue #62](https://github.com/ICTU/GBO-TO/issues/62).

### Q-61: What must MijnOverheid deliver or allow for the portal UI and the link to the consent facility? {#q-61}

- **Status**: open

GBO builds the UI of the consent portal as a contribution to the
MijnOverheid code base. Several requirements therefore depend on what
MijnOverheid delivers or allows. This question collects the points
without a question of their own, so that one meeting can discuss them
all. They include the interface to the portal backend, the redirect
protocol, the request context across the login, and ownership of the UI.
Others are accessibility, house style, the switch to the apps, and
delegation. There is no working assumption apart from the imitated shell
in which the demo runs the portal.

Forum, options, working assumption and links: [issue #63](https://github.com/ICTU/GBO-TO/issues/63).

### Q-62: What must the management organization record or deliver for the consent process? {#q-62}

- **Status**: open

Several parts of the consent screen and the overview depend on data or
processes of the management organization. This question collects them in
one place. They are the validity limits per service, the privacy officer
per consumer, the voluntariness text, the owner of the texts, and the
support contact. The incident processes for a failure of BSNk,
MijnOverheid or the register, and for a compromised key, are also open.
Until the management organization provides these, the demo uses fixed
configuration values.

Forum, options, working assumption and links: [issue #64](https://github.com/ICTU/GBO-TO/issues/64).

### Q-63: How long are consents, polymorphic values and citizen references kept? {#q-63}

- **Status**: open

The consent register keeps a record per consent, and the polymorphic
values per citizen under a reference. The question is how long it keeps
expired or revoked consents, the values of a citizen without a running
consent, and empty references. It is also open how long the citizen sees
old consents, and whether the citizen can ask to delete them. Retention
and deletion must follow legal and audit requirements, so this is a
legal decision. The demo keeps expired and revoked consents without a
time limit.

Forum, options, working assumption and links: [issue #65](https://github.com/ICTU/GBO-TO/issues/65).

### Q-64: Must a Dutch ASIP also offer clause 6.2 (ISO 15000) besides clause 6.1, and with it deferred responses? {#q-64}

- **Status**: open

ETSI TS 119 478 lets an ASIP choose between clause 6.1 (HTTP and OAuth)
and clause 6.2 (ISO 15000). Only clause 6.2 has a deferred response, for
a source that cannot answer immediately. The question is whether a Dutch
ASIP must also offer clause 6.2, and whether such slow sources exist. If
so, it is open whether clause 6.2 can run over the eDelivery of the
Basisinrichting OOTS. The working assumption is clause 6.1 only, which
is synchronous.

Forum, options, working assumption and links: [issue #66](https://github.com/ICTU/GBO-TO/issues/66).

### Q-65: Must the ASI support requests on behalf of another person (representation)? {#q-65}

- **Status**: open

With a mandate request, a QTSP asks the ASI for attributes of a subject
while another person acts on behalf of that subject. ETSI makes support
optional and leaves the details out of the specification. The question
is whether the ASI must support such requests, and if so, whether the
authorization server or the ASIP checks the evidence of representation.
Support needs a legal basis, a source for the representation and an
agreement on who checks it. The working assumption is no support, and
the ASI answers such a request with status 501.

Forum, options, working assumption and links: [issue #67](https://github.com/ICTU/GBO-TO/issues/67).

### Q-66: Which security profile does the authorization server of a Dutch ASIP get? {#q-66}

- **Status**: open

ETSI lets the authorization server of an ASIP choose its client
authentication (mTLS, private_key_jwt or both) and its token binding
(mTLS or DPoP). It also leaves open whether the server fully follows
FAPI 2.0 with PAR. The question is which profile the Dutch ASIP picks. A
profile stricter than ETSI excludes QTSPs that implement only ETSI, and
a QTSP that serves several member states must support every variant. The
demo uses private_key_jwt and DPoP without PAR, as a demo choice without
a decision.

Forum, options, working assumption and links: [issue #68](https://github.com/ICTU/GBO-TO/issues/68).

### Q-67: How do Dutch data services get into the Discover Interface, and who registers them? {#q-67}

- **Status**: open

A QTSP uses the Discover Interface to find, per attribute, the data
service that verifies it. ETSI intends this interface for the OOTS
common services of the European Commission, such as the Data Service
Directory. No document describes how a Dutch ASIP registers its data
services there, or whether this goes through the Basisinrichting OOTS.
The question is where QTSPs find the Dutch data services, and who
registers them. The demo has a stub for the Discover Interface, and the
ASIP publishes the records itself.

Forum, options, working assumption and links: [issue #69](https://github.com/ICTU/GBO-TO/issues/69).

### Q-68: Can policy read the FSC Peer ID as the OIN of the consumer, or must that link come from the register? {#q-68}

- **Status**: open

In FSC, the Peer ID of a party is the serial number of its certificate,
and with PKIoverheid that value is the OIN. The question is whether
policy can treat "Peer ID = OIN" as a system rule, or must get the link
between peer and organization from the admission register. The register
is necessary when one peer acts for several organizations, as with
hosting or an integrator, or when an organization changes certificate.
The working assumption is the system rule: the DvTP policy compares the
Peer ID directly with the consumer OIN in the consent.

Forum, options, working assumption and links: [issue #70](https://github.com/ICTU/GBO-TO/issues/70).

### Q-69: Must the consent proof bind the purpose, so that the PDP checks it? {#q-69}

- **Status**: open

A consent binds one consumer, one service with its purpose, and at least
one data set. The purpose is in the register record, but the consent
proof does not carry it, so the PDP does not check it. The question is
whether the proof must bind the purpose or service, and whether the PDP
must check the admission of the consumer for it. The demo has one
service per data set, so the difference is not visible there. The
working assumption is that the service follows from the data set only.

Forum, options, working assumption and links: [issue #71](https://github.com/ICTU/GBO-TO/issues/71).

### Q-70: Which normalization applies in fuzzy matching per kind of value, and who sets it? {#q-70}

- **Status**: open

The ASI allows fuzzy matching only for free text, to accept spelling
variations, and excludes dates, codes and numbers. The demo normalizes
white space, case, hyphens and diacritics, but not every kind of value
tolerates all of these rules. The question is whether the rules differ
per kind of value, and who sets that kind: the ASIP, the source or the
EU catalogue. In the demo, every string without a format gets the full
normalization. Postal code and country code have no format, so they get
it too, and that conflicts with the requirement.

Forum, options, working assumption and links: [issue #72](https://github.com/ICTU/GBO-TO/issues/72).

### Q-71: Which form do address and name get as attributes, until the EU catalogue of attributes fixes it? {#q-71}

- **Status**: open

The ASIP compares an attribute in the form of a schema from the EU
catalogue of attributes. Until that catalogue has schemas, GBO sets the
schema per attribute, and each source maps its own fields to it. The BRP
splits house number and surname into parts, while the amended PID puts
the house number into the street. The question is which form address and
name get, and who registers the Dutch attributes in the catalogue. The
working assumption keeps a separate house number with letter and
addition, and puts the surname prefix (`voorvoegsel`) in the family name.

Forum, options, working assumption and links: [issue #73](https://github.com/ICTU/GBO-TO/issues/73).

### Q-72: Do GBO components write attributes outside the LDV core, and if so under which extension? {#q-72}

- **Status**: open

LDV allows attributes outside its core only within an approved
extension. Several GBO components write local GBO attributes, such as
the consent ID and attestation claims, and that extension has no
approval. As a result, the demo does not log according to LDV. The
question is whether the core is enough, or whether GBO must submit an
extension to Logius for the consent ID that citizen access needs. The
starting point is core only, but the demo still writes the local
attributes.

Forum, options, working assumption and links: [issue #74](https://github.com/ICTU/GBO-TO/issues/74).

### Q-73: Whose consent is a consent given by an authorized representative, and what does the register record? {#q-73}

- **Status**: open

If a service allows delegation, an authorized representative can give
consent for another person. The requirements assume one person, who logs
in, sees only their own consents, and gets polymorphic values while
logged in. The question is in whose name the consent is, whether the
register records the representative, and who can see and revoke the
consent. It is also open whether BSNk can make a value for the
represented person during the login of the representative. There is no
working assumption, because the demo has no mandates.

Forum, options, working assumption and links: [issue #75](https://github.com/ICTU/GBO-TO/issues/75).

### Q-74: Does GBO build the registration and onboarding facility for service providers, or the management organization? {#q-74}

- **Status**: open

Three requirements describe a facility where a service provider logs in
with eHerkenning, applies with supporting documents, and gets its
certificate checked. GBO builds the admission register, but that
register knows only FSC Peer IDs and has no accounts or certificates. In
this design, the registration and review process is with the management
organization. The question is whether that organization builds or buys
the facility, or GBO builds a self-service flow on top of the register.
There is no working assumption, because the demo loads its participants
into the register in advance.

Forum, options, working assumption and links: [issue #76](https://github.com/ICTU/GBO-TO/issues/76).

### Q-75: Does every source response get one seal, regardless of channel (DvTP, EUDI, ASI)? {#q-75}

- **Status**: open

The functional requirements ask the bronhouder to seal all outgoing
data sets with a qualified electronic seal, without naming the standard.
In the ASI, the ASIP already seals every result, and in issuance the
attestation carries the seal of the issuer. A DvTP source response has
no seal, and FSC mTLS protects only the transport. The question is
whether every response gets one seal, which level and format apply, who
holds the key, and what happens when sealing fails. The starting point
is one seal for every channel, and in the demo only the ASI seals.

Forum, options, working assumption and links: [issue #77](https://github.com/ICTU/GBO-TO/issues/77).

### Q-76: Does the validity period apply per consent or per source within the consent? {#q-76}

- **Status**: open

The functional requirements give each consent rule its own validity
period per source, while the register and the proof know one valid-until
per consent. The question is which of the two levels applies. A validity
per source changes the screen, gives the proof a valid-until per source,
and lets a consent expire for one source only. The demo calls one source
per consent, so the difference is not visible. The working assumption is
one validity per consent, equal to the expiry time of the proof.

Forum, options, working assumption and links: [issue #78](https://github.com/ICTU/GBO-TO/issues/78).

### Q-77: What is a change of a consent: a new consent or an amendment of the existing one? {#q-77}

- **Status**: open

The PSA asks the consent register to support granting, change,
revocation and expiry of a consent, but no requirement covers change.
The consent proof binds the data sets and the validity, so a change also
affects the proof that the consumer holds. The question is which changes
the citizen can make, who starts them, and whether the consumer then
gets a new proof. The options range from no change, through restrictions
only, to a new consent that replaces the old one. The working assumption
is no change: the citizen revokes, and the consumer starts a new
request.

Forum, options, working assumption and links: [issue #79](https://github.com/ICTU/GBO-TO/issues/79).

### Q-78: How does the reference policy show that it is not tied to one policy language or engine? {#q-78}

- **Status**: open

The PSA requires that policy is product-independent and not tied to one
policy language or engine. The reference policy of GBO uses one language
for one engine. A source with another PDP cannot take it over or show
equal decisions. The question is how GBO shows independence: rules as
data, a shared decision test set, or one open language with an exit
path. There is no decision, and the demo has one engine and one policy
language.

Forum, options, working assumption and links: [issue #80](https://github.com/ICTU/GBO-TO/issues/80).

### Q-79: Does GBO build the OOTS adapter, or does the OOTS-V operator extend its facility with the GBO interface? {#q-79}

- **Status**: open

The PSA lets an OOTS adapter connect to the national interface of
OOTS-V, and OOTS requests use the same authorization and logging as
other requests. The question is whether GBO builds that adapter, or the
OOTS-V operator extends its facility with the GBO interface. The choice
decides the route to the source, the regime and evidence for OOTS, and
the versioned mapping to OOTS-EDM. The PDP knows only the consent and
PID regimes, so it denies an OOTS request without its own evidence.
There is no working assumption, because the demo has no OOTS route.

Forum, options, working assumption and links: [issue #81](https://github.com/ICTU/GBO-TO/issues/81).

### Q-80: Which component onboards sources for all channels, and who manages their lifecycle? {#q-80}

- **Status**: open

More than one channel depends on the description that a source
publishes. Attestation issuance and the ASIP both read the active
release from the source registry. In the building block view, the
EUDI adapter fetches, validates and refreshes that description, so the
ASIP depends on a component of another channel. A source that offers
only verification attributes then has no natural place. The GBO team
proposes a separate onboarding component that serves all channels,
while the channels only read. Also open is who manages the lifecycle of
a source and acts when its description expires.

Forum, options, working assumption and links: [issue #83](https://github.com/ICTU/GBO-TO/issues/83).
