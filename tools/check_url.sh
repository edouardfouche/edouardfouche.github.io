#!/bin/sh
# Check one URL: HEAD first, then a ranged GET if HEAD is refused.
# Prints: status<TAB>final URL<TAB>number of redirects<TAB>original URL
# Many URLs in parallel (list from the "external_links" of tools/html_audit.py's JSON report):
#   tr '\n' '\0' < links.txt | xargs -0 -n1 -P12 sh tools/check_url.sh > results.tsv
# Amazon, LinkedIn, Redbubble, ACM, OpenReview, Medium sites and Wikipedia answer scripts with
# 403/429/503/999: check those by hand.
u="$1"
r=$(curl -sS -o /dev/null -L --max-time 25 --max-redirs 8 -I -w '%{http_code}\t%{url_effective}\t%{num_redirects}' "$u" 2>/dev/null)
case "$(printf '%s' "$r" | cut -f1)" in
  2*) ;;
  *) r=$(curl -sS -o /dev/null -L --max-time 25 --max-redirs 8 -r 0-1023 -w '%{http_code}\t%{url_effective}\t%{num_redirects}' "$u" 2>/dev/null) ;;
esac
printf '%s\t%s\n' "$r" "$u"
