# Blog: side margins and phone layout

**Date:** 2026-11-21
**Scope:** the blog index (`/`) and the posts. Other pages are unchanged (checked pixel by pixel,
see Verification).

## Observations

The site owner reported that the side margins of the blog did not look good, and that the text moved
when opening a post from the index.

Distance in px between the text and the left / right edge of the window, measured on the index and
on the post "Knowledge work as we know it is dying":

| Width | Index | Post |
| --- | --- | --- |
| 1280px | 150 / 130 | 136 / 131 |
| 1000px | 108 / 88 | 94 / 89 |
| 800px | 116 / 96 | 101 / 96 |
| 375px (phone) | 27 / 7 | 13 / 8 |
| 320px (phone) | 26 / 6 | 11 / 6 |

Causes:

- **Text moved when opening a post.** [`_layouts/default.html`](../_layouts/default.html) (used only
  by [`_layouts/post.html`](../_layouts/post.html)) put the post inside a Bootstrap `.row`, whose
  `margin-left: -15px` shifted it left. On the index ([`_layouts/index.html`](../_layouts/index.html)),
  `.posts` sits directly in the `.container`, so it was not shifted.
- **Uneven margins.** `.post` had `margin-left: 20px` in
  [`css/customstyle.css`](../css/customstyle.css) and `padding: 1%` on each side in
  [`css/style.css`](../css/style.css). The left margin was therefore about 20px wider than the right one.
  On a phone the right margin was 6 to 8px, so the text almost touched the edge of the screen.
- **Very long lines on desktop.** The text filled the container: about 1000px at 1280px, around 130
  characters per line at 18px.
- **Phone-only issues.** Justified text in a column about 330px wide had large gaps between words.
  In two older posts ("Fun with Tensorflow im2txt", "Transportation Schedule on RPi"), long inline
  file paths in `code` ran off the right edge of the screen and were cut off. Bootstrap 3.1.1 sets
  `white-space: nowrap` on `code`, and `body` has `overflow-x: hidden`. This predates the change.

## Changes

| File | Change |
| --- | --- |
| [`_layouts/default.html`](../_layouts/default.html) | The `.row` around the post content became `<div class="blog-column">`. |
| [`_layouts/index.html`](../_layouts/index.html) | The posts list became `<div class="posts blog-column">`. |
| [`css/customstyle.css`](../css/customstyle.css) | New `.blog-column` rule: centered (`margin: auto`), `max-width: 752px` (720px of text, about 80 characters a line), `padding: 0 16px`, which gives about 20px between the text and each edge on a phone. Removed `margin-left: 20px` from `.post`. |
| [`css/customstyle.css`](../css/customstyle.css) | Below 768px, paragraphs in `.blog-column` are aligned left instead of justified. |
| [`css/customstyle.css`](../css/customstyle.css) | Inline code in `.blog-column` (`:not(pre) > code`) may wrap anywhere and is never hyphenated. Hyphenation had to be turned off because the global `hyphens: auto` made WebKit split `show_and_tell` as `tel-l`, which changed the path and still overflowed. Code blocks are unchanged. |
| [`css/style.css`](../css/style.css) | Removed `padding-left: 1%` and `padding-right: 1%` from `.post`. |

Not changed: the vertical gap between the navbar and the first title on phones (about 70px). It is
the same on every page of the site, so changing it for the blog alone would make the content jump
when moving between the blog and the other pages.

## Verification

No headless browser is installed, so pages were rendered with a small Swift script around an
offscreen `WKWebView` (WebKit, the engine of Safari), at window widths of 1280, 1000, 800, 414, 375
and 320px. The script is not kept in the repository. The site was built with `bundle exec jekyll
build` and served locally.

- Text edges after the change, identical on the index and on a post at every width:

  | Width | Index and post |
  | --- | --- |
  | 1280px | 280 / 280 |
  | 1000px | 140 / 140 |
  | 800px | 106 / 106 |
  | 414px, 375px | 20 / 20 |
  | 320px | 19 / 19 |

- On a post, the previous/next links and the giscus comments have the same edges as the text.
- Every one of the 18 posts was checked at 375px and 1280px for elements that extend past the text
  column (outside a scrolling container), and for a page wider than the window. After the inline code
  fix, none remain.
- The About, CV, Publications, Services, Book Me, Impressum, Citation Policy and 404 pages were
  rendered at 1280px and 375px from a build of the previous commit (`fa20903`) and from the
  working tree. The screenshots are byte-identical.
