"""Add width/height to the kramdown attribute list of every raster image in _posts/ that lacks them.

Usage: python3 tools/add_image_sizes.py <repo> [--dry-run]
Turns ![alt](/img/x.jpg){:class="img-responsive"} into
      ![alt](/img/x.jpg){:class="img-responsive" width="1440" height="960"}
(SVGs are skipped). Run it after adding images to a post; see CLAUDE.md, "Blog posts".
"""
import os
import re
import sys

from PIL import Image

REPO = sys.argv[1]
DRY = "--dry-run" in sys.argv
RASTER = (".jpg", ".jpeg", ".png", ".gif", ".webp")
IMG = re.compile(r'(!\[[^\]]*\]\((/img/[^)\s]+)(?:\s+"[^"]*")?\))(\{:[^}]*\})?')

total = 0
for name in sorted(os.listdir(os.path.join(REPO, "_posts"))):
    path = os.path.join(REPO, "_posts", name)
    text = open(path, encoding="utf-8").read()
    changes = []

    def fix(m):
        image, src, ial = m.group(1), m.group(2), m.group(3)
        if not src.lower().endswith(RASTER) or (ial and re.search(r"\bwidth\s*=", ial)):
            return m.group(0)
        with Image.open(os.path.join(REPO, src.lstrip("/"))) as im:
            w, h = im.size
        attrs = f'width="{w}" height="{h}"'
        changes.append(f"{src} -> {w}x{h}")
        return image + (("{:" + ial[2:-1].rstrip() + " " + attrs + "}") if ial else ("{:" + attrs + "}"))

    new = IMG.sub(fix, text)
    if changes:
        total += len(changes)
        print(f"{name}: " + ", ".join(changes))
        if not DRY:
            open(path, "w", encoding="utf-8").write(new)
print(f"{total} image(s) updated" + (" (dry run)" if DRY else ""))
