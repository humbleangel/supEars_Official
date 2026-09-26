# 2026-09-26 04:0x UTC — 30s masterpiece promo (018) rendered from scratch

**File:** `mkt/video/018-promo-masterpiece-30s.mp4` — 1920x1080, 30fps, 30.000s, H.264 + AAC stereo, 4.9 MB.
Rendered entirely in code: `promo30.html` (canvas scene) + `render-promo.py` (6 parallel Playwright
workers over 900 frames, numpy/scipy score, ffmpeg encode, loudnorm).

## Structure (every hit lands on a visual beat)
| Beat | Time | What happens | Sound |
|---|---|---|---|
| Boot | 0.0-3.2 | ear + idle emerald ring, slow dolly-in, tagline | sub boom + shimmer |
| Pain | 3.2-6.8 | "You pay every month." zoom-slam / "to type one sentence." zoom-out | whip streaks + staccato hits |
| Mechanism | 6.8-11.5 | three real icons in three live rings: Talk in (green idle) / Your input (red recording) / Write in (yellow busy) | three synced hits, "Right Alt" |
| The ear | 11.5-19.0 | hero: red recording ring with the app's real circular waveform, chips overlaid (Portuguese → English), then yellow busy pulse, then paste | the "voice" that drives the waveform + heartbeat pulse |
| Output | 19.0-23.5 | typewriter both languages in a terminal card, paste flash, caret | typing ticks + paste thunk |
| Proof | 23.5-27.2 | 5x5 grid = exactly 25 flags, staggered wave; "25 languages in." / "English out." | rising arpeggio |
| End | 27.2-30.0 | gold ring completes, emblem, wordmark, release date, offline line | impact + resolve chord |

## Exact code ports (not eyeballed)
- Ring + glyph phases straight from `ear.rs:259-296`: idle rgba(16,185,129,25) r=105·s; recording
  rgba(231,76,60) r=(104+raw·12)·s with waveform; busy rgba(255,225,0) r=(98+6f)·s at 184·s glyph.
- `paint.rs:63` circular waveform: 120 buckets, loudest peak per bucket with sign kept,
  r = base·(1 + clamp(peak·1.2,-1,1)·0.7), stroke 2.5·clamp(base/67.2, .5, 1).
- `paint.rs:37` radial waveform: 16 bars, alpha 140+level·115, len 8+level·34, stroke 3.5.
- `paint.rs:11-23` ring_light/ring_dark: hue kept, brightest channel pinned to 255/170 with alpha floors.

## Claims discipline (subagent fact-check vs code)
- Says "25 languages in. English out." — true (26 codes incl. auto-detect; output is English).
- No "5 phrases/day" claim (not enforced in code), no prices (no store yet), no streaming (parked).
- Version-free (README's 0.8.71 is 66 patches stale; app is 0.9.37).
- 100% offline / no account / no cloud: audio never leaves — true.

## Mix
- Synthesised in numpy/scipy, then ffmpeg loudnorm: **-17.7 LUFS integrated, -0.9 dBTP, LRA 6.4** (first pass measured +3.9 dBTP — AAC overshoot on the sub content, fixed by loudnorm).

## Process notes
- Beats reviewed as stills before rendering: caught 4 real defects (ear blown out to a white blob, the
  three slots mis-centred with one off-screen, icons drawn above their rings, illegible typed line) and
  one invisible element (chips passed alpha 0).
- Five language flags were missing from the asset folder (`vi, el, sv, cs, ur`); fetched vi/sv and
  completed el/cs/ur from the app's own gr/cz/pk so the grid is exactly 25 and the claim is provable.
- `--audio-only` remux path means mix iterations never re-render frames.
- Cost: 0. Public post: NO (internal, owner review pending).
