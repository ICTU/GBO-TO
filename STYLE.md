# Style guide for the GBO Technisch Ontwerp

This guide applies to all prose in `docs/` and `README.md`. It combines
three rule sets:

1. **ASD-STE100 Simplified Technical English, pragmatic mode.** Agents
   load the `simple-english` skill.
2. **Google developer documentation style.** Agents load the
   `google-developer-documentation-style` skill.
3. **Humanizer** (remove AI writing patterns), from
   [blader/humanizer](https://github.com/blader/humanizer). Agents load
   the `humanizer` skill.

The three rule sets conflict in places. This guide settles the conflicts
and fixes the vocabulary. Where this guide and a rule set disagree, this
guide wins.

When you edit existing text, keep the meaning. Do not add or remove a
fact, a status, an ID, a link target, a number, a date, a name or a claim
unless that is the purpose of the change.

## Untouchables (never change these)

- Fenced code blocks, including every ```mermaid diagram (labels too).
- Inline code in backticks, file paths, commands, field names, error
  strings, reason codes.
- Link targets (the part in parentheses). You MAY change link text, but
  link text that is an ID (`[REQ-74](…)`) or a page title stays as is.
- Heading anchors `{#…}` and the ID part of a heading (`## REQ-74: …`,
  `### F-70: …`, `# ADR-0031: …`). You MAY improve the title after the
  colon, in sentence case, without a dash.
- The field labels at the start of list items in register entries:
  `- **Status**:`, `- **Source**:`, `- **Addressee**:`, `- **Evidence**:`,
  `- **Related**:`, `- **Notes**:`, `- **Type**:`, `- **Trigger**:`,
  `- **Observation**:`, `- **Why it matters**:`, `- **Proposal**:`,
  `- **Forum**:`, `- **Question**:`, `- **Why the demo cannot answer it**:`,
  `- **Options**:`, `- **Current working assumption**:`, `- **Demo work**:`,
  `- **What it showed**:`, `- **Produced**:`, `- **Explained in**:`,
  `- **Answer**:`, `- **Landed in**:`, `- **History**:`, `- **Outcome**:`
  and similar labels. They are a data structure (a script reads
  `**Status**`). Keep the label. Rewrite the value.
- The first status word after `- **Status**:` (open, closed, resolved in
  demo, superseded, premise lapsed, answered, partly answered, draft,
  ready for review, approved, covered, withdrawn, candidate, done, planned,
  blocked, dropped, merged, accepted, proposed, deferred, fixed). Text
  after that word you may rewrite.
- The whole `## Traceability` section at the end of a page (footer).
  Do not touch it.
- RFC 2119 keywords in CAPITALS inside requirement statements and
  guidelines: MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, NEED NOT. They are
  normative technical terms (ASD-STE100 rule 1.5). Keep them in the
  requirement sentence (the `>` blockquote) and in RL and AV statements.
  Everywhere else use lowercase "must" and "can" (see modals).
- Quoted text from a source (in quotation marks) and Dutch proper names
  (MijnOverheid, Logius, Belastingdienst, Toestemmingsportaal, ...).
- Tables: keep the columns and rows. Rewrite the prose inside cells.
  A cell that holds only `—` means "none": keep it.
- Table rows in the "Data per hop" tables keep their hop numbers.

## Hard rules (the linter reports these as errors)

1. **Sentence length.** Descriptive sentences: 25 words at most.
   Instructions (imperative): 20 words at most. A Markdown link, text in
   parentheses, inline code, a number, and an ID each count as one word.
   Split long sentences. Turn enumerations into vertical lists.
2. **No semicolons** in prose, tables, headings or lists. Write two
   sentences, use a comma, or a list. In "Related" fields separate links
   with commas.
3. **No dashes as connectors**: no em dash (—), no en dash (–), no ` -- `.
   Use a period, comma, colon or parentheses. Ranges: "REQ-83 to REQ-95",
   "2 to 5". (A table cell with only `—` stays.)
4. **Modal verbs**: only can, must, will. No should, would, may, might,
   could (lowercase or sentence-start). Requirement → must. Possibility or
   permission → can. Recommendation → state it as a fact with the reason,
   or "it is better to … because …". Hypothetical → "If X, Y."
5. **No contractions** (don't, it's, isn't, can't …): write them out.
6. **No present perfect**: no "has been / have been / had been / has
   changed". Use simple past or simple present.
7. **No Latin abbreviations**: "for example", "that is", name the items
   instead of "etc.".
8. **No first person** (we, our, us). Name the actor: "the GBO team",
   "the demo", "this design", "the TO".
9. **No "not just / not only / not merely"**, no "It is not X, it is Y".
10. **No and/or, no exclamation marks, no "please", no curly quotes.**
11. **Dates**: "November 2, 2026" (month spelled out). Never "2 Nov 2026".
12. **Headings**: sentence case, no end period, no dash, do not start with
    an -ing word.

## Judgment rules (the linter warns; fix unless you have a reason)

- **Conditions first**: "If the token is missing, the PDP denies." Move
  every trailing "if/when/unless" clause to the start of the sentence.
- **Active voice.** Name who acts. Passive only when the actor is unknown
  or does not matter.
- **Present tense** for behavior. Simple past for history ("PR #363
  removed the property").
- **Timeless wording**: no "currently, now, recently, soon, latest, at
  present, not yet, new" to describe behavior. Anchor to the demo
  release: "In demo v0.9.0, …", "not built in demo v0.9.0", or give the
  date. "Not yet" → "not built", "open", or "no decision".
- **No directional words**: "the following", "the preceding", not
  above/below. For limits write "more than / less than".
- **One new fact per sentence. Paragraphs: six sentences at most.**
- **Lists and tables** get a lead-in sentence that is a complete sentence
  about the subject, ending in a colon. Not "The table below shows:" (the
  reader can see it, humanizer §25) and not a fragment ("The PDP:"). Good:
  "The PDP refuses a contract for one of eight reasons, in this order:".
- **Humanizer patterns to remove**: §1 not-X-but-Y and "X, not Y"
  contrasts that only add weight (keep a contrast that corrects a real,
  stated belief, for example a superseded decision); §2 one-line closers
  and "This means/This shows" restatements; §3 aphorisms; §4 run-ups
  ("Note that", "In short", "The point is"); §5 arguing with no one;
  §6 forced triads; §12 stock words (additionally, crucial, key as an
  adjective, robust, enhance, highlight, valuable, pivotal, landscape,
  align with, underscore, showcase); §13 inflated significance;
  §15 -ing riders (", ensuring …", ", making …"); §18 "serves as / stands
  as / represents" → is; §19 bold as decoration (remove bold in running
  text; keep the field labels and the bold in "Data per hop" only where it
  marks a sensitive value such as **BSN**, and keep it sparingly);
  §25 writing about the document ("This page describes", "The port
  updated") → state the subject fact. A page may keep one opening
  sentence that tells the reader what the page covers (Google "know your
  reader"); make it about the subject.
- **Arrows (→)** are fine inside tables and diagrams as a direction
  notation ("Portal backend → register"). In running text write "to",
  "calls", "sends".
- **Parentheses**: fine for IDs, links, abbreviations and short
  explanations. Do not hide an important fact in parentheses.
- **Numbers**: zero to nine in words in running text, except versions,
  IDs, technical quantities, durations with units, percentages and
  counts in tables.
- **Serial comma** in series of three or more.
- **Articles and "that"** stay: no telegraph style ("Ensure file
  exists" → "Make sure that the file exists").

## Fixed vocabulary (use exactly these, everywhere)

| Concept | Use | Do not use |
|---|---|---|
| test a condition (general) | check (verb and noun) | confirm, ensure, assert, examine |
| cryptographic or identity check; the ASI operation | verify, verification | — |
| check against a schema or rule set | validate, validation | — |
| make something true | make sure that (instructions); MUST (requirements) | ensure |
| settings | configuration, configure | config, settings, set-up |
| start a program or test | run | execute, invoke, launch |
| use an API or service | call | invoke, hit, query (unless GraphQL query) |
| show to a user | show | display, render, present |
| take data away | delete | drop, destroy, purge |
| take out of code, design or a list | remove | — |
| a fault message | error | issue (for faults), problem |
| a failed operation | failure | — |
| PDP outcome | allow, deny (decision) | permit, reject |
| other components saying no | refuse | reject |
| afnemer | consumer | client (except OAuth client), customer |
| bron | source | data source (except in "authentic source") |
| burger | citizen | user (except user of software) |
| toestemming | consent | permission |
| toestemmingsbewijs | consent proof (verified); consent token (the JWT before verification) | — |
| increment (SL-NN) | demo increment | slice |
| demo baseline | gbo-demo v0.9.0, "the demo" | "the current demo", "now" |

The TO is written in English. Use the English term from the
[glossary](docs/glossary.md) for every domain concept. On the first use
on a page, add the Dutch name of the Globaal Ontwerp in parentheses, for
example "consent register (toestemmingsregister)". After that, use the
English term only. Never translate proper names: MijnOverheid, DigiD,
Logius, BSN, Autorisatielijst BSN, Basisinrichting OOTS, Logboek
Dataverwerkingen, GBO Basis. Quotes from Dutch sources stay in Dutch.

The glossary is the source for all domain and system terms. Each
glossary table has a "Do not use" column. The linter reports those words
as errors in every page except the glossary, unless the word stands
directly inside parentheses. When you add a term, add it to the glossary
first. `scripts/gen_abbreviations.py` turns the abbreviations into
tooltips on every page.

US spelling (authorization, organization, recognize, pseudonymization).

## Register entries

Each entry keeps its structure: the heading with the ID and the anchor,
then the `- **Status**:` line (the traceability script reads it), then
the readable part, then a collapsible block with the labeled fields.

- A finding or an open question starts with a plain summary of three to
  five sentences that a newcomer can read. The fields with evidence,
  links and history go into a collapsible block, for example
  `??? note "Evidence, impact and proposal"`, with the content indented
  by four spaces.
- A requirement shows the requirement statement (the blockquote) and the
  case table. Its fields (source, addressee, evidence, related, notes) go
  into the block `??? note "Source, evidence and notes"`.
- Closed findings and answered questions are short entries and have no
  collapsible block. They live on their own pages.
## Diagrams

The TO is diagram first, like the Globaal Ontwerp and the EUDI ARF. Each
page in the building block view starts with a diagram, and the text
explains the diagram.

- Use the shared palette. Put `--8<-- "mermaid/classes.mmd"` in every
  flowchart and assign a class to every node: `basis` (GBO Basis),
  `dvtp` (GBO DvTP component), `eudi` (GBO EUDI or OOTS component),
  `source` (source or citizen), `ext` (external party), `store`
  (register, log, store), `mock` (demo scaffolding), `planned` (design
  only). The legend is in the building block overview.
- In a sequence diagram, group the participants in `box` blocks with the
  same colors: GBO Basis `rgb(220,252,231)`, DvTP `rgb(254,220,216)`,
  EUDI `rgb(255,237,213)`, source `rgb(221,235,247)`, external
  `rgb(241,239,232)`, records `rgb(237,233,254)`.
- A block that zooms in to a deeper page gets the class `zoom` (thick
  border) and a `click` line. Mermaid click targets are site URLs,
  relative to the page URL, with a trailing slash (`"authorization/"`).
  After a build, `python3 scripts/check_diagram_links.py site` checks
  every click target. CI runs it.
- Put a caption under each diagram: `*Figure N: ...*` followed by
  `{: .caption }` on the next line. Number the figures per page.
- Keep a diagram readable at page width: at most about 15 nodes. Split a
  larger picture into levels.


## Check your text

Run the style linter on the files you changed:

```bash
python3 scripts/style_lint.py docs/concepts/consent.md
python3 scripts/style_lint.py --summary   # all pages
```

- The linter must show 0 errors. CI runs it with `--strict`.
- Warnings need a decision. Fix them, or keep the text when the rule does
  not apply, for example "confirmation" as the defined FR-08 term, or bold
  **BSN** in a "Data per hop" table.
- Text in straight double quotes is source text. The linter ignores it
  and counts it as one word. Keep source quotes exact.
- Roman numerals (Annex I, Part II) are fine.
- The demo calls parts of an epic "slices". Write "part N of epic #336":
  the TO reserves "demo increment" for SL-NN.

Then run the traceability check and the strict build:

```bash
python3 scripts/gen_traceability.py
mkdocs build --strict
```

Last, read the text once as a reader. Every sentence must add a fact,
read naturally, and survive one read.
