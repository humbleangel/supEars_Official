# Judgment: Remotion for our videos — YES, for the series template

> Filed 2026-09-23 00:08 UTC per owner order ("judge this tool"). Read the repo (60.1k stars, 4.6k forks) + license/pricing pages. INTERNAL.

## What it is

Remotion = videos as React code. You write a component (text, timing, transitions, captions), it renders real MP4 — exact fps, exact sizes, batch rendering, 1000+ pages of docs, 35+ templates.

## License: FREE for us, verified

- Free License covers **individuals and for-profit orgs up to 3 people, commercial use allowed**. We are one person → free, no signup, no watermark games.
- Paid Company License ($25/seat/mo; automators $0.01/render, $100 min) only matters at 4+ people. Revisit if we ever grow; until then, cost 0.

## Fit with our plan (countdown-tail micros)

- **One template renders all 8 videos.** Parametrize two strings (days-left, pitch line) → 18/14/10/7/5/3/1/launch fall out of one script, landscape + vertical cuts together. Our PNG→ffmpeg chain would hand-build 16 files; Remotion builds 16 from 1.
- Exact 24fps, exact 1080p/1080×1920, countdown end-card math in code (no manual frame counting).
- Captions/transitions included if we ever want motion beyond static text — without changing tools.
- Renders locally on CPU (text video is cheap); Node.js + `npx create-video` to start.

## Costs and cautions

- Cost: 0 (license) + learning curve (React/JS — owner already vibecodes; one template is a weekend-scale job, and templates exist to copy).
- Anti-slop still applies: Remotion makes template spam *easier*, so narration + varied edits per the video plan stay mandatory.
- Do NOT rebuild the pipeline around it on day one: keep ffmpeg as fallback; adopt Remotion for exactly one job (the countdown series). Expand only if it earns it.

## Verdict

**Adopt for the countdown-tail series.** Free, license-clean, purpose-built for "same video, 8 variants". Suggested file home if approved: `mkt/video/` with one `CountdownTails` composition. Owner decides; dev not needed.

---
*Filed 2026-09-23 00:08 UTC · cost 0 · no public post · internal.*
