# Invitation-video journey — PT baseline to 25 languages (2026-09-28)

## Arc

1. **Baseline PT** (`promo_invite_pt.html` → 027 60fps + 028 12fps, 21s, 6 blocks:
   opener → testimonial → hook → 4 doors → how → finale), LONOWN bed.
2. **First 24** (029–076, 30+12fps each, edge-tts voices, every mix gated).
3. **Night Drive era**: bed → #10 (CC-BY 1000Handz, credit in descriptions),
   hottest 21s @103s at +12dB. 077 proved the sound; 078–091 refined it with
   the owner in VLC, one fix per round:
   - dual-line testimonial (PT keystroke + EN translation, tall card, clear of stars)
   - plural doors on screen AND in VO ("Bugs, críticas, sugestões ou elogios")
   - HOW card spacing, per-language viewer handle (`NAME`, avatar letter derives)
   - synth SFX got its own 21s map (`score_invite`, a hit on every cut) + its own
     duck stage so risers punch through the hot bed
   - ring smoothed (causal avg 5f); whips on HOW + finale; brand on top of
     block 1; universal DOWNLOAD NOW! (always EN); strip slides fully out
     before it lands; 12fps post = σ0.35 blur + 5% grain (master stays clean)
   - standing QA rule: every line fit-checked in frame, all 25 langs
4. **All 24 rebuilt on the perfected baseline** (092–139) via MASTER port +
   localized handles + EN lines, two subagent waves, all gates passed.
5. **Translation-verb correction** (my mistake — see below): 24 new takes,
   rebuilt as 148–195 (v13).
6. **HOW overflow fixes**: FR/IT/EL/HI split via pipeline `|` marker (196–205,
   v14). Current finals per language:
   PT 090/091 · ES 148/149 · FR 196/197 · DE 152/153 · IT 198/199 · NL 156/157 ·
   EN 158/159 · RU 160/161 · UK 162/163 · PL 164/165 · CS 166/167 · HU 168/169 ·
   EL 200/201 · ZH 172/173 · JA 174/175 · KO 176/177 · VI 178/179 · TH 180/181 ·
   ID 182/183 · AR 184/185 · HI 204/205 · UR 188/189 · TR 190/191 · RO 192/193 ·
   SV 194/195. (Superseded: 029–076 v11, 077–089 PT drafts, 140–147, 202/203.)

## Mistakes made (so the next run doesn't repeat them)

- **Strip silently missing for 11 builds**: `peaks_ptnd\.js` backslash typo meant
  the data never inlined and `strip()` exited every frame. Caught by owner's
  eyes, not by review. Lesson: stills must assert key elements present.
- **Hand-split wiped by rebuild**: v12's in-spine fix died when v13
  regenerated spines from MASTER. Lesson: fixes live in translations/pipeline
  (`|` marker), never in generated files.
- **HI missed**: patch covered lang_a/b, HI lives in lang_d. Lesson: assert
  coverage counts (24/24) after batch edits.
- **Translation verb dropped**: carried old "writes only" testi into 24 langs
  instead of the baselined "translates" concept. Lesson: baseline deltas become
  a checklist before any batch run.

## Companion docs

- `ORCHESTRATOR_BRIEF.md`: voice-model table per language + rebuild checklist.
- `JOURNEY.md`: pipeline tools, gates, bugs-fixed register.
- `promo_storyboards.html`: 20 promo ad concepts v2 (everyday audiences).

## Standing rules for marketing actions

Cost 0 · nothing public without owner approval · new files only, never touch
renders · commits `-c user.name="marketing-agent" -c user.email=""` · log
efforts with `YYYY-MM-DD HH:mm UTC` · owner approves each video in VLC.
