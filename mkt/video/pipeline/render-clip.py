import argparse
import base64
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from playwright.sync_api import sync_playwright
from scipy.io import wavfile
from scipy.signal import butter, lfilter

HERE = Path(__file__).resolve().parent


def inline_assets(html: str) -> str:
    def repl(m: re.Match) -> str:
        p = HERE / m.group(1)
        if not p.exists():
            return m.group(0)
        return 'src="data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode() + '"'

    return re.sub(r'src="(caps/[^"]+)"', repl, html)


def score(path: Path, dur: float, sr: int = 48000) -> None:
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(7)

    def env(start, attack, decay, curve=1.0):
        e = np.zeros(n)
        i0 = int(start * sr)
        i1 = min(n, i0 + int((attack + decay) * sr))
        seg = np.arange(i1 - i0) / sr
        e[i0:i1] = np.clip(seg / max(attack, 1e-6), 0, 1) ** curve * np.exp(-seg / decay)
        return e

    out = np.zeros(n)

    out += 0.55 * np.sin(2 * np.pi * 58 * t) * env(0.10, 0.004, 0.30)
    out += 0.22 * np.sin(2 * np.pi * 87 * t) * env(0.10, 0.004, 0.18)

    noise = rng.normal(0, 1, n)
    b, a = butter(2, 0.25)
    out += 0.30 * lfilter(b, a, noise) * env(0.35, 0.6, 0.9)

    pad = (np.sin(2 * np.pi * 110 * t) + 0.6 * np.sin(2 * np.pi * 164.8 * t)
           + 0.35 * np.sin(2 * np.pi * 220 * t))
    pad *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.7 * t)
    out += 0.16 * pad * env(0.9, 0.9, 1.6)

    click = lfilter(*butter(4, 0.08), rng.normal(0, 1, n))
    out += 0.5 * click * env(2.45, 0.002, 0.05)

    out += 0.7 * np.sin(2 * np.pi * 46 * t) * env(3.85, 0.005, 0.55)
    shimmer = sum(np.sin(2 * np.pi * f * t) for f in (1180, 1770, 2360))
    out += 0.10 * shimmer * env(3.86, 0.004, 0.5)

    tail = 0.10 * lfilter(*butter(2, 0.06), rng.normal(0, 1, n)) * env(3.9, 0.25, 1.0)
    out += tail

    out[: int(0.005 * sr)] = 0
    fade = int(0.30 * sr)
    out[-fade:] *= np.linspace(1, 0, fade) ** 1.5
    out /= max(1e-9, np.abs(out).max()) * 1.08
    wavfile.write(path, sr, (out * 32767).astype(np.int16))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default=str(HERE / "frames.html"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=float, default=5.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--scale", type=int, default=1, help="supersample factor, downscaled on encode")
    args = ap.parse_args()

    total = int(round(args.seconds * args.fps))
    work = Path(tempfile.mkdtemp(prefix="supears_clip_"))
    frames = work / "f"
    frames.mkdir()

    src_html = Path(args.html)
    page_html = work / "frames.html"
    page_html.write_text(inline_assets(src_html.read_text(encoding="utf-8")), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": args.width * args.scale,
                                          "height": args.height * args.scale},
                                device_scale_factor=1)
        page.goto(page_html.resolve().as_uri())
        page.wait_for_function("window.__ready !== undefined")
        page.evaluate("window.__ready")
        for i in range(total):
            page.evaluate("t => window.__draw(t)", i / args.fps)
            page.screenshot(path=str(frames / f"{i:04d}.png"))
        browser.close()

    pngs = sorted(frames.glob("*.png"))
    assert len(pngs) == total, f"expected {total} frames, got {len(pngs)}"

    wav = work / "score.wav"
    score(wav, args.seconds)

    vf = []
    if args.scale != 1:
        vf = ["-vf", f"scale={args.width}:{args.height}:flags=lanczos"]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(args.fps), "-i", str(frames / "%04d.png"),
         "-i", str(wav), *vf,
         "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "160k",
         "-shortest", "-movflags", "+faststart", str(out)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    size = out.stat().st_size
    assert size > 20_000, f"suspiciously small output: {size}"
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
        capture_output=True, text=True).stdout.strip()
    print(f"OK {out} {size} bytes | {total} frames @{args.fps}fps | {dur}s | frames in {frames.parent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
