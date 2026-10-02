# Automating the remaining Shorts uploads to YouTube (research 2026-10-02 12:21 UTC)

Live state: 6 videos up (EN launch, FR, JA, KO, ES, "Who am I" dev episode).
Remaining: ~19 invite Shorts. All 21s vertical — ideal API candidates.

## The one fact that decides everything

**Videos uploaded through the YouTube API from an unverified project are locked to
private and cannot be made public** (official docs, `videos.insert` page:
"All videos uploaded via the videos.insert endpoint from unverified API projects
created after 28 July 2020 will be restricted to private viewing mode. To lift
this restriction, each API project must undergo an audit.").
The audit is a compliance review by YouTube — free, but takes weeks, and needs a
demo + ToS paperwork. No audit = the API can upload, but only YOU EVER SEE IT.

## Paths

### A. Full automation (API + audit) — slowest, most complete
- Owner creates a Google Cloud project (browser, ~15 min): enable YouTube Data
  API v3, OAuth consent screen, `client_secrets.json`, scope
  `https://www.googleapis.com/auth/youtube.upload`.
- Script (Python + `google-api-python-client`, resumable upload, exponential
  backoff — Google publishes the sample) loops over the 19 files with
  title/description/tags/categoryId `28` (Science & Technology) + `publishAt`
  for scheduling. Shorts need no special flag: vertical + ≤3min + `#Shorts`
  in description = auto-classified.
- Quota is NOT the blocker: default is 100 `videos.insert`/day + 10,000
  units/day for everything else — 19 Shorts fit in one afternoon.
  (Older guides say 1600 units/upload = 6/day; current official docs show the
  separate 100/day insert bucket. Either way, 19 videos pass.)
- OAuth in testing mode: refresh tokens expire after 7 days — fine for a
  one-day batch, re-auth if it spans longer.
- Then file the audit and wait weeks. Only after approval do uploads go public
  by themselves.
- Verdict: correct for a 500-video future, overkill for 19 videos due in days.

### B. Hybrid (RECOMMENDED): API uploads private, owner flips to public — 19 clicks
- Same setup + same script, NO audit needed.
- Script uploads all 19 as private with full metadata (titles, descriptions
  with `#Shorts`, tags, category 28, thumbnails via `thumbnails.set`).
- Owner opens Studio → 19 clicks private→public (or scheduled), checking each
  title/poster on the way — which doubles as the VLC-approval pass already owed
  on every video.
- Total owner time: ~30 min. Total setup: ~1–2h script + 15-min Cloud project.
- Verdict: cheapest path that still kills the boring part (uploads + metadata).

### C. Browser automation (Playwright/Selenium driving Studio) — DO NOT
- Against YouTube's automation rules on non-API access; a channel strike is the
  failure mode, and this channel is 10 days from launch with 6 videos up.
- We literally just watched an auto-filter eat the Reddit community for looking
  like a bot. Don't audition for the sequel on YouTube.
- Verdict: rejected.

### D. Third-party schedulers (PostEverywhere, PostFast, Aether, PostPeer) — rejected
- They work (they upload through THEIR audited projects), but all are paid and
  all need full OAuth write access to the channel. Violates cost-0 and hands
  the keys to a stranger.
- Verdict: rejected.

### E. Stay manual — the honest baseline
- 19 Shorts × ~3 min in Studio ≈ 1 focused hour, zero setup, zero new risk.
- If the remaining videos trickle out over days anyway, manual may beat even
  path B on total effort.
- Verdict: keep as fallback; decide after seeing B's setup cost.

## What the script needs from the repo (path B)

Per-video metadata already exists: titles + descriptions live in
`mkt/video/post_texts_25langs.txt`, schedule in `posting_schedule_brt*.md`.
Script reads that file, matches each language to its 12fps companion MP4,
uploads private, prints the video ID per language. One new file, e.g.
`mkt/video/pipeline/upload_shorts.py` (+ `requirements` line:
`google-api-python-client google-auth-oauthlib`). `client_secrets.json` NEVER
enters the repo (owner keeps it local, gitignored).

## Decision needed from owner

B (hybrid, recommended), A (full + audit wait), or E (manual hour)?
On "B, go": owner creates the Cloud project + sends `client_secrets.json`
path (never the contents), agent writes the script.

*Filed 2026-10-02 12:21 UTC · cost 0 · no public post · internal.*
