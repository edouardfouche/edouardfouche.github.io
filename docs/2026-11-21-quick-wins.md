# Quick wins from the full audit

**Date:** 2026-11-21
**Follows:** the [full site audit](2026-11-21-full-audit.md), items L4, B1, B2, B3, A5, C3 (CV page only) and P2.
**Branch:** `site-audit-quick-wins`, not yet merged into `master`, so nothing is live yet (see
[Deploying](#deploying)).

## Changes, one commit each

| Commit | Change | Audit item | Visible on the site? |
| --- | --- | --- | --- |
| `bd01874` | Strip the GPS position and other metadata from `img/knight/study.jpg` | L4 | No (pixel-identical) |
| `4375b99` | Replace the 10 dead external links | B1 | Only two short texts (see below) |
| `b46dfb3` | CV: text for the PDF fallback link, `type` and `title` on the `<object>`; `title` on the PDF embed of the workout post | B2, A5 | Only where browsers cannot show the PDF |
| `7b440a3` | CV: remove the commented-out code and two stray `</div>` | B2, C3 | No |
| `5a7a978` | Book Me: restore the heading and intro, add a direct link to the form, `title` on the iframe | B3 | **Yes** |
| `5cc3cfe` | Load MathJax only on pages with `math: true`; [`CLAUDE.md`](../CLAUDE.md) explains the key | P2 | No |

### GPS metadata (`bd01874`)

The photo carried EXIF (with latitude and longitude), XMP and Photoshop/IPTC blocks. These segments
were cut from the JPEG without re-encoding it. The ICC profile and the Adobe marker, which affect
colours, were kept. The decoded pixels are identical to before. The EXIF orientation was 1, so the
photo does not rotate. File size: 183 KB → 154 KB.

### Dead links (`4375b99`)

| Page | Before | After |
| --- | --- | --- |
| Impressum | GitHub "Global Privacy Practices" (404) | GitHub General Privacy Statement. The sentence now names that document, and the GitHub Pages link points to the current page instead of a redirect |
| Citation Policy | Cambridge "Citing blogs" PDF (removed) | Its Wayback Machine copy of 2024-08-08, marked "(archived copy)" |
| Fun with Tensorflow im2txt | `tensorflow/models/tree/master/im2txt` (2 links, 404) | The same code on the `archive` branch |
| Fun with Tensorflow im2txt | `mscoco.org` (2 links, no response) | `cocodataset.org` and `cocodataset.org/#explore` |
| Fun with Tensorflow im2txt | Google Drive checkpoint (404) | Link removed. The post now says that the file is no longer available |
| Observations about my transition from Academia to Industry | "Goodbye, Academia!" and "Goodbye academia, I get a life." (no response) | Wayback Machine copies (2026-03-12 and 2025-06-26) |
| Neural-based Outlier Discovery | KIT HiCS page (redirected to an unrelated page) | Its Wayback Machine copy of 2022-01-21 |

**Correction to the audit:** B1 suggested the HiCS paper's DOI for the last link. The link text is
"data sets", though. It pointed to the page where the HiCS synthetic data could be downloaded, so the
archived copy of that page, which still offers "all 21 synthetic datasets", replaces it more
faithfully.

### CV page (`b46dfb3`, `7b440a3`)

- The fallback link reads "Download the CV as a PDF" instead of being empty. The `<object>` has
  `type="application/pdf"`, so browsers without a PDF viewer can skip the 900 KB download. Its `title`
  is the accessible name.
- About 1,440 commented-out lines (old HTML CV, gallery, dropdown and sidebar scripts) are gone. Two
  `</div>` that closed nothing went with them. The layout shrinks from 1,514 to 44 lines, and the built
  page from 60 KB to 11 KB. The old code remains in git history, e.g. `b46dfb3:_layouts/cv.html`.
- The audit's B2 suggestion to add a download link above the embed was dropped before the audit was
  committed. The page already has one ("you can download it here").

### Book Me (`5a7a978`)

The heading "Book Me — Tengu Consulting" and two paragraphs of the owner's intro were commented out
as "redundant with the form", and they are visible again. The first paragraph ("Welcome to the intake
form…") stays out, because the heading says the same. A new sentence links the form directly, in a new
tab, and offers LinkedIn as an alternative, so the page is usable when the embedded form does not load.
The iframe has a `title`, and the template's "INSTRUCTIONS: Replace YOUR_GOOGLE_FORM_ID" comment is gone.

The wording of the new sentence is a suggestion. Adjust it freely in
[`_layouts/book-me.html`](../_layouts/book-me.html).

### MathJax (`5cc3cfe`)

[`_includes/head.html`](../_includes/head.html) wraps the MathJax script in `{% if page.math %}`, and
the two posts with LaTeX set `math: true`. A scan of all built pages (text outside `script`, `style`,
`pre` and `code`, for `\(`, `\[`, `$$` and `\begin{`) found math only in these two posts, not in any
excerpt on the home page, and not in any draft. A future post with LaTeX needs `math: true`, which
[`CLAUDE.md`](../CLAUDE.md) now says.

## Verification

- **Build:** `bundle exec jekyll build` succeeds without warnings. Compared with the build of `master`,
  29 files differ: all 27 pages (the MathJax script, or on the two math posts its HTML comment, left
  every `<head>`, plus the content changes above), `img/knight/study.jpg`, and `feed.xml` (build time,
  and the new links of the Academia post). `sitemap.xml` is unchanged.
- **Links:** all 10 replacement URLs return 200. The archived pages were opened and contain the expected
  content (titles "HiCS experimental details", "Goodbye academia, I get a life.", the "Goodbye,
  Academia!" blog, and the Cambridge PDF as `application/pdf`). The `#install-required-packages` anchor
  exists in the archived im2txt README.
- **Rendering:** the same WebKit screenshot procedure as in the audit (all 27 pages at 1280 px and
  375 px, analytics, giscus and Google Forms blocked), before (`master`) and after:
  - 46 of 54 screenshots are pixel-identical. Among them: the CV page, the Knight's Tour post with the
    stripped photo, and every page that no longer loads MathJax.
  - The 8 that differ are the four pages whose text changed on purpose: Book Me (new heading and
    text), Impressum (longer GitHub sentence), Citation Policy ("(archived copy)") and the im2txt post
    (checkpoint sentence). Book Me was inspected visually at both widths and matches the other pages'
    title style.
  - MathJax runs on the two math posts only, and typesets all 15 and 6 formulas with no errors.
  - No page is wider than the window at 375 px.
- **CV page:** with HTML comments ignored, the DOM before and after differs only in the new `<object>`
  attributes and the fallback text.
- **Accessibility:** axe-core 4.14.1 no longer reports `object-alt` (CV, workout post), `frame-title`
  (Book Me) or `link-name` (CV). The remaining findings on these pages are the site-wide ones from the
  audit (A1, A3, A6).

## Deploying

The commits are on the branch `site-audit-quick-wins`, together with the audit itself (`694f884`). To
publish them, fast-forward `master` and push. GitHub Pages builds in about a minute.

After the deploy:

- **Purge the photo from Cloudflare's cache.** Cloudflare caches images for up to 4 hours, so the edge
  can keep serving the old `img/knight/study.jpg` with its GPS data until the copy expires. Caching →
  Configuration → Purge Cache → Custom Purge: `https://edouardfouche.com/img/knight/study.jpg`. The old
  version also stays in the public git history, as noted in the audit.
- Check that `/book-me/` shows the new heading, that `/cv/` is about 11 KB, and that only the two math
  posts load `MathJax.js`.

## Still open from the audit's list

The legal texts (L1–L3, L6), the Cloudflare settings (S2, T1, T2), lighter images (P1), link underlines
and contrast (A1, A2), the home page introduction (S1), the Google Scholar link (S5), `css/style.css`
(C1), and the remaining junk and unused files (C3, C4). See the
[recommended order of work](2026-11-21-full-audit.md#recommended-order-of-work).
