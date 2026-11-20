# SEO follow-up: duplicate poster, sitemap submission, Cloudflare redirects

**Date:** 2026-11-20
**Follows:** the [SEO record](2026-11-20-seo.md), items 1, 2 and 16 of
[what could still be done](2026-11-20-seo.md#what-could-still-be-done).

Section 1 records a change made in the repository. Sections 2 and 3 are instructions for the owner,
because they happen in the Google, Bing and Cloudflare dashboards, outside the repository. Dashboard
labels are as of November 2026. These services rename menus from time to time, so look for the
equivalent entry if a label differs.

## 1. Duplicate poster removed

Git tracked the same poster twice, under names that differ only in case:
`publications/POSTER_DS32020_SGMRD.pdf` and `publications/Poster_DS32020_SGMRD.pdf` (identical
content, blob `98370d9`). GitHub Pages builds on Linux, where file names are case-sensitive, so it
served both URLs, and both were in the sitemap. `_layouts/publications.html` links only the upper-case
name.

**Change:** `git rm --cached publications/Poster_DS32020_SGMRD.pdf`. The linked file stays.

On macOS (case-insensitive file system), a checkout only ever had one file on disk for both entries,
which is why the local build listed 62 sitemap URLs and production 63. After this change, both list 62.
No other case collisions exist in the repository (`git ls-files | tr 'A-Z' 'a-z' | sort | uniq -d` is
empty). The file on disk was also renamed to the upper-case name, so the working tree matches the
index.

**About the "side effect" in the [draft extensions record](2026-11-20-draft-extensions.md):** that
staged deletion was not caused by git or macOS. It was this removal, staged on purpose by the Claude
Code session doing this SEO work, while a second session was renaming the drafts in the same checkout.
The drafts session saw the change in the shared index, took it for an accident, and unstaged it with
`git restore --staged`. The removal was then redone and committed right away. Lesson: when two sessions share one checkout, stage and
commit in a single step, or work in separate git worktrees.

**Checked again after deploy (same day), by the drafts session:**

- `45b07cc` removed the right copy. HEAD tracks only `POSTER_DS32020_SGMRD.pdf`. That is the name the
  publications page links to, and it matches the `POSTER_<NAME>_<VENUE><YY>.pdf` convention of the
  other posters.
- Live, the upper-case URL returns 200, and the downloaded file hashes to blob `98370d9`. The
  lower-case URL returns 404, and `sitemap.xml` lists 62 URLs, with only the upper-case poster.
- History: the lower-case name is the original. It was added in `df8bc4a` (2021-01-05), and the
  publications page linked it until `2906a65` (2022-08-31) switched the link to the upper-case copy.
  Links saved or shared during those 20 months now get a 404. If that matters, a Cloudflare redirect
  rule (301 from `/publications/Poster_DS32020_SGMRD.pdf` to the upper-case URL) restores them. A
  redirect inside the repository is not possible: a macOS checkout cannot hold both names, and
  `jekyll-redirect-from` writes HTML pages, not PDFs.

## 2. How to submit the sitemap

The sitemap is generated at every build: https://edouardfouche.com/sitemap.xml (62 URLs: the home page,
7 pages, 17 posts and 37 PDFs). `robots.txt` already points to it, so crawlers find it on their own.
Submitting it registers the site with each search engine, speeds up discovery, and gives you reports
on what is indexed and why pages are excluded.

Google and Bing both retired their anonymous "sitemap ping" URLs (Google in 2023), so use their
webmaster tools.

### Google Search Console

1. Open https://search.google.com/search-console and sign in with the Google account that should own
   the site.
2. **Add the property:** in the property menu (top left), choose **Add property**, then the **Domain**
   type, and enter `edouardfouche.com`. Don't add `https://` or `www`. A Domain property covers every
   variant (`http`, `https`, `www`), and only DNS can verify it.
