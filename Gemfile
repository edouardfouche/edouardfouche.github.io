source "https://rubygems.org"

# This site is deployed by GitHub Pages' built-in Jekyll build (from the root of `master`), which
# ignores this Gemfile and uses its own pinned versions: https://pages.github.com/versions/
# The `github-pages` gem pins exactly those versions (Jekyll, kramdown, jekyll-feed, minima, ...),
# so a local build renders the same HTML as the live site.
#
# Usage:   bundle install && bundle exec jekyll serve
# Upgrade: when https://pages.github.com/versions/ lists a newer `github-pages` version, bump the
#          constraint below and run `bundle update github-pages`.
gem "github-pages", "~> 232", group: :jekyll_plugins

# `jekyll serve` needs webrick, which is no longer bundled with Ruby >= 3.0.
gem "webrick", "~> 1.8"

# Silences the "To use retry middleware with Faraday v2.0+" warning from jekyll-github-metadata.
gem "faraday-retry", "~> 2.2"
