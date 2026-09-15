# Dev lock-in: prices + licenses, and speak-back note (ingested)

> Filed 2026-09-15 11:34 UTC. Sources: `mkt req\2026-09-15-1120-UTC-dev-prices-licenses.txt` (LOCKED) and `mkt req\2026-09-15-1115-UTC-dev-speakback-note.txt` (FYI). Owner-relayed, owner-approved. Internal reference for copy planning. Supersedes the looser price read in `2026-09-15-1131-UTC-dev-answers-round2-ingest.md` where the two disagree.

# PART A — LOCKED prices and licenses

## Free tier (forever, full quality always, no account)

- **Days 1–30: unlimited, no key.**
- **Day 31+: 5 completed phrases/day, free forever.**
- Cancelled recordings are free (do not count).
- Resets at local midnight.
- 6th attempt auto-opens the license window (also shown every launch before the main UI).
- Blocked window shows: countdown to midnight + **"come back tomorrow, or remove the limit now"** + 3 buttons.

## Paid tier (cap removal only — same models, same quality)

- **$4.99 = 1 month** — "coffee", impulse buy.
- **$15 = 6 months** — "lunch", value pick, ~$2.50/mo.
- **$50 = forever** — "souvenir", ~10 weeks of Wispr = yours forever.
- **$25 = founding forever** — first 1,000 only, "gift", then $50.
- **No auto-renewal, ever.** Expired = manual repurchase. (Dev calls this headline-worthy in 2026.)
- Icons for all pieces: coffee / lunch / souvenir / gift.

⚠ **Precision warning for the motto.** Paid time is still sold per period ($4.99/mo, $15/6mo), it simply **never auto-renews**. So the exact, unbeatable claim is **"No auto-renewal. Ever."** — not the looser "No subscription." The forever tiers keep the **"rent vs own"** frame valid.

## Localized (same tiers, PPP + rails)

- **IN** ~₹129/429/899 (founding 699) + UPI Autopay.
- **BR** ~R$21/70/159 + Pix/boleto.
- **DE/FR** EUR 4.99/15/50/25 + PayPal/SEPA/CB, offline + GDPR wording.
- **JP** JPY-billed (~600/2000/3900 cap). **KR** (~₩5.5k/17.8k/39k cap) + Naver/Kakao Pay.
- **Processor:** Polar default (keys + activations), Stripe fallback.

## Positioning lines (dev-supplied, ours to rewrite)

- **"10 weeks of Wispr = forever with us."** Rent vs own.
- **"Same quality free. Cancelled doesn't count."** (print in-window)
- **"No server — nothing to retain, nothing to ban you for."**
- **"The floating ear"** (ear = signature; floating alone is table stakes).

## Restraints (binding)

No live-display claim ("speak, release, appear"). No Hindi % until measured (bar = Scribe 5.5% table format). No competitor names in public copy. Speak-back = future tease only.

# PART B — Speak-back (language learners) — ROADMAP, future tense only

## The angle (dev-confirmed)

Speak-back (the app reads the transcription aloud) turns supEars from a dictation tool into a **language loop: speak → see → hear → compare → repeat.** That loop is what enthusiasts (shadowing), students (pronunciation self-check) and teachers (classroom demo) already do by hand. Offline + 26 talk languages makes it special: a student drills pt↔en, es↔en, fr↔en on a plane or in class with no account and nothing leaving the machine. **No cloud rival can claim that sentence.**

## What marketing MAY say today

- **"Speak-back is on the roadmap, designed offline-first like everything else."**
- Use cases: shadowing practice, pronunciation comparison (I said X, correct is Y), teacher-led listen-and-repeat, accessibility (hear what was written).
- Future tense. No date, no demo claim.

## What marketing MUST NOT claim

- No "ships in vX", no accuracy/voice numbers, **no demo video of it.**
- Reference material (`reference/speak.json/.py/.ts`) is **Edge TTS = ONLINE** — opposite of our architecture, will never ship as-is. Offline TTS engine is **unevaluated / unscheduled.**

## Copy seeds (ours to rewrite)

- **"Hear what you said — in the language you're learning."**
- Icons: ear (listen) + speech bubble (speak) + repeat arrow (drill).
- Video seed: 20s loop — student dictates FR, reads the correction, hears it back, repeats until match. No cloud, no account, classroom-safe.

## Q&A

- Works today? **No.** Reference only. Roadmap, researching, not scheduled.
- Online TTS shortcut? **No** — offline-first is non-negotiable; an online speak-back would break the "no server" promise.

## Owner questions raised by these two files

1. **Handoff §2 is now outdated on price.** §2 says "paid license with a 60-day trial"; the locked model is **30 days unlimited free, then 5 phrases/day forever.** Confirm so I can update §2 (I will not edit your standing orders without a yes), and confirm the **30-day money-back** guarantee still stands alongside.
2. **Public clearance for prices.** Dev says "use freely in copy planning"; handoff §2 says marketing never announces a price. **Are prices cleared for README/landing now, or planning + video only?**
3. **Motto final wording:** approve **"No auto-renewal. Ever."** as the precise line (with "rent vs own" for the forever tiers) instead of "No subscription."?
4. **Speak-back:** cleared to publish as roadmap teaser in copy/video, per the constraints above?

---
*Filed 2026-09-15 11:34 UTC · cost 0 · no public post · internal.*
