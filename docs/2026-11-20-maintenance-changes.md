# Maintenance changes

**Date:** 2026-11-20
**Deployed:** `master` moved from `97ff75d` to `68b144c`, and the GitHub Pages build succeeded (49 s).
**Ground rule:** do not change the design, navigation, links or resources unless a change fixes a
problem found in the [site audit](2026-11-20-site-audit.md). Every change below was checked against
that rule.

## Changes, one commit each

| Commit | Change | Fixes audit # | Visible on the site? |
| --- | --- | --- | --- |
| `480270c` | Pin the local build toolchain to the GitHub Pages versions (`github-pages` gem, `.ruby-version`, committed `Gemfile.lock`, README setup section) | 1, 2 | No |
| `16d88f9` | Merge the duplicate `exclude` keys in `_config.yml` and exclude `CLAUDE.md` and `vendor/` | 3 | No |
| `8775c55` | Set `timezone: Europe/Berlin` | 4 | **Yes:** 7 post dates move one day forward to their intended date |
| `9d8598c` | Canonical link: `{{ page.url \| absolute_url }}` instead of the Hugo syntax | 5 | No (head only) |
| `c08ba2d` | Remove the unused `width=500` viewport tag | 9 | No |
| `56c4f9d` | Load the Google Fonts stylesheet over https | 10 | No |
| `de49fac` | Remove the CDN Bootstrap script that loaded before jQuery | 6 | No (console error gone) |
| `fcd83fe` | jQuery 1.11.0 → 3.7.1; Bootstrap JS 3.1.1 → 3.4.1 (Bootstrap CSS unchanged) | 7 | No |
| `9fef72e` | Add `CLAUDE.md` (guidance for AI-assisted maintenance) | n/a | No (excluded from the site) |
| `e424092` | Remove the unused Playfair Display SC font | 11 | No |
| `68b144c` | MathJax 2.7.0 → 2.7.9 | 8 | **Yes:** math variables in 2 posts now render in italic |

Follow-up on the same day: `docs/` was created (this folder) and excluded from the site.

### Post dates that changed

| Post | Before (live) | After |
| --- | --- | --- |
| What remains once AI overtakes most of the execution? Taste. | April 20, 2026 | April 21, 2026 |
| The Identity Crisis of Software Engineers | April 13, 2026 | April 14, 2026 |
| Anthropic's Claude Code Leak | April 7, 2026 | April 8, 2026 |
| Why using AI requires us to be even better | March 25, 2026 | March 26, 2026 |
| On becoming a German citizen (as a French native) | November 28, 2024 | November 29, 2024 |
| Observations about my transition from Academia to Industry | December 5, 2023 | December 6, 2023 |
| Almost 30: I am, I have, I can, I want | July 20, 2022 | July 21, 2022 |

URLs are unaffected (permalinks contain no date), and so are the giscus threads (mapped by pathname).
The RSS `pubDate` of these posts changes accordingly.

### Front-end libraries after the change

| Library | Before | After | Source and integrity |
| --- | --- | --- | --- |
| jQuery | 1.11.0 | 3.7.1 | Google CDN, `integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo="`. The file was verified to be byte-identical to the code.jquery.com release. |
| Bootstrap JS | 3.1.1 (local and CDN) | 3.4.1 (local `js/` only) | Taken from the npm tarball (registry integrity verified). `bootstrap.min.js` matches Bootstrap's published SRI `sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd`. |
| Bootstrap CSS | 3.1.1 | 3.1.1 | Unchanged on purpose: upgrading it could change the design. |
| MathJax | 2.7.0 | 2.7.9 | cdnjs, `integrity="sha512-M36RUChW…34NTsg=="` (cdnjs's published hash, verified against the file). |
| Playfair Display SC | loaded | removed | It was not used by any CSS. |

Bootstrap JS 3.4.1 is the last 3.x release and supports jQuery 1.9.1 through 3.x. If you change a CDN
version, update its `integrity` attribute too, or the browser refuses to run the script.

## How the changes were verified

### 1. Local build reproduces production

After the toolchain change, the local build was compared byte for byte with the live HTML of all 27
pages. The only remaining differences were Cloudflare's edge rewrites and the timezone issue (fixed in
`8775c55`). Builds made with `TZ=UTC` and in local time are identical except for the feed's build
timestamp.

### 2. Visual regression test (before and after each change)

The site has no test suite, so a throwaway check was run with Playwright and headless Chromium,
installed in an isolated Python virtualenv outside the repository:

- Build the site before and after the change, and serve both folders locally.
- Load every page (10 pages plus 17 posts) at **desktop** (1280×900) and **mobile** (390×844,
  touch) sizes. Wait for the network to go idle and for MathJax's queue to finish. Block the
  third-party widgets (giscus, analytics) so screenshots are deterministic.
- Take full-page screenshots and compare them pixel by pixel with Pillow.
- Record JavaScript console errors and page errors, the jQuery, Bootstrap and MathJax versions, the
  layout viewport width, the canonical URL and the number of typeset formulas.
- On mobile, tap `.navbar-toggle` and check that the menu opens and closes again. Also compare
  screenshots taken with the menu open.

Results:

| Change set | Screenshots (54 = 27 pages × 2 sizes) | Errors | Mobile menu |
| --- | --- | --- | --- |
| Canonical, viewport, font https, script order, jQuery/Bootstrap upgrade | 54/54 pixel-identical, and the open-menu screenshots are identical too | Before: `Bootstrap's JavaScript requires jQuery` on every page. After: none. | Works |
| Remove Playfair Display SC | 54/54 pixel-identical | None | Works |
| MathJax 2.7.9 | 50/54 identical. The 4 that differ are the 2 math posts at both sizes. | None | Works |

The MathJax differences were inspected visually. In 2.7.0, variables such as *m*, *n*, *t*₁ and *S*ₖ
were drawn upright, a rendering bug of that version (both versions used the same STIX font, and no
font request failed). In 2.7.9 they render in italic as TeX intends, matching the italic variables in
the surrounding prose. All 21 formulas (15 + 6) still typeset.

### 3. Production check after deploy

After the Pages build of `68b144c`:

- The live HTML serves jQuery 3.7.1, MathJax 2.7.9 and Bootstrap JS 3.4.1. It has one viewport tag,
  no Playfair font and no bootstrapcdn script.
- Canonical URLs are correct (e.g. `https://edouardfouche.com/cv/`, including posts whose titles
  contain `&`, `'` and parentheses).
- The blog index shows the corrected dates.
- `/CLAUDE.md`, `/Gemfile.lock`, `/.ruby-version` and `/README.md` return 404, so they are not
  published.
- Headless Chromium on the live site shows no console errors: the integrity hashes are accepted,
  formulas typeset and the mobile menu opens.

## Housekeeping

- The work was done on a branch (`maintenance/toolchain-and-head-fixes`), fast-forwarded into
  `master`, then deleted.
- A global git identity was configured on the maintenance machine, which previously had none.
