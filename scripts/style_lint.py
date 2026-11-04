#!/usr/bin/env python3
"""Check the prose in docs/ against the house style.

The house style combines three rule sets:

- ASD-STE100 Simplified Technical English, pragmatic mode (sentence
  length, approved modal verbs, no semicolons, no contractions, no
  present perfect, conditions first);
- the Google developer documentation style guide (sentence case,
  timeless wording, no Latin abbreviations, no directional language);
- the humanizer rules (no dashes as connectors, no stock AI words,
  no staged contrasts, no decorative formatting);
- the glossary: a word from a "Do not use" column of docs/glossary.md is
  an error outside the glossary itself.

The script removes everything that is not prose before it checks:
code blocks, mermaid diagrams, inline code, URLs, HTML comments and
heading anchors. A Markdown link counts as one word, and so does text
in parentheses (ASD-STE100 rules 8.5 and 8.6).

Quoted text in straight double quotes is source text: it counts as one
word and the rules do not apply to it.

Usage:
  python3 scripts/style_lint.py [FILE ...]        report per file
  python3 scripts/style_lint.py --summary         counts only
  python3 scripts/style_lint.py --strict          exit 1 on any error

Errors break a hard rule. Warnings need a human decision.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SKIP = {"traceability/coverage.md"}  # generated

MAX_WORDS = 25

ERRORS = {
    "semicolon": re.compile(r";"),
    "contraction": re.compile(
        r"\b(?:[A-Za-z]+n't|[A-Za-z]+'(?:ll|re|ve|d)|it's|It's|that's|That's|"
        r"there's|There's|here's|Here's|what's|What's|let's|Let's|who's)\b"),
    "modal": re.compile(r"\b(?:should|would|may|might|could|Should|Would|Might|Could)\b|\bMay\b(?! \d)"),
    "perfect tense": re.compile(r"\b(?:has|have|had) been\b"),
    "dash": re.compile(r"[—–]| -- "),
    "latin abbreviation": re.compile(r"\b(?:e\.g\.|i\.e\.|etc\.)", re.I),
    "and/or": re.compile(r"\band/or\b", re.I),
    "curly quote": re.compile(r"[“”‘’]"),
    "exclamation": re.compile(r"!(?=\s|$)"),
    "please": re.compile(r"\bplease\b", re.I),
    "first person": re.compile(r"\b(?:we|We|our|Our|us)\b|\bI (?:am|think|have|was|will|believe|see|use|do|did|can|propose|suggest|recommend|found|checked)\b"),
    "date format": re.compile(
        r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{4}\b"),
    "ing rider": re.compile(r", (?:making|allowing|enabling|ensuring|highlighting|"
                            r"underscoring|emphasizing|reflecting|showcasing|fostering)\b"),
    "not-x-but-y": re.compile(r"\bnot (?:just|only|merely)\b|\bit is not .{1,40}, it is\b", re.I),
}

SLOP = re.compile(
    r"\b(?:leverag\w*|utiliz\w*|in order to|prior to|ensur\w*|simply|easily|"
    r"seamless\w*|robust|powerful|comprehensive|crucial\w*|additionally|delv\w*|"
    r"enhanc\w*|showcas\w*|underscor\w*|pivotal|valuable|meticulous\w*|vibrant|"
    r"testament|intricac\w*|intricate|interplay|garner\w*|bolster\w*|align(?:s|ed)? with|"
    r"facilitat\w*|allows? you to|enables? you to|is designed to|plays? a (?:key )?role|"
    r"serves? as|stands? as|boasts?|in the event that|due to the fact|streamlin\w*|"
    r"notably|importantly|it is worth noting|at its core|landscape|"
    r"configuration settings|settings|confirm\w*)\b", re.I)

TIME = re.compile(r"\b(?:currently|recently|soon|at present|at the moment|"
                  r"nowadays|now|not yet|latest)\b", re.I)
DIRECTION = re.compile(r"\b(?:above|below)\b", re.I)
WEAK_CONTRAST = re.compile(r"\brather than\b|, not (?:a |an |the )?\w+", re.I)

ING_HEADING = re.compile(r"^#{1,6} [A-Z][a-z]+ing\b")


def glossary_banned():
    """Words from the "Do not use" columns of docs/glossary.md."""
    path = DOCS / "glossary.md"
    banned = {}
    if not path.exists():
        return banned
    col = None
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            col = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "Do not use" in cells:
            col = cells.index("Do not use")
            continue
        if col is None or set(line) <= set("|-: "):
            continue
        term = re.sub(r"[`*]", "", cells[0])
        for word in cells[col].split(","):
            word = word.strip()
            if word and word != "—":
                banned[word] = term
    return banned


BANNED = glossary_banned()
BANNED_RX = [(re.compile(r"(?<![-/\w(])(?<!trust )(?<!technical )" + re.escape(w) + r"(?:s|en|ken)?\b", re.I), w, t)
             for w, t in BANNED.items()]


def strip_nonprose(text):
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    out, fence = [], False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
            out.append("")
            continue
        out.append("" if fence else line)
    return out


def clean_line(line):
    line = re.sub(r"\{#[^}]*\}", "", line)
    line = re.sub(r"`[^`]*`", "CODE", line)
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "IMG", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", lambda m: "LINK", line)
    line = re.sub(r"https?://\S+", "URL", line)
    # quoted source text counts as one word and is not checked (ASD-STE100 8.6)
    line = re.sub(r'"[^"\n]{1,400}"', "QUOTE", line)
    return line


def collapse_parens(s):
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^()]*\)", "PAREN", s)
    return s


def sentences(par):
    par = collapse_parens(par)
    par = re.sub(r"\b(?:Mr|Dr|vs|No|Fig|cf)\.", "ABBR", par)
    parts = re.split(r"(?<=[.?!:])\s+(?=[A-Z0-9\[\*`\"])", par)
    return [p.strip() for p in parts if p.strip()]


def words(s):
    s = re.sub(r"\*\*|__|\*", "", s)
    return [w for w in re.split(r"\s+", s) if re.search(r"[A-Za-z0-9]", w)]


def is_table(line):
    return line.lstrip().startswith("|")


def table_cells(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return [c for c in cells if c and not re.fullmatch(r":?-{2,}:?", c)]


def blocks(lines):
    """Yield (lineno, kind, text): paragraphs, list items, table cells, headings."""
    buf, start = [], 0
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip()
        if re.match(r"^\s*>", line):  # blockquote: check the quoted prose
            line = re.sub(r"^\s*>\s?", "", line)
        if not line.strip():
            if buf:
                yield start, "para", " ".join(buf)
                buf = []
            continue
        if line.lstrip().startswith("#"):
            if buf:
                yield start, "para", " ".join(buf)
                buf = []
            yield i, "heading", line.strip()
            continue
        if is_table(line):
            if buf:
                yield start, "para", " ".join(buf)
                buf = []
            for c in table_cells(line):
                yield i, "cell", c
            continue
        m = re.match(r"^\s*(?:[-*+]|\d+\.)\s+(.*)$", line)
        if m:
            if buf:
                yield start, "para", " ".join(buf)
            buf, start = [m.group(1)], i
            continue
        if line.startswith("    ") and buf:
            buf.append(line.strip())
            continue
        if not buf:
            start = i
        buf.append(line.strip())
    if buf:
        yield start, "para", " ".join(buf)


def lint_file(path):
    try:
        rel = path.relative_to(DOCS).as_posix()
    except ValueError:
        rel = str(path)
    lines = strip_nonprose(path.read_text())
    issues = []

    def add(level, rule, ln, text):
        issues.append((level, rule, ln, text[:140]))

    for ln, kind, raw in blocks(lines):
        text = clean_line(raw)
        if kind == "heading":
            h = re.sub(r"\s*\{#[^}]*\}\s*$", "", raw)
            if h.rstrip().endswith("."):
                add("E", "heading ends with period", ln, h)
            if ING_HEADING.match(h):
                add("W", "heading starts with -ing", ln, h)
            body = re.sub(r"^#+\s*", "", h)
            body = re.sub(r"^(?:ADR-\d+|[A-Z]+-\d+[a-c]?|E\d+):\s*", "", body)
            ws = [w for w in re.findall(r"[A-Za-z][\w'-]*", body)]
            caps = [w for w in ws[1:] if w[0].isupper() and not w.isupper()
                    and not re.search(r"[A-Z].*[A-Z]", w)]
            if len(ws) > 3 and len(caps) > len(ws) / 2:
                add("W", "title case heading", ln, h)
            for rule in ("dash", "semicolon", "curly quote"):
                if ERRORS[rule].search(clean_line(body)):
                    add("E", rule, ln, h)
            continue
        if kind == "cell" and text.strip() in ("—", "–", "-"):
            continue
        # field labels "**Status**:" are structure, not decoration
        text_nolabel = re.sub(r"^\*\*[^*]{1,40}\*\*:?\s*", "", text)
        for rule, rx in ERRORS.items():
            m = rx.search(text_nolabel)
            if m:
                add("E", rule, ln, text_nolabel[max(0, m.start() - 40):m.end() + 60])
        if rel != "glossary.md":
            for rx, word, term in BANNED_RX:
                m = rx.search(text_nolabel)
                if m:
                    add("E", f"glossary: use '{term}', not '{word}'", ln,
                        text_nolabel[max(0, m.start() - 40):m.end() + 60])
        for rx, rule in ((SLOP, "stock word"), (TIME, "time word"),
                         (DIRECTION, "directional word"), (WEAK_CONTRAST, "contrast")):
            m = rx.search(text_nolabel)
            if m:
                add("W", rule, ln, text_nolabel[max(0, m.start() - 40):m.end() + 60])
        if re.search(r"\*\*[^*]+\*\*", text_nolabel):
            add("W", "bold in prose", ln, text_nolabel)
        if "→" in text_nolabel and kind == "para":
            add("W", "arrow in prose", ln, text_nolabel)
        sents = sentences(text_nolabel)
        for s in sents:
            n = len(words(s))
            # a run of links ("REQ-1, REQ-2, ...") is a list, not a sentence
            if n and s.count("LINK") >= n / 2:
                continue
            if n > MAX_WORDS:
                add("E", f"sentence over {MAX_WORDS} words ({n})", ln, s)
        if kind == "para" and len(sents) > 6:
            add("W", f"paragraph over 6 sentences ({len(sents)})", ln, text_nolabel)
    return rel, issues


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    summary = "--summary" in sys.argv
    strict = "--strict" in sys.argv
    files = [pathlib.Path(a).resolve() for a in args] if args else sorted(DOCS.rglob("*.md"))
    tot_e = tot_w = 0
    rule_counts = {}
    for f in files:
        try:
            rel = f.relative_to(DOCS).as_posix()
        except ValueError:
            rel = str(f)
        if rel in SKIP:
            continue
        rel, issues = lint_file(f)
        e = sum(1 for i in issues if i[0] == "E")
        w = len(issues) - e
        tot_e += e
        tot_w += w
        for lvl, rule, _, _ in issues:
            key = (lvl, re.sub(r" \(\d+\)", "", rule))
            rule_counts[key] = rule_counts.get(key, 0) + 1
        if summary:
            if e or w:
                print(f"{e:5d} E {w:5d} W  {rel}")
        else:
            for lvl, rule, ln, text in issues:
                print(f"{rel}:{ln}: {lvl} {rule}: {text}")
    print("\nBy rule:")
    for (lvl, rule), n in sorted(rule_counts.items(), key=lambda x: (x[0][0], -x[1])):
        print(f"  {lvl} {n:6d}  {rule}")
    print(f"\nTotal: {tot_e} errors, {tot_w} warnings")
    sys.exit(1 if strict and tot_e else 0)


if __name__ == "__main__":
    main()
