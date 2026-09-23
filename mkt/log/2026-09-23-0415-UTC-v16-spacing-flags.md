# 2026-09-23 04:15 UTC — v16: spacing fixes + full flag set (80 flags)

- Owner order (3 items): (1) tighten end-card stack so the URL line isn't cut (zoom crop was clipping it in landscape); (2) tighten language screen: tagline → language name → (English) → flags → stop-line gaps; (3) add all flags judged relevant per language.
- Spacing: end card pulled up (17→DAYS TO GO gap ~26px; URL now at y=932 land / 1339 vertical, clear of the 1.10/1.20 zoom crop). Language screen: LangY 660→610 (land), 1090→1050 (vertical); Lang2/Flag/Stop follow tighter.
- Flags: 51 new flagcdn PNGs downloaded (80 total in `mkt/video/flags/`); `$FlagMap` expanded per the swarm research, e.g. English +in,ng,pk,ph · Portuguese +ao,mz,cv · Chinese +tw,sg,my,hk · Spanish +co,ar,pe,us · Arabic +dz,sd,ma,iq · Dutch +be,sr,aw,cw · Ukrainian +pl,ca,de · Romanian +md,it,de,es · Vietnamese +us,fr,au,cz. Composite builder now handles any flag count (was 1-2); hstack output needed explicit `-map` (fixed).
- Rendered `mkt/video/016-seventeen-days-v16.mp4` + `-vertical.mp4` (40s, 17 days). Frames verified: English shows 6 flags; end card fully visible in both orientations, URL no longer cut.
- Cost: 0. Public post: NO (awaiting owner approval).
