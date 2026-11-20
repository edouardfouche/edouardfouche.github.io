# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal website and blog of Edouard Fouché, served at https://edouardfouche.com (see `CNAME`). It is a
Jekyll static site with no tests, linter, or CI.

## Build and deploy

- Toolchain: rbenv (Homebrew) with the Ruby version pinned in `.ruby-version`, matching the Ruby that
  GitHub Pages uses.
- Setup: `bundle install`. Preview: `bundle exec jekyll serve`, then open http://localhost:4000 (add
  `--drafts` to render `_drafts/`). Build only: `bundle exec jekyll build`, which writes to `_site/`.
  `_config.yml` is not reloaded by `serve`, so restart the server after you edit it.
- Deploy: GitHub Pages builds the site directly from the root of `master` (legacy Pages build, no
  workflow). **Pushing to `master` publishes the site.**
- The `Gemfile` uses the `github-pages` gem, which pins the same versions that GitHub Pages builds with
  (Jekyll 3.10, kramdown with GFM input, jekyll-feed, minima): see https://pages.github.com/versions/.
  A local build therefore renders the same HTML as production. Do not add plugins that are not on the
  GitHub Pages allowlist, or Jekyll 4-only features, because the production build ignores the
  `Gemfile` and would break or render them differently.
- Upgrading: when https://pages.github.com/versions/ lists a newer `github-pages` version, bump the
  constraint in the `Gemfile`, run `bundle update github-pages`, and commit `Gemfile.lock`.
- `_config.yml`'s `exclude` list keeps repo-only files (README, CLAUDE.md, Gemfile, ...) out of the
  published site. Jekyll copies every other file without front matter as-is, so add any new repo-only
  file to that list.

## Architecture

**The top-level `.md` pages are only stubs.** `about.md`, `cv.md`, `publications.md`, `services.md`,
`book-me.md`, `citation-policy.md`, `impressum.md` and `404.md` contain front matter (layout, title,
permalink) and a placeholder body that is never rendered. Each page's real content is hand-written HTML
in the matching `_layouts/<name>.html`. To change what a page says, edit its layout.

**Most layouts are standalone documents.** Every layout except `post.html` (which extends
`default.html`) is a full `<!doctype html>` page that includes `head.html`, `navbar.html`,
`footer.html` and `script.html` itself. Change shared page chrome in `_includes/`. A new top-level page
needs its own layout, a stub `.md`, and a link in `_includes/navbar.html`.

**Styling:** Bootstrap 3.1.1 CSS (`css/bootstrap*.css`) plus `css/customstyle.css` and
`css/style.css`, all loaded from `_includes/head.html`. `theme: minima` is set in `_config.yml` and
`_sass/` exists, but the custom layouts do not reference either. Upgrading the Bootstrap CSS can change
the design, so leave it unless that is the goal.

**Global scripts in `head.html`:** MathJax 2.7 (so LaTeX works in posts), jQuery 3.7.1 from Google's CDN
with an `integrity` hash, then the local Bootstrap JS 3.4.1 (`js/bootstrap.min.js`). Bootstrap JS must
load after jQuery. The only active JavaScript that uses them is Bootstrap's collapse plugin, which
drives the mobile navbar toggle. The gallery, dropdown and scrollspy scripts in `_layouts/cv.html` are
commented out. If you change the jQuery version, update its `integrity` hash, or the browser refuses to
run it. Analytics is Simple Analytics in `_includes/script.html`. Google Analytics and Disqus were
removed over GDPR concerns, so do not add tracking or third-party embeds that collect personal data.

**Edge rewrites:** the site is served through Cloudflare, which rewrites some HTML (`http://` links to
`https://`, email obfuscation). The live HTML can therefore differ slightly from `_site/`.

## Blog posts

- Posts are files in `_posts/` named `YYYY-MM-DD-Title-With-Dashes.markdown`. Their front matter is
  `layout: post`, `title`, `date`, `comments: true` and `categories`. Dates are rendered in the
  `timezone: Europe/Berlin` set in `_config.yml`. Without that setting, GitHub's UTC build would show a
  midnight `+0100` post on the previous day.
- `permalink: /:title/` builds each post's URL from the **filename** slug, not from the `title` field.
  Renaming a post file changes its public URL and detaches its giscus comments, which are mapped by
  pathname to GitHub Discussions (`_includes/giscus.html`).
- `<!--more-->` separates the excerpt. The blog index (`_layouts/index.html`) shows the excerpt.
  `feed.xml` is a hand-written RSS feed of the last 10 posts with their full content. It takes the place
  of the feed that jekyll-feed would generate.
- Images: recent posts use `/img/posts/YYYY-MM-DD-<name>.png`, and older posts use
  `/img/<post-slug>/`. The usual pattern is kramdown attribute lists:
  ```
  <br>
  ![img](/img/posts/2026-04-21-taste.png){:class="img-responsive"}
  {:style="max-width: 600px; margin: auto"}
  <br>
  ```

## Publications and CV

- `_layouts/publications.html` holds the publication list as hand-maintained HTML, grouped by year
  under `<h2><b> YEAR </b><h2>` headings, newest first. Each entry is a
  `<div class="information-line"><p>…</p></div>` that contains bold authors, a linked title, the venue,
  and then `<b> Supplementary Material:</b>` links. Copy an existing entry when you add one.
- Paper PDFs, slides and posters go in `publications/` and are linked by absolute URL
  (`https://edouardfouche.com/publications/<file>`). Name the files `SLIDES_<NAME>_<VENUE><YY>.pdf` and
  `POSTER_<NAME>_<VENUE><YY>.pdf`, for example `POSTER_SARAF_KDD26.pdf`.
- The CV page is hand-written HTML in `_layouts/cv.html`. The downloadable CV is `Resume_CV_FOUCHE.pdf`
  at the repo root.