3. **Verify through Cloudflare DNS:** Google shows a TXT record that looks like
   `google-site-verification=…`. If Google offers an automatic flow for Cloudflare, you can use it.
   Otherwise, add the record by hand:
   - Cloudflare dashboard → `edouardfouche.com` → **DNS** → **Records** → **Add record**.
   - **Type** `TXT`, **Name** `@`, **Content**: paste the whole `google-site-verification=…` string,
     **TTL** Auto. Save.
   - Back in Search Console, click **Verify**. On Cloudflare this usually succeeds within a few
     minutes. If not, retry later.
   - **Keep the TXT record.** Google re-checks it, and the property loses verification if it
     disappears.
4. **Submit the sitemap:** in the left menu, **Indexing** → **Sitemaps**. Under **Add a new sitemap**,
   enter `https://edouardfouche.com/sitemap.xml` and click **Submit**. The row should show status
   **Success** and about 62 discovered URLs (it may take a few minutes to fetch).
5. **Afterwards (optional):**
   - **URL Inspection** (search bar at the top): inspect the home page and the latest posts, then
     click **Request indexing**. There is a daily quota, so use it for a handful of important pages.
   - After a few days, **Indexing** → **Pages** lists the indexed pages and the reason for each excluded
     one. Expect `/404.html` under "Excluded by 'noindex' tag"; that is intended.
   - **Enhancements** may list structured data found on the site (the JSON-LD from jekyll-seo-tag). To
     check one page right away, use https://search.google.com/test/rich-results or
     https://validator.schema.org/.

**Alternative without DNS:** a **URL prefix** property (`https://edouardfouche.com/`) can be verified
with an HTML meta tag. jekyll-seo-tag emits it if you add the token to `_config.yml`:
```yaml
webmaster_verifications:
  google: <token from Search Console>
```
It only covers that exact prefix, and it needs a deploy. The Domain property above is preferable.

### Bing Webmaster Tools (also feeds DuckDuckGo, Ecosia and Yahoo)

1. Open https://www.bing.com/webmasters and sign in (Microsoft, Google or Facebook account).
2. **Easiest:** once the Google property is verified, choose **Import** under "Import your sites from
   GSC" and authorize access. Bing copies the verified site and its submitted sitemaps, so there is
   nothing else to do.
3. **Manual alternative:** **Add your site manually** → `https://edouardfouche.com/`, then verify with
   the **CNAME** method. Bing gives a record name (a code) and the target `verify.bing.com`. In
   Cloudflare, add **Type** `CNAME` with that **Name** and **Target**, and set **Proxy status** to
   **DNS only** (grey cloud). A proxied record would hide the CNAME target, and verification would
   fail. Then click **Verify** in Bing, open **Sitemaps** → **Submit sitemap**, and enter
   `https://edouardfouche.com/sitemap.xml`.

## 3. How to fix the redirect chains in Cloudflare

### Diagnosis (measured on 2026-11-20)

| Request | Today | Hops to the final page |
| --- | --- | --- |
| `http://edouardfouche.com/` | Cloudflare → `https://edouardfouche.com/` | 1 |
| `https://www.edouardfouche.com/` | GitHub → `http://edouardfouche.com/` → Cloudflare → `https://…` | 2 |
| `http://www.edouardfouche.com/` | Cloudflare → `https://www…` → GitHub → `http://edouardfouche.com/` → Cloudflare → `https://…` | 3 |
| `https://edouardfouche.com/about` | GitHub → `http://edouardfouche.com/about/` → Cloudflare → `https://…/about/` | 2 |
| `https://edouardfouche.github.io/` | GitHub → `http://edouardfouche.com/` → Cloudflare → `https://…` | 2 |

The `http://` → `https://` redirects come from Cloudflare (**Always Use HTTPS**, no
`x-github-request-id` header). The `www` → apex and trailing-slash redirects come from GitHub Pages
(they carry an `x-github-request-id` header), and they point to `http://`. GitHub builds those URLs
with the scheme it was reached by, so Cloudflare must be reaching GitHub over plain HTTP. That is the
SSL/TLS mode **Flexible**.

To check what the other modes would do, GitHub's servers were queried directly, the way Cloudflare
connects to them (Pages IP `185.199.108.153`):

- **Over HTTP** (what Flexible does): `/about` → `http://edouardfouche.com/about/`, and `www` →
  `http://edouardfouche.com/`. These are the redirects seen today.
