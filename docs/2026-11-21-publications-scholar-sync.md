# Publications page compared with Google Scholar

**Date:** 2026-11-21

The publication list in [`_layouts/publications.html`](../_layouts/publications.html) was compared
with the Google Scholar profile (https://scholar.google.com/citations?user=UUTBItQAAAAJ), entry by
entry. The one missing paper was added, and a few errors in existing entries were fixed. The year
headings, which were never closed, were fixed without changing how the page looks. Every link on the
page was checked.

## Sources

| Source | What it gave | Notes |
| --- | --- | --- |
| Google Scholar profile, sorted by date, 100 per page | 29 items | Includes duplicates and preprints of published papers (see below) |
| OpenAlex works API, filtered on the author | 26 distinct works | Cross-check. Lists the same works as Scholar, nothing more |
| arXiv API | Full author lists, comments ("accepted at …"), journal references | Scholar drops one author of `2610.28200` (see below) |
| DBLP | Nothing | Every DBLP host answers scripts with a bot check (HTTP 202) |
| Conference pages (ICML 2026, the ICML forecasting workshop, IEEE PESS 2026 at KIT, the EGU 2017 programme) | Dates, places, session | |

Before this change the page had **24** entries, from 2018 to 2026.

## Comparison

Scholar items that were **missing** from the site:

1. **Aliullah, Julian Oelhaf, Edouard Fouché, Jessica Deuschel, Christian Bergler, Andreas Maier,
   Siming Bayer.** "Parameter-Efficient Adaptation of Time Series Foundation Models for Electrical Load
   Forecasting". arXiv `2610.28200`. The arXiv comment says it was accepted at the IEEE Power & Energy
   Student Summit (PESS 2026), Karlsruhe. The PESS agenda on the KIT website confirms it (21–23 October
   2026, Technical Session 6). Scholar lists the authors as "J Oelhaf, E Fouché, …" and leaves out the
   first author, Aliullah (a mononym). The site uses the arXiv author list. **Added.**
2. **Avipsa Roy, Edouard Fouché, Rafael Rodriguez Morales, Gregor Moehler.** "Ibmdbpy-spatial: An
   Open-source implementation of in-database geospatial analytics in Python". EGU General Assembly
   2017, Vienna. Geophysical Research Abstracts, Vol. 19, EGU2017-10205-2: a one-page conference
   abstract. **Not added**, by the author's decision: an abstract is not worth listing. It was briefly
   added during this work and then removed.

Scholar items that are **not** missing; they duplicate entries already on the page:

| Scholar item | Relation to the site |
| --- | --- |
| "Reducing Energy Time Series …", it–Information Technology 57, 1, **2015** | Duplicate of the 2019 paper (DOI `10.1515/itit-2019-0025`), with a wrong year and volume |
| "Maximum mean discrepancy on exponential windows …", arXiv `2205.12706`, 2022 | Preprint of the TMLR 2025 paper on the site. Scholar has no separate TMLR item |
| "Scalable Online Change Detection for High-dimensional Data Streams", arXiv `2205.12706v2`, 2023 | Version 2 of the same preprint, under its earlier title |
| "Finite-time analysis of globally nonstationary multi-armed bandits", arXiv `2107.11419`, 2021 | Preprint of the JMLR 2024 paper, already linked as "Previous pre-print (2021)" |

Every site entry has a matching Scholar item.

## Changes

### Entries

All in [`_layouts/publications.html`](../_layouts/publications.html):

| Entry | Change | Why |
| --- | --- | --- |
| *(new)* PESS'26 | Added at the top of 2026, title linked to arXiv | Missing. No code, slides or poster are public, so there is no "Supplementary Material" line (the it–IT 2019 entry already has none) |
| SERAF, ICML'26 workshop | "Jeju, Korea" → "Seoul, Korea" | ICML 2026 and its workshops took place at COEX, Seoul. The workshop was on 11 July 2026. Jeju is where KDD'26 was held |
| SARAF, KDD'26 | "32th" → "32nd" | Ordinal |
| Tandem, SSDBM'22 | "34st" → "34th" | Ordinal (SSDBM'18 is the 30th) |
| DEAL, PAKDD'24 | Title "… for regression under drift" → "… for Regression Under Drift" | Published title |
| BALM-TSF, CIKM'25 and MMDEW, TMLR'25 | Added the missing space before "Supplementary Material" | Rendered as "Korea.Supplementary" and "2025.Supplementary" |
| MMDEW, TMLR'25 | Comma → semicolon between links; added a "Preprint" link to arXiv `2205.12706` | Matches the other entries. The arXiv item is the one Scholar lists |
| Budgeted MAB, KDD'24 | Removed a leading space inside the Teaser link's `href` | Browsers tolerated it, but it was wrong |

