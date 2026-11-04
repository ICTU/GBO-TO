#!/usr/bin/env python3
"""Generate docs/traceability/coverage.md and check traceability IDs.

The script reads:

- the registers: requirement pages (docs/requirements/*.md), findings,
  open questions, demo increments and standards feedback
  (docs/traceability/*.md). Each entry is a heading
  "## ID — title {#anchor}" or "### ID — title {#anchor}" followed by a
  "- **Status**: ..." line;
- the "## Traceability" footer of every arc42 page, concept page,
  runtime page and ADR.

It writes docs/traceability/coverage.md with two tables:

1. decision chains: ADR -> requirements -> increments -> findings ->
   open questions;
2. where each ID is explained: ID -> TO pages and ADRs.

It exits with status 1 when a page refers to an ID that no register
defines, or when an open finding or open question has no TO page or ADR.

Usage: python3 scripts/gen_traceability.py [--check]
  --check  do not write; fail when coverage.md is out of date.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "traceability" / "coverage.md"

ID = r"(?:REQ|RL|AV|BSNK|F|Q|SL)-\d+[a-c]?|E\d+"
HEAD = re.compile(rf"^#{{2,3}} ({ID})(?: —|:) (.+?) \{{#([a-z0-9-]+)\}}\s*$")
STATUS = re.compile(r"^- \*\*Status\*\*: (.+)$")
OPEN_PAGES = {"traceability/findings.md": "F", "traceability/open-questions.md": "Q"}
CLOSED_PAGES = {"traceability/findings-closed.md": "F", "traceability/answered-questions.md": "Q"}
LINK = re.compile(rf"\[({ID})\]\(([^)]+)\)")
KINDS = {"REQ": "Requirement", "RL": "Guideline", "AV": "Connection condition",
         "BSNK": "BSNk precondition", "F": "Finding", "Q": "Open question",
         "SL": "Demo increment", "E": "Standards feedback items"}
OPEN_F = {"open"}
OPEN_Q = {"open", "partly answered"}


def plural(word):
    return word if word.endswith("s") else word + "s"


def kind(i):
    return "E" if re.fullmatch(r"E\d+", i) else i.split("-")[0]


def sort_key(i):
    m = re.match(r"([A-Z]+)-?(\d+)([a-c]?)", i)
    return (m.group(1), int(m.group(2)), m.group(3))


def short_status(s):
    s = s.strip().rstrip(".")
    s = re.sub(r"\*", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # drop link markup
    if re.match(r"(accepted|proposed|superseded|deferred|rejected)\b", s):
        return s if len(s) <= 90 else s[:87] + "..."
    for word in ("partly answered", "ready for review", "resolved in demo",
                 "premise lapsed", "partly covered", "answered", "approved",
                 "covered", "withdrawn", "superseded", "candidate", "planned",
                 "blocked", "dropped", "merged", "closed", "draft", "done",
                 "open", "fixed", "accepted", "proposed", "deferred",
                 "rejected"):
        if s.lower().startswith(word):
            return word
    return s.split(";")[0].split(" — ")[0][:40]


def read_registers():
    reg = {}
    files = sorted((DOCS / "requirements").glob("*.md")) + sorted(
        (DOCS / "traceability").glob("*.md"))
    for f in files:
        if f.name in ("index.md", "coverage.md", "matrix.md"):
            continue
        rel = f.relative_to(DOCS).as_posix()
        cur = None
        for line in f.read_text().splitlines():
            m = HEAD.match(line)
            if m:
                cur = m.group(1)
                reg[cur] = {"title": m.group(2), "anchor": m.group(3),
                            "page": rel, "status": ""}
                continue
            if cur and not reg[cur]["status"]:
                s = STATUS.match(line)
                if s:
                    reg[cur]["status"] = short_status(s.group(1))
            if line.startswith("## ") and not HEAD.match(line):
                cur = None
    return reg


def page_title(text, fallback):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def read_footers():
    pages = {}
    skip = ("requirements/", "traceability/")
    for f in sorted(DOCS.rglob("*.md")):
        rel = f.relative_to(DOCS).as_posix()
        if rel.startswith(skip):
            continue
        text = f.read_text()
        if "## Traceability" not in text:
            continue
        foot = text.split("## Traceability", 1)[1]
        ids = [m.group(1) for m in LINK.finditer(foot)]
        pages[rel] = {"title": page_title(text, rel), "ids": ids,
                      "status": adr_status(text) if rel.startswith("decisions/0") else ""}
    return pages


def adr_status(text):
    m = re.search(r"^- Status: (.+)$", text, re.M)
    return short_status(m.group(1)) if m else ""


def all_mentions():
    """IDs linked anywhere in docs (to check that every link has a register entry)."""
    found = {}
    for f in DOCS.rglob("*.md"):
        rel = f.relative_to(DOCS).as_posix()
        if rel == "traceability/coverage.md":
            continue
        for m in LINK.finditer(f.read_text()):
            found.setdefault(m.group(1), set()).add(rel)
    return found


def link(reg, i, frm="traceability/coverage.md"):
    e = reg.get(i)
    if not e:
        return i
    target = pathlib.PurePosixPath(e["page"])
    base = pathlib.PurePosixPath(frm).parent
    rel = pathlib.PurePosixPath(*([".."] * len(base.parts))) / target if base.parts else target
    rel = str(rel).replace("../traceability/", "") if base.as_posix() == "traceability" else str(rel)
    return f"[{i}]({rel}#{e['anchor']})"


def page_link(rel, title):
    return f"[{title}](../{rel})"


def build(reg, pages):
    out = []
    w = out.append
    w("# Coverage\n")
    w("The script `scripts/gen_traceability.py` makes this page from the "
      "registers and from the *Traceability* section of every page. Do not "
      "edit this page by hand. After you change a register entry or a "
      "*Traceability* section, run `python3 scripts/gen_traceability.py`.\n")
    adrs = {k: v for k, v in pages.items() if k.startswith("decisions/0")}
    w("## Decision chains\n")
    w("Each architecture decision has one row. The row names the requirements "
      "that the decision serves and the demo increments that are its evidence. "
      "It also names the findings that led to the decision or stay open "
      "against it, and the open questions that the decision depends on. "
      "An open finding or an open question is in bold.\n")
    w("| Decision | Status | Requirements | Demo increments | Findings | Open questions |")
    w("|---|---|---|---|---|---|")

    def cell(ids, kinds, bold=None):
        sel = sorted({i for i in ids if kind(i) in kinds and i in reg}, key=sort_key)
        parts = []
        for i in sel:
            s = link(reg, i)
            if bold and reg[i]["status"] in bold:
                s = f"**{s}**"
            parts.append(s)
        return ", ".join(parts) or "—"

    for rel, p in sorted(adrs.items()):
        num = re.search(r"(\d{4})", rel).group(1)
        title = re.sub(r"^ADR-\d{4}:\s*", "", p["title"])
        w(f"| [ADR-{num}](../{rel}) {title} | {p['status']} | "
          f"{cell(p['ids'], {'REQ', 'RL', 'AV', 'BSNK'})} | {cell(p['ids'], {'SL'})} | "
          f"{cell(p['ids'], {'F'}, OPEN_F)} | {cell(p['ids'], {'Q'}, OPEN_Q)} |")

    where = {}
    for rel, p in pages.items():
        for i in p["ids"]:
            where.setdefault(i, set()).add(rel)

    w("\n## Where each ID is explained\n")
    w("Each register entry has one row. The row names the TO pages and the "
      "decisions that explain the entry or depend on it. Open entries that "
      "no page cites are in [Not explained](#not-explained).\n")
    for k in ("REQ", "RL", "AV", "BSNK", "SL", "F", "Q", "E"):
        ids = sorted([i for i in reg if kind(i) == k], key=sort_key)
        if not ids:
            continue
        w(f"### {plural(KINDS[k])}\n")
        w("| ID | Title | Status | Explained in |")
        w("|---|---|---|---|")
        for i in ids:
            ps = sorted(where.get(i, []))
            cells = ", ".join(page_link(r, short_page(r, pages[r]["title"])) for r in ps) or "—"
            w(f"| {link(reg, i)} | {reg[i]['title']} | {reg[i]['status']} | {cells} |")
        w("")

    missing = [i for i in sorted(reg, key=sort_key)
               if not where.get(i) and (
                   (kind(i) == "F" and reg[i]["status"] in OPEN_F) or
                   (kind(i) == "Q" and reg[i]["status"] in OPEN_Q))]
    w("## Not explained\n")
    if missing:
        w("No TO page or decision cites these open findings and open questions:\n")
        for i in missing:
            w(f"- {link(reg, i)} {reg[i]['title']}")
    else:
        w("Every open finding and every open question is cited by at least one "
          "TO page or decision.")
    w("")
    return "\n".join(out), missing


def short_page(rel, title):
    if rel.startswith("decisions/0"):
        return "ADR-" + re.search(r"(\d{4})", rel).group(1)
    return title


def main():
    check = "--check" in sys.argv
    reg = read_registers()
    pages = read_footers()
    text, missing = build(reg, pages)
    errors = []
    for i, files in sorted(all_mentions().items(), key=lambda x: sort_key(x[0])):
        if i not in reg:
            errors.append(f"{i} is linked in {', '.join(sorted(files))} but no register defines it")
    for i in missing:
        errors.append(f"{i} ({reg[i]['status']}) has no TO page or decision")
    for i, e in reg.items():
        is_open = (kind(i) == "F" and e["status"] in OPEN_F) or (
            kind(i) == "Q" and e["status"] in OPEN_Q)
        if e["page"] in OPEN_PAGES and not is_open:
            errors.append(f"{i} is {e['status']}: move it to the closed page")
        if e["page"] in CLOSED_PAGES and is_open:
            errors.append(f"{i} is {e['status']}: move it to the open page")
    if check:
        if not OUT.exists() or OUT.read_text() != text:
            errors.append("docs/traceability/coverage.md is out of date; run the script")
    else:
        OUT.write_text(text)
        print(f"wrote {OUT.relative_to(ROOT)}: {len(reg)} register entries, "
              f"{len([p for p in pages if p.startswith('decisions/0')])} decisions, "
              f"{len(pages)} pages with a footer")
    for e in errors:
        print("ERROR:", e, file=sys.stderr)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
