# 2026-09-26 01:31 UTC — Video toolchain built + verified; message to dev

- Owner instruction: focus on the tool chain, then tell the coordinator what is being built.
- Installed the only two missing pieces: `playwright` (Python) + pinned Chromium. Present already: Node 24, Python 3.12, numpy 2.5, ffmpeg 9, Edge (unused - pinned Chromium keeps renders reproducible).
- Smoke test `mkt/video/pipeline/smoke.py` passes: JS canvas frames -> Playwright screenshots -> ffmpeg libx264 -> numpy/scipy-synthesised audio -> muxed mp4 (24 frames @ 24fps), with a blank-frame luminance guard.
- New capability: code-driven promo videos (canvas/WebGL motion graphics, own soundtrack, zero licences, variants per language/platform) - replaces the ffmpeg-text-slide + CC-BY-track class of work.
- Dev message filed: `D:\WORK_B\PRJS\supEars\mkt req\2026-09-26-0131-UTC-video-toolchain-and-public-release-promise.txt` - toolchain state, the page's public-release promise (needs a real public download on 10/10), free-tier/price confirmation, and the ask for public-safe app captures + OK to show the UI.
- Cost: 0. Public post: NO (internal notes only).
