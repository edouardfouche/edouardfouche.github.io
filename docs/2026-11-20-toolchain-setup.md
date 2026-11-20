# Toolchain setup

**Date:** 2026-11-20
**Goal:** be able to build and preview the site locally, with exactly the software GitHub Pages uses
in production.

## What is used and why

| Component | Version | Why |
| --- | --- | --- |
| rbenv + ruby-build | from Homebrew | Per-project Ruby versions; reads `.ruby-version`. |
| Ruby | 3.3.14 (`.ruby-version`) | GitHub Pages runs Ruby 3.3 (3.3.4 at the time). 3.3.14 is the latest 3.3 patch release. |
| Bundler | 2.5.x (ships with Ruby 3.3) | Installs the gems pinned in `Gemfile.lock`. |
| `github-pages` gem | 232 (`~> 232` in `Gemfile`) | Pins exactly the gem versions that GitHub Pages builds with, including Jekyll 3.10.0, kramdown 2.4.0 and jekyll-feed 0.17.0. |
| `webrick` | ~> 1.8 | `jekyll serve` needs it; Ruby 3 no longer bundles it. |
| `faraday-retry` | ~> 2.2 | Silences a warning from jekyll-github-metadata. It has no effect on output. |

`Gemfile.lock` is committed, so `bundle install` gives the same versions on every machine.

## First-time setup on a Mac

```sh
brew install rbenv ruby-build libyaml
rbenv init zsh            # adds rbenv to ~/.zprofile; open a new terminal afterwards
cd edouardfouche.github.io
rbenv install             # installs the Ruby version named in .ruby-version
bundle install
```

## Daily use

```sh
bundle exec jekyll serve            # http://localhost:4000, rebuilds on change
bundle exec jekyll serve --drafts   # also renders _drafts/
bundle exec jekyll build            # one-off build into _site/
```

`jekyll serve` does not reload `_config.yml`, so restart it after you edit that file.

## Upgrading

GitHub publishes the versions it uses at https://pages.github.com/versions/ (also available as JSON at
https://pages.github.com/versions.json). Only upgrade when the `github-pages` version listed there
changes. A newer gem on rubygems.org alone is not a reason: version 233 was released on 2026-11-03,
but Pages was still on 232.

1. Bump the constraint in `Gemfile`, e.g. `gem "github-pages", "~> 233"`.
2. `bundle update github-pages`
3. If the Ruby version changed, update `.ruby-version` and run `rbenv install`.
4. Build, check the output, and commit `Gemfile`, `Gemfile.lock` and `.ruby-version` together.

Do not add Jekyll plugins that are not on the Pages allowlist, or features that need Jekyll 4. The
production build ignores the `Gemfile` and would fail or render them differently.

## Deploying

Push to `master`; GitHub Pages builds and publishes in about a minute. To check the build status:

```sh
gh api repos/edouardfouche/edouardfouche.github.io/pages/builds/latest --jq '{commit, status, error}'
```

## Git access over SSH

The remote uses SSH (`git@github.com:...`). The SSH key on the maintenance machine is registered on
GitHub but protected by a passphrase. Until the key is loaded into the agent, `git push` fails with
`Permission denied (publickey)`. Load it once and store the passphrase in the macOS keychain:

```sh
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

The deploy on 2026-11-20 was pushed over HTTPS with the GitHub CLI's credentials instead, as a one-off
that changed no git configuration:

```sh
git -c credential.helper= -c credential.helper='!gh auth git-credential' \
  push https://github.com/edouardfouche/edouardfouche.github.io.git master:master
```
