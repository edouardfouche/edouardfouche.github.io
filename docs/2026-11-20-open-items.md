# Open items

**Date:** 2026-11-20
Observations from the [site audit](2026-11-20-site-audit.md) that were **not** acted on, ordered by
usefulness. None of them is urgent. When you resolve one, record it in a new dated file and link it
here.

## 1. Large images slow down post pages

The header images of recent posts are full-size PNGs: `img/posts/2026-04-21-taste.png` (4.4 MB),
`2026-03-26-autopilot.png` (3.1 MB), `2026-04-09-claude-code-leak.png` (2.6 MB) and
`2026-04-14-identity-crisis.png` (2.1 MB). They are displayed at most 600 px wide. Each post page
downloads several megabytes for one image.

**Suggestion:** export these images as JPEG or WebP at about 1200 px wide (2× the display width for
high-density screens), usually 100–300 KB each, and keep the same filenames (or update the post's
image path). This changes the files, not the design. The 10 MB print-quality press photo in
`img/press-package-edouard-fouche/` is intended as a download, so leave it.

## 2. RSS feed is announced twice, with the wrong type

**Resolved** on 2026-11-20 in `cf8246a`: see the [SEO record](2026-11-20-seo.md).

The built `<head>` contains two `<link rel="alternate">` tags for the same `/feed.xml`: one from
jekyll-feed's `{% feed_meta %}` and one written by hand in `_includes/head.html`. Both declare
`type="application/atom+xml"`, but `feed.xml` is a hand-written **RSS 2.0** feed, which should be
`application/rss+xml`. jekyll-feed's own Atom feed is not generated, because the hand-written
`feed.xml` takes its place.

**Suggestion:** keep a single tag,
`<link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Edouard Fouché">`, and
remove `{% feed_meta %}` (or drop the hand-written feed and let jekyll-feed generate Atom). Feed
readers would then detect the format correctly.

## 3. Bootstrap CSS is still 3.1.1

The JavaScript was upgraded, but `css/bootstrap.css` and `css/bootstrap-theme.css` are still 3.1.1.
That is intentional: the CSS has no known vulnerabilities, and an upgrade could shift the design.
Upgrade only together with a visual review, using the screenshot comparison described in
[the maintenance changes record](2026-11-20-maintenance-changes.md).

## 4. MathJax 2 is end of life

MathJax 2.7.9 is the final 2.x release. MathJax 3 or 4 is faster but needs a different configuration
and renders slightly differently. Only two posts use math, so there is no pressure. If you migrate,
verify those two posts visually.

## 5. Dead code and leftovers

- Large commented-out blocks in `_layouts/cv.html` (galleriffic gallery, dropdowns, sidebar
  scrollspy) and the unused `js_gallery/`, `js_timeliner/` and `css_gallery/` assets. The galleriffic
  stylesheet is still loaded on every page from `head.html`. Removing all of this is safe only after
  a visual check.
- `_sass/` and `theme: minima` are not used by the custom layouts.
- `.vscode/settings.json` contains Python and pylint settings that do not apply to this repository.
- Five files in `_drafts/` have no `.markdown` extension. With `jekyll serve --drafts`, four of them
  are skipped entirely. The fifth, `2016-11-24-Automatic-backup-with-SSH-on-Ubuntu-16.04`, is read as
  having the extension `.04`: it renders at `/Automatic-backup-with-SSH-on-Ubuntu-16/` without
  Markdown conversion. Add `.markdown` to these files when you resume work on them. Drafts are never
  published, so the live site is unaffected.

## 6. Dependabot and the `github-pages` gem

Now that `Gemfile.lock` is committed, GitHub's Dependabot can open pull requests for gem updates. Do
not merge a bump of `github-pages` (or of the gems it pins) unless https://pages.github.com/versions/
lists that version. Otherwise local builds stop matching production. See
[the toolchain setup record](2026-11-20-toolchain-setup.md#upgrading).
