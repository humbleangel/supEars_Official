# supEars promo pipeline — JOURNEY (2026-09-25 → 2026-09-28)

How the V9 masterpiece, the 26 voice collage and the PT invitation baseline were
built. Read this before producing the other 24 language versions.

## 1. What exists and works (proven in production)

- **Voice wall** (`voice2.py`): 26 clips, 24 languages + 2 EN, strict M/F alternation,
  per-clip rates, `vo2/timings.json`. Voices in `VOICES` dict.
- **Collage engine** (`collage.py --seconds 15|30|60`): anchors at fixed beats +
  language cascade with overlap, strict M/F seeding, mud-avoidance (slide past
  anchors, never co-start, drop >1.2s anchor overlaps), per-voice loudness
  unification (hits −17 dBFS, anchors −15), single `collage_cues.js` truth
  (anchors with durs + hits + spans). Emits placement audit with winRMS.
- **Mixers with AUDIBILITY GATE** (`mix_v8.py`, `mix_v9.py`, `mix_invite.py`):
  ONE soundtrack (LONOWN hottest window) + VO collage + optional score-SFX stem.
  Bed −7..−12 dB + EQ carve @300/2.5 kHz, VO +7 dB, duck thr −24 dB ratio 5–6,
  att 15 rel 500, loudnorm −14 LUFS/−1.5 TP. Gate: every VO window ≥ +6 dB over
  ducked-bed-only render (stem truth), true peak check. Gate FAILS LOUD — never ship red.
- **VO polish** (`vo_polish.py`, numpy, deterministic): cut lead (keep 30 ms),
  trail (80 ms), shrink internal pauses >0.25 s to 0.12 s. 29.8 s dead air cut.
  `ffmpeg silenceremove` DESTROYED a file (start+stop combined bug) — never use it.
- **App-true ring** (`ring_raw.py` + spine `ringEar`): paint.rs VERBATIM —
  120 buckets loudest-signed-sample per 50 ms, r = R·(1+peak·0.7), 16 bars
  len = 8+level·34 rotating, saturated twins — fed with OUR audio at 60 fps.
  Smoothed envelopes look DEAD; raw looks alive. Color: red speaking, emerald rest.
- **True-waveform strip** (`peaks_data.py` + spine `strip()`): per-10 ms min/max
  of the FINAL MIX scrolling under a playhead that surfs loudness (fwd on loud).
- **Renderer** (`render-promo.py`): Playwright screenshots per frame, bakes PNGs
  to data URIs + inlines `*.js`. Canvas auto-resizes to viewport; spines use
  `S = c.width/DESIGN_W`. `__draw` guard aborts on JS parse errors. ≤3 workers
  (6 OOM-crashes Chromium). `score()` fixed for sub-30 s (pad/riser/voice clamp).
- **QA** (`analyze_video.py`): holds/flats/flash report. Note: mean-diff dilutes
  small-element motion; calm finales are a choice, not always a bug.
- **Review loop**: stills with `-ss` AFTER `-i` (accurate); ktype reveals need
  settled-time stills. Subagents CAN review stills (vision works) — use them.
- **PT invitation baseline** (`promo_invite_pt.html` → 027 60 fps + 028 12 fps,
  21 s, 540×960): opener → testimonial → hook → 4 doors → how → finale.
  AvaMultilingual brand word spliced as sonic logo. Gate +7 dB.

## 2. Bugs found and fixed (do not reintroduce)

1. V7 silence: triple `amix(normalize=0)` buried VO ~15 dB. Fix: per-stem gains,
   ONE mix, gate. Also once FORGOT the vox bus in the final amix (total absence).
2. Quarter-frame finals: canvas 960×540 in a 1920×1080 viewport. Fix: resize
   canvas to viewport in render-promo + `S` scaling in spines. 022 repaired via
   crop+scale. Always check `diag_bbox.py` on finals.
3. edge-tts ESCAPES SSML (reads tags aloud, 23 s garbage). Prosody via
   rate/pitch params only. Pitch accepts Hz only (`-20Hz`, never `-1st`).
4. ktype DELETES text after `dur` (and fades last 20%). End-card lines need
   dur past video end + `hold: 0.99`.
5. Baked-page image race: building blurred bg before decode caches blank forever.
   Guard `complete && naturalWidth`.
6. Bake path: data JS must live in `pipeline/` (it globs there); `vo_invite/`
   files silently skip. `peaks_pt.js` vanished this way once.
7. Threshold trimmers ate soft syllables ("o" @ −45 dB) and kept hiss (−41 dB).
   Manual cuts from measured profiles only.
8. Digital black tails (Antonio 1 s) ride through splices — profile every file.
9. PowerShell `>` corrupts binaries (use `git --output` / python bytes).
10. Stray nested output paths (relative `--out` from pipeline cwd) — absolute paths.
11. Stale VLC stack = "eternal loop". Kill + `--no-repeat --no-loop`.
12. `__pycache__` committed once — `.gitignore` now covers.

## 3. Voice research (standing directive: use per-language findings)

- edge-tts keeps NL/PL/SV/RO/EL/HU/CS/TR-F/AR/UR/TH + all invite lines.
- UPGRADES (phased, each A/B first): EN Kokoro af_heart/am_michael (or instant
  edge Ava/AndrewMultilingual); ES/IT/PT-BR Kokoro; DE Thorsten-high (M);
  RU Silero v5 (MIT variant); UK ukrainian-tts (proven here: Dmytro works, CPU,
  free); ZH/JA/KO Qwen3-TTS int8; HI indic-parler; VI VieNeu; ID NusaVoice.
- REJECTED: XTTS/Bark/Fish (license/speed), MMS (CC-BY-NC non-commercial),
  BridgeSpeak (needs paid OpenAI key), any download before CPU/Win check.

## 4. Multi-language readiness — what is missing (1 prep sprint)

1. **Translations**: cats/how/testi/open lines exist ONLY in PT. Need 24×
   (hook+CTA already in `gen_invite_boards.py` INVITES; cats/how/testi missing).
2. **Spine template**: `promo_invite_pt.html` is PT-hardcoded (texts, CATS,
   flag, timings). Refactor to `promo_invite.html` + per-lang pack JS
   (texts, chips, flag code, VO map) — 1 job.
3. **Voices**: per-lang voice known (research table §3); generate + polish +
   probe per lang (script loop, same gates).
4. **Native OK**: owner ticks per language (storyboard checkboxes).
5. **QA per lang**: gate + bbox + 2 stills each (subagent review passes).
6. Open question: opener stays EN+Ava worldwide, or translated? (Recommend: keep EN.)

Then: 24 × (gen VO → data → render → mix → gate → review → commit). Pipeline
handles it; the prep sprint is the only blocker.
