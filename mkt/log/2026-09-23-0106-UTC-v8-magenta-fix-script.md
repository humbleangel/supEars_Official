# 2026-09-23 01:06 UTC — v8 magenta fix + render script

- Read dev answers (2 new files) → review filed: `mkt/research/2026-09-23-0106-UTC-dev-answers-review.md`. Headline: 10/10 beta countdown GREEN on owner approval (beta-invitation framing, not a public release promise — flag raised for owner on the "Download free" end card); cloud BYOK + ask-days built, wording/tutorial owed by us; Polar keys stay manual (offline verify can't read them).
- Fixed v7 magenta bug: screen blend ran in YUV — chroma math (128→192) painted first+last screens neon magenta. Fix: blend in RGB (gbrp) via black-canvas overlay then screen. Verified frames clean.
- Re-rendered both formats: `mkt/video/008-seventeen-days-v8.mp4` + `-vertical.mp4` (14s, 17 days, URL end card, fades on every element, music from frame one with end fade).
- Saved editable renderer `mkt/video/render.ps1` + `mkt/video/langs.txt`. Usage: `powershell -ExecutionPolicy Bypass -File mkt\video\render.ps1 -Days 17 -OutBase 008-seventeen-days-v8`. Language text goes through UTF-8 textfiles (PowerShell 5.1 native-arg encoding mangles raw non-ASCII); screen blend stays in RGB (comment in script says why).
- Cost: 0. Public post: NO (008 awaiting owner approval).
