"""Compare two screenshot folders made by tools/render.swift (same pages, same widths).

Usage: python3 tools/compare_shots.py <before dir> <after dir>
Reports per page and width: SAME, SIZE (page height changed) or DIFF (bounding box of changed pixels,
share of changed pixels, maximum difference). Also compares the menu-open screenshots (*-375-menu.png)
and MathJax formula counts. Animated images can differ between runs (another frame).
"""
import glob
import json
import os
import sys

from PIL import Image, ImageChops

before, after = sys.argv[1], sys.argv[2]
B = {(r["path"], r["width"]): r for r in json.load(open(os.path.join(before, "results.json")))}
A = {(r["path"], r["width"]): r for r in json.load(open(os.path.join(after, "results.json")))}
same = 0
for key in sorted(B):
    if key not in A:
        print(f"MISSING in after: {key}")
        continue
    fb, fa = json.loads(B[key]["facts"]), json.loads(A[key]["facts"])
    extra = []
    if fb["formulas"] != fa["formulas"]:
        extra.append(f"formulas {fb['formulas']}->{fa['formulas']}")
    if fa["overflow"]:
        extra.append("OVERFLOW " + ", ".join(fa["wide"][:3]))
    ib = Image.open(os.path.join(before, os.path.basename(B[key]["shot"]))).convert("RGB")
    ia = Image.open(os.path.join(after, os.path.basename(A[key]["shot"]))).convert("RGB")
    if ib.size != ia.size:
        print(f"SIZE  {key[0][:58]:58s} @{key[1]:<4} {ib.size} -> {ia.size} {' '.join(extra)}")
        continue
    diff = ImageChops.difference(ib, ia)
    bbox = diff.getbbox()
    if bbox is None:
        same += 1
        if extra:
            print(f"SAME* {key[0][:58]:58s} @{key[1]:<4} {' '.join(extra)}")
        continue
    hist = diff.convert("L").histogram()
    total = ib.size[0] * ib.size[1]
    print(f"DIFF  {key[0][:58]:58s} @{key[1]:<4} bbox={bbox} changed={sum(hist[1:])/total:.3%} "
          f"max={max(i for i, v in enumerate(hist) if v)} {' '.join(extra)}")
print(f"pixel-identical: {same} of {len(B)}")

menu_same = menu_total = 0
for f in sorted(glob.glob(os.path.join(before, "*-menu.png"))):
    g = os.path.join(after, os.path.basename(f))
    if not os.path.exists(g):
        continue
    menu_total += 1
    a, b = Image.open(f).convert("RGB"), Image.open(g).convert("RGB")
    if a.size == b.size and ImageChops.difference(a, b).getbbox() is None:
        menu_same += 1
    else:
        print(f"MENU DIFF {os.path.basename(f)}")
if menu_total:
    print(f"menu-open screenshots identical: {menu_same} of {menu_total}")
