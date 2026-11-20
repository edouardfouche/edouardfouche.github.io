# docs/

Maintenance records for this website: what was found, what was changed and why, and how to reproduce
or verify it. The folder is excluded from the published site (`exclude` in [`_config.yml`](../_config.yml)),
so nothing here ends up on edouardfouche.com.

## Conventions

- **One topic per file**, named `YYYY-MM-DD-<topic>.md`: the date the work was done, then a short
  kebab-case topic, e.g. `2026-11-20-site-audit.md`. Sorting by name gives the chronology.
- **Markdown only**, with no Jekyll front matter (these files are never rendered by Jekyll).
- **Records, not living specs:** a dated record describes the state at that date. When something
  changes later, add a new dated file and link back to the old one rather than rewriting history.
  Fixing typos or broken links is fine.
- **Link to the source** (relative links to repo files, commit hashes) so claims can be checked.
- **No private data:** the repository is public. Leave out email addresses, tokens, local machine
  paths and anything else that should not be published.
- The current how-to for working in the repo lives in [`../CLAUDE.md`](../CLAUDE.md) and
  [`../README.md`](../README.md). These records explain how it got that way.

## Index

| Date | Document | Summary |
| --- | --- | --- |
| 2026-11-20 | [Site audit](2026-11-20-site-audit.md) | How the site is built and served, and the problems found in it |
| 2026-11-20 | [Toolchain setup](2026-11-20-toolchain-setup.md) | Ruby/Jekyll environment matching GitHub Pages: install, run, upgrade |
| 2026-11-20 | [Maintenance changes](2026-11-20-maintenance-changes.md) | Every change made, why, and how it was verified before and after deploy |
| 2026-11-20 | [Open items](2026-11-20-open-items.md) | Observations not acted on yet, with suggested fixes |
