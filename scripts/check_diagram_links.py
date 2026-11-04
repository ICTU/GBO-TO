#!/usr/bin/env python3
"""Check the click targets in Mermaid diagrams against the built site.

MkDocs does not validate links inside Mermaid blocks. This script reads
every `click NODE "target"` line in docs/, resolves the target against the
URL of its page (use_directory_urls), and checks that the page and the
anchor exist in the built site.

Usage: python3 scripts/check_diagram_links.py [SITE_DIR]   (default: site)
Run it after `mkdocs build`.
"""
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site"
CLICK = re.compile(r'^\s*click\s+\S+\s+(?:href\s+)?"([^"]+)"')


def page_url(md):
    rel = md.relative_to(DOCS).as_posix()[:-3]
    if rel == "index":
        return "/"
    if rel.endswith("/index"):
        return "/" + rel[: -len("index")]
    return "/" + rel + "/"


def main():
    errors = 0
    checked = 0
    for md in sorted(DOCS.rglob("*.md")):
        base = page_url(md)
        for n, line in enumerate(md.read_text().splitlines(), 1):
            m = CLICK.match(line)
            if not m:
                continue
            target = m.group(1)
            if target.startswith(("http://", "https://")):
                continue
            checked += 1
            path, _, frag = target.partition("#")
            url = posixpath.normpath(posixpath.join(base, path)) if path else base
            if not url.endswith("/"):
                url += "/"
            html = SITE / url.lstrip("/") / "index.html"
            rel = md.relative_to(ROOT)
            if not html.exists():
                print(f"{rel}:{n}: no page for '{target}' ({url})")
                errors += 1
                continue
            if frag and f'id="{frag}"' not in html.read_text():
                print(f"{rel}:{n}: no anchor '#{frag}' on {url}")
                errors += 1
    print(f"{checked} diagram links checked, {errors} broken")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
