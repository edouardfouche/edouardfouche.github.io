# Blog post from the LinkedIn post "Knowledge work as we know it is dying"

Work date: 2026-11-21. The LinkedIn post was published on 2026-11-19 (12:34 UTC):
<https://www.linkedin.com/feed/update/urn:li:activity:7529160068785803264/>.

## What was observed

- The logged-out view of the LinkedIn post contains the full text in its JSON-LD (`articleBody`) and
  in `og:description`. Both were identical, and the text was copied from there rather than retyped.
- The post has one attached image: a Tengu Consulting graphic titled "The bottleneck is shifting."
  that shows the same flow as the text (Problem → Human intent → Specification → AI execution →
  Validation → Adoption). LinkedIn serves it publicly only as an 800×533 JPEG (`feedshare-shrink_800`).
  Larger variants return 403, because the URL token is tied to the size.
- The author's own comment on the post links the Stanford AI100 report as a broader, society-level
  version of the same conclusion.
- The previous LinkedIn-derived posts (2026-03-26, 2026-04-14, 2026-04-21) share one pattern: category
  `Technology`, a short teaser before `<!--more-->`, the header image block from `CLAUDE.md`, a few key
  sentences in bold, and a filename that matches the title. The 2026-04-21 post was renamed so that its
  title is the opening hook and the body does not repeat it.

## What was changed

- [`_posts/2026-11-19-Knowledge-work-as-we-know-it-is-dying.markdown`](../_posts/2026-11-19-Knowledge-work-as-we-know-it-is-dying.markdown):
  the new post, URL `/Knowledge-work-as-we-know-it-is-dying/`.
  - The text is the LinkedIn text word for word. The opening line became the title, as in the
    2026-04-21 post, and the next two paragraphs are the excerpt.
  - Formatting added in the usual style: four key phrases in bold, and the flow line bold and centered.
  - A *P.S.* at the end carries the author's comment and the Stanford AI100 link (checked: HTTP 200).
  - Front matter goes slightly beyond the earlier posts, following the open items in
    [SEO, "what is left"](2026-11-20-seo.md):
    - `image:` makes link previews show the post graphic instead of the default portrait (item 4).
    - `description:` is made of two of the author's own sentences (the hook and the conclusion).
      Otherwise the meta description would start with "That sounds dramatic…", which makes no sense
      in search results without the title (item 6).
    - The header image has descriptive alt text that transcribes the graphic's text, instead of
      `img` (item 5).
- [`img/posts/2026-11-19-knowledge-work.jpg`](../img/posts/2026-11-19-knowledge-work.jpg): the 800×533
  JPEG from LinkedIn (62 KB, no EXIF). It is shown at most 600 px wide, so it is adequate, though
  slightly soft on high-density screens. If the original export is available, it can replace this file
  under the same name (see [open item 1](2026-11-20-open-items.md#1-large-images-slow-down-post-pages)
  for target size).

## How it was verified

Local build with `bundle exec jekyll build` (the `github-pages` gem, same versions as production):

- The post renders at `_site/Knowledge-work-as-we-know-it-is-dying/index.html` with the date
  "November 19, 2026". The image paragraph has the same markup as the 2026-04-21 post.
- Head tags: `<title>Knowledge work as we know it is dying | Edouard Fouché</title>`, the
  `description` above, `og:image` pointing to the post graphic, canonical URL
  `https://edouardfouche.com/Knowledge-work-as-we-know-it-is-dying/`, and `datePublished`
  `2026-11-19T00:00:00+01:00`.
- The post is first on the blog index (excerpt shown) and first in `feed.xml`, which still has 10 items.
  It is listed in `sitemap.xml`, and the 2026-04-21 post now links to it as "next".
- giscus maps comments by `pathname`, so the post gets its own discussion on first comment.

## After deploy

Committed as `26effd1` and pushed to `master`. The GitHub Pages build finished about a minute later.
Checked on https://edouardfouche.com:

- `/Knowledge-work-as-we-know-it-is-dying/` returns 200 with the expected `<title>`, `description`,
  `og:image` and the date "November 19, 2026".
- `/img/posts/2026-11-19-knowledge-work.jpg` returns 200 (`image/jpeg`, 63,204 bytes).
- The post is on the blog index and is the first item of `/feed.xml`.
- `/docs/2026-11-21-knowledge-work-post.md` returns 404, so `docs/` is still excluded.
