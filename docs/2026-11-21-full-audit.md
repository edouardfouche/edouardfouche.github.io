# Full site audit (second pass)

**Date:** 2026-11-21
**Scope:** the repository at `abae645` and the live site https://edouardfouche.com. `abae645` is also the
commit that GitHub Pages built last, so the local build is what visitors get, apart from Cloudflare's
edge rewrites (checked on 5 pages).
**Builds on:** the [site audit](2026-11-20-site-audit.md), [open items](2026-11-20-open-items.md),
[SEO](2026-11-20-seo.md) and the later records. Findings already described there are only referenced.
[Section 9](#9-status-of-earlier-open-items) gives their status today.
**Changes made:** none. The audit only read the repository and the live site. This file and its line in
the [index](README.md) are the only changes.

## Summary

The foundations are sound: HTTPS with a valid certificate, a local build that matches production,
complete search metadata, no broken internal links, no mixed content, and a layout that works at
phone width. The earlier maintenance work holds.

The main gaps:

- **Legal texts are out of date.** The Impressum cites two repealed laws, and the privacy notice says
  no personal data is processed, although the site embeds Google Forms and giscus and loads code from
  Google's servers. Three statements about the license contradict each other.
- **Privacy.** One published photo still contains the GPS position where it was taken.
- **Weight.** Eight posts weigh 2 to 7 MB, almost all of it oversized images. MathJax is loaded on all
  27 pages, although only 2 posts contain math.
- **Accessibility.** Links in text are told apart by colour alone (258 links), there are no
  landmarks, the heading structure is off, and 19 images have the alt text "img".
- **Code health.** `css/style.css` is uncompiled Sass, so browsers drop part of it, and
  `css/bootstrap.css` carries undocumented local changes. Many unused files are published, among them
  Windows `Thumbs.db` files and Photoshop sources.
- **Still pending from 2026-11-20:** the Cloudflare SSL/TLS mode (redirects still go through
  `http://`) and the search engine registration.

### Recommended order of work

| # | Action | Findings | Effort | Needs |
| --- | --- | --- | --- | --- |
| 1 | Update the Impressum and privacy notice: current laws, every data flow, one license statement, working links | [L1](#l1-the-impressum-cites-repealed-laws)–[L3](#l3-three-license-statements-contradict-each-other), [L6](#l6-cloudflare-hides-the-impressum-email-address-behind-javascript) | M | Owner (wording, legal advice if wanted) |
| 2 | Strip the GPS position from `img/knight/study.jpg` | [L4](#l4-a-published-photo-contains-its-gps-position) | S | Repo |
| 3 | Cloudflare: SSL/TLS mode Full (steps already written), HSTS, minimum TLS 1.2 | [S2](#s2-redirect-chains-still-go-through-http), [T1](#t1-no-security-headers), [T2](#t2-tls-10-and-11-are-accepted) | S | Owner (Cloudflare dashboard) |
| 4 | Book Me and CV pages: heading, fallback link, accessible names | [B2](#b2-cv-page), [B3](#b3-book-me) | S | Repo |
| 5 | Replace the 10 dead links | [B1](#b1-dead-external-links) | S | Repo |
| 6 | Shrink the heavy images; add `width`/`height` and lazy loading | [P1](#p1-images) | M | Repo |
| 7 | Load MathJax only on the two posts with math | [P2](#p2-mathjax-on-every-page) | S | Repo + visual check |
| 8 | Underline links in text; fix the low-contrast code and award colours | [A1](#a1-links-are-told-apart-by-colour-only), [A2](#a2-contrast) | S | Repo + visual check |
| 9 | Say on the home page whose site it is | [S1](#s1-the-home-page-does-not-say-whose-site-it-is) | S | Owner (wording) |
| 10 | Link the Google Scholar profile (and ORCID or DBLP, if they exist) | [S5](#s5-scholarly-profiles-are-not-linked) | S | Repo |
| 11 | Turn `css/style.css` into valid CSS that keeps today's look | [C1](#c1-cssstylecss-is-uncompiled-sass) | M | Repo + visual check |
| 12 | Delete junk files, unused assets and commented-out code | [C3](#c3-dead-code), [C4](#c4-unused-files-on-the-live-site) | M | Repo + visual check |

Effort: S = under an hour, M = a few hours. "Visual check" means the before/after screenshot
comparison described in the
[maintenance changes record](2026-11-20-maintenance-changes.md#2-visual-regression-test-before-and-after-each-change).

## 1. Legal and privacy

These are observations, not legal advice. For the final wording of the Impressum and the privacy
notice, use a maintained generator or a lawyer.

### L1. The Impressum cites repealed laws

[`_layouts/impressum.html`](../_layouts/impressum.html) and the meta description in
[`impressum.md`](../impressum.md) refer to the Telemediengesetz and the Rundfunkstaatsvertrag:

| Text on the page | Status | Current reference |
| --- | --- | --- |
| "Angaben gemäß § 5 TMG" | The TMG was repealed on 14 May 2024 | § 5 DDG (Digitale-Dienste-Gesetz) |
| "Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV" | The RStV was replaced on 7 November 2020 | § 18 Abs. 2 MStV (Medienstaatsvertrag) |
| "§ 7 Abs.1 TMG", "§§ 8 bis 10 TMG" (Haftungsausschluss) | Repealed with the TMG | The liability rules are now in the EU Digital Services Act (Art. 4–6) and the DDG |

The obligations themselves did not change, only the references. The chambers of commerce (IHK)
recommend updating them. Also, "90489, Nürnberg" is normally written without the comma.

### L2. The privacy notice does not describe the site

The Datenschutzerklärung (a section of the Impressum) says: "Auf dieser Webseite werden keine
personenbezogenen Daten erhoben, gespeichert oder verarbeitet. Es werden keine Cookies verwendet."
The site's own responses do set no cookies, but visitors' data goes to several parties:

| Data flow | Pages | In the notice? |
| --- | --- | --- |
| Cloudflare (DNS, proxy, CDN) receives every request, including the IP address | all | No |
| GitHub Pages, the origin server behind Cloudflare | all | Yes, but the link to GitHub's privacy page is dead ([B1](#b1-dead-external-links)) |
| jQuery from `ajax.googleapis.com` (Google) | all | No |
| MathJax from `cdnjs.cloudflare.com` | all | No |
| License badge from `i.creativecommons.org`, which redirects to `licensebuttons.net` | all | No |
| Simple Analytics (cookieless, aggregated) | all | Yes |
| giscus comments: `giscus.app` loads when a reader scrolls to the comments, avatars come from GitHub, and commenting requires a GitHub sign-in | 18 posts | No |
| Google Forms iframe: loads Google's code and can set Google cookies, and what people type (name, email, request) is personal data | Book Me | No |
| PayPal donation button | none: the button is commented out | Yes (stale) |

The notice also lacks most of what Art. 13 GDPR asks for: purposes and legal bases, recipients and
transfers to the US, storage periods, the data subject's rights, and the right to complain to a
supervisory authority. German sites usually put this on a separate "Datenschutz" page, linked from the
footer of every page.

German courts have held that loading resources from Google's servers sends the visitor's IP address to
Google without a legal basis (LG München I, 20 January 2022, 3 O 17493/20, about Google Fonts). The same
reasoning applies to jQuery from Google's CDN.

Suggestions:

1. **Remove what is easy to remove:** self-host jQuery (same file, same integrity hash) or drop it
   ([P3](#p3-render-blocking-scripts-and-styles)), self-host the 1.5 KB license badge, load MathJax only
   where needed ([P2](#p2-mathjax-on-every-page)), and link to the Google Form instead of embedding it
   (or embed it only after a click). The Google Forms embed and giscus predate the rule in
   [`CLAUDE.md`](../CLAUDE.md) against third-party embeds that collect personal data, and they do not
   fit it.
2. **Describe what remains** (Cloudflare, GitHub Pages, Simple Analytics, giscus, the form), for
   example with the free generators of eRecht24 or datenschutz-generator.de, on its own page.
3. **Drop the PayPal section** while the button is hidden.

### L3. Three license statements contradict each other

| Where | What it says |
| --- | --- |
| Footer, license badge, [Citation Policy](../_layouts/citation-policy.html), repository [`LICENSE`](../LICENSE) | CC BY-SA 4.0: anyone may share and adapt, also commercially, with attribution and under the same license |
| `<meta name="copyright">` in [`_includes/head.html`](../_includes/head.html), on every page | "All Rights Reserved" |
| Impressum, section "Urheberrecht" | Downloads and copies are allowed only for private, non-commercial use |

The CC BY-SA statement also claims too much. The portraits are by Chérie Birkner (credited on the
About page and in the press package), and the papers, slides and posters may be under the publishers'
copyright. The site cannot relicense either.

Suggestion: one statement everywhere, for example "Texts and images by Edouard Fouché are licensed
under CC BY-SA 4.0 unless marked otherwise. Photos by Chérie Birkner, publications and third-party
material are excluded." Then remove the `copyright` meta tag (or make it match), and rewrite the
Urheberrecht paragraph. Creative Commons also advises against CC licenses for software. The vendored
Bootstrap and gallery scripts keep their own licenses.

### L4. A published photo contains its GPS position

`img/knight/study.jpg`, shown in the post
[Digital Art & the Knight's Tour Problem](../_posts/2017-05-09-Digital-Art-&-the-Knight's-Tour-Problem.markdown),
is an iPhone photo from May 2017. Its EXIF metadata includes the latitude and longitude where it was
taken. Anyone who downloads the image can read them. The coordinates are deliberately not repeated
here.

No other published image contains a position. `img/deutsche-bahn/DSC_8839.JPG` has an empty GPS
block, and two unused profile pictures carry camera data only.

Fix: strip the metadata (`exiftool -all= img/knight/study.jpg`, or re-save the image without EXIF) and
commit it. The old file stays in the public git history. Removing it from there would mean rewriting
history, which is probably not worth it for a 2017 location. Check new photos for location data
before publishing them.

### L5. Contact details: three versions, one of them only as an image

- The About page shows a personal webmail address as a handwritten image with the alt text "contact".
  Screen readers cannot read it, and nobody can copy or click it.
- The Impressum shows a different address, on the site's own domain.
- The public CV PDF lists the webmail address and a mobile phone number. The CV is in the sitemap, so
  search engines index it.

Suggestion: use one address everywhere, as a normal `mailto:` link. The domain address is the better
choice, because it can later forward anywhere. Cloudflare already obfuscates email addresses in the
HTML against harvesting. Whether the phone number belongs in a public, indexed PDF is the owner's
decision. A public CV variant without it is common.

### L6. Cloudflare hides the Impressum email address behind JavaScript

Cloudflare's Email Obfuscation replaces the address on the live Impressum with "[email protected]"
plus a decoding script. Without JavaScript, the legally required address does not appear at all.
Cloudflare skips everything between `<!--email_off-->` and `<!--/email_off-->`. Wrapping the address
(ideally a `mailto:` link) in these markers in [`_layouts/impressum.html`](../_layouts/impressum.html)
shows it to everyone.

### L7. Drafts are public

The 12 files in `_drafts/` are not published on the site, but the repository is public, so anyone
can read them on GitHub. Keep notes that are not meant for the public elsewhere.

## 2. Broken or misleading things

### B1. Dead external links

All 124 distinct external links on the 27 pages were requested. 100 work. 14 could not be checked,
because the target answers scripts with a bot check or a rate limit (Amazon 6, Redbubble 2, LinkedIn 2,
ACM, OpenReview, Towards Data Science, Wikipedia). 10 are dead:

| Page | Link | Result | Replacement (checked on the audit date) |
| --- | --- | --- | --- |
| Impressum | GitHub "Global Privacy Practices" (`help.github.com`) | Redirects to a 404 | https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement |
| Citation Policy | Cambridge PDF "Citing blogs as reference sources" | Redirects to a general research-integrity page | Archived copy: https://web.archive.org/web/20240808130837/https://www.research-integrity.admin.cam.ac.uk/files/citing_blogs_as_reference_sources.pdf, or a current guide |
| Fun with Tensorflow im2txt | `github.com/tensorflow/models/tree/master/im2txt` (2 links) | 404 | https://github.com/tensorflow/models/tree/archive/research/im2txt |
| Fun with Tensorflow im2txt | Google Drive file (the pre-trained model) | 404 | None. Say that it is no longer available |
| Fun with Tensorflow im2txt | `mscoco.org`, `mscoco.org/explore` | No response | https://cocodataset.org/ |
| Observations about my transition from Academia to Industry | `blog.devicerandom.org` ("Getting a life", 2011) | No response | https://web.archive.org/web/20250626123546/http://blog.devicerandom.org/2011/02/18/getting-a-life/ |
| Observations about my transition from Academia to Industry | `goodbyeacademia.com/wordpress` | No response (twice) | https://web.archive.org/web/20260312172219/https://goodbyeacademia.com/wordpress/ |
| Neural-based Outlier Discovery | KIT HiCS project page | Redirects to an unrelated KIT team page | The paper: https://doi.org/10.1109/ICDE.2012.88 (Keller, Müller, Böhm, ICDE 2012) |

About 20 working links go through a redirect, and 12 still use `http://`. Update them when you edit
those pages. Check the two Redbubble links (the owner's shop) by hand.

### B2. CV page

- The fallback inside the `<object>` in [`_layouts/cv.html`](../_layouts/cv.html) reads
  `Download the PDF <a href="/Resume_CV_FOUCHE.pdf"></a>.` The link has no text, so it is invisible.
  Browsers that do not display embedded PDFs show exactly this fallback. Chrome on Android is one of
  them; this was not tested on a device.
- The CV exists only as the embedded PDF. The page itself has no CV text for search engines or screen
  readers, and at 375 px the embedded page is too small to read. The `<object>` has no accessible name.
- About 1,440 of the layout's 1,513 lines are commented out: an old HTML CV, the gallery, dropdown and
  sidebar scripts. They make up 84% of the page's HTML (51 of 60 KB), and every visitor downloads them.

Suggestions: give the link a text, and add `type="application/pdf"` and a `title` to the `<object>`.
The sentence above the embed already links the PDF ("you can download it here"), so the CV stays
reachable. Optionally, add a short HTML summary (current role, education, awards). Remove the
commented-out code ([C3](#c3-dead-code)).

### B3. Book Me

- The page has no heading and no text of its own. The intro ("Your answers go directly to me…",
  "Please do not submit any sensitive or confidential information") is commented out as "redundant
  with the form". If the Google Form does not load (blocked by a privacy extension, a company network,
  or offline), visitors see an empty page.
- The iframe has no `title`, uses the obsolete `frameborder`, `marginheight` and `marginwidth`
  attributes, and the template's "INSTRUCTIONS: Replace YOUR_GOOGLE_FORM_ID" comment ships in the HTML.
- For privacy, see [L2](#l2-the-privacy-notice-does-not-describe-the-site).

Suggestion: restore an `<h1>` and the two sentences, add a direct link "Open the form in a new tab"
and an email alternative, and give the iframe a `title`.

### B4. Wrong menu item highlighted

The `<body>` class decides which menu item is highlighted. Citation Policy and Impressum use
`class="about"`, so "About" lights up on them. The 404 page uses `class="home"`, so "Blog" lights up.
Pages outside the menu should use a class that matches no menu item.

### B5. Visible typos and copy errors

| Page | Text | Fix |
| --- | --- | --- |
| Services | `Why "Tengu''?` (opened with a double quote, closed with two apostrophes) | `Why “Tengu”?` |
| About | Portrait alt text "Profil picture" | For example "Portrait of Edouard Fouché" |
| Citation Policy | "creative common CC-BY-SA-4.0 license" | "Creative Commons CC BY-SA 4.0 license" |
| Citation Policy | "Citing blog article", "LaTex", "BibLatex", "how an entry to my blog may look like", "In doubt" | "Citing blog articles", "LaTeX", "BibLaTeX", "what an entry for my blog may look like", "If in doubt" |
| Citation Policy | Example entry: `urldate = {January 5th, 2025}` | BibLaTeX needs ISO 8601: `urldate = {2025-01-05}`. Biber reports the current value as an invalid date and ignores it |
| 404 | "Oops ! 404 Error", "back to the homepage !" | No space before "!" in English |
| Footer, every page | "Twitter Bootstrap", "Github" | "Bootstrap", "GitHub" |
| Publications | "Github" 5 times, next to "GitHub" 16 times | "GitHub" |
| Services | "3 to 6-month long mentorships" | "3- to 6-month mentorships" |

## 3. Performance

### P1. Images

Heaviest pages, counting the HTML, CSS, JavaScript, images and embedded PDFs served by the site itself
(uncompressed, third-party scripts excluded):

| Page | Total | Of which images |
| --- | --- | --- |
| Transportation Schedule on RPi | 6.8 MB | 6.6 MB, of which one photo is 6.25 MB |
| What remains once AI overtakes most of the execution? Taste. | 4.9 MB | 4.6 MB (one PNG) |
| Why using AI requires us to be even better | 3.5 MB | 3.3 MB (one PNG) |
| Anthropic's Claude Code Leak | 3.0 MB | 2.8 MB (one PNG) |
| The Extended Color Wheel by Itten | 2.9 MB | 2.6 MB, of which a 1.9 MB GIF |
| Neural-based Outlier Discovery | 2.5 MB | 2.3 MB, of which two SVGs of 590 and 393 KB |
| The Identity Crisis of Software Engineers | 2.4 MB | 2.2 MB (one PNG) |
| Digital Art & the Knight's Tour Problem | 2.2 MB | 2.0 MB |
| A page without pictures, for comparison | about 245 KB | 22 KB (navbar icons, favicon) |

The largest files:

| File | Size | Pixels |
| --- | --- | --- |
| `img/deutsche-bahn/DSC_8839.JPG` | 6.25 MB | 4928×3264 |
| `img/posts/2026-04-21-taste.png` | 4.6 MB | 2644×1600 |
| `img/posts/2026-03-26-autopilot.png` | 3.3 MB | 1536×1024 |
| `img/posts/2026-04-09-claude-code-leak.png` | 2.8 MB | 1024×1024 |
| `img/posts/2026-04-14-identity-crisis.png` | 2.2 MB | 1536×1024 |
| `img/color-wheel/animation.gif` | 1.9 MB | 1000×998 |
| `img/einbuergerung.jpg` | 684 KB | 2016×1512 |
| `img/color-wheel/farbkreis_extended.png` | 385 KB | 3900×3900 |

Posts display images at most 720 px wide (600 px for the header images). The four PNGs are
[open item 1](2026-11-20-open-items.md#1-large-images-slow-down-post-pages). The photo, the GIF and the
SVGs were not listed there.

Suggestions:

- Re-export photos and the PNG illustrations as JPEG or WebP, about 1440 px wide (twice the column
  width), usually 100–300 KB each. macOS can do it without extra software:
  `sips -Z 1440 -s format jpeg -s formatOptions 80 in.png --out out.jpg`.
- Turn the GIF into a looping video (`<video autoplay loop muted playsinline>`), usually a tenth of
  the size.
- Run the two SVGs through an optimizer such as SVGO, or export them as PNG.
- Give every `<img>` its `width` and `height` (none has them today), so that the page does not jump
  while images load. Add `loading="lazy"` to images below the first screen (none has it today).

### P2. MathJax on every page

MathJax 2.7.9 is loaded on all 27 pages, but only two posts contain math (concept drift, knight's
tour). It is `async`, so it does not block rendering. Still, every page downloads at least 90 KB
compressed (two files, 310 KB of JavaScript), and MathJax then scans the page. On a page without
pictures, which transfers about 195 KB in total (estimated from the measured file sizes), that is
almost half.

Suggestion: set `math: true` in the front matter of the two posts, and wrap the script in `head.html`
in `{% if page.math %}…{% endif %}`. Check both posts visually afterwards.

### P3. Render-blocking scripts and styles

- **jQuery** (30 KB, Google's CDN) and **Bootstrap JS** (11 KB) are synchronous scripts in `<head>`.
  The browser stops building the page until both have loaded. Their only job is the toggle of the
  navbar on phones. In order of increasing change: add `defer` to both (keeps their order),
  self-host jQuery (removes the Google request, [L2](#l2-the-privacy-notice-does-not-describe-the-site)),
  or replace both with about ten lines of plain JavaScript for the toggle.
- **Six stylesheets** (29 KB compressed) load before anything is shown. One of them,
  `css_gallery/galleriffic-2.css`, styles a gallery that no page uses. `css/bootstrap.css` is the
  unminified file because it carries local changes ([C2](#c2-cssbootstrapcss-is-a-modified-bootstrap-311)).
- **The footer writes the year with `document.write`**, an inline script that blocks parsing.
  `{{ site.time | date: '%Y' }}` gives the build year without JavaScript.

### P4. Comments in the HTML

HTML comments make up 6–35% of each page, and 84% of the CV page. They include the old Google
Analytics snippet, old navbar entries and the PayPal form (Liquid still renders the commented-out
include into every page). Compressed, that is a few KB per page, except on the CV page. The bigger cost
is maintenance. Liquid's `{% comment %}…{% endcomment %}` keeps notes out of the published HTML, and
deleted code stays available in git history.

## 4. Accessibility

[axe-core](https://github.com/dequelabs/axe-core) 4.14.1 checked every page against WCAG 2.0–2.2 A/AA
and best practices, in WebKit at 1280 px and 375 px. The results were the same at both widths, except
where noted:

| Rule | Impact | Where | Count |
| --- | --- | --- | --- |
| `link-in-text-block` | serious | all 27 pages | 258 links |
| `list` | serious | all pages, desktop | the navbar |
| `target-size` | serious | all pages | 2 footer links per page |
| `color-contrast` | serious | 4 posts and Publications | 35 elements |
| `object-alt` | serious | CV, Simple Workout Exercises | 2 |
| `frame-title` | serious | Book Me | 1 |
| `link-name` | serious | CV | 1 |
| `scrollable-region-focusable` | serious | Citation Policy, phone | 1 |
| `region` | moderate | all pages | 63 |
| `landmark-one-main`, `empty-heading` | moderate, minor | 404 | 1 each |
| `aria-allowed-role`, `aria-deprecated-role` | minor | 5 posts with footnotes | generated by kramdown |

Automated tools find only part of the problems. No screen reader or keyboard walkthrough was done.

### A1. Links are told apart by colour only

[`css/customstyle.css`](../css/customstyle.css) removes the underline from all links. In running
text, the link colour (#005e86) and the text colour (#333) have a contrast of only 1.77:1. WCAG asks
for 3:1 plus a second cue, which in practice means an underline. Suggestion: underline links inside
`.entry`, `.content-paragraph` and `.information-line`, and leave the navbar and footer as they are.
`text-underline-offset` and a thinner `text-decoration-thickness` keep it discreet.

### A2. Contrast

- **Code blocks** use Monokai colours on #272822. Comments (#75715e) reach 3.02:1 and keywords
  (#f92672) 3.92:1, where 4.5:1 is required. For example, #a6a28c for comments gives 5.8:1, and #ff6188
  for keywords 5.2:1. The rules are in [`css/syntax.css`](../css/syntax.css). Check the other token
  colours too.
- **"Best Paper Award!"** on the Publications page is pure red (#ff0000) on white, 3.99:1. #c00000
  gives 6.5:1.

### A3. Structure and semantics

- **Duplicate IDs.** The four navbar icons share `id="icon-container"` on every page, and the section
  headings of About, Services and Impressum all use `id="sec0"` (3, 4 and 7 times). The CSS uses the
  ID, so turn it into a class.
- **Lists.** The navbar's right-hand `<ul>` contains `<a>` elements directly, without `<li>`. About and
  Citation Policy put a `<ul>` inside a `<p>`, so the browser closes the paragraph before the list and
  adds an empty one after it.
- **Headings.** The blog index has 18 `<h1>`, one per post title. One `<h1>` for the page and `<h2>`
  for the posts is the usual structure. Book Me has no heading at all, Citation Policy starts at `<h2>`,
  and the 404 page closes its `<h1>` with `<h1>`, which creates a second, empty heading.
- **Landmarks.** There is no `<main>`, the navbar is a `<div role="navigation">` and the footer a
  `<div>`. Use `<main>`, `<nav>` and `<footer>`, but first remove the dead `nav` and `footer` rules
  from `css/style.css` ([C1](#c1-cssstylecss-is-uncompiled-sass)). Otherwise `nav { float: right; … }`
  suddenly applies to the navbar.
- **Language.** The Impressum is mostly German, but the page declares `lang="en"`. Mark the German
  sections with `lang="de"` so that screen readers pronounce them correctly.

### A4. Images

- 19 post images have the alt text "img": 6 in the Knight's Tour post, 5 in the Color Wheel post, 2 in
  the citizenship post, and one each in six others (im2txt, RPi, and the four 2026 posts with header
  images). Only the author can describe them. Purely decorative images should get `alt=""`.
- About: "Profil picture" ([B5](#b5-visible-typos-and-copy-errors)) and the email image
  ([L5](#l5-contact-details-three-versions-one-of-them-only-as-an-image)).

### A5. Embedded content

- The Book Me iframe has no `title`. The `<object>` elements on the CV page and in "Simple Workout
  Exercises for Confinement" have no accessible name ([B2](#b2-cv-page)).
- On phones, the BibLaTeX example on Citation Policy scrolls horizontally but cannot be reached with
  the keyboard. `tabindex="0"` on the `<pre>` fixes it.

### A6. Small touch targets in the footer

The Impressum and Citation Policy links are single lines of 15 px text separated only by `<br>`. More
line height or padding fixes it.

### A7. The main font is missing on most devices

All text uses Cambria (`font-family: 'Cambria'`) with no fallback. Cambria comes with Windows and
Microsoft Office only, so visitors on Mac, iPhone, Android and Linux see their browser's default font
instead. In this audit's WebKit that was Times. The site therefore looks different on almost every
platform, and the screenshots taken during maintenance show the fallback, not Cambria.

Suggestion: a font stack such as `Cambria, Georgia, "Times New Roman", serif`. Georgia is close to
Cambria and installed on Apple devices, so the look changes there. The other option is a self-hosted
web font. This is a design decision, so compare screenshots.

## 5. Search and discoverability

### S1. The home page does not say whose site it is

The navbar brand reads "Blog", and the home page starts directly with the latest post. The owner's
name appears only in the browser tab, in the footer and on About. Someone arriving from a search or a
shared link does not see who writes here. Suggestion: use "Edouard Fouché" as the navbar brand, and
add a one-line introduction with a link to About at the top of the index. That also gives the index its
`<h1>` ([A3](#a3-structure-and-semantics)).

### S2. Redirect chains still go through http://

Measured today:

| Request | Hops |
| --- | --- |
| `https://www.edouardfouche.com/` → `http://edouardfouche.com/` → `https://edouardfouche.com/` | 2 |
| `http://www.edouardfouche.com/` | 3 |
| `https://edouardfouche.com/about` → `http://edouardfouche.com/about/` → `https://…/about/` | 2 |

GitHub still builds its redirects with `http://`, so Cloudflare still reaches GitHub over plain HTTP
(SSL/TLS mode "Flexible"). `CLAUDE.md` names "Full" as the intended mode, but the switch has not
happened yet. Step-by-step instructions:
[SEO follow-up, section 3](2026-11-20-seo-follow-up.md#3-how-to-fix-the-redirect-chains-in-cloudflare).

### S3. Search engine registration

No verification token is visible: no `google-site-verification` TXT record on the domain, and no
verification meta tag or file. The sitemap has therefore probably not been submitted yet. Instructions:
[SEO follow-up, section 2](2026-11-20-seo-follow-up.md#2-how-to-submit-the-sitemap).

### S4. Share images and descriptions of posts

- Only the newest post sets `image:`. The four 2026 posts with header images still show the default
  portrait in link previews. Set `image:` once the images are smaller ([P1](#p1-images)).
- Meta descriptions come from the excerpts. 11 posts have descriptions over 300 characters (search
  results show about 155), and "Almost 30" has only "I am almost 30…". A `description:` in the front
  matter fixes the important ones.
- The Knight's Tour title is written with `&amp;` in its front matter. The JSON-LD headline is not
  HTML, so it literally reads "Digital Art &amp; the Knight’s Tour Problem". Write a plain `&` in the
  YAML.

### S5. Scholarly profiles are not linked

The Google Scholar profile exists (it was the source of the
[publications sync](2026-11-21-publications-scholar-sync.md)), and the CV PDF links it, but no page of
the site does. The same goes for ORCID and DBLP, if those profiles exist. Link them from About and
Publications, and add them to `social.links` in [`_config.yml`](../_config.yml), which jekyll-seo-tag
emits as `sameAs`.

### S6. Feed items use relative URLs

[`feed.xml`](../feed.xml) embeds the full HTML of each post, and its images and links start with `/`
(for example `/img/posts/…`). RSS has no base URL, so some feed readers show broken images, and the
W3C feed validator warns about it. In `feed.xml`, add `replace: 'src="/', 'src="https://edouardfouche.com/'`
and the same for `href="/` before `xml_escape`. Optionally, add `<language>en</language>`.

### S7. Sitemap dates of the PDFs are the build time

All 37 PDFs in `sitemap.xml` carry the time of the last deploy as `lastmod`, because GitHub checks
the files out afresh for each build. A 2018 paper therefore looks as if it changed today, and search
engines learn to ignore the dates. This is low priority. jekyll-sitemap cannot read dates from git, so
either accept it, or exclude the PDFs with a front matter default `sitemap: false` (shown in
jekyll-sitemap's README) and lose their sitemap entries.

### S8. PDF titles

Search engines and browser tabs show a PDF's embedded title. Some publication files carry template
leftovers:

| File | Embedded title (author) |
| --- | --- |
| `POSTER_SARAF_KDD26.pdf` | "Repulsion Loss: Detecting Pedestrians…" ("Name") |
| `SLIDES_SARAF_KDD26.pdf` | "PowerPoint Presentation" ("Design and Publications") |
| `SLIDES_DEAL_PAKDD24.pdf` | "KIT_GRK_Legende" |
| `komiyama_gnsbandit.pdf` | "PowerPoint プレゼンテーション" |
| `SLIDES_PLASTIC_ECML24.pdf` | "Leveraging Plasticisty…" (typo) |

10 more PDFs have no title. Setting them takes a minute each, for example with exiftool or when
exporting.

### S9. Smaller points

- The `google: notranslate` meta tag and the indexable Impressum are still open owner decisions from
  the [SEO record](2026-11-20-seo.md#what-could-still-be-done) (items 13 and 14).
- 5 post titles are longer than 60 characters, so search results cut them. That is acceptable.

## 6. Security and transport

### T1. No security headers

Neither GitHub Pages nor Cloudflare adds any: there is no `Strict-Transport-Security`,
`X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `X-Frame-Options` or
`Content-Security-Policy`. For a static site the risk is small, but Cloudflare adds them for free:

- **HSTS:** SSL/TLS → Edge Certificates → HTTP Strict Transport Security. Start with a short `max-age`
  (one day), then raise it to 6–12 months once everything works. Add `includeSubDomains` or preload
  only after checking every subdomain.
- **Other headers:** Rules → Transform Rules → modify response headers, for example
  `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` and
  `X-Frame-Options: SAMEORIGIN`.
- **CSP:** possible, but it has to allow MathJax, jQuery, Simple Analytics, giscus, Google Forms and the
  inline `document.write`. Start with `Content-Security-Policy-Report-Only`, or wait until the third
  parties are reduced ([L2](#l2-the-privacy-notice-does-not-describe-the-site)).

### T2. TLS 1.0 and 1.1 are accepted

`openssl s_client` completes handshakes with TLS 1.0 and 1.1, Cloudflare's default minimum. Both
versions are deprecated (RFC 8996). Set SSL/TLS → Edge Certificates → Minimum TLS Version to TLS 1.2.
TLS 1.3 is already offered.

### T3. The Dependabot alert is still open

The high-severity rubyzip alert (path traversal, in `Gemfile.lock`) is still open. The
[SEO record](2026-11-20-seo.md#observed-during-the-deploy-not-seo) explains why it does not affect the
site and why it cannot be fixed within the GitHub Pages gem set. Dismissing it as "vulnerable code is
not actually used" keeps the alert list meaningful.

## 7. Code health and maintainability

### C1. `css/style.css` is uncompiled Sass

[`css/style.css`](../css/style.css) is a Sass file served as plain CSS. It uses Sass variables
(`$white`, `$gray`, `$blue`…), `@include mobile { … }`, nesting, `//` comments and a trailing
`@import "_highlights";`. Browsers drop what they cannot parse:

- **Every declaration with a `$variable`**, for example the colours of headings, dates and links, and
  `font: 16px/1.4 $helvetica`.
- **Five whole rules** whose selector starts with a `//` comment: `.posts > .post` (the separator lines
  between posts that the index was meant to have), `table { overflow: auto; … }` (would let wide tables
  scroll on phones; no post has a table yet), `.clearfix`, `::-moz-selection` and `.wrapper-masthead`.
- **The `@include mobile` blocks**, including `line-height: 1.4` for headings on phones. That is why
  titles that wrap look loosely spaced on phones (they keep the line height 1.7).
- **Nested rules** (`h1 { a { … } }`, `.post { blockquote { … } .read-more { … } }`) work only in
  browsers with native CSS nesting, released from 2023 on. The dark post titles and the upper-case
  "READ MORE" on the index depend on it. In older browsers the titles are link-blue and "Read More" is
  in mixed case.

[`_sass/_variables.scss`](../_sass/_variables.scss) holds the values the variables were meant to have.

Suggestion: rewrite `style.css` as plain CSS that reproduces what current browsers show. Flatten the
nested rules, and delete the dropped declarations and the rules that match nothing (masthead,
site-avatar, `nav`, `footer`, `.wrapper-footer`, …). Verify with the screenshot comparison. Then decide
separately whether to add the rules that were meant but never applied (post separators, mobile heading
line height, scrolling tables), since each is a visible change.

### C2. `css/bootstrap.css` is a modified Bootstrap 3.1.1

A rule-by-rule comparison with the stock 3.1.1 file from cdnjs finds these local changes, made in 2019
(`209cec6`, `7bf6376`):

| Rule | Stock 3.1.1 | Local | Effect |
| --- | --- | --- | --- |
| `a` color | #428bca | #005e86 | The site's link colour |
| `pre` background, border radius | #f5f5f5, 4px | #272822, 10px | The dark code blocks that `css/syntax.css`'s colours need |
| `.navbar-nav > li > a` padding-top | 10px | 20px | Spacing of the items in the phone menu |
| `.navbar-default …` transition and brand hover colour, `.btn` user-select | | | None (the site uses `navbar-inverse` and no `.btn`) |

`css/bootstrap-theme.css` is unmodified. The repository's `css/bootstrap.min.css` is the stock file
without these changes, so switching the `<link>` to it would silently change the link and code colours.
Before any switch or upgrade ([open item 3](2026-11-20-open-items.md#3-bootstrap-css-is-still-311)),
move the first three rules into `css/customstyle.css`.

### C3. Dead code

- [`_layouts/cv.html`](../_layouts/cv.html): about 1,440 of 1,513 lines are commented out
  ([B2](#b2-cv-page)).
- [`_includes/head.html`](../_includes/head.html): the old Google Analytics snippet, and the gallery
  stylesheet ([P3](#p3-render-blocking-scripts-and-styles)).
- [`_includes/navbar.html`](../_includes/navbar.html): commented-out Facebook, Twitter, Xing,
  Projects and Contact entries, and the PayPal include, which still renders inside a comment on every
  page.
- [`_includes/donations-paypal.html`](../_includes/donations-paypal.html) and the `donations` block in
  `_config.yml`, unused while the button is hidden.
- [`css/customstyle.css`](../css/customstyle.css): rules for the old CV, gallery, sidebar, tag cloud,
  IBM logo, `#custom-button` and `.featurette-heading`, and a broken `@media @media …` block at the end.
- The placeholder bodies of the stub pages. `about.md` includes minima's `icon-github.html`, which
  makes the build depend on the theme (see [C4](#c4-unused-files-on-the-live-site)).

### C4. Unused files on the live site

- **Images.** 94 of the 160 files in `img/` (30 of 79 MB) are referenced by no page or stylesheet.
  Clear junk among them: four Windows thumbnail caches (`img/Thumbs.db`, `img/gallery/Thumbs.db`,
  `img/Thumbs.db_encryptable`, `css_gallery/Thumbs.db`), Photoshop and GIMP sources
  (`img/skills_5-5_5_200x50.psd`, `img/btn_donate_LG_coffee.psd`, `img/build-logs/weight_rack.xcf`),
  `img/test.png`, and a 5001×5001 `img/Instagram_icon.png` (1.3 MB). There are also old profile
  pictures, the gallery images and unused logos. The individual press-package photos are probably meant
  as downloads, so keep them.
- **CSS and JavaScript.** `css/basic.css`, `css/carousel.css`, `css/galleriffic-2.css` (a second copy),
  `css/syntax_default.css`, `css/bootstrap.min.css`, `css/bootstrap-theme.min.css`, the gallery GIFs in
  `css/`, the unminified `js/bootstrap.js`, `js_gallery/`, `js_timeliner/` and `css_gallery/`.
- **Theme assets.** `theme: minima` publishes `/assets/main.css` and `/assets/minima-social-icons.svg`.
  A scratch build showed that the theme cannot simply be removed. Without the theme line, the build
  fails, because the `about.md` placeholder body uses a minima include. With that body removed too, the
  build works, but the `github-pages` gem falls back to its default theme, `jekyll-theme-primer`, which
  publishes `/assets/css/style.css` instead. Keep the theme, and delete the placeholder bodies so that
  nothing depends on it.

Deleting a file removes its public URL. The repository (149 MB packed) keeps it in its history.

### C5. Outdated or invalid markup

- Posts use an XHTML 1.0 Strict doctype ([`_layouts/default.html`](../_layouts/default.html)), all
  other pages `<!doctype html>`.
- `<meta http-equiv="Content-Language">` is obsolete (the `lang` attribute does this), and
  `X-UA-Compatible` only ever mattered for Internet Explorer.
- `<img padding=10%>` on Services (there is no such attribute), and the iframe attributes on Book Me
  ([B3](#b3-book-me)).
- `comments: true` in [`_layouts/post.html`](../_layouts/post.html) and in every post has no effect,
  because giscus is included unconditionally.
- Footer: `http://` links to Bootstrap and the license (Cloudflare rewrites them), and the hotlinked
  license badge, which now redirects to `licensebuttons.net` (self-host it).

### C6. Leftovers in `_config.yml`

`enforce_ssl` (no plugin reads it), `twitter_username` (jekyll-seo-tag reads `twitter.username`, so
nothing is emitted, which is the intended state), `donations` ([C3](#c3-dead-code)), commented-out
build settings, and Jekyll's generic welcome comments.

### C7. Post files

- Five posts have a different date in the filename than in the front matter, which wins: Hello World
  (`2016-11-05` and `2016-03-05`), Data Stream Generation with Concept Drift (May 9 and May 19), the
  Knight's Tour (May 9 and May 11), arXiv and the Information Explosion (Nov 19 and Nov 18) and Almost
  30 (July 6 and July 21). Align them, whichever date is right. Changing only the date part of a
  filename does not change the URL or the giscus thread.
- One post uses the extension `.md`, all others `.markdown`.
- `categories: Machine Learning` and `categories: Project RPi` are split at the space into two
  categories each. Use `categories: [Machine Learning]`. Categories only appear in the feed today.

### C8. Repository documentation

- The TODO list in [`README.md`](../README.md) is stale. For example, the Book Me section exists.
- [`CLAUDE.md`](../CLAUDE.md) says that Cloudflare prepends its managed comment block to `robots.txt`.
  The live `robots.txt` now contains only the `Sitemap:` line.
- `.vscode/settings.json` holds Python settings that do not apply to this repository
  ([open item 5](2026-11-20-open-items.md#5-dead-code-and-leftovers)).

### C9. Typography on phones

Headings are hyphenated on phones ("Confine-ment", "Engi-neers"), because `hyphens: auto` applies to
the whole body. `h1, h2, h3 { hyphens: manual; }` prevents it. Together with the lost mobile line
height ([C1](#c1-cssstylecss-is-uncompiled-sass)), titles that wrap look loose on phones.

## 8. Ideas (optional, not defects)

- **Home page:** a short introduction with the portrait, the main topics, and a few "start here" posts.
- **Archive:** a page by year or by category, and category links under each post. The categories
  exist in the front matter but are not shown anywhere.
- **Services:** concrete outcomes, a few testimonials or past talks, how a first call works, and an
  email alternative to the form.
- **Publications:** highlight the owner's name in the author lists instead of bolding every author.
  Add BibTeX per entry (or one `.bib` file) and DOIs.
- **Posts:** an author line linking to About, the reading time, and related posts.
- **Dark mode** with `prefers-color-scheme`.
- **Icons:** an Apple touch icon and an SVG favicon. The favicon is a 15 KB 32×32 PNG, and
  `/favicon.ico` returns 404, which some feed readers and services request.
- **Re-runnable checks:** keep the audit scripts (section 11) in a repository-only `tools/` folder,
  excluded from the site, so they can run before deploys.

## 9. Status of earlier open items

| Source | Item | Status on 2026-11-21 |
| --- | --- | --- |
| [Open items](2026-11-20-open-items.md) | 1. Large images | Open, and larger than listed ([P1](#p1-images)) |
| | 2. RSS feed announced twice | Resolved (`cf8246a`) |
| | 3. Bootstrap CSS 3.1.1 | Open. New: the local copy has three effective customizations ([C2](#c2-cssbootstrapcss-is-a-modified-bootstrap-311)) |
| | 4. MathJax 2 end of life | Open. New: loaded on all 27 pages ([P2](#p2-mathjax-on-every-page)) |
| | 5. Dead code and leftovers | Open (the drafts part is resolved), quantified in [C3](#c3-dead-code) and [C4](#c4-unused-files-on-the-live-site) |
| | 6. Dependabot and the `github-pages` gem | The rubyzip alert is still open ([T3](#t3-the-dependabot-alert-is-still-open)) |
| [SEO](2026-11-20-seo.md#what-could-still-be-done) | 1. Register with search engines | Probably not done ([S3](#s3-search-engine-registration)) |
| | 2. Fix the redirect chains | Open ([S2](#s2-redirect-chains-still-go-through-http)) |
| | 3. Lighter images | Open ([P1](#p1-images)) |
| | 4. A share image per post | Done for the newest post only ([S4](#s4-share-images-and-descriptions-of-posts)) |
| | 5. Alt text for post images | Open, 19 images ([A4](#a4-images)) |
| | 6. Weak excerpts as descriptions | Open ([S4](#s4-share-images-and-descriptions-of-posts)) |
| | 7. Scholarly profiles | Open ([S5](#s5-scholarly-profiles-are-not-linked)) |
| | 8. Per-paper pages for Google Scholar | Not needed: Scholar already lists the papers ([publications sync](2026-11-21-publications-scholar-sync.md)) |
| | 9. Defer jQuery and Bootstrap JS | Open ([P3](#p3-render-blocking-scripts-and-styles)) |
| | 10. Heading structure | Open ([A3](#a3-structure-and-semantics)) |
| | 11. Doctype | Open ([C5](#c5-outdated-or-invalid-markup)) |
| | 12. `copyright` meta vs. license | Open, and a third conflicting statement was found ([L3](#l3-three-license-statements-contradict-each-other)) |
| | 13. `google: notranslate` | Open, owner's decision |
| | 14. Impressum in search results | Open, owner's decision |
| | 15. Twitter card attribution | Not applicable while the account is unused |
| | 16. Duplicate poster | Done (`45b07cc`) |
| [Publications sync](2026-11-21-publications-scholar-sync.md#not-changed-open-items) | Scholar profile clean-up, missing supplementary material | Open, owner and co-authors |

## 10. What is already good

- HTTPS everywhere: a valid certificate (Google Trust Services through Cloudflare, valid until
  February 2027 and renewed automatically), TLS 1.3, HTTP/3 offered, and `http://` redirects to
  `https://` in one hop.
- Compression (Brotli for HTML, gzip for CSS) and sensible caching (10 minutes for HTML, 4 hours for
  static files).
- No mixed content, and every internal link and resource exists in the build.
- Search metadata on every page (jekyll-seo-tag): title, description, canonical URL, Open Graph and
  JSON-LD. Also a sitemap and `robots.txt`, and a 404 page that returns status 404 and is excluded from
  indexing.
- Both CDN scripts carry integrity hashes, and jQuery 3.7.1 and Bootstrap JS 3.4.1 are the last
  releases of their lines.
- The site's own responses set no cookies, and the analytics are cookieless.
- No page is wider than the screen at 375 px, and posts share a centered reading column.
- The RSS feed is well-formed, with full content for the last 10 posts.
- The toolchain is pinned, so a local build reproduces production, and the maintenance history is
  documented in `docs/`.
- The email domain publishes SPF and DMARC (`p=quarantine`).
- Every file linked from the Publications page exists, and the list matches Google Scholar.

## 11. How the audit was done

Nothing was changed in the repository or on the live site. All tools ran outside the repository, and
the scripts were not kept.

- **Build:** `bundle exec jekyll build` with the pinned toolchain (`github-pages` 232), with no warnings.
  The GitHub Pages API confirmed that `abae645` is the last production build. The live HTML of 5 pages
  matched the build except for Cloudflare's rewrites (`http://` links, email obfuscation).
- **Static checks** (Python with html5lib, BeautifulSoup, Pillow, pypdf and tinycss2, in a temporary
  virtualenv):
  - parse errors, duplicate IDs, headings, alt texts, links, third-party resources, the share of
    comments in the HTML, and metadata, on all 27 built pages;
  - an inventory of all images with dimensions and EXIF data, and the metadata of all PDFs;
  - a rule-by-rule comparison of the CSS with the stock Bootstrap 3.1.1 files from cdnjs, and a parse
    of `css/style.css` to list the rules browsers drop.
- **Rendering:** a small Swift program around `WKWebView` (WebKit, the engine of Safari) loaded every
  page from a local web server at 1280 px and 375 px widths. On each page it ran
  [axe-core](https://github.com/dequelabs/axe-core) 4.14.1 (from cdnjs, integrity hash checked), and it
  measured overflow, fonts, link styles and code block colours. Simple Analytics, giscus and Google
  Forms were blocked during the run, so no page views were recorded. Full-page screenshots were reviewed
  by eye.
- **Network:**
  - curl: response headers, redirects, compression, caching, and all 124 external links (`HEAD`, then a
    ranged `GET` on failure);
  - `openssl s_client`: TLS versions and the certificate;
  - `dig`: DNS records;
  - GitHub API: Pages settings, latest build, Dependabot alerts;
  - archive.org availability API and Crossref: replacements for dead links.
- **Experiments:** two builds of a scratch copy of the repository, to see what happens without
  `theme: minima` ([C4](#c4-unused-files-on-the-live-site)).
- **Legal references:** checked against current chamber of commerce and law firm publications about the
  DDG (in force since 14 May 2024) and the MStV (since 7 November 2020).

## 12. Not covered

- Other browsers and real phones. Rendering was checked in WebKit only, and Android's handling of the
  embedded CV is known browser behaviour, not tested.
- Field data on loading speed (Core Web Vitals). The site's URL was not sent to third-party testing
  services.
- A screen reader or keyboard-only walkthrough. Automated checks find only part of the accessibility
  problems.
- Proofreading of the posts. Only errors noticed in the templates and while checking links are listed.
- The Cloudflare and Google Search Console dashboards. Their settings were inferred from HTTP
  responses and DNS.
- Legal advice. Section 1 lists observations to take to a generator or a lawyer.
