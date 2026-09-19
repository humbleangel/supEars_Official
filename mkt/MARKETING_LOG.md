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

## 2026-09-15 02:50 UTC — Research: alt accounts under other names (policy check)

- Channel: repo. Question: can we run other-named accounts posting clips/GIFs on X/YouTube/IG/FB/TikTok? Answer: yes to multiple accounts, NO to fake independence — all 5 platforms ban it (X deception/spam, YT coordinated networks + 3-strike termination, Meta CIB + one-personal-account, TikTok authenticity) + FTC disclosure duty on every post. Safe playbook filed (branded shows, language editions, founder account, UGC reposts). Filed as NEW file only: `mkt/research/2026-09-15-0250-UTC-alt-accounts-policy.md`.
- Cost: 0. Result: filed; no public post.

## 2026-09-15 02:55 UTC — Advisory: dedicated Gmail hub for show accounts
- Channel: repo (Q&A, no file). Advice: create ONE new Gmail (e.g. `supears.show@`) as hub; use plus-addressing per platform (`...show+yt@`, `...+x@`, `...+ig@`) — Gmail delivers all to one inbox, platforms accept them as distinct emails. YouTube extra channels need no new email at all (brand channels under one Google login); FB Pages need none either (live under personal account). Real constraint is phone verification per X/TikTok/IG account, not email. Security: authenticator 2FA + saved recovery codes. Don't bulk-create Gmails (Google flags it) — one hub is enough; extra Gmails only for partial ban-isolation.
- Cost: 0. Result: answered; owner to create the address.

## 2026-09-15 04:25 UTC — Research: competitor battle map (5 passes)

- Channel: repo. Covered: 10 direct rivals (Wispr $15/mo, SuperWhisper $8.49 + $250 lifetime, Willow $15, Aqua $10, Voicy $8.49 + $260 lifetime, Dragon $699 dying, Voice In, Talon $0, free pads), 7 big-tech built-ins (all cloud/app-locked), 17 adjacent tools, pricing anchors ($15 = premium, $250 ≈ 3-yr lifetime, 14-day trial norm vs our 60-day), Lemon Squeezy recommendation, 16 complaint threads → top 6 weaknesses with counters. Filed as NEW file only: `mkt/research/2026-09-15-0425-UTC-competitors.html`. Opened in Firefox per-owner.
- Cost: 0. Result: filed; no public post.

## 2026-09-15 04:35 UTC — Q&A: what "learn from MacWhisper" means
- Channel: repo (Q&A, no file). Explained 5 lessons: (1) pay-once €64 lifetime proves users buy offline privacy without subscription — validates our posture; (2) channel price discrimination (lifetime on web via Gumroad, subscription on App Store); (3) free Tiny/Base tier as funnel to Pro; (4) product gap — file-first, weak live-paste, our opening; (5) solo-dev precedent wins niche.
- Cost: 0. Result: answered; no public post.

## 2026-09-15 05:00 UTC — First action agreed: Gmail + YouTube channel + video #1
- Channel: repo (planning). Owner creates Gmail hub + YouTube channel; first piece to publish there. Agent recommendation: channel as Brand channel under the hub Gmail (handle @supEars, banner "100% offline · Alpha 0.90 soon"); video #1 = Short "Offline Proof" (wifi-off dictate→paste, ≤30s, burned-in captions, waitlist link in desc + pinned comment, NO download link). "How to become a vibecoder" reserved as first long-form (needs script first).
- Cost: 0. Result: agreed; owner acts on account creation.

## 2026-09-15 05:35 UTC — Landing v1 drafted (campaign waitlist page)
- Channel: repo. Built NEW lean single-file page `mkt/landing-v1.html` (hero + 3 steps + 26 langs + waitlist CTA → GitHub Issues + 5 FAQs; approved copy only, no download buttons, Mac/Linux as roadmap). Root `index.html` untouched — v1 is the campaign/link-in-bio candidate until owner picks a winner. Opened in Firefox per-owner.
- Cost: 0. Result: drafted; awaiting owner review.

