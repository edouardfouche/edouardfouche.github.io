"""Static audit of a built site: HTML parse errors, duplicate IDs, headings, images, links, metadata.

Usage: python3 tools/html_audit.py <built site dir> <report.json>
Prints a summary per page; the JSON report also lists external links and missing internal targets.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse, unquote

import html5lib
from bs4 import BeautifulSoup, Comment

SITE, OUT = sys.argv[1], sys.argv[2]
GENERIC_ALTS = {"img", "image", "icon", "picture", "photo", "contact", "profil picture"}

pages = sorted(os.path.join(r, f) for r, _, fs in os.walk(SITE) for f in fs if f.endswith(".html"))
report, external_links, internal_missing = {}, defaultdict(set), defaultdict(set)


def resolve_internal(url, page_path):
    """Map an internal URL to a file of the built site; None if it does not exist."""
    path = unquote(urlparse(url).path)
    if not path:
        return "self"
    full = os.path.join(SITE, path.lstrip("/")) if path.startswith("/") else os.path.normpath(
        os.path.join(os.path.dirname(page_path), path))
    if os.path.isdir(full):
        full = os.path.join(full, "index.html")
    if os.path.exists(full):
        return full
    return full + ".html" if os.path.exists(full + ".html") else None


for page in pages:
    rel = os.path.relpath(page, SITE)
    raw = open(page, "rb").read()
    text = raw.decode("utf-8")
    r = {"bytes": len(raw)}

    parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
    parser.parse(raw)
    r["parse_errors"] = [f"L{pos[0]}: {code} {data or ''}" for pos, code, data in parser.errors]

    soup = BeautifulSoup(text, "html5lib")
    ids = Counter(t["id"] for t in soup.find_all(attrs={"id": True}))
    r["duplicate_ids"] = {k: v for k, v in ids.items() if v > 1}

    heads = [(h.name, h.get_text(" ", strip=True)[:60]) for h in soup.find_all(re.compile(r"^h[1-6]$"))]
    r["h1_count"] = sum(1 for h in heads if h[0] == "h1")
    r["empty_headings"] = [h for h in heads if not h[1]]
    skips, prev = [], 0
    for name, txt in heads:
        lvl = int(name[1])
        if prev and lvl > prev + 1:
            skips.append(f"h{prev} -> {name} ({txt})")
        prev = lvl
    r["heading_skips"] = skips

    imgs = soup.find_all("img")
    r["img_count"] = len(imgs)
    r["img_missing_alt"] = [i.get("src") for i in imgs if i.get("alt") is None]
    r["img_generic_alt"] = [f'{i.get("src")} (alt="{i.get("alt")}")' for i in imgs
                            if (i.get("alt") or "").strip().lower() in GENERIC_ALTS]
    r["img_no_dimensions"] = sum(1 for i in imgs if not (i.get("width") and i.get("height")))
    r["img_lazy"] = sum(1 for i in imgs if i.get("loading") == "lazy")

    empty_links = []
    for a in soup.find_all("a"):
        href = a.get("href")
        has_img_alt = any((im.get("alt") or "").strip() for im in a.find_all("img"))
        if href is not None and not a.get_text(" ", strip=True) and not has_img_alt and not a.get("aria-label"):
            empty_links.append(href)
        if not href or href.startswith(("mailto:", "#", "javascript:", "tel:")):
            continue
        u = urlparse(href)
        if u.scheme in ("http", "https") and u.netloc not in ("edouardfouche.com", "www.edouardfouche.com"):
            external_links[href].add(rel)
        elif resolve_internal(u.path if u.scheme else href, page) is None:
            internal_missing[href].add(rel)
    r["empty_links"] = empty_links

    res = [(t.name, a, t.get(a)) for t in soup.find_all(["script", "img", "iframe", "link", "source", "object"])
           for a in ("src", "href", "data") if t.get(a)]
    r["http_resources"] = [f"{n}[{a}]={v}" for n, a, v in res if v.startswith("http://")]
    r["third_party_hosts"] = sorted({urlparse(v).netloc for n, a, v in res
                                     if urlparse(v).netloc and urlparse(v).netloc != "edouardfouche.com"
                                     and not (n == "link" and a == "href")})
    for n, a, v in res:
        if n in ("img", "script", "iframe", "source", "object") and not v.startswith(("http", "data:", "//")):
            if resolve_internal(v, page) is None:
                internal_missing[v].add(rel)

    r["iframes_without_title"] = [i.get("src") for i in soup.find_all("iframe") if not i.get("title")]
    head = soup.head
    r["title"] = soup.title.get_text() if soup.title else None
    desc = head.find("meta", attrs={"name": "description"}) if head else None
    r["description_len"] = len(desc["content"]) if desc else 0
    canon = head.find("link", rel="canonical") if head else None
    r["canonical"] = canon["href"] if canon else None
    r["lang"] = soup.html.get("lang")
    comments = soup.find_all(string=lambda s: isinstance(s, Comment))
    r["comment_share"] = round(sum(len(c.encode("utf-8")) + 7 for c in comments) / len(raw), 3)
    report[rel] = r

json.dump({"pages": report,
           "external_links": {k: sorted(v) for k, v in sorted(external_links.items())},
           "internal_missing": {k: sorted(v) for k, v in sorted(internal_missing.items())}},
          open(OUT, "w"), indent=1, ensure_ascii=False)

P = report
print(f"pages: {len(P)}  external links: {len(external_links)}  missing internal targets: {len(internal_missing)}")
for k, v in internal_missing.items():
    print(f"  MISSING {k} <- {sorted(v)}")
other_errors = {p: [e for e in r["parse_errors"] if "named-entity" not in e] for p, r in P.items()}
print("parse errors (ignoring '&' in URLs):", {p: e for p, e in other_errors.items() if e} or "none")
print("duplicate IDs:", {p: r["duplicate_ids"] for p, r in P.items() if r["duplicate_ids"]} or "none")
print("pages without exactly one <h1>:", [(p, r["h1_count"]) for p, r in P.items() if r["h1_count"] != 1] or "none")
print("heading skips:", {p: r["heading_skips"] for p, r in P.items() if r["heading_skips"]} or "none")
print("missing/generic alt:", [x for r in P.values() for x in r["img_missing_alt"] + r["img_generic_alt"]] or "none")
print("empty links:", {p: r["empty_links"] for p, r in P.items() if r["empty_links"]} or "none")
print("http:// resources:", {p: r["http_resources"] for p, r in P.items() if r["http_resources"]} or "none")
print("third-party hosts:", sorted({h for r in P.values() for h in r["third_party_hosts"]}))
print("max share of HTML comments:", max((r["comment_share"], p) for p, r in P.items()))
