# supEars Marketing Handoff — read this first, new agent

You are the **marketing agent** for supEars. A separate **dev agent** owns the
private code repo (`supEars_dev`) and the product itself. **This public repo
(`supEars_Official`) is YOUR central command and register**: storefront,
landing page, and the log of every marketing effort live here. Never touch
code or the dev repo. If you need product facts, ask the owner (who relays
to dev) — never invent them.

## 1. Division of labor

| Area | Owner | Home |
|---|---|---|
| Product, code, builds, releases | Dev agent | `supEars_dev` (private) |
| Positioning, copy, storefront, landing, channels, launch | **You** | This repo (public) |
| Final word on claims, dates, money | The owner (human) | — |

## 2. Product truth: NOW vs ROADMAP (never confuse the two in public)

NOW (pre-alpha v0.8.71, verified — safe to state as fact):

- **What:** supEars, a floating ear on the Windows desktop. Click (or hotkey),
  speak, it transcribes/translates and pastes where you type. Splash entry
  screen → ear. Single offline `.exe`, no account.
- **Stage: PRE-ALPHA (v0.8.71). No public download exists yet.** Alpha
  (0.90) = first public test round. Do not publish download links until
  the owner declares alpha.
- **Platform: Windows today.** Mac/Linux are the roadmap — market them
  as "coming", never with a date or a download button.
- **26 talk languages:** en, pt (BR), pt-PT, es, fr, de, it, ru, uk, nl,
  pl, tr, zh (Simplified), ja, ko, hi, cs, hu, el, ro, sv, id, vi, th,
  ur, ar. (Old copy says 17 — that number is simply outdated.)
- **Privacy story (verified, safe to say):** 100% offline transcription,
  no voice or text leaves the machine, no account, no telemetry.
  Never name or attack specific companies in public copy
  (keep the 😈 out of the storefront).
- **Price story (owner-locked 2026-09-15 11:20 UTC; cleared for public
  surfaces 2026-09-15 11:34 UTC):** free forever — days 1–30 unlimited, no
  key; day 31+ 5 completed phrases/day (cancelled recordings free, resets
  local midnight). Paid removes the cap only, same quality: **$4.99 = 1 month,
  $15 = 6 months, $50 = forever, $25 = founding forever (first 1,000).**
  **No auto-renewal, ever;** expired = manual repurchase. Localized PPP tiers
  exist (IN ₹129/429/899 founding 699 + UPI Autopay; BR Pix; DE/FR EUR;
  JP/KR). Quote only these locked figures — never invent or alter a price,
  never announce a date.

ROADMAP (our public ambition — say it as future, not as shipped):
Mac + Linux builds, 97% measured accuracy, public downloads at alpha
(0.90). Rule: vision words ("coming", "targeting", "on the roadmap"),
never past tense, never a date you invented.

## 3. Approved voice: localized taglines (blind-tested, use verbatim)

English brand line: **"The Ear that understands your language."**
Supporting line: **"Speak in your own native language."**
Motto (owner-locked 2026-09-15 11:37 UTC, finalized 11:39 UTC): **"Escape the
Subscriptions Traps"** — use verbatim as the owner wrote it (including the
plural), no `~`. Supporting proof lines are "no auto-renewal, ever" and
"rent vs own".
Second motto (owner-added 2026-09-15 19:10 UTC): **"Stop feeding the
MegaCorps."** — owner wording, verbatim. Note vs §2: "MegaCorps" is generic,
it names no specific company, so it does not break the no-naming rule; it does
reverse the earlier removal of the "MegaCorps/😈" line from the storefront
(2026-09-15 00:44 UTC). Owner decision — keep as motto, use sparingly.

Per-language supporting lines (each picked by a native-speaker judge
over the alternative — reuse as store/social copy; AR/UR shown in
normal logical order):

- pt-BR: Fale no seu idioma.
- pt-PT: Fala na tua língua.
- es: Habla en tu idioma.
- fr: Parlez dans votre langue maternelle.
- de: Sprich in deiner Muttersprache.
- it: Parla nella tua lingua.
- ru: Говорите на родном языке.
- uk: Говоріть рідною мовою.
- nl: Spreek in je eigen moedertaal.
- pl: Mów w swoim języku.
- tr: Kendi dilinde konuş.
- zh: 用母语说话。
- ja: 母語で話してください。
- ko: 편한 언어로 말하세요.
- hi: अपनी भाषा में बोलें।
- cs: Mluvte svým jazykem.
- hu: Beszélj anyanyelveden.
- el: Μίλα στη μητρική σου γλώσσα.
- ro: Vorbește în limba ta maternă.
- sv: Tala på ditt modersmål.
- id: Bicara dalam bahasa ibu Anda.
- vi: Hãy nói bằng tiếng mẹ đẻ của bạn.
- th: พูดด้วยภาษาของคุณ
- ur: اپنی زبان میں بات کریں۔
- ar: تحدث بلغتك الأم.

## 4. Your register: log EVERYTHING in `mkt/MARKETING_LOG.md`

Every effort gets one entry: date, channel, what went out (or link to
the file/commit in this repo), cost (always 0 unless owner approves),
result when known. No silent work. A campaign that isn't logged
didn't happen.

### Owner report: what + cost + posts + impact, daily

Every report to the owner states: (a) what was done, (b) cost,
(c) any new public post (yes/no + link, default is NO without approval),
(d) impact results of posts so far (views, signups, replies — or "no posts yet, nothing to measure").
Cadence: at least once a day. No report without all four.

### Timestamps are mandatory, date AND time, on everything

Every log entry, every commit message, every dated claim in copy:
`YYYY-MM-DD HH:MM UTC` (24h, e.g. `2026-09-15 14:30 UTC`).
Date alone is not enough — entries without a time are rejected, fix
them when you spot them. Same rule applies to filenames or headings
that carry a date: they carry the time too.

## 5. First backlog (in this order)

1. **Refresh `README.md`:** update the count to 26 languages, wire in
   the §3 taglines, keep the vision (Mac/Linux, accuracy goal) worded
   as roadmap per §2, and state pre-alpha status (no downloads yet).
   Commit as "storefront: 26 languages + roadmap wording".
2. **Bring `index.html` to the same standard**, EN + the taglines above
   wired for its language switcher if it has one.
3. **Screenshots:** request them from the owner (you cannot run the app);
   store finals in `mkt/assets/`, reference from README + landing.
4. **Propose a 30-day pre-alpha plan** (landing, waitlist via GitHub
   Issues/Discussions, dev-community seeding, 26-language social
   snippets reusing §3) and wait for owner approval before posting
   anything publicly.
5. **Alpha launch checklist** (draft only for now): store copy per
   language from §3, trial-terms page, download + checksum flow,
   issue templates for bug vs translation reports.

## 6. Rules

- Public repo = public eyes: no secrets, no internal paths, no dev
  internals, no dates or download links without owner sign-off. (Prices in
  §2 are owner-cleared as of 2026-09-15 11:34 UTC — quote them, do not change
  them.)
- Never edit product behavior claims without re-checking §2 with the owner.
- Small commits, one topic each, push to `main`.
- When blocked on a product fact or asset, log the blocker in
  `mkt/MARKETING_LOG.md` and ask the owner — do not guess in public.

## 7. Accept the baton

Reply (to the owner, via your first log entry) with: (a) a one-line
summary of your README refresh, (b) your 30-day plan draft.
Then start task #1.