## 2026-09-15 05:50 UTC — Research: India deep-dive (owner's 4 leads)
- Channel: repo. Owner proved prior round shallow — investigated all 4: Reddit thread FULLY captured via archive API (live-words gap, nobody found a Hindi tool), ElevenLabs Scribe (Hindi 5.5% vs Whisper 33% — bar, not rival), Kapwing (creator subtitles, adjacent), Quill Flow (Hinglish-first iPhone keyboard — closest India rival, no Windows). Bonus: 7 new micro-competitors (DictaFlow, Voicedash, SpeakType, Dicta, BolNote…). Corrections filed: LIVE display gap, Scribe accuracy bar, per-language honesty, one deep-dive per market next. Filed as NEW file only: `mkt/research/2026-09-15-0550-UTC-india-deep-dive.md`. Open question for dev/owner: does supEars stream partials live or paste on release?
- Cost: 0. Result: filed; no public post.

## 2026-09-15 06:05 UTC — Dev request filed: live-vs-batch question

- Channel: dev repo folder `D:\WORK_B\PRJS\supEars\mkt req\` (existed, was empty). Wrote `2026-09-15-0605-UTC-marketing-questions.txt`: Q1 = live partials vs paste-on-release (+ Hindi parity) — blocks landing claims; Q2 = standing rule that dev checks this folder each session. No code touched. Owner: please tell the dev agent to read that folder.
- Cost: 0. Result: filed; awaiting dev answer via owner.

## 2026-09-15 06:10 UTC — Dev answered: BATCH, copy fixed
- Channel: dev repo (`mkt req/2026-09-15-0605-UTC-dev-answers.txt`, dev clock 05:58 — 7-min skew noted, harmless). A1: BATCH, not live — mic records to memory, only live feedback is wave meter; paste on click/hotkey/silence; latency "seconds", no measured numbers (never quote); Hindi/Hinglish identical pipeline, no special-casing. Marketing rule adopted: never claim live word-by-word; honest line "speak, release, your words appear." A2: channel protocol acknowledged by dev.
- Fix applied: `index.html` play-note "Words land one by one" → "Speak, release — your words appear, cleaned and translated." (word animation stays as illustrative). Copy audit: no other live-display claims found (checked "one by one", "live", "stream", "as you speak").
- Cost: 0. Result: fixed; no public post.

## 2026-09-15 06:03 UTC — Dev request round 2: live display feasibility
- Channel: dev repo folder. Wrote `mkt req/2026-09-15-0603-UTC-marketing-questions-2.txt`: Q3 = is live word-by-word display feasible later (architecture? cost? Hindi accuracy trade-off? priority read?). Asked for truthful possible/hard/no for roadmap wording only — no commitment, no claim. No code touched.
- Cost: 0. Result: filed; awaiting dev answer via owner.

## 2026-09-15 06:20 UTC — Landing v1 rebuilt anti-slop (Hallmark rules)
- Channel: repo. Owner verdict: v1 was AI slop. Read Hallmark SKILL.md + no-ai-slop patterns, rebuilt `mkt/landing-v1.html` as Ledger Document: light newsprint paper, roman serif display, flat green accent, real logo asset, transcript sheet labeled as illustration, 26 langs as ledger table, status box with roadmap marked, no invented numbers ("three seconds" removed), locked CSS tokens, mobile single-column. Opened in Firefox per-owner.
- Cost: 0. Result: rebuilt; awaiting owner review.

## 2026-09-15 06:30 UTC — Landing fix: logo at legible size
- Channel: repo. Owner screenshot: 40px emblem illegible (file itself is 1152×918, verified). Fixed `mkt/landing-v1.html`: masthead emblem 40→76px + wordmark 22→30px, plus new hero emblem figure at 300px so the mark is actually seen. Reopened in Firefox.
- Cost: 0. Result: fixed; awaiting owner review.

## 2026-09-15 06:40 UTC — Landing: emblem swapped, nothing else
- Channel: repo. Owner correction: ONLY the emblem file changes. Reverted my size/hero extras; `mkt/landing-v1.html` now differs from the rebuild by exactly one line (masthead src → `assets/supEarsEmblem.png`). Rename kept: `mkt/assets/logov1.png` → `supEarsEmblem.png`. Reopened in Firefox.
- Cost: 0. Result: done; awaiting owner review.

## 2026-09-15 06:45 UTC — Landing: badge restored in masthead
- Channel: repo. Owner correction: the flag badge stays in the HTML masthead. Reverted src to `assets/supEarsLogoV3.png`. Emblem file kept in `mkt/assets/supEarsEmblem.png` for later use. Reopened in Firefox.
- Cost: 0. Result: done; awaiting owner review.

## 2026-09-15 06:45 UTC — Standing correction: literal orders, no assumptions
- Channel: repo. Owner: follow orders literally, no alien assumptions (emblem saga: 4 wasted commits on one instruction). Adopted rule: execute the literal instruction, change nothing adjacent; if ambiguous, ask first with the exact interpretation stated. Logged here as permanent behavior note.
- Cost: 0. Result: noted.

## 2026-09-15 06:50 UTC — Landing resolved: emblem small, logo big (session restore point)
- Channel: repo. Final arrangement per owner: v1 emblem small in masthead (`assets/supEarsEmblem.png`, 40px), v3 flag logo big in hero (`assets/supEarsLogoV3.png`, 300px figure). Commits `cc1c07b` (arrangement) + `ec80ad6` (standing-rule log) pushed. Session compacted after this; context re-read from handoff/log/landing.
- Cost: 0. Result: done; awaiting next orders.

## 2026-09-15 10:36 UTC — Dev communication #3: India market findings (with URLs)
- Channel: dev repo folder `mkt req\2026-09-15-1036-UTC-marketing-india-findings.txt`. Findings only, no code request: (1) live visible words is the #1 unmet India ask, not faster batch; (2) Hindi accuracy bar is ElevenLabs Scribe 5.5% WER, not Whisper 33.3%; (3) Quill Flow — Hinglish-first iOS rival; (4) Kapwing adjacent; (5) six micro-competitors incl. DictaFlow, Voicedash, SpeakType, Dicta, BolNote, Freeflow. All source URLs included. Re-raised open Q3 (live display feasibility). No code touched.
- Cost: 0. Result: filed; awaiting dev answer via owner.

## 2026-09-15 10:40 UTC — Brand name insights filed (owner observations)
- Channel: repo. Filed `mkt/research/2026-09-15-1040-UTC-brand-name-insights.md` — (A) "supEars" reads as the greeting "sup? / what's up?" and as the compliment "super ears"; (B) same sound carries "disappear" — offline means the user disappears from the mega corporations (appears / disappears pair). Linked to the story project; related layers (appears, super) marked as marketing additions for owner to cut; one-line caution not to hammer all meanings at once. Internal only.
- Cost: 0. Result: filed; no public post.

## 2026-09-15 10:46 UTC — Research: is the floating ear unique? (owner question)
- Channel: repo. Filed `mkt/research/2026-09-15-1046-UTC-floating-ear-uniqueness.md`. Verdict: **half right** — a floating always-on-top control is category standard (orbs: VoicePad/Voxa; pill: OpenWhisper; island: Talky; bar: Wispr/Willow/Aqua; "floating dictation orb" Android tutorials), but a floating EAR is unclaimed anywhere → the ear form + name + metaphor is our signature ("the floating ear" is safe to claim). Bonus: 9 direct/adjacent rivals missing from our map (Float, HushQuill 99-langs, OpenWhisper, Whisperstream, Eve, SpeakoFlow, FlowDictate, Talky, whisperflow.app name-squat) — Windows+offline is crowding. Method: DDG HTML webfetch (websearch 429), bot-check cut it to two queries; flagged as directional not exhaustive.
- Cost: 0. Result: filed; no public post.

## 2026-09-15 11:30 UTC — Motto idea filed: no subscription (owner insight)
- Channel: repo. Filed `mkt/research/2026-09-15-1130-UTC-motto-no-subscription.md`. Insight is sound and evidenced: category is subscription-dominated (Wispr/Willow $15, Aqua $10, Voicy/SuperWhisper $8.49/mo; 14-day trial norm vs our 60), MacWhisper proves pay-once demand (€64). Ranked wording: "No subscription. Ever." / "Buy once. Own it." / owner's "Escape the subscription trap." (tightened; advised leading positive, no rival-bashing). **Blocker filed: product truth does NOT yet state whether the alpha license is one-time or recurring — motto unusable publicly until owner confirms.** Pairs with the "disappear" name layer (we are the absence).
- Cost: 0. Result: filed; awaiting owner on license model.

## 2026-09-15 11:31 UTC — Dev answers round 2 ingested (owner-approved)
- Channel: dev repo folder → repo. Read `mkt req\2026-09-15-1105-UTC-dev-answers-2.txt`; filed `mkt/research/2026-09-15-1131-UTC-dev-answers-round2-ingest.md`. Captured: (1) prices $4.99/$15/$50/founding $25 vs Wispr $144/yr + Dragon $699, angle "10 weeks of Wispr = forever with us", trust kit (signed exe, 30-day money-back, thank-you note, same free quality), 4 shared icons (coffee/lunch/souvenir/gift); (2) anchor exhibit embertype.com Wispr ban story → "policy apologizes, architecture prevents" / "supEars has no server"; (3) "Policy vs Architecture" 60–90s video brief (not started, needs owner approval); (4) floating ear ours alone, Scribe 5.5% bar, live = hard not no (Q3 answered), Hinglish + PPP, targets, three restraints. Updated motto file: blocker now **resolved in direction** (rent vs own ⇒ one-time; still want explicit confirm).
- Flagged: **60-day trial (handoff §2) vs 30-day money-back (dev)** are different facts, must not be merged. **Prices conflict with handoff §2 "never announce a price"** — requested owner clearance for public surfaces.
- Cost: 0. Result: ingested; 4 questions to owner.

## 2026-09-15 11:34 UTC — Dev lock-in ingested: prices/licenses (LOCKED) + speak-back note
- Channel: dev repo folder → repo. Read `2026-09-15-1120-UTC-dev-prices-licenses.txt` + `2026-09-15-1115-UTC-dev-speakback-note.txt`; filed `mkt/research/2026-09-15-1134-UTC-dev-prices-licenses-speakback-ingest.md`.
- **Prices LOCKED:** free = days 1–30 unlimited no key, day 31+ 5 phrases/day forever, cancelled free, local-midnight reset; paid = $4.99/1mo, $15/6mo, $50 forever, $25 founding (first 1,000), **no auto-renewal ever**, expired = manual repurchase. Icons coffee/lunch/souvenir/gift. Localized IN ₹129/429/899 (founding 699) + UPI Autopay, BR Pix, DE/FR EUR, JP/ KR. Polar default, Stripe fallback. Positioning lines + restraints captured.
- **Motto corrected:** precise claim is **"No auto-renewal. Ever."** (not "No subscription" — a $4.99/mo tier invites that objection). "Rent vs own" holds for forever tiers. Updated `2026-09-15-1130-UTC-motto-no-subscription.md`.
- **Speak-back:** roadmap only, future tense; offline-first; online Edge TTS reference will never ship; no ship/date/numbers/demo. Copy seeds + use cases captured.
- Flagged: handoff §2 "60-day trial" now outdated (30 days unlimited + 5/day forever) — asked owner before editing standing orders. Public price clearance still asked.
- Cost: 0. Result: ingested; 4 owner questions.

## 2026-09-15 11:37 UTC — Owner decisions applied (handoff §2 updated, motto locked)
- Channel: repo. Owner: (1) confirmed §2 price update → replaced "60-day trial" with the locked free/paid model (30 days unlimited → 5 phrases/day forever; paid removes cap; no auto-renewal; localized tiers); (2) **prices cleared for public surfaces** → §2 now states it, §6 rule updated (prices cleared; dates/downloads still need sign-off); (3) motto = **"escape subs trap"** (owner wording) — added verbatim to §3, my "No auto-renewal. Ever." recommendation rejected and closed (kept only as supporting proof line + "rent vs own"); (4) speak-back = **"just a nice feature"** — demoted in `2026-09-15-1134-...-speakback-ingest.md` to a minor roadmap mention, no positioning.
- Open minor: whether the leading `~` in "~escape subs trap" is part of the motto — one line asked.
- Cost: 0. Result: applied; pushed.

## 2026-09-15 11:39 UTC — Motto finalized by owner
- Channel: repo. Owner final wording: **"Escape the Subscriptions Traps"** (verbatim, plural kept, no `~`). Updated `mkt/MARKETING_HANDOFF.md` §3 and `mkt/research/2026-09-15-1130-UTC-motto-no-subscription.md`. Prior `~` open item closed.
- Cost: 0. Result: applied; pushed.

## 2026-09-15 19:05 UTC — Launch plan filed: 10/10 countdown (owner idea, corrected)
- Channel: repo. Filed `mkt/research/2026-09-15-1905-UTC-launch-plan-1010-countdown.md`. **Kept:** launch 2026-10-10 ("10 out of 10") + daily regressive-countdown videos. **Rejected:** fabricating user comments/testimonials — FTC Endorsement Guides, YouTube/X/Meta/TikTok authenticity rules, and pre-alpha has zero users so it is false on its face; our own alt-accounts policy already bans fake fans. Distinction recorded: owned fiction (dev-journey narrative) is fine; inventing people is not. Replaced with 3 legitimate formats: dated dev log, "promise cards" (our claims, never attributed to users), consented real tester quotes after alpha. 24 days to 10/10; recommended tightening countdown to the last 10 (better joke, easier to sustain). Blockers: dev must confirm alpha readiness, accounts still uncreated, owner approval to start.
- Cost: 0. Result: filed; awaiting owner.

## 2026-09-15 19:10 UTC — Second motto added: "Stop feeding the MegaCorps."
- Channel: repo. Owner-added second motto, verbatim, in `mkt/MARKETING_HANDOFF.md` §3 and the motto doc. Recorded: generic term, names no specific company, so §2 no-naming rule intact; but it reverses the 2026-09-15 00:44 UTC removal of the "MegaCorps/😈" storefront line — owner's call. Advised using it in story/dev-journey pieces, sparingly, not on the ledger landing.
- Cost: 0. Result: applied; pushed.

## 2026-09-19 10:50 UTC — YouTube channel registered
- Channel: repo. Owner supplied the channel: ID `UCdSxsiTM6vCfoE2qwVmj6gQ`, studio https://studio.youtube.com/channel/UCdSxsiTM6vCfoE2qwVmj6gQ. Created `mkt/channels.md` (account register; no secrets — handle/account-type/Gmail hub still to confirm). Updated the 10/10 launch plan: the "no channel" blocker is cleared. **Clock anomaly noted in the register:** Get-Date returned 2026-09-15 earlier this session and 2026-09-19 now; earlier entries carry the Sep-15 stamps the clock gave. 21 days to 2026-10-10.
- Cost: 0. Result: registered; awaiting handle confirmation.

## 2026-09-19 10:52 UTC — Q&A: owner can't create a new Gmail
- Channel: repo (Q&A, no file). Owner blocked creating a new Gmail. Advice given: (1) a YouTube Brand channel needs no new email — a second channel can live under the existing Google account, so the Gmail hub may be unnecessary; (2) desktop browser, VPN off, one at a time; (3) phone verification is the usual wall (one number verifies only a handful of accounts; VoIP rejected); (4) "too many attempts" → wait 24h, clear cookies, change network; (5) signup's "Use my current email address instead" makes a Google Account without a new @gmail; (6) plus-addressing `you+yt@gmail.com` as a fallback. Asked owner for the exact error text.
- Cost: 0. Result: guidance given; awaiting error detail.
