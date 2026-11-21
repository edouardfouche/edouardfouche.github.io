# Performance, accessibility and cleanup

**Date:** 2026-11-21
**Follows:** the [full site audit](2026-11-21-full-audit.md), items P1, P3 (partly), A1, A2, A5, A6, C1,
C4 (partly), L2 (partly), S5 and S6. The legal texts and the Book Me page are in a separate record:
[Impressum and privacy policy](2026-11-21-impressum-privacy.md).

## Changes, one commit each

| Commit | Change | Audit item | Visible? |
| --- | --- | --- | --- |
| `46ae659` | Shrink the 18 heaviest images, 26.5 MB → 7.0 MB; five PNGs become JPEGs, the GIF becomes an animated WebP | P1 | No (see verification) |
| `2300ed0` | Rewrite `css/style.css` as plain CSS that keeps what browsers applied | C1 | No |
| `7f3244b` | Remove unused CSS, JavaScript and junk files (30 files), and the gallery stylesheet loaded on every page | C4 | No |
| `de1f748` | Self-host jQuery and the license badge, `defer` the scripts, year from the build | L2, P3 | No |
| `51c4f84` | Feed: absolute URLs for images and links, `<language>` | S6 | No (feed only) |
| `47bc7be` | `width`/`height` on the 35 raster images in posts, `loading="lazy"` on all but the first | P1 | No |
| `2c2955c` | Underline links in running text, readable code and award colours, roomier footer links | A1, A2, A6 | **Yes** |
| `006d461` | Link the Google Scholar profile (Publications, About, `sameAs`) | S5 | **Yes** |

[`CLAUDE.md`](../CLAUDE.md) was updated with the new conventions in the same push.

### Images (`46ae659`)

Every image was re-encoded at most 1440 px wide (twice the 720 px reading column), without EXIF or XMP
metadata, with its ICC profile kept. For each JPEG, the script tried qualities 82–94 with 4:2:0 and
4:4:4 chroma, and kept the smallest file whose PSNR against the original (resampled to the same size)
was at least 38 dB, which is not visible at normal viewing distance. Same-format files were only
replaced if they shrank by at least 15%.

| File | Before | After |
| --- | --- | --- |
| `img/deutsche-bahn/DSC_8839.JPG` (4928×3264 → 1440×954) | 6,253 KB | 80 KB |
| `img/posts/2026-04-21-taste` (PNG → JPEG) | 4,609 KB | 133 KB |
| `img/posts/2026-03-26-autopilot` (PNG → JPEG) | 3,295 KB | 720 KB |
| `img/posts/2026-04-09-claude-code-leak` (PNG → JPEG) | 2,758 KB | 792 KB |
| `img/posts/2026-04-14-identity-crisis` (PNG → JPEG) | 2,180 KB | 86 KB |
| `img/color-wheel/animation` (GIF → lossless animated WebP, identical frames and timing) | 1,939 KB | 1,292 KB |
| `img/einbuergerung.jpg`, six Knight's Tour images, `img/deutsche-bahn/Rpi` (PNG → JPEG), `farbkreis_extended.png`, the About portrait, the handwritten email, the favicon | 3,450 KB | 1,939 KB |

Renamed files (`.png` → `.jpg`, `.gif` → `.webp`) are referenced from their posts. Their old URLs now
return 404. They were only ever embedded by the site itself. SVG charts were left alone: they are text
and travel compressed (a 590 KB SVG transfers as about 55 KB).

Weight of the heaviest pages (HTML, CSS, JavaScript and images served by the site, uncompressed):

| Page | Before | After |
| --- | --- | --- |
| Transportation Schedule on RPi | 6.83 MB | 0.46 MB |
| What remains once AI overtakes most of the execution? Taste. | 4.85 MB | 0.45 MB |
| Why using AI requires us to be even better | 3.54 MB | 1.04 MB |
| Anthropic's Claude Code Leak | 3.00 MB | 1.11 MB |
| The Extended Color Wheel by Itten | 2.87 MB | 2.11 MB |
| The Identity Crisis of Software Engineers | 2.43 MB | 0.40 MB |
| Digital Art & the Knight's Tour Problem | 2.21 MB | 1.49 MB |
| About | 0.59 MB | 0.37 MB |

Pages without large images now count jQuery among their own files (88 KB uncompressed, 30 KB
transferred), which used to come from Google. They no longer load MathJax (at least 90 KB transferred,
see the [quick wins](2026-11-21-quick-wins.md)). In total, a page without pictures transfers roughly
half as much as before the two batches.

### `css/style.css` (`2300ed0`)

The file now contains exactly the rules browsers applied before: the declarations without Sass
variables, `.posts > .post:last-child`, the `.PageNavigation` and table rules, and the nested rules
flattened (`h1 a`, `.post blockquote`, `.post .comments`, `.post .read-more`). Gone: declarations with
`$variables`, the `@include` blocks, the five rules whose selector began with a `//` comment, the trailing
`@import`, and rules for elements the site does not have (masthead, site-avatar, site-info, site-name,
site-description, `nav`, `footer`, `.wrapper-footer`; checked against all 27 built pages). Flattening
also gives older browsers without CSS nesting the same look as current ones.

