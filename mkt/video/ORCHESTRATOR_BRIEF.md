# Orchestrator brief — invitation-video journey + voice-model findings (2026-09-28)

Baseline is READY (090 30fps + 091 12fps, PT Night Drive). This doc tells the
orchestrator what we learned so the other 24 languages ship fast and correct.

## 1. Journey in 10 lines

1. V8/V9 30s masters + 26-voice collage wall proved the pipeline (gated mixes).
2. PT invitation baseline: 6 blocks × 21s vertical (opener → testimonial → hook →
   4 doors → how → finale), 027 (60fps) + 028 (12fps), LONOWN bed.
3. All 25 languages rendered as 029–076 (30+12fps each), every mix gated ≥+6dB.
4. Bed moved to Night Drive #10 (CC-BY 1000Handz — credit in descriptions),
   hottest 21s @103s, +12dB. 077 proved the new sound.
5. Testimonial went dual-line (PT keystroke + EN translation, tall card).
6. Doors pluralized on screen AND in VO ("Bugs, críticas, sugestões ou elogios").
7. Synth score-SFX got its own 21s map (`score_invite`: hit on every cut) and its
   own duck stage so risers punch through the hot bed.
8. Ring smoothed (causal avg, 5 frames); strip re-appeared after a backslash typo
   (`peaks_ptnd\.js` never inlined — strip silently drew nothing for 11 builds).
9. Finale: DOWNLOAD NOW! (always EN) + strip slides fully out before it lands.
10. Post: 30fps master stays clean; 12fps deliverable gets σ0.35 blur + 5% grain.

## 2. Voice models per language — what talks best

SHIPPED (all 25, edge-tts, free, proven in production):

| lang | male (hook/cats/how/cta) | female (testimonial) |
|------|--------------------------|----------------------|
| pt | Antonio | Francisca |
| es | Alvaro | Elvira |
| fr | Henri | Denise |
| de | Conrad | Katja |
| it | Diego | Elsa |
| nl | Maarten | Colette |
| en | Guy (+Ava/Andrew brand stamp) | Aria |
| ru | Dmitry | Svetlana |
| uk | Ostap | Polina |
| pl | Marek | Zofia |
| cs | Antonin | Vlasta |
| hu | Tamas | Noemi |
| el | Nestoras | Athina |
| zh | Yunxi | Xiaoxiao |
| ja | Keita | Nanami |
| ko | InJoon | SunHi |
| vi | NamMinh | HoaiMy |
| th | Niwat | Premwadee |
| id | Ardi | Gadis |
| ar | Hamed | Zariyah |
| hi | Madhur | Swara |
| ur | Asad (Uzma-F fixed a bad take) | Uzma |
| tr | Ahmet | Emel |
| ro | Emil | Alina |
| sv | Mattias | Sofie |

Notes: edge-tts ESCAPES SSML (reads tags aloud) — prosody via rate/pitch params
only, pitch in Hz (`-20Hz`, never `-1st`). Rate-fit slow/fast takes into slot
durations (SLOTS in build_lang.py); polish with vo_polish.py (numpy) — NEVER
`ffmpeg silenceremove` (destroys files). Profile every clip (digital-black tails
ride through splices).

UPGRADE PATH (researched, phased, A/B each before swapping):
EN Kokoro af_heart/am_michael (or instant edge Ava/AndrewMultilingual); ES/IT/PT
Kokoro; DE Thorsten-high (M); RU Silero v5 MIT; UK ukrainian-tts Dmytro (PROVEN
here, CPU, free); ZH/JA/KO Qwen3-TTS int8; HI indic-parler; VI VieNeu;
ID NusaVoice. REJECTED: XTTS/Bark/Fish (license/speed), MMS (CC-BY-NC),
BridgeSpeak (paid key), anything before CPU/Windows check.

## 3. Per-language rebuild checklist (standing)

- Spine: synth from MASTER via build_lang.py (literal swaps — no template drift).
- `name` (viewer handle, localized common name — avatar letter auto-derives) +
  plural `chips` + `cats` VO matching the doors word-for-word.
- Fit-check EVERY line inside 1080 wide (FR overflowed once) — shrink/track.
- Timeline identical: testi ≤3.1s (ends before hook 6.8), cats ≤3.6s (ends
  before how 14.0). Rate-fit, don't slide beats.
- Data: ring_raw.py --smooth 5 + peaks_data.py from the FINAL mix, then render.
- Mix: `mix_invite.py <mp4> <lang> --seconds 21 --bed-file <ND#10> --bed-start
  103 --bed-gain 12 --sfx-gain 6 --score-invite` render; gate MUST pass ≥+6dB.
- QA: diag_bbox + stills @ 1.5/6.5/12.5/15.5/20.0 (brand? card? doors? spacing?
  strip out before DOWNLOAD NOW!?) + analyze_video.
- Post: 12fps companion `ffmpeg -vf "gblur=sigma=0.35,noise=alls=5:allf=t,fps=12"`
  with `-c:a copy`.
- Cost 0. Nothing public without owner OK. New files only — never touch renders.
  Commits `-c user.name="marketing-agent" -c user.email=""`. Owner approves each
  video in VLC before the next.
