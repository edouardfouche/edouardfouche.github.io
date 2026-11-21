# Impressum, privacy policy and the Book Me form

**Date:** 2026-11-21
**Follows:** the [full site audit](2026-11-21-full-audit.md), items L1, L2, L3, L6 and B3, and parts of
A3, A5, B4 and B5.
**Status:** a draft written at the owner's request and published right away. It is not legal advice.
The owner should check it, ideally against a maintained generator or with a lawyer (see
[What to check](#what-the-owner-should-check)).

## Changes

| Commit | Change |
| --- | --- |
| `a57c23d` | Book Me links the Google Form (new tab) instead of embedding it |
| `9e4e2cd` | New Impressum and privacy policy; one license statement everywhere; footer privacy link; Citation Policy fixes; the commented-out PayPal include replaced by a Liquid comment |

### Book Me (`a57c23d`)

The embedded form loaded Google's code, and could set Google cookies, for everyone who opened the page.
Now the page has the heading, an intro, a prominent "Open the intake form (Google Forms, opens in a new
tab)" link, the note not to submit sensitive data with a link to the privacy policy, and LinkedIn as an
alternative. Data goes to Google only when a visitor opens the link. This also brings the page in line
with the rule in [`CLAUDE.md`](../CLAUDE.md) against third-party embeds that collect personal data.

### Impressum (`9e4e2cd`, [`_layouts/impressum.html`](../_layouts/impressum.html))

| Section | Before | After |
| --- | --- | --- |
| Provider information | "Angaben gemäß § 5 TMG" (the TMG was repealed on 14 May 2024) | "Angaben gemäß § 5 DDG", same name and address, "90489 Nürnberg" without the comma |
| Contact | Plain address, which Cloudflare replaced with "[email protected]" unless JavaScript ran | `mailto:` link between `<!--email_off-->` markers, so it shows without JavaScript |
| Responsible for content | § 55 Abs. 2 RStV (replaced in 2020) | § 18 Abs. 2 MStV |
| Disclaimer | Cited §§ 7–10 TMG | A short paragraph on content and links without statute numbers. The old sections have no one-to-one successor in the DDG, and disclaimers carry little legal weight anyway |
| Copyright | "Downloads und Kopien … nur für den privaten, nicht kommerziellen Gebrauch" | "Urheberrecht und Lizenz": CC BY-SA 4.0 for texts and images by the owner. Excluded: Chérie Birkner's photos, the publications and marked third-party content |
| Privacy policy | "Keine personenbezogenen Daten", Simple Analytics, a PayPal button that is not shown, and a dead GitHub link | Rewritten, see below |

The German sections are marked `lang="de"`, the duplicate `id="sec0"` headings got unique IDs
(`#angaben`, `#verantwortlich`, `#haftung`, `#urheberrecht`, `#datenschutz`), and the page no longer
highlights "About" in the menu. The meta description in [`impressum.md`](../impressum.md) names the DDG
and the privacy policy.

### Privacy policy (section `#datenschutz` of the Impressum)

It covers, each with its legal basis under Art. 6 GDPR:

| Topic | Content |
| --- | --- |
| Controller | The site owner, contact as in the Impressum |
| Principles | No cookies, no advertising or tracking services; IP addresses are processed by the services below |
| Hosting and delivery | GitHub Pages (GitHub, Inc.) and Cloudflare (Cloudflare, Inc.) process connection data. GitHub logs visitors' IP addresses for security, as its documentation states. Possible transfers to the US. Links to both privacy statements |
| Simple Analytics | Cookieless, aggregated statistics only |
| Comments (giscus) | The script from giscus.app loads on every post, and the comment area when scrolled to. IP address goes to giscus.app and GitHub. Signing in stores an encrypted token in local storage. Comments and usernames are public. Facts taken from giscus's own privacy policy |
| Google Form | Linked, not embedded. Answers stored in the owner's Google account, used only for the request, deleted when no longer needed |
| E-mail | Used only to answer |
| MathJax | Loaded from cdnjs on the posts with formulas |
| Links | No data before a click |
| Rights | Articles 15–18, 20, 21 and 7(3) GDPR, and the complaint to a supervisory authority (Art. 77), naming the Bavarian authority (BayLDA) as an example |

All cited URLs returned 200 on the audit date.

### Other changes in `9e4e2cd`

- **Footer** ([`_includes/footer.html`](../_includes/footer.html)): a "Datenschutz / Privacy Policy" link
  to `/impressum/#datenschutz`, and "Bootstrap", "GitHub" and "CC BY-SA 4.0" spelled correctly.
- **`copyright` meta tag** ([`_includes/head.html`](../_includes/head.html)): "© Edouard Fouché. Texts
  and own images: CC BY-SA 4.0 unless marked otherwise (see /impressum/)" instead of "All Rights
  Reserved".
- **Citation Policy** ([`_layouts/citation-policy.html`](../_layouts/citation-policy.html)):
  - the license sentence has the same scope as the Impressum;
  - typos fixed ("Creative Commons", "blog articles", "LaTeX", "BibLaTeX", "If in doubt");
  - the BibLaTeX example uses `urldate = {2025-01-05}`, because biber rejects "January 5th, 2025";
  - the title is an `<h1>`, the list is no longer inside a `<p>`, and the example block can be scrolled
    with the keyboard (`tabindex="0"`);
  - the menu no longer highlights "About".
- **PayPal:** the commented-out include in [`_includes/navbar.html`](../_includes/navbar.html) still
  rendered the PayPal form, with a tracking-pixel URL, inside an HTML comment on every page. It is now a
  Liquid comment explaining how to bring the button back. The include file and its button image are
  kept.

## Verification

- `bundle exec jekyll build` succeeds. `/book-me/` contains no iframe and no request to
  `docs.google.com` other than the link. `/impressum/` contains the `email_off` markers around the
  address.
- Screenshots of Book Me, Impressum, Publications, About, Citation Policy and two posts at both widths
  were reviewed by eye.
- axe-core 4.14.1 on Book Me, Impressum and Citation Policy: no `frame-title`,
  `scrollable-region-focusable`, `link-in-text-block` or `color-contrast` findings left.

## What the owner should check

1. **The whole text.** Is everything described true for how you run the site, in particular the Google
   Form? Where are the answers stored, who sees them, and when do you delete them?
2. **Tengu Consulting.** If you offer services commercially, the Impressum may need more: the business
   name, a VAT ID (USt-IdNr.) if you have one, and for some professions supervisory or chamber details.
   Nothing about this was added, because the repository does not say how the business is set up.
3. **Simple Analytics wording.** "Keine Cookies, keine Nutzerprofile, nur aggregierte Angaben" follows
   Simple Analytics' public statements. Check it against your account settings.
4. **Cloudflare features.** If you turn on Cloudflare features that set cookies (bot protection, for
   example) or log more data, add them to the privacy policy.
5. **A second opinion.** Generators such as eRecht24 or datenschutz-generator.de, or a lawyer, can
   confirm the wording. Keep the facts listed above, which were checked during this work.

## Post-deploy check

Deployed with `1a8365d`; see the
[post-deploy check](2026-11-21-performance-accessibility-cleanup.md#post-deploy-check) of the
performance record. The live `/impressum/` and `/book-me/` match the build.