The rules that were meant but never applied (separators between posts on the index, a smaller line
height for headings on phones, scrolling tables) were **not** added, because each would change the
look. See [C1](2026-11-21-full-audit.md#c1-cssstylecss-is-uncompiled-sass).

### Unused files (`7f3244b`)

Removed: `css_gallery/`, `js_gallery/`, `js_timeliner/`, and the gallery `<link>` in `head.html`;
`css/basic.css`, `css/carousel.css`, a second `galleriffic-2.css` with its loader and arrow images,
`css/syntax_default.css`, the stock `css/bootstrap.min.css` and `css/bootstrap-theme.min.css` (which lack
the site's customizations, see [C2](2026-11-21-full-audit.md#c2-cssbootstrapcss-is-a-modified-bootstrap-311)),
`js/bootstrap.js`; four `Thumbs.db` files, two `.psd` files, one `.xcf` file and `img/test.png`. No page
referenced any of them.

Not removed: the other unused images (old profile pictures, gallery images, logos, the 5001×5001
`img/Instagram_icon.png`, the Tengu logo originals). They cost visitors nothing, some may be wanted as
originals, and deleting them is the owner's call.

### Self-hosting and deferred scripts (`de1f748`)

- `js/jquery-3.7.1.min.js` is byte-identical to the Google CDN copy, and its SHA-256 equals the
  `integrity` hash the site used. jQuery and Bootstrap JS load with `defer`.
- `img/cc-by-sa-4.0-88x31.png` is the same badge that `i.creativecommons.org` served via a redirect to
  `licensebuttons.net`.
- The footer year comes from the build (`{{ site.time | date: '%Y' }}`) instead of `document.write`.

Together with the MathJax change of the [quick wins](2026-11-21-quick-wins.md), third parties on every
page went from four (Google, cdnjs, Creative Commons, Simple Analytics) to one (Simple Analytics). Posts
add giscus, and the two math posts add cdnjs.

### Feed (`51c4f84`)

`feed.xml` turns `src="/…"` and `href="/…"` in the post HTML into absolute URLs and leaves
protocol-relative `//…` URLs alone. The built feed is well-formed and contains no relative URL.

### Image dimensions and lazy loading (`47bc7be`)

A script added the pixel size to the kramdown attribute list of the 35 raster images in posts, for
example `{:class="img-responsive" width="1440" height="954"}`. `.entry img { height: auto; }` in
`css/customstyle.css` keeps the proportions when `max-width: 100%` narrows an image. `_layouts/post.html`
adds `loading="lazy"` to images that have both attributes, except the first image of each post. The
SVG charts have no dimensions and load as before. A first version lazy-loaded them too: their space
collapsed until they loaded, and three pages got shorter in the screenshots. That is why the rule
requires both attributes.

### Accessibility (`2c2955c`)

- Links inside `.entry`, `.content-paragraph`, `.subcontent-wrapper li`, `.information-line` and the
  footer are underlined (1px, offset 0.15em).
- `css/syntax.css`: comments #75715e → #95917b (4.68:1), keywords and operators #f92672 → #fa4e8c
  (4.62:1), lexer errors #960050 → #ed007e (4.61:1 on their own background). Each colour was lightened in
  HSL just enough to pass 4.5:1, so the hues stay.
- "Best Paper Award!" #ff0000 → #c00000 (6.5:1).
- Footer line height 1.8 (about 27px between the stacked links).

### Google Scholar (`006d461`)

The profile is linked at the top of Publications and in the About page's list, and added to
`social.links`, so jekyll-seo-tag lists it as `sameAs` in the JSON-LD of the home and About pages.

## Verification

All checks used the WebKit screenshot procedure from the audit (27 pages at 1280 px and 375 px from a
local server, analytics, giscus and Google Forms blocked), comparing each change set with the build
before it.

- **Images:** 36 of 54 screenshots pixel-identical. The other 18 are the 9 pages with re-encoded
  images, with unchanged page heights and differences inside the images only, plus a 1px shift below
  one header whose aspect ratio was rounded (871.4 → 871 px). The citizenship photo, the largest
  difference, was compared side by side and looks the same.
- **`style.css`, unused files, self-hosting, feed, dimensions, lazy loading:** 50 of 54 screenshots
  pixel-identical. The other 4 are at 375 px only, inside lazily loaded images of four posts (at most 76
  of 255 levels on 0.2% of the pixels). That is resampling noise from WebKit decoding the images at a
  different moment, invisible side by side. The phone menu was tapped open on all 27 pages, and the
  menu-open screenshots are identical to the previous build's, so the deferred scripts work.
- **Visible changes** (underlines, colours, footer, Scholar line, Book Me, Impressum) were reviewed in
  screenshots at both widths.
- **axe-core 4.14.1** on six representative pages (home, Publications, the Knight's Tour post,
  Citation Policy, Impressum, Book Me) after all changes: `link-in-text-block`, `target-size`,
  `color-contrast`, `scrollable-region-focusable` and `frame-title` are gone. What remains: `list` (the
  navbar's icon links are not in `<li>`), `region` and `landmark-one-main` (no `<main>`, `<nav>`,
  `<footer>` landmarks), and kramdown's footnote roles. These are audit items A3 and C5, still open.
- **Build:** `bundle exec jekyll build` without warnings at every step.

## Still open

From the audit's list: width/height for the SVG charts, landmarks and the navbar list (A3), the home
page introduction (S1), share images and descriptions for posts (S4), alt texts (A4), the font stack
(A7), the remaining unused images (C4), the CSS dead code in `customstyle.css` (C3), and the owner's
dashboard tasks (Cloudflare, Search Console). See the
[recommended order of work](2026-11-21-full-audit.md#recommended-order-of-work).
