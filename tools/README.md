# tools/

Checks used for the maintenance recorded in `docs/` (audit of 2026-11-21 and the follow-up work).
Repository-only: `tools/` is in the `exclude` list of `_config.yml`, so nothing here is published.
Run everything from the repository root. Keep outputs (builds, screenshots, reports) outside the
repository, e.g. in a temporary folder.

| Tool | What it does |
| --- | --- |
| `html_audit.py` | Static checks of a built site: parse errors, duplicate IDs, one `<h1>` per page, heading skips, missing or generic `alt`, empty links, `http://` resources, third-party hosts, missing internal targets. Writes a JSON report that also lists every external link. |
| `check_url.sh` | Status of one URL (HEAD, then ranged GET), for checking the external links in parallel. |
| `dead_css.py` | Rules of a stylesheet that match no element on any built page. |
| `render.swift` | macOS only. Renders pages in WebKit at 1280 and 375 px: full-page screenshots, phone-menu test, overflow, navbar height, fonts, MathJax formulas, and optionally axe-core. |
| `compare_shots.py` | Compares two `render.swift` runs pixel by pixel (the before/after check behind "pixel-identical" in `docs/`). |
| `optimize_image.py` | Prepares an image for a post: at most 1440 px wide, metadata (GPS) removed, ICC kept, JPEG quality chosen for PSNR ≥ 38 dB. |
| `add_image_sizes.py` | Adds `width`/`height` to the images in `_posts/` that lack them. |

## Setup

```sh
python3 -m venv ../site-tools-venv          # any folder outside the repository
../site-tools-venv/bin/pip install -r tools/requirements.txt
swiftc -O -swift-version 5 -o /tmp/render tools/render.swift   # macOS, for screenshots and axe
```

axe-core (for accessibility checks) is not stored in the repository. Download it and check its hash
against the one cdnjs publishes:

```sh
curl -sS -o /tmp/axe.min.js https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.14.1/axe.min.js
curl -sS 'https://api.cdnjs.com/libraries/axe-core/4.14.1?fields=sri'          # expected sha512
echo "sha512-$(openssl dgst -sha512 -binary /tmp/axe.min.js | openssl base64 -A)"  # must match
```

## Typical workflows

**Static audit of the current state**

```sh
eval "$(rbenv init - zsh)"      # if the shell has not loaded rbenv
bundle exec jekyll build -d /tmp/site
../site-tools-venv/bin/python tools/html_audit.py /tmp/site /tmp/audit.json
../site-tools-venv/bin/python tools/dead_css.py /tmp/site css/customstyle.css
```

**External links**

```sh
../site-tools-venv/bin/python -c "import json; print('\n'.join(json.load(open('/tmp/audit.json'))['external_links']))" > /tmp/links.txt
tr '\n' '\0' < /tmp/links.txt | xargs -0 -n1 -P12 sh tools/check_url.sh > /tmp/links.tsv
cut -f1 /tmp/links.tsv | sort | uniq -c        # 403/429/503/999 come from sites that block scripts
```

**Before/after screenshots of a change**

Build the site before the change (e.g. with `git stash` or a worktree) into `/tmp/site-before`, and
after it into `/tmp/site-after`. Serve each and render the same pages:

```sh
python3 -m http.server 4001 --bind 127.0.0.1 --directory /tmp/site-before &
python3 -m http.server 4002 --bind 127.0.0.1 --directory /tmp/site-after &
cd /tmp/site-after && PAGES=$( (find . -name index.html | sed -e 's|^\.||' -e 's|index.html$||'; echo /404.html) | sort ); cd -
/tmp/render http://127.0.0.1:4001 /tmp/shots-before $PAGES
/tmp/render http://127.0.0.1:4002 /tmp/shots-after $PAGES
../site-tools-venv/bin/python tools/compare_shots.py /tmp/shots-before /tmp/shots-after
```

(Paths with spaces or quotes, such as the Knight's Tour post, need quoting; passing the list through
`tr '\n' '\0' | xargs -0` is safest.) Add `AXE=/tmp/axe.min.js` before `/tmp/render` to run axe-core
on every page; the violations are in `results.json`. Today axe finds none on any page.

**Images for a new post**

```sh
../site-tools-venv/bin/python tools/optimize_image.py ~/Downloads/photo.png img/posts/2026-12-01-name.jpg
# reference it in the post with a real alt text, then:
../site-tools-venv/bin/python tools/add_image_sizes.py .
```