- **Over HTTPS** (what **Full** does): the home page is served normally (200, same page). `/about` →
  `https://edouardfouche.com/about/`, and `www` → `https://edouardfouche.com/`.
- **Certificate:** GitHub presents its `*.github.io` certificate, which does not match
  `edouardfouche.com`. The GitHub Pages API confirms it: `https_certificate: null`,
  `https_enforced: false`. **Full (strict)** validates the origin certificate, so it would fail with
  Cloudflare error 526. Use **Full**, which encrypts the connection without checking the name.

### Step 1: set the SSL/TLS mode to Full (this fixes the chains)

1. Cloudflare dashboard → `edouardfouche.com` → **SSL/TLS** → **Overview**.
2. Check the current encryption mode (expected: **Flexible**, or **Automatic SSL/TLS** having chosen
   Flexible). Click **Configure**, choose **Custom SSL/TLS** → **Full**, and **Save**. It takes effect
   within seconds.
3. Leave **SSL/TLS** → **Edge Certificates** → **Always Use HTTPS** **on** (it already is). It handles
   `http://` → `https://` at the edge.
4. Do **not** pick **Full (strict)** (see the certificate finding above).
5. Do **not** enable **Enforce HTTPS** in the GitHub Pages settings. It is unavailable anyway, because
   GitHub has no certificate for the domain. Cloudflare already enforces HTTPS. Note that GitHub's
   Enforce HTTPS combined with Cloudflare Flexible would cause an endless redirect loop.

Expected result:

| Request | After step 1 |
| --- | --- |
| `https://www.edouardfouche.com/` | 1 hop: GitHub → `https://edouardfouche.com/` |
| `http://www.edouardfouche.com/` | 2 hops: Cloudflare → `https://www…`, then GitHub → `https://edouardfouche.com/` |
| `https://edouardfouche.com/about` | 1 hop: GitHub → `https://edouardfouche.com/about/` |
| `https://edouardfouche.github.io/` | unchanged, 2 hops (see below) |

**Rollback:** if the site shows a Cloudflare 5xx error page after the switch, set the mode back to
**Flexible**. The site then works exactly as before.

### Step 2 (optional): redirect `www` at the Cloudflare edge

After step 1, `www` already takes a single hop, but that request still travels to GitHub. A redirect
rule answers it at the edge, which is faster and independent of GitHub's settings.

1. Cloudflare dashboard → `edouardfouche.com` → **Rules** → **Overview** → **Create rule** →
   **Redirect Rule**. Cloudflare also offers this as the template "Redirect from WWW to root".
2. **Rule name:** `www to apex`.
3. **If incoming requests match:** Custom filter expression, **Field** `Hostname`, **Operator**
   `equals`, **Value** `www.edouardfouche.com`.
4. **Then:** **Type** `Dynamic`, **Expression** `concat("https://edouardfouche.com", http.request.uri.path)`,
   **Status code** `301`, and check **Preserve query string**.
5. **Deploy.** The `www` DNS record must stay **Proxied** (orange cloud), as it is today. Otherwise the
   rule never sees the request.

`http://www…` then takes 1 or 2 hops, depending on whether Cloudflare applies Always Use HTTPS before
the rule. Either is fine.

### The `edouardfouche.github.io` address

That redirect is served by GitHub directly, without Cloudflare, and GitHub uses `http://` because it
has no certificate for the custom domain. It cannot be fixed while the domain is proxied by Cloudflare.
It does not matter in practice: nothing should link to the `github.io` address, and every page
declares `https://edouardfouche.com/…` as its canonical URL.

### Verify after the change

```sh
for u in https://www.edouardfouche.com/ http://www.edouardfouche.com/ https://edouardfouche.com/about http://edouardfouche.com/; do
  curl -sL -o /dev/null -w "%{num_redirects} hop(s): $u -> %{url_effective} (%{http_code})\n" "$u"
done
```

Every line should end at an `https://edouardfouche.com/…` URL with status 200, in 1 hop (2 for
`http://www` without step 2). To see each individual hop: `curl -sIL https://www.edouardfouche.com/ |
grep -iE '^HTTP|^location'`. None of the `location:` lines should start with `http://`.
