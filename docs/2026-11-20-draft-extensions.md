# Draft file extensions

**Date:** 2026-11-20
**Resolves:** the `_drafts/` bullet of [open item 5](2026-11-20-open-items.md#5-dead-code-and-leftovers).
**Commit:** `52fe52d`

## Problem

Five files in `_drafts/` had no `.markdown` extension, unlike the other drafts. Jekyll reads a draft
only if its filename ends in an extension, and that extension decides how the file is converted. A
build with `--drafts` therefore:

- skipped four of them entirely: `2017-01-30-Why-we-need-more-Scientists-as-Politicians`,
  `2017-07-17-Are-political-TV-debates-fair-_`, `2017-07-17-Visualizing-New-York-Taxi-Data` and
  `2017-09-18-A-Gentle-Introduction-to-Time-Series-Forecasting`;
- read `2016-11-24-Automatic-backup-with-SSH-on-Ubuntu-16.04` as a file with the extension `.04`. It
  rendered at `/Automatic-backup-with-SSH-on-Ubuntu-16/`, and its body was inserted as raw text
  without Markdown conversion.

Drafts are never published, so this only affected local previews.

## Change

Each file was renamed with `git mv` to `<name>.markdown`. The contents are unchanged.

## Verification

Builds before and after the rename, compared with `diff -r`:

- **Production build** (`jekyll build`, no drafts): identical, except the feed's build timestamp.
  The live site does not change.
- **Drafts build** (`jekyll build --drafts`): the five drafts now render, at `/<slug>/` as usual.
  - `/Why-we-need-more-Scientists-as-Politicians/`
  - `/Are-political-TV-debates-fair-_/`
  - `/Visualizing-New-York-Taxi-Data/`
  - `/A-Gentle-Introduction-to-Time-Series-Forecasting/`
  - `/Automatic-backup-with-SSH-on-Ubuntu-16.04/`, which replaces `/Automatic-backup-with-SSH-on-Ubuntu-16/`.
    Its body is now converted from Markdown (wrapped in `<p>`).

  The other differences in that build follow from those additions: the blog index and sitemap list
  the five drafts, and the neighbouring drafts' previous/next links point to them.

## Side effect observed: the duplicate poster in the git index

During the rename, git also staged a deletion of `publications/Poster_DS32020_SGMRD.pdf` that was not
asked for. Right before, `git status` had been clean. The repository tracks that poster twice, under
two names that differ only in case (see item 16 in the
[SEO record](2026-11-20-seo.md#what-could-still-be-done)). macOS filesystems are case-insensitive by
default, so a checkout holds only one file, and rewriting the index dropped the second entry.

The deletion was unstaged with `git restore --staged publications/Poster_DS32020_SGMRD.pdf`, so it is
not part of this change. Until item 16 is decided, check `git status` before committing on a Mac.
Otherwise, a commit can remove that poster's public URL without anyone noticing.
