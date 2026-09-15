# supEars Marketing Log

Every entry: `YYYY-MM-DD HH:MM UTC`, channel, what went out (file/commit link), cost (0 unless owner approves), result. No silent work.

## 2026-09-15 00:43 UTC — Session start: baton accepted (handoff §7)

- Channel: repo (`supEars_Official`, local work only so far).
- Read in full: `MARKETING_HANDOFF.md`, `README.md`, `index.html`. No `MARKETING_LOG.md` existed — created this file.
- Cost: 0. Result: session open, no public posts, no spend.
- (a) README refresh summary (one line): Refresh README to 26 languages + §3 taglines, pre-alpha v0.8.71 status (no downloads yet), and roadmap wording for Mac/Linux/accuracy.
- (b) 30-day pre-alpha plan (DRAFT — no posts without owner approval):
  1. Week 1 — Storefront: refresh `README.md` (task #1) + `index.html` (task #2) per §§2–3; keep all vision claims as roadmap.
  2. Week 2 — Waitlist: open GitHub Issues/Discussions waitlist for alpha (0.90) notify-me; no download links.
  3. Week 3 — Dev-community seeding (draft posts only): Windows productivity / dictation corners, EN + one §3 line per snippet.
  4. Week 4 — 26-language social snippets reusing §3 verbatim (drafts in repo first, post only after approval).
- Blockers for owner: (1) screenshots — I cannot run the app, please supply finals for `assets/` (backlog #3); (2) confirm README draft below before I push; (3) confirm 30-day plan before any public post.

## 2026-09-15 00:44 UTC — Backlog #1 done: README refreshed

- Channel: repo. Changed `README.md`: 26 languages (was 17), all 26 §3 taglines verbatim, pre-alpha v0.8.71 (no downloads yet), Windows-today / Mac+Linux-coming roadmap wording, accuracy as target, MegaCorps/😈 line removed, free-during-testing price line.
- Cost: 0. Result: uncommitted; awaiting commit per backlog wording.
- Question for owner: `index.html` demo + FAQ mention "auto-detect" — not in handoff §2. Kept as-is; confirm or cut?

## 2026-09-15 00:44 UTC — Backlog #2 done: index.html to same standard

- Channel: repo. Changed `index.html` only: meta + pill (14-day → free-during-testing / 60-day testers), counts 17→26 (demo labeled a sample of 26; kept 14 embedded-flag demo — new flags needed for full 26, flagged below), trial section carries pre-alpha v0.8.71 + Windows-first/Mac+Linux-coming, FAQ language list → full 26, offline wording tightened.
- Cost: 0. Result: uncommitted.
- Blocker for owner: full 26-voice demo needs 12 more flag embeds + example sentences (en, uk, cs, hu, el, ro, sv, id, vi, th, ur, pt-PT) — say the word and I'll draft, or keep the 14-sample.

## 2026-09-15 00:47 UTC — Pushed to main

- Channel: repo. Pushed `c701020` (README + log) + `2e68d38` (index) to `origin/main`. Identity: `marketing-agent` (empty email, per-owner). Working tree clean.
- Cost: 0. Still open: screenshots (#3), auto-detect confirm, 26-flag demo decision, 30-day plan approval.

## 2026-09-15 00:48 UTC — Repo reorganized into mkt/

- Channel: repo. Moved `MARKETING_HANDOFF.md`, `MARKETING_LOG.md` (this file), `SESSION_PROMPT.md`, `assets/` → `mkt/` via `git mv`. Root now holds only `README.md` + `index.html` (kept at root per-owner so Pages stays live) plus `.github/` (templates must stay at root).
- Fixed `README.md` logo path → `mkt/assets/supEarsLogoV3.png`; handoff `assets/` ref → `mkt/assets/`. Old log entries above still cite pre-move paths — history, left as-is.
- Cost: 0. Result: committed + pushed as `7432923`.

## 2026-09-15 01:20 UTC — Research: worldwide distribution channels (free-first)

- Channel: repo. Ran 7 research subagents (round 1: direct channels, launch platforms, communities/social, partners/press, paid+waitlist+analytics; round 2: regional free venues, free outreach/production stack). Synthesized into one self-contained file: `mkt/research/2026-09-15-0120-UTC-distribution-channels.html` (free-first: FREE NOW / FREE AT-ALPHA / PAID-LATER appendix). Opened in Firefox per-owner.
- Cost: 0. Result: filed; awaiting owner green light on the NOW-batch (tester call, RSI answers, Launching Next queue) before any public post.

## 2026-09-15 01:29 UTC — Research round 2: organic visibility (divulgation, not distribution)

- Channel: repo. Per-owner redirect: 5 new subagents (social playbooks, forums/groups, $0 GIF tooling, 24-audience discovery, content engine). Synthesized into NEW file only: `mkt/research/2026-09-15-0129-UTC-organic-visibility.html` — distribution files untouched. Opened in Firefox per-owner.
- Cost: 0. Result: filed; awaiting owner pick of series #1 (recommendation: 26 Tongues day 1) before any public post.

## 2026-09-15 01:59 UTC — Side quest filed: Wispr Flow + Indian accent

- Channel: repo. Question: do Indians struggle with Wispr Flow due to strong Indian accent? Answer: yes, documented but nuanced (accent + Hinglish code-switch + auto-detect = weak spot; mild accents fine). Filed as NEW file only: `mkt/research/2026-09-15-0159-UTC-wispr-flow-indian-accent.md`. Existing research files untouched. Note: `websearch` API 429'd throughout; used `webfetch` via DuckDuckGo HTML + primary docs instead.
- Cost: 0. Result: filed; no public post.

## 2026-09-15 02:12 UTC — Video plan opened (3 Shorts/day + 2 longs/week)

- Channel: repo. Owner directive: accelerator pedal on videos. Filed as NEW file: `mkt/video-plan.md` (cadence + idea #1 "How to become a vibecoder" collected, concept TBD). No videos shot or posted yet.
- Cost: 0. Result: filed; awaiting owner brief/script direction.
