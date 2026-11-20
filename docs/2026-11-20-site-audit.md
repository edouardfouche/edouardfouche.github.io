# Site audit

**Date:** 2026-11-20
**Scope:** the whole repository and the live site at https://edouardfouche.com, as of commit `97ff75d`
(before any of the changes in [the maintenance changes record](2026-11-20-maintenance-changes.md)).

## How the site is built and served

- **Generator:** Jekyll. There is no CI, no test suite and no linter.
- **Deployment:** GitHub Pages builds the site from the root of `master` (legacy build, not a GitHub
  Actions workflow). Pushing to `master` deploys it. A build takes about one minute.
- **Pages build environment:** GitHub uses its own pinned gem set and ignores the repo's `Gemfile`. On
  the audit date that set was `github-pages` 232: Ruby 3.3.4, Jekyll 3.10.0, kramdown 2.4.0 (GFM
  input), Liquid 4.0.4, minima 2.5.1, jekyll-feed 0.17.0. The source is https://pages.github.com/versions/.
- **Edge:** the domain is served through Cloudflare (`server: cloudflare`). Cloudflare redirects
  `http://` to `https://` with a 301, rewrites `http://` URLs in the HTML to `https://` (Automatic
  HTTPS Rewrites), and obfuscates email addresses. The served HTML can therefore differ slightly from
  the build output. GitHub's own "Enforce HTTPS" setting is off, and Cloudflare does that job instead.
- **Comments:** giscus, mapped by page pathname to GitHub Discussions ("Announcements" category).
- **Analytics:** Simple Analytics. Google Analytics and Disqus had been removed earlier over GDPR
  concerns (see the README history).

## How the code is organised

- **The top-level pages are stubs.** `about.md`, `cv.md`, `publications.md`, `services.md`,
  `book-me.md`, `citation-policy.md`, `impressum.md` and `404.md` contain only front matter and a
  placeholder body that is never rendered. The content of each page is hand-written HTML in
  `_layouts/<name>.html`.
- **The layouts are standalone documents.** Every layout except `post.html` (which extends
  `default.html`) is a complete HTML page that includes `_includes/head.html`, `navbar.html`,
  `footer.html` and `script.html`. Shared page chrome therefore lives in `_includes/`.
- **Styling:** Bootstrap 3.1.1 CSS plus `css/customstyle.css` and `css/style.css`. `theme: minima` and
  `_sass/` exist but are not used by the custom layouts.
- **Posts:** `_posts/YYYY-MM-DD-Title.markdown`. Because `permalink: /:title/` is set, the URL comes
  from the filename slug and contains no date. Renaming a file therefore changes the post's URL and
  detaches its giscus thread. The excerpt ends at `<!--more-->`.
- **Publications:** a hand-maintained HTML list in `_layouts/publications.html`, with PDFs, slides and
  posters in `publications/`.
- **JavaScript:** the only active code that needs jQuery is Bootstrap's collapse plugin, which runs the
  mobile navbar toggle. The gallery (galleriffic), dropdown and scrollspy scripts in `_layouts/cv.html`
  are all commented out. MathJax is loaded on every page; two posts use it (concept drift, knight's
  tour).

## Problems found

| # | Area | Problem | Impact |
| --- | --- | --- | --- |
| 1 | Toolchain | `Gemfile` pinned Jekyll 4.2, but production builds with Jekyll 3.10 (`github-pages` gem). | Local builds could differ from the live site; Jekyll-4-only features would work locally and break in production. |
| 2 | Toolchain | No Ruby toolchain on the machine (only the macOS system Ruby 2.6); `Gemfile.lock` was gitignored. | The site could not be built locally, and installs were not reproducible. |
| 3 | Config | `_config.yml` had two `exclude:` keys. YAML keeps only the last one. | The first list was silently ignored. |
| 4 | Dates | Post dates such as `2026-04-21 00:00:00 +0100` are 23:00 UTC the day before. Pages builds in UTC and no `timezone` was set. | 7 posts showed a date one day earlier than their front matter and filename. A build on a machine in Germany showed different dates from production. |
| 5 | SEO | `<link rel="canonical" href="{{ .Permalink }}"/>` is Hugo syntax, which Liquid renders as an empty string. | Every page had `href=""`. |
| 6 | JS | Bootstrap JS was loaded from `netdna.bootstrapcdn.com` **before** jQuery, then again locally after it. | Every page threw `Bootstrap's JavaScript requires jQuery`. It did no harm because the second copy worked. |
| 7 | Security | jQuery 1.11.0 (2014) and Bootstrap JS 3.1.1. | Known XSS issues: jQuery CVE-2015-9251, CVE-2019-11358, CVE-2020-11022, CVE-2020-11023; Bootstrap CVE-2018-14040, CVE-2018-14041, CVE-2018-14042, CVE-2019-8331. |
| 8 | Security | MathJax 2.7.0. | CVE-2018-1999024 (XSS via `\unicode`, fixed in 2.7.4). The real risk was low, because only the site owner writes the TeX. MathJax 2.7.0 also drew math variables upright instead of italic. |
| 9 | Markup | Two `viewport` meta tags (`width=500` and `width=device-width`). | Browsers apply the last one, so the first was dead code. |
| 10 | Resources | The Google Fonts stylesheet (Playfair Display SC) was requested over `http://`. | It would be blocked as mixed content on https; it only worked thanks to Cloudflare's rewrite. |
| 11 | Resources | Playfair Display SC is not used by any stylesheet. | An extra third-party request on every page for nothing. |

All of these were fixed on 2026-11-20. See [the maintenance changes record](2026-11-20-maintenance-changes.md).
Observations that were not acted on are listed in [Open items](2026-11-20-open-items.md).

## How the audit compared local and live output

A local build was compared byte for byte with the live HTML of all 27 pages (10 pages plus 17 posts).
Once the toolchain matched production, the only differences were Cloudflare's edge rewrites (problem 10
and the email obfuscation) and the timezone issue (problem 4). That confirmed the local build
reproduces production.
