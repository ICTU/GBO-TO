#!/usr/bin/env python3
"""Find Dutch words in the English prose of docs/.

The TO is written in English. Dutch is allowed only in these places:

- proper names (PROPER_NAMES), for example Gemeenschappelijke
  Bronontsluiting or Delen van gegevens via Toestemming met Private
  dienstverleners;
- the Dutch GO name directly inside parentheses after the English term,
  on its first use on a page, for example "consent register
  (toestemmingsregister)";
- quotes from Dutch sources in double quotes;
- code, identifiers, field names and URLs;
- the glossary, which gives the Dutch names on purpose.

A word counts as Dutch when the wordfreq frequency for Dutch is clearly
higher than for English. ALLOW lists the words that are not Dutch in this
text (technical terms, product names).

Usage: python3 scripts/check_dutch.py [--strict] [FILE ...]
"""
import pathlib
import re
import sys

from wordfreq import zipf_frequency

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SKIP = {"glossary.md", "traceability/coverage.md"}

PROPER_NAMES = re.compile(
    r"Gemeenschappelijke\s+Bronontsluiting|Delen\s+van\s+gegevens\s+via\s+"
    r"Toestemming\s+met\s+Private\s+dienstverleners|Globaal\s+Ontwerp|"
    r"Technisch\s+Ontwerp|Projectstartarchitectuur|Basisinrichting\s+OOTS|"
    r"Logboek\s+Dataverwerkingen|Federatieve\s+Toegangsverlening|"
    r"Federatief\s+Datastelsel|Generieke\s+Digitale\s+Infrastructuur|"
    r"Autorisatielijst\s+BSN|Forum\s+Standaardisatie|MijnOverheid|"
    r"Belastingdienst|Rijksdienst\s+voor\s+Identiteitsgegevens|"
    r"Installatie\s+Register|Hypotheek-BV|GBO\s+Basis|eHerkenning|"
    r"Digikoppeling|PKIoverheid|Logius|DigiD|ICTU|eIDAS2?\b|[Bb]ronhouders?\b")

ALLOW = set("""
schema door demo lint opa's ok blader gbo-semantiek ldv-logboek
dienstverlener-backend dienstverlener-mock req-azp
""".split())

PROTECT = re.compile(
    r"```.*?```|`[^`\n]*`|\]\([^)]*\)|https?://\S+|\{#[^}]*\}"
    r"|\"[^\"]{1,600}\"|“[^”]{1,600}”|<[^>]+>", re.S)


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def is_dutch(word):
    w = word.lower().strip("'-")
    if w in ALLOW or len(w) < 4 or re.search(r"\d", w):
        return False
    en = zipf_frequency(w, "en")
    nl = zipf_frequency(w, "nl")
    return nl > 0 and (en == 0 or nl >= en + 0.8)


def scan(path):
    text = path.read_text()
    prose = PROTECT.sub(blank, text)
    prose = PROPER_NAMES.sub(blank, prose)
    hits = []
    for m in re.finditer(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]{3,}", prose):
        if not is_dutch(m.group(0)):
            continue
        # allowed: a Dutch name of at most five words that fills a pair of
        # parentheses, for example "(akte van overlijden)"
        op = prose.rfind("(", 0, m.start())
        cl = prose.find(")", m.end())
        if op != -1 and cl != -1 and "\n\n" not in prose[op:cl]:
            inner = prose[op + 1:cl]
            if ")" not in inner and "(" not in inner and len(inner.split()) <= 5:
                continue
        line = prose.count("\n", 0, m.start()) + 1
        hits.append((line, m.group(0), text.split("\n")[line - 1].strip()))
    return hits


def main():
    strict = "--strict" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = [pathlib.Path(a).resolve() for a in args] if args else sorted(DOCS.rglob("*.md"))
    total = 0
    for f in files:
        try:
            rel = f.relative_to(DOCS).as_posix()
        except ValueError:
            rel = str(f)
        if rel in SKIP:
            continue
        for line, word, ctx in scan(f):
            total += 1
            print(f"{rel}:{line}: '{word}': {ctx[:140]}")
    print(f"{total} Dutch words outside names, quotes and parentheses")
    sys.exit(1 if strict and total else 0)


if __name__ == "__main__":
    main()
