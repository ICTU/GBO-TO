# GBO-TO: Technisch Ontwerp

The Technisch Ontwerp (TO) is the technical design for Gemeenschappelijke
Bronontsluiting (GBO). MkDocs Material and mike build the site. The setup
is the same as in the other GBO documentation repositories.

## Document chain

The TO is level 3 of the GBO document chain:

| Level | Document | Repository |
|---|---|---|
| 0 | [GBO site](https://ictu.github.io/GBO/) | entry point |
| 1 | [Globaal Ontwerp](https://ictu.github.io/GBO-GO/main/) | [ICTU/GBO-GO](https://github.com/ICTU/GBO-GO) |
| 2 | [Projectstartarchitectuur](https://ictu.github.io/GBO-PSA/main/) | [ICTU/GBO-PSA](https://github.com/ICTU/GBO-PSA) |
| 3 | Technisch Ontwerp (this repository) | [ICTU/GBO-TO](https://github.com/ICTU/GBO-TO) |
| 4 | gbo-demo | [ICTU/GBO-demo](https://github.com/ICTU/GBO-demo): reference implementation, ground truth for the behavior of GBO |

## Structure

The TO is the standalone reference for the GBO technical design. It has
three parts, all under `docs/`:

| Part | Path | Content |
|---|---|---|
| arc42 | `docs/*.md`, `docs/runtime/`, `docs/concepts/`, `docs/decisions/` | The 12 [arc42](https://arc42.org/overview) sections, with an ADR log in MADR format. |
| Requirements | `docs/requirements/` | Requirements (REQ), guidelines for bronhouders (RL), candidate connection conditions (AV), and BSNk preconditions (BSNK). |
| Traceability | `docs/traceability/` | The design-to-demo matrix, demo increments (SL), findings (F), open questions (Q), and feedback to standards bodies (E1 to E10). |

The TO absorbs the archived reference architecture v0.6.2. The ADR log
holds its decisions, including the superseded ones. The TO also absorbs
the traceability work that ran next to the demo. The IDs did not change.

## Rules of this document

When you change the TO, follow these four rules:

- **Pin the demo tag.** Each version of the TO is pinned to one gbo-demo
  tag. The pin for this version is
  [v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0). The demo at
  that tag is the ground truth. Link each statement about behavior to
  code or a test at that tag, as
  `https://github.com/ICTU/GBO-demo/blob/v0.9.0/<path>#L<n>`. Do not link
  to `blob/main`, because paths move.
- **Link, do not copy.** Link to PSA and GO content by URL (the `main`
  version). Do not restate it.
- **Record every divergence.** Record each deviation from the PSA, the
  GO, or the demo as an ADR, a finding, or a risk entry.
- **Link IDs to their page.** Link each mention of a REQ, F, Q, or SL ID
  to its anchor. End each arc42 page and each ADR with a "Traceability"
  section.

To move the pin to a newer demo tag, do these steps:

1. Check every changed statement against that tag.
2. Update the links and the baseline in `docs/index.md`.

## Local development

To build and preview the site on your computer, run these commands:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve          # live preview at http://localhost:8000
mkdocs build --strict # must pass before merging
```

Git ignores the `refs/` directory. This directory holds local clones of
the source repositories that the authors used while writing. To check
claims against the sources, clone the repositories into `refs/`.

## Writing style

All prose follows [STYLE.md](STYLE.md). Before you open a pull request,
run `python3 scripts/style_lint.py --summary`. The linter must show 0
errors.

## Contribute and release

The repository uses this workflow:

- Open a pull request. CI builds the site and publishes a PR preview
  (`.github/workflows/preview.yml`).
- A merge to `main` deploys the working version to
  `https://ictu.github.io/GBO-TO/main/` through mike
  (`.github/workflows/publish.yml`).
- A tag `v<X.Y.Z>` deploys that version with the `latest` alias. That
  version becomes the site default.
- Keep `extra.document_version` in `mkdocs.yml` in sync with the tag.

If a content change touches behavior, cite gbo-demo code at the pinned
tag. If a change diverges from the PSA or the GO, add or update an ADR or
a risk entry.
