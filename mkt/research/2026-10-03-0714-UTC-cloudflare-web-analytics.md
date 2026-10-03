# Cloudflare Web Analytics for the Pages site (research 2026-10-03 07:14 UTC)

Owner found it in the dashboard (Observability -> Analytics -> Web analytics).
Status 2026-10-03: DOCUMENTED ONLY, not enabled — owner decision. If it is
ever switched on, it complements our Worker beacon; it does not replace it.

## What it is
Free, privacy-first analytics: one JS snippet, no DNS change, no proxy
needed. No cookies, no localStorage, no fingerprinting (their docs state
all three explicitly). Works for sites NOT on Cloudflare via manual setup:
enter hostname -> copy snippet -> paste before </body>.

## Setup for us (owner, ~10 min)
1. "Set up hostname": enter `humbleangel.github.io` (full host, not bare
   `github.io` — matching is postfix-based, so the full host scopes it to
   us). Done.
2. Manage site -> copy the JS snippet (a `beacon.min.js` script tag with a
   per-site token; tokens are domain-locked, safe to expose in HTML).
3. Send the snippet to marketing -> added next to our own sendBeacon in
   index.html (+ mirror), committed, pushed.

## Facts that matter
- Limits: 10 non-proxied sites per account — we need 1. Fine.
- Retention 6 months rolling; dashboard only, no raw export on free.
- Only ONE Cloudflare snippet per page (our own sendBeacon is a separate
  script and coexists fine).
- Extra over ours: Core Web Vitals (real load speeds), nicer dashboard,
  bot filtering at edge.
- Weaker than ours: dashboard-only (no API into the observatory),
  `cloudflareinsights.com` is on some adblock lists (our first-party
  Worker beacon is less likely blocked), data lives with Cloudflare.

## Division of labor (decided)
- OUR Worker beacon = system of record: raw API feeding the observatory.
- Cloudflare Web Analytics = free cross-check + Web Vitals.
- If the two ever disagree hard, trust ours for counts (first-party,
  unblocked) and theirs for performance.

*Filed 2026-10-03 07:14 UTC · cost 0 · no public post · internal.*
