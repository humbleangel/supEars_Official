# 2026-09-23 01:20 UTC — v9: merged screens + bigger end logo

- Owner order: keep total time (14s) unchanged; tagline of screen 1 stays visible while the 26 languages flash below (screens 1+2 become one); end-card logo was too small (bigger than screen 1's, allowed).
- `mkt/video/render.ps1` edits: tagline now fades in 0–0.3s and holds until 9.7s (enable 0–10); language flashes moved below it (land y 540→660, vertical 1000→1090); end emblem 100→240 (land) / 90→220 (vertical), vertical Y 380→300 to clear the big number.
- Rendered `mkt/video/009-seventeen-days-v9.mp4` + `-vertical.mp4` (14s, 17 days). Frames verified: merged screen correct, end card logo big and clean, vertical no collisions.
- Cost: 0. Public post: NO (awaiting owner approval).
