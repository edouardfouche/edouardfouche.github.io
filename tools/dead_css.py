"""List rules of a stylesheet whose selectors match no element on any built page.

Usage: python3 tools/dead_css.py <built site dir> <file.css>
Pseudo-classes such as :hover are stripped before matching, and the class that Bootstrap's collapse
plugin adds at run time (.navbar-collapse.in) is simulated. Prints DEAD (no selector matches), PART
(some selectors of the list match) and parse errors. A rule that matches nothing today may still be
wanted for future content: check before deleting.
"""
import os
import re
import sys

import tinycss2
from bs4 import BeautifulSoup

SITE, CSS = sys.argv[1], sys.argv[2]
docs = []
for root, _, files in os.walk(SITE):
    for f in files:
        if f.endswith(".html"):
            soup = BeautifulSoup(open(os.path.join(root, f), encoding="utf-8").read(), "html5lib")
            for el in soup.select(".navbar-collapse"):
                el["class"] = el.get("class", []) + ["in"]
            docs.append(soup)

DYNAMIC = re.compile(r"::?(hover|focus|active|visited|link|before|after|selection|-moz-selection|first-letter|first-line)\b")


def matches(sel):
    s = DYNAMIC.sub("", sel).strip()
    if not s:
        return True
    try:
        return any(d.select_one(s) is not None for d in docs)
    except Exception as e:  # selector soupsieve cannot evaluate: treat as live, report it
        print(f"   ? cannot test {sel!r}: {e}")
        return True


def walk(rules, ctx=""):
    for r in rules:
        if r.type == "qualified-rule":
            prelude = tinycss2.serialize(r.prelude).strip()
            sels = [s.strip() for s in prelude.split(",") if s.strip()]
            live = [s for s in sels if matches(s)]
            dead = [s for s in sels if s not in live]
            if dead:
                status = "DEAD " if not live else "PART "
                print(f"{status} L{r.source_line:<4} {ctx}{prelude[:90]}" + (f"   dead parts: {dead}" if live else ""))
        elif r.type == "at-rule":
            if r.content is not None and r.lower_at_keyword in ("media", "supports"):
                walk(tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True),
                     ctx + "@" + r.lower_at_keyword + tinycss2.serialize(r.prelude).strip()[:40] + " ")
        elif r.type == "error":
            print(f"ERROR L{r.source_line:<4} {r.message}")


walk(tinycss2.parse_stylesheet(open(CSS, encoding="utf-8").read(), skip_comments=True, skip_whitespace=True))
print("done (no DEAD/PART/ERROR lines above = every rule matches something)")
