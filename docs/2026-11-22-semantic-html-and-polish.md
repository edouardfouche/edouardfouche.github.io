# Semantic HTML, share images, PDF titles and polish

**Date:** 2026-11-22 (night, started on 2026-11-21)
**Context:** the owner went to bed and asked for everything meaningful to be done overnight, to review in
the morning. This record covers the work after [alt texts, dead CSS and the font](2026-11-21-dead-css-alt-texts-font.md).
Anything that needs the owner's voice or a decision was left as a proposal (see [below](#left-for-the-owner)).
Every commit can be undone on its own with `git revert <commit>`.

## Changes, one commit each

| Commit | Change | Audit item | Visible? |
| --- | --- | --- | --- |
| `9a7ec21` | Semantic HTML: landmarks, one `<h1>` per page, no duplicate IDs, valid markup, no HTML comments shipped | A3, C3, C5 | Only the 404 page (fixed heading) |
| `51188b3` | Stub pages without placeholder bodies; dead `_config.yml` settings removed | C3, C6 | No (identical build output) |
| `e0fb7b4` | Share images for the four illustrated posts; descriptions for "Hello World" and "Almost 30" | S4 | Link previews and search snippets only |
| `062abd6` | Five wrong PDF titles fixed | S8 | Browser tabs and search results only |
| `0883bfc` | Copy fixes (Services, Publications); no hyphenation inside titles | B5, C9 | **Yes**, small |
| `7059731` | Footnotes: the ARIA roles axe flags are removed | A3 | No |
| `b9c9b5a` | **Not merged:** name in the navbar and an introduction on the home page (branch `proposal/home-intro`) | S1 | Would be |

### Semantic HTML (`9a7ec21`)

- **Landmarks:**
  - `_includes/navbar.html` uses `<nav aria-label="Main">`, and `_includes/footer.html` a `<footer>`.
  - Each layout wraps its content in one `<main>`. A script inserted it in the seven page layouts at the
    right `<div>` depth; the blog index, the posts and the 404 page were done by hand.
- **Headings:**
  - The blog index had 18 `<h1>`. It now has one, visually hidden (`.sr-only`) until the home page gets a
    visible introduction. Post titles there are `<h2 class="post-title">`, with the size and colour of the
    old `<h1>` titles (rules in `css/customstyle.css`).
  - The 404 page closed its `<h1>` with `<h1>`. Fixed, and "Oops !" became "Oops!".
  - Every page now has exactly one `<h1>` and no skipped levels.
- **IDs:** the navbar icons shared `id="icon-container"` (now a class), and unused `id="sec0"` anchors
  were repeated on About, Services and others. No duplicate ID is left.
- **Markup:**
  - The profile icons were `<a>` directly inside a `<ul>`; the group is now a `<div>` with the same
    classes.
  - The menu button names the menu it controls (`aria-controls`, `aria-expanded`).
  - Post pages use the HTML5 doctype.
  - Obsolete `Content-Language` and `X-UA-Compatible` meta tags are gone, and so is the invalid `padding`
    attribute on the Services logo.
  - The Citation Policy closes all its `<div>`s.
- **Comments:** the HTML comments sent with every page are gone or became Liquid comments: the old Google
  Analytics snippet, disabled navbar entries, layout notes. Two of the owner's notes are kept as Liquid
  comments: an earlier Services tagline and three ACM Author-izer links. Comments are now under 1% of any
  page's HTML (up to 84% before the audit).

### Stubs and `_config.yml` (`51188b3`)

The stub pages contained placeholder text that is never rendered. `about.md`'s even included minima's
`icon-github.html`, which tied the build to the theme. They now hold only front matter.

`_config.yml` lost:
- the Jekyll welcome boilerplate;
- the unused `enforce_ssl`;
- commented-out duplicates of the markdown, highlighter, kramdown and feed settings;
- the old Disqus and Google Analytics notes (history is in `docs/` and git).

Short comments explain the settings that are not obvious. A build with the old files and one with the new
files are identical (`diff -r` finds nothing).

### Share images and descriptions (`e0fb7b4`)

- `image:` in the front matter of the 2026 posts on autopilot, the Claude Code leak, the identity crisis
  and taste. Link previews now show their header illustration instead of the default portrait.
- `description:` for the two posts whose excerpts made poor search snippets. Both are sentences from the
  posts themselves:
  - **Hello World:** "In this blog, I will speak about my work as a scientist, but also about art, culture
    and all the things I like."
  - **Almost 30:** "I am almost 30... I am much happier than when I was almost 20. I am more open-minded,
    tolerant, aware of my body."

### PDF titles (`062abd6`)

Search engines and browser tabs show a PDF's embedded title. Five files carried template leftovers.