### Year headings

Each year was written `<h2><b> 2026 </b><h2>`: the second `<h2>` should have been `</h2>`. The
browser therefore closed each heading at the next `<h2>` and opened a new, empty one, so all entries
of a year sat inside an `<h2>`. They inherited its font weight (500) and line height (1.7). The empty
headings also added spacing: their top margin (`1em`) replaced the year heading's 15px bottom margin,
and the last one added 5px below the list.

- The 9 closing tags are now `</h2>`.
- Three rules for `body.publications` in [`css/customstyle.css`](../css/customstyle.css) reproduce
  the previous look: `font-weight: 500; line-height: 1.7` on `.information-line`, `margin-bottom: 1em`
  on the year headings, and `padding-bottom: 25px` (20 + 5) on `.subcontent-wrapper`. They are scoped
  to the publications page because the CV layout also uses `.information-line`.
- [`CLAUDE.md`](../CLAUDE.md) now describes the corrected heading markup and points to these rules.

## Verification

- `bundle exec jekyll build` succeeds. The built `/publications/` page has 25 entries (24 + 1) and
  year headings from 2026 down to 2018.
- The current `HEAD` and the working tree were built side by side. Among the built files, only
  `publications/index.html` differs because of the entry changes. Other differences came from an
  unrelated new post in the working tree.
- **Heading fix, before and after:** screenshots of the publications and CV pages with headless
  Chromium (Playwright), at desktop (1280×900) and mobile (390×844) sizes, before and after the
  heading and CSS change. **4/4 are pixel-identical.** In the DOM after the fix, the 9 `<h2>`
  elements contain only the year, no entry sits inside an `<h2>` (25 before), and every entry
  has the same computed style as before (weight 500, line height 27.2px, justified). No page errors.
- The new PESS'26 entry renders like its neighbours at both sizes.
- Links: all unique `href` values on the page were requested. All local PDFs exist. All GitHub,
  arXiv, JMLR, KIT, Springer, YouTube and Dropbox links return 200. `dl.acm.org`, the OpenReview PDF
  link and the Towards Data Science article answer scripts with 403 (bot protection), so they could not
  be checked this way. The three `dl.acm.org/authorize` links are inside HTML comments and are not rendered.

## Not changed (open items)

1. **Scholar profile clean-up** (only the profile owner can do this): merge the 2015 "Reducing Energy
   Time Series" item into the 2019 one. Merge both arXiv `2205.12706` items with each other and, if
   Scholar ever indexes it, with the TMLR version. Merge the 2021 arXiv item with the JMLR 2024 paper.
   Add Aliullah as first author of the PESS'26 item.
2. **Unlinked file:** `publications/Bernstein_Change_Detector_DMKD2024_AV.pdf` is the author's
   accepted manuscript of the ABCD paper (DMKD 2024). It states that it is not the version of record.
   It was added in `73ce658` (2024-02-05) together with `s10618-023-00999-5.pdf`, the Springer version
   of record, which is open access ("© The Author(s) 2024"). Only the version of record has ever been
   linked, as the ABCD entry's title link. The accepted manuscript adds nothing a reader needs. It is
   still served (HTTP 200) and listed in `sitemap.xml`. **Decision: leave it as is**, unlinked and
   in place. The author chose not to delete it.
3. **Missing supplementary material**, which only the authors can provide: talk slides for PESS'26,
   code for SERAF (`github.com/ShiqiaoZhou` has a SARAF repository but no SERAF one), and slides or
   posters for the PAKDD'25, DSAA'24, DS'23, e-Energy'21, ARIC'19 and SSDBM'18 papers.
