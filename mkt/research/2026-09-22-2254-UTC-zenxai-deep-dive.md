# ZenXai / ZenVoice deep dive (NOT Yash's ZenVoice)

> Filed 2026-09-22 22:54 UTC per owner order ("look deep, page and its links, all info"). 6 fetches + 2 searches. INTERNAL — names stay out of public copy.

## Identity (verified across Tracxn, LinkedIn, their sites)

- **ZenXai**, Chennai, Tamil Nadu, India. Founded 2024, **unfunded**. 11–50 staff (LinkedIn) / 17 (Tracxn). Contact `hello@zenxai.io`.
- Founders: Praveen T, Monalisha Anand (CMO), Harivikash Bakthavatchalam (LinkedIn headline: "Founder @ZenVoice | Building Voice AGI for the World from India"; also runs martech/edtech ventures — split focus again).
- Web: `zenxai.io` (enterprise agentic platform) → `voice.zenxai.io` (voice product) → `wbl.zenxai.io` (white-label). LinkedIn: `company/voicezenxai`.

## Product: B2B phone-call agents — a different lane from us

- **They automate business phone calls** (inbound support, outbound telecalling, appointment booking, lead qualification). **We do personal offline dictation.** No overlap: they sell to companies, we sell to humans. Not a direct competitor.
- Tamil-first multilingual (Chennai roots), white-label partner program, integrations wall (Salesforce, Stripe, Calendly, Epic EHR, Shopify...), industry pages (healthcare, real estate, legal, retail).
- Sales-led enterprise: no public pricing, "Start Application / Schedule Call". Our transparent locked prices are the opposite — and the contrast favors us.

## Broken pages (owner's eye confirmed, technically)

- `/` serves a **framework-level Next.js 404** in its own HTML (the route's notFound renders instead of the page) while meta tags still advertise the title — half-deployed site.
- `/pricing` (linked in their own nav) returns **HTTP 404**.
- `/partner` and `/signup` render fine. So: polished skin, rotten routes — exactly what you sensed.

## Trust gaps worth studying (their mistakes, our rules)

- "Trusted by 200+ Enterprise Partners", "70% cost savings", "5x faster scaling", "Reduce no-shows by 40%" — precise numbers, **zero proof, zero named customer, zero methodology**. This is why our "no % until measured" rule exists. Claims without receipts read as slop.
- Name collision: TWO products called ZenVoice exist (Yash's macOS app + this one) plus a `zenvoice.io` fintech — the market can't tell them apart. Lesson: our odd name is an asset; never dilute it.

## What to copy: their content marketing

- Their blog guide "AI Voice Agents in India" (May 2026, ~22 min) is genuinely good craft: language matrix (Tamil/Hindi/Telugu/Kannada/Malayalam + code-switching), TRAI compliance section, pricing-model explainer, FAQ, sourced market number (**Indian Voice AI: ~$153M 2024 → ~$958M 2030, 35.7% CAGR** — useful context for our India sequencing).
- Takeaway: long-form real guides rank and persuade. Our demand wall + promo pieces play the same game; keep writing them.

## Bottom line

- Not us, not against us: enterprise cloud phone agents vs personal offline dictation. Their lane validates that voice money flows in India; our lane (private, Windows, CPU, pay-once) is still empty.
- Watch item only: if they ever ship an offline personal tier, reassess. Until then, file and move on.

---
*Filed 2026-09-22 22:54 UTC · cost 0 · no public post · internal.*
