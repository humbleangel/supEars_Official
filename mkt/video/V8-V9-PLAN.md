# V8 (30s) / V9 (30s refined) PLAN — 2026-09-26

## 1. What went wrong in V7 (023) — root causes, not excuses
1. **VO buried, not missing.** Chain applied three `amix(normalize=0)` stages (÷4, ÷2, ÷2 on the
   voice bus) against ONE ÷2 on the mastered LONOWN bed, then loudnorm normalized to the BED.
   Result: voice ~12–15 dB under music = "no voices at all". Fix: per-stem gains (bed −14 dB
   base, VO +6 dB), ONE mix stage, hard duck (depth 12–18 dB), EQ carve on bed @300 Hz/2.5 kHz,
   and a measured audibility gate (VO-window RMS ≥ +6 dB over bed-only windows) or the mix FAILS.
2. **Ear not additive.** Dark icon drawn normal-blend over dark bg = invisible. Fix: `lighter`
   halo + brightness(1.6) + radial backplate punched behind it + bloom ring; stills-checked on
   EVERY background it sits on (light gold card AND dark grid).
3. **Grid static.** A grid that doesn't move is wallpaper. Fix: real 2001 grammar — perspective
   tunnel with z-velocity toward camera + slit-scan streak pass on transitions (per-column time
   smear) + warp starfield. The grid must FLY, not hang.
4. **Generic motion (AI slop markers).** Linear-feeling reveals, holds with nothing changing,
   effects competing. Fix per research: overshoot easing on every entrance, ghost motion-blur on
   fast moves, sequential (never simultaneous) reveals, one hero effect per beat, change
   something every ≤2 s, hook inside 1.5 s, contrast floor on all text.

## 2. Audio: the collage engine (`collage.py`, reusable for 15/30/60)
- Material: vo2/ 26 clips ALREADY alternate M/F (Antonio/Elvira/Henri/Katja/…/Brian/Ava).
  EN anchors: vo/ (male) + NEW female twins (AriaNeural) for hook/brand/privacy/cta2.
- Placement rule: next line starts `overlap` (0.5–0.7 s) BEFORE previous ends; alternate M/F
  strictly; language hits duck −4 dB under EN anchors (anchors = foreground, wall = texture).
- Stems: (1) LONOWN hottest 30 s @ −14 dB base, (2) VO collage @ +6 dB, (3) whisper wall @ −10 dB,
  (4) sub drop + riser SFX. Duck: threshold −24 dB, ratio 8, attack 15 ms, release 450 ms,
  hold 0.25 s (no un-duck between words). Master: loudnorm −14 LUFS / −1.5 TP.
- **Gates (mix fails if violated):** every stem non-silent (RMS > −50 dBFS); every VO window in
  the FINAL ≥ +6 dB over nearest bed-only window; true peak ≤ −1.5 dBTP.

## 3. V8 30 s beat sheet (6 beats × 5 s, one hero effect each)
| t | Beat | Hero | VO (M/F overlap) |
|---|------|------|------------------|
| 0–3 | HOOK | slit-scan whip-in, red flash | hook M (EN anchor) |
| 3–6 | BATTLE CRY | gold card slam + shake | brand F (EN anchor) |
| 6–12 | 2001 TUNNEL | flying perspective grid, ear dives through; flags streak past | 5 lang hits M/F (pt F? per vo2 order: es F, fr M, de F, it M, ru F…) |
| 12–18 | EAR HERO | additive ear + bloom ring + orbiting chips | 3 lang hits + es anchor overlap |
| 18–23 | PRIVACY | grid freeze → clean dark, chips lock | privacy M + 2 lang hits |
| 23–27 | HOW 1-2-3 | staggered slam cards | how F short |
| 27–30 | END CARD | emblem settle + date | cta2 F over last lang tail |

## 4. 15/30/60 cleverness
- `collage.py --seconds 15|30|60` + spines `promo_v7/v8/v9`: same stems, same gates.
- 15 s = beats 1,2,4-tail,7 condensed. 60 s = V6 spine re-fitted with collage VO + tunnel.
- V9 = V8 review fixes at FULL 1920×1080 + any new owner notes. No new engine, only fixes.

## 5. Review gates before V9
Stills @ 1.5/4/8/11/14/20/25/28.5 (hook readable? ear visible on both bgs? grid moving?
contrast floor?) + QA analyzer (holds ≤2.5 s) + stem RMS table + final audibility report.
Fix list → V9. Then log + commit. Cost 0. Nothing public without owner OK.
