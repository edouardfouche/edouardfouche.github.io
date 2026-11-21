# Alt texts, dead CSS and the Cambria fallback

**Date:** 2026-11-21 (evening; published with the work of the following night)
**Follows:** the [full site audit](2026-11-21-full-audit.md), items A4, C3 and A7, done at the owner's
request.

| Commit | Change | Visible? |
| --- | --- | --- |
| `3e594f8` | An alt text for every image (56) | No (screen readers, search engines, broken-image fallback) |
| `3c8b767` | Remove the dead CSS from `css/customstyle.css` | No (pixel-identical) |
| `618316a` | Font stack `Cambria, Caladea, Georgia, serif`, with Caladea self-hosted | **Yes**, for visitors without Cambria (Mac, iPhone, Android, Linux) |

## Alt texts (`3e594f8`)

Before: 19 images had the alt text "img". Others had "img1" … "img31", file names ("3d-plot-outlier",
"counts_arxiv", "comfort_zone"), "Profil picture" or "contact". Only the newest post had a real
description.

Each image was looked at, together with the paragraphs around it, and described for someone who cannot
see it:

- **Photos:** what they show, e.g. "A yellow road bike leaning against a metal railing beside a
  tree-lined canal". In the im2txt post, the point is to compare the model's caption (which follows as
  text) with reality, so the alt text says what the photo really shows.
- **Charts:** chart type, axes and the point the text makes, e.g. "Total number of arXiv articles on a
  base-2 logarithmic scale, 1991 to 2019, with a vertical line at each doubling: the doublings come
  further and further apart". Numbers were read off the charts and are approximate ("about 1.6
  million").
- **Illustrations and memes:** their text, e.g. the four quotes of the Rick Rubin meme in the order they
  are spoken.
- **People** are named only where the post itself names them (Rick Rubin in the Taste post, Mayor Marcus
  König in the citizenship post). An unclear species stays generic ("dark-headed seabirds").
- **About page:** "Portrait of Edouard Fouché". The handwritten email image spells the address out in
  words (`… dot … at … dot com`), so that screen reader users get it while address harvesters do not.
- **Services:** the Tengu logo is described ("a winding path up a red mountain").

Check: the built pages keep the same 219 `<img>` elements. No content image has a generic or empty alt.
Quotes in alt texts are escaped correctly (`&quot;`).

## Dead CSS (`3c8b767`)

Every selector of `css/customstyle.css` was tested against the 27 built pages with a script. Pseudo
classes such as `:hover` were stripped, and the class Bootstrap's collapse plugin adds at run time was
simulated. About 50 rules matched nothing and were removed:

- the old HTML CV (`.main-info`, `.info-icon`, `.university-name`, `.from-to`, `.skills-*`, …);
- the gallery, the sidebar with its affix states, the tag cloud;
- `#ibm`, `#custom-button`, `#splitter`, `#gallery-title`;
- leftovers from Bootstrap's carousel example (`.marketing`, `.featurette-heading`);
- the `body.contact` selector, and a broken `@media @media` block at the end.

Also removed: commented-out code, a `body:after` that "preloaded" an image the navbar loads anyway, and
five `font-family: 'Cambria'` lines that repeated what `body` sets. An exact duplicate of the
`#flickr-container` rules was merged.

The file shrank from 930 lines (21 KB) to 361 lines (9 KB).

Check: screenshots of all 27 pages at 1280 and 375 px, and of the open phone menu on every page, before
and after: **54/54 and 27/27 pixel-identical**.

## Font (`618316a`)

All text was set in Cambria without a fallback. Cambria comes only with Windows and Microsoft Office. On
Macs, iPhones, Android and Linux the site showed the browser's default font instead (Times in WebKit), so
most visitors never saw the intended design.

**Choice:** Caladea, by Huerta Tipográfica for Google, under the SIL Open Font License. It was designed as
a *metric-compatible* substitute for Cambria: same character widths, so lines, wraps and page lengths
match the Cambria design. It looks close to Cambria. Georgia (similar, preinstalled on Apple devices) and
the generic `serif` are the next fallbacks.

**Setup:**

- `fonts/caladea/`: the four styles as WOFF2 (31–33 KB each, converted from Google's
  `google/fonts` repository with fontTools), plus `OFL.txt`, which the license requires to travel with
  the fonts.
- `css/style.css`: four `@font-face` rules (`font-display: swap`: text shows at once in a fallback, then
  switches), and `font-family: Cambria, Caladea, Georgia, serif` on `body`, the only place a font is set.
- Browsers download a style only if Cambria is missing and the page uses that style. That is typically
  regular, bold and italic, about 97 KB on the first visit, then cached. No request goes to Google.
- Coverage: Caladea has every character the site uses, except emoji and ↩ ☺ ♥, which browsers take from
  other fonts, as they did before.
- A Latin-only subset would have saved 6 KB per file but risked missing characters later, so the full
  fonts are shipped.

**Checks (WebKit, which has no Cambria here):**

- On all 27 pages at 1280 and 375 px, Caladea loads (regular, bold and italic where used), the navbar
  stays one line (51 px), no page is wider than the window, and the phone menu opens.
- At 992 and 768 px the navbar stays one line too. Its inner container sticks out 4–6 px at those widths,
  but that is older than this change (identical with the old font) and clipped invisibly.