| File | Before | After |
| --- | --- | --- |
| `POSTER_SARAF_KDD26.pdf` | "Repulsion Loss: Detecting Pedestrians in a Crowd" (author "Name") | "Stationarity-Aware Retrieval-Augmented Time Series Forecasting (poster)" |
| `SLIDES_SARAF_KDD26.pdf` | "PowerPoint Presentation" | "… (slides)", same paper |
| `SLIDES_DEAL_PAKDD24.pdf` | "KIT_GRK_Legende" | "DEAL: Data-Efficient Active Learning for Regression Under Drift (slides)" |
| `komiyama_gnsbandit.pdf` | "PowerPoint プレゼンテーション" | "Finite-time Analysis of Globally Nonstationary Multi-Armed Bandits (slides)" |
| `SLIDES_PLASTIC_ECML24.pdf` | "Leveraging Plasticisty …" | "Leveraging Plasticity in Incremental Decision Trees (slides)" |

Title and authors come from the matching entry on the Publications page. Each file was changed by an
incremental update (pypdf): the original bytes stay, and about 1 KB is appended. Page counts and
first-page text are unchanged, and all five render (macOS Quick Look).

Ten PDFs have no title at all. They were left alone, because Google falls back to their first line, and
every rewritten PDF adds a full copy to the git history.

### Copy and typography (`0883bfc`)

- Services: `Why "Tengu''?` became `Why “Tengu”?`, and "3 to 6-month long mentorships" became "3- to
  6-month mentorships".
- Publications: "Github" became "GitHub" in five link texts.
- Headings no longer hyphenate (`hyphens: manual`). On phones, titles broke inside words
  ("Confine-ment", "Engi-neers"). Running text still hyphenates.
- About: the "Miscellaneous" list is no longer inside a `<p>`. The page renders pixel-identically.

### Footnotes (`7059731`)

kramdown puts `role="doc-noteref"` on `<sup>` (not allowed by ARIA) and uses the deprecated roles
`doc-endnotes` and `doc-endnote`. `_layouts/post.html` removes these three roles. The 36 footnote links
and their valid `doc-backlink` roles stay.

## Verification

All renderings: WebKit, 27 pages at 1280 and 375 px from a local server, with analytics and giscus
blocked. The previous build is the baseline each time.

- **Semantic HTML and cleanup:**
  - 51 of 54 screenshots pixel-identical. The other three are the 404 page at both widths (intended), and
    one frame of the animated knight's tour GIF caught one move later.
  - The phone menu opens on all pages, and its screenshots are identical except on the 404 page, where
    "Blog" is no longer highlighted.
- **Copy and typography:** the changed pages were compared and reviewed in screenshots. About is
  pixel-identical.
- **Static checks on the final build:**
  - no missing internal link or resource;
  - no HTML parse error besides html5lib's strictness about `&` in two URLs;
  - no duplicate ID, exactly one `<h1>` per page;
  - no image with a missing or generic alt;
  - third parties: Simple Analytics everywhere, giscus on posts, cdnjs on the two math posts.
- **axe-core 4.14.1 on all 27 pages, at 1280 and 375 px: no violation**, after the footnote fix
  (re-checked on the five posts with footnotes). Before the audit, axe reported 12 kinds of violations,
  including 258 links told apart by colour alone.
- **External links:** 127, of which 117 return 200. The other 10 are bot-protected hosts (Amazon,
  LinkedIn, Redbubble, ACM, OpenReview, Towards Data Science, Wikipedia's rate limit), the same as in the
  audit; none is newly broken.

## The home page proposal (not merged)

Branch `proposal/home-intro`, commit `b9c9b5a`, local only:

- the navbar brand reads "Edouard Fouché", and "Blog" becomes the first menu item;
- the blog index opens with the name as its visible `<h1>` and one sentence: "AI engineer and data
  scientist. I write about how AI is changing software engineering and knowledge work, and why it makes
  human judgment more important, not less. More about me";
- a thin rule separates the introduction from the posts.

The sentence is the About page's own description of the blog, in the first person. To publish it: merge
the branch into `master` (or ask for other wording).

## Left for the owner

- **Wording and decisions:**
  - the home page introduction (above);
  - one public contact address everywhere, and the phone number in the public CV;
  - deleting the remaining unused images (old profile pictures, gallery images, logo originals);
  - the post-file dates that differ from their front matter;
  - what Tengu Consulting's Impressum needs if it is a registered business.
- **Dashboards:**
  - Cloudflare: Full SSL mode, HSTS, minimum TLS 1.2, and a cache purge after this deploy;
  - Google Search Console and Bing: submit the sitemap;
  - the rubyzip Dependabot alert.
- **Noticed, not changed:**
  - at 992 and 768 px, the navbar's inner container sticks out 4–6 px, clipped invisibly (Bootstrap's
    nested containers);
  - the rules the old Sass file intended but browsers never applied (separators between posts on the
    index, a tighter heading line height on phones) would be visible design changes;
  - ten PDFs without an embedded title.
