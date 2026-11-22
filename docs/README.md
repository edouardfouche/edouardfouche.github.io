# docs/

Maintenance records for this website: what was found, what was changed and why, and how to reproduce
or verify it. The folder is excluded from the published site (`exclude` in [`_config.yml`](../_config.yml)),
so nothing here ends up on edouardfouche.com.

## Conventions

- **One topic per file**, named `YYYY-MM-DD-<topic>.md`: the date the work was done, then a short
  kebab-case topic, e.g. `2026-11-20-site-audit.md`. Sorting by name gives the chronology.
- **Markdown only**, with no Jekyll front matter (these files are never rendered by Jekyll).
- **Records, not living specs:** a dated record describes the state at that date. When something
  changes later, add a new dated file and link back to the old one rather than rewriting history.
  Fixing typos or broken links is fine.
- **Link to the source** (relative links to repo files, commit hashes) so claims can be checked.
- **No private data:** the repository is public. Leave out email addresses, tokens, local machine
  paths and anything else that should not be published.
- The current how-to for working in the repo lives in [`../CLAUDE.md`](../CLAUDE.md) and
  [`../README.md`](../README.md). These records explain how it got that way.

## Index

| Date | Document | Summary |
| --- | --- | --- |
| 2026-11-20 | [Site audit](2026-11-20-site-audit.md) | How the site is built and served, and the problems found in it |
| 2026-11-20 | [Toolchain setup](2026-11-20-toolchain-setup.md) | Ruby/Jekyll environment matching GitHub Pages: install, run, upgrade |
| 2026-11-20 | [Maintenance changes](2026-11-20-maintenance-changes.md) | Every change made, why, and how it was verified before and after deploy |
| 2026-11-20 | [Open items](2026-11-20-open-items.md) | Observations not acted on yet, with suggested fixes |
| 2026-11-20 | [SEO](2026-11-20-seo.md) | Search and link-preview metadata: findings, jekyll-seo-tag and sitemap, verification, what is left |
| 2026-11-20 | [Draft file extensions](2026-11-20-draft-extensions.md) | Five drafts that Jekyll skipped or rendered unconverted, renamed to `.markdown` |
| 2026-11-20 | [SEO follow-up](2026-11-20-seo-follow-up.md) | Duplicate poster removed; how to submit the sitemap (Google, Bing) and fix the redirect chains in Cloudflare |
| 2026-11-21 | [About page biography](2026-11-21-about-bio.md) | New bio (AI-driven business transformation, Siemens Healthineers) and matching meta descriptions |
| 2026-11-21 | [Knowledge work post](2026-11-21-knowledge-work-post.md) | LinkedIn post of 2026-11-19 added as a blog post, with its own share image, description and alt text |
| 2026-11-21 | [Publications vs. Google Scholar](2026-11-21-publications-scholar-sync.md) | Missing PESS'26 paper added, entry errors fixed, unclosed year headings fixed (pixel-identical), all links checked; open items for the page and the Scholar profile |
| 2026-11-21 | [Blog margins](2026-11-21-blog-margins.md) | Index and posts share one centered 720px reading column with equal margins; left-aligned text and wrapping inline code on phones |
| 2026-11-21 | [Full site audit](2026-11-21-full-audit.md) | Second, broader audit (legal texts, privacy, dead links, performance, accessibility with axe-core, search, security headers, code health), with a prioritized list of what to fix and the status of earlier open items |
| 2026-11-21 | [Quick wins](2026-11-21-quick-wins.md) | First fixes from the audit: GPS data stripped from a photo, 10 dead links replaced, CV and Book Me pages repaired, MathJax only on the two posts with math; verified with before/after screenshots |
| 2026-11-21 | [Performance, accessibility and cleanup](2026-11-21-performance-accessibility-cleanup.md) | Images 26.5 MB → 7.0 MB with dimensions and lazy loading, `style.css` as plain CSS, unused files removed, jQuery and the license badge self-hosted, feed URLs absolute, link underlines and contrast, Google Scholar linked |
| 2026-11-21 | [Impressum and privacy policy](2026-11-21-impressum-privacy.md) | Impressum on current law (DDG, MStV), privacy policy covering every data flow, one license statement, Google Form linked instead of embedded; what the owner should check |
| 2026-11-21 | [Alt texts, dead CSS and the Cambria fallback](2026-11-21-dead-css-alt-texts-font.md) | 56 alt texts written from the images and their context; about 50 dead CSS rules removed (pixel-identical); self-hosted Caladea as metric-compatible fallback for Cambria |
| 2026-11-22 | [Semantic HTML and polish](2026-11-22-semantic-html-and-polish.md) | Overnight: landmarks, one h1 per page, no duplicate IDs, share images, PDF titles, copy fixes; axe-core finds no violation on any page; home page proposal on a branch; what is left for the owner |
| 2026-11-22 | [Handover](2026-11-22-handover.md) | **Start here on a new machine:** where things stand, branches, setup, the new `tools/` folder, open items for the owner and technical ones |
