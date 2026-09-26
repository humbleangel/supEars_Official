# 2026-09-26 10:1x UTC — Storyboard v1: cue sheet + readability gate (nothing rendered yet)

Adopted from the successful streamer's workflow (their screenshots):
1. **One cue sheet is the single source of truth** for picture and sound (`cue_sheet.json`),
   built by `build_cues.py`: chapters, text cues with in/out + style + y, VO table with measured
   durations, sfx on the beat grid, counter widgets, camera keys.
2. **Readability gate**: the builder validates and prints violations; nothing renders until it prints
   `[]`. It caught 5 real problems on first run (two hero overlaps, a 1.0s on-screen line, a hero with
   no voice, an overlap with the Japanese segment) — all fixed, now zero.
3. **One BPM spine**: 140 BPM, beat 0.42857s, bar 1.71429s; chapter boundaries snap to bars
   (0, 5, 12, 23, 26, 31, 35 bars = 0, 8.571, 20.571, 39.429, 44.571, 53.143, 60.0).

## New voices this round
- Owner's hook line: **"Are you tired of paying subscriptions to talk?"** (opens the film).
- Our approved mottos now spoken: "Escape the Big Tech Corps subscriptions traps." (48.4s),
  "supEars. October tenth." (CTA).
- Two real user voices inside the wall: en-US-Jenny and en-US-Guy reading actual demand-wall quotes.
- VO plan rebuilt: 14 lines, every gap >= 0.25s, verified by the script.

## Storyboard (approved structure, pending owner sign-off)
HOOK 0.0-8.6 · hook question -> "You pay every month." -> a real user quote
MECH 8.6-20.6 · tagline on the crest -> Click. / Speak. / Magic. -> live draft bubble -> battle cry
WALL 20.6-39.4 · ES/FR/DE/JA heroes with live use-case windows + 26-voice wall + 4 user quotes + counters
PRIVACY 39.4-44.6 · 100% offline · No account. No cloud.
PROOF 44.6-53.1 · old CPUs · MegaCorps motto · 30 days free
CTA 53.1-60.0 · emblem, release date, offline line, Developed by HumbleAngel

## Still to wire (next, after sign-off)
promo_v6.html reads cue_sheet.json instead of hardcoded chapter code; add the streamer's
stills-first render step (render one frame per cue boundary, verify every requested file exists,
inspect, then render the full film).
- Cost: 0. Public post: NO.
