import argparse
import base64
import json
import multiprocessing as mp
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
BEATS = [0.0, 3.2, 6.8, 11.5, 19.0, 23.5, 27.2, 30.0]


def inline_assets(html: str) -> str:
    """Bake every referenced PNG into the page: file:// images taint the canvas."""

    def repl(m: re.Match) -> str:
        p = HERE / m.group(1)
        if not p.exists():
            return m.group(0)
        return 'src="data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode() + '"'

    out = re.sub(r'src="((?:caps|assets30)/[^"]+\.png)"', repl, html)
    out = re.sub(r"'assets30/flags/' \+ n \+ '\.png'", r"'FLAG_' + n", out)
    return out


def score(path: Path, dur: float, sr: int = 48000) -> None:
    """Every hit lands on a visual beat."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(11)
    out = np.zeros(n)

    def hit(at, f0, f1, decay, amp, curve=2.2):
        i0 = int(at * sr)
        seg = np.arange(min(n - i0, int(decay * 4 * sr))) / sr
        if seg.size == 0:
            return
        sweep = f0 + (f1 - f0) * (seg / seg[-1])
        env = np.exp(-seg / decay) * (1 - np.exp(-seg * 900)) ** curve
        out[i0:i0 + seg.size] += amp * np.sin(2 * np.pi * sweep * seg) * env

    def noise_hit(at, decay, amp, cut=0.22, q=2.0):
        i0 = int(at * sr)
        seg = np.arange(min(n - i0, int(decay * 5 * sr))) / sr
        if seg.size == 0:
            return
        src = rng.normal(0, 1, seg.size)
        b, a = butter(2, cut)
        env = np.exp(-seg / decay) * (1 - np.exp(-seg * 1400))
        out[i0:i0 + seg.size] += amp * lfilter(b, a, src) * env

    def riser(frm, to, amp, cut0=0.06, cut1=0.5):
        i0, i1 = int(frm * sr), int(to * sr)
        if i1 <= i0:
            return
        m = i1 - i0
        tt = np.arange(m) / sr
        src = rng.normal(0, 1, m)
        nyq = 0.5 * (cut0 + (cut1 - cut0) * (tt / tt[-1]))
        acc = np.zeros(m)
        srcf = src.copy()
        for k in range(6):
            b, a = butter(2, float(np.clip(nyq[k::6].mean() if len(nyq) > k else nyq[-1], 0.01, 0.9)))
            acc += lfilter(b, a, srcf) / 6
        env = (tt / tt[-1]) ** 2.1
        out[i0:i1] += amp * acc * env

    def pad(frm, to, amp, roots=(55.0, 82.41, 110.0, 164.81), trem=0.23):
        i0, i1 = int(frm * sr), int(to * sr)
        m = i1 - i0
        if m <= 0:
            return
        tt = np.arange(m) / sr
        v = sum(np.sin(2 * np.pi * f * tt) for f in roots) / len(roots)
        v *= 0.62 + 0.38 * np.sin(2 * np.pi * trem * tt)
        v *= np.minimum(1, tt / 1.4) * np.minimum(1, (tt[-1] - tt) / 1.8 + 0.25)
        out[i0:i1] += amp * v

    def arp(frm, every, count, f0, f1, amp, decay=0.22):
        for k in range(count):
            f = lerp(f0, f1, k / max(1, count - 1))
            at = frm + k * every
            i0 = int(at * sr)
            m = min(n - i0, int(decay * 6 * sr))
            if m <= 0:
                continue
            tt = np.arange(m) / sr
            v = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(4 * np.pi * f * tt) + 0.2 * np.sin(6 * np.pi * f * tt))
            out[i0:i0 + m] += amp * v * np.exp(-tt / decay) * (1 - np.exp(-tt * 700))

    def voice(frm, to, amp):
        """the 'speech' that drives the on-screen waveform: formant bumps + glottal pulse"""
        i0, i1 = int(frm * sr), int(to * sr)
        m = i1 - i0
        if m <= 0:
            return
        tt = np.arange(m) / sr
        syl = 2.6
        ph = (tt + frm) * syl
        env = np.maximum(0, np.sin(ph * np.pi)) ** 0.55
        word = 0.55 + 0.45 * np.sin((tt + frm) * 1.35)
        glot = sum(np.sin(2 * np.pi * f * tt) / f for f in (120, 240, 360, 480))
        src = rng.normal(0, 1, m)
        f1b, f1a = butter(2, 0.05)
        f2b, f2a = butter(2, 0.45)
        voiced = 0.5 * glot + 0.9 * lfilter(f1b, f1a, src) + 0.35 * lfilter(f2b, f2a, src)
        out[i0:i1] += amp * voiced * env * word

    # bed
    pad(0.0, 30.0, 0.10)
    pad(6.6, 12.0, 0.09, (49.0, 73.42, 98.0))
    pad(11.4, 19.4, 0.12, (55.0, 82.41, 110.0, 164.81), 0.4)
    pad(23.4, 27.6, 0.11, (65.41, 98.0, 130.81, 196.0), 0.5)

    # beat markers: sub + air
    for b in BEATS[:-1]:
        amp = 0.62 if b in (0.0, 11.5, 27.2) else 0.44
        hit(b, 62, 38, 0.42, amp)
        noise_hit(b, 0.16, 0.22 if b else 0.3, 0.3)
    hit(27.2, 70, 34, 0.7, 0.7)
    noise_hit(27.2, 0.5, 0.18, 0.5)

    # transitions
    riser(2.5, 3.2, 0.16); riser(6.0, 6.8, 0.15); riser(18.2, 19.0, 0.15)
    riser(22.6, 23.5, 0.17, 0.1, 0.6); riser(26.3, 27.2, 0.2, 0.12, 0.7)

    # typing ticks (mechanism labels + typewriter)
    for at in (7.15, 8.55, 9.95, 19.4, 19.55, 19.7, 19.85, 20.0, 20.15, 20.3, 20.45, 20.6,
               20.75, 20.9, 21.0, 21.12, 21.24, 21.36, 21.48, 21.6, 21.72, 21.84, 21.96, 22.08,
               22.2, 22.32, 22.44, 22.56, 22.68, 22.8, 22.92):
        hit(at, 2100, 1400, 0.018, 0.055, 3.0)
    noise_hit(22.0, 0.09, 0.16, 0.5)   # the paste

    # the voice, 11.9 - 18.6
    voice(11.9, 15.35, 0.30)
    voice(15.5, 17.5, 0.16)
    # heartbeat pulse under the hero
    for k in range(16):
        at = 11.6 + k * 0.5
        hit(at, 55, 41, 0.16, 0.16)

    # proof-wave arpeggio, 24.2 - 26.6
    arp(24.2, 0.11, 22, 220.0, 880.0, 0.085, 0.13)
    # resolve chord at the end card
    for f in (110.0, 164.81, 220.0, 329.63):
        hit(28.0, f, f, 1.5, 0.11, 1.4)

    out[: int(0.004 * sr)] = 0
    fade = int(0.5 * sr)
    out[-fade:] *= np.linspace(1, 0, fade) ** 1.4

    # bus compression: social-video level without crushing the sub hits
    def follow(env, atk, rel):
        ka = float(np.exp(-1.0 / max(atk * sr, 1)))
        kr = float(np.exp(-1.0 / max(rel * sr, 1)))
        y = lfilter([1 - ka], [1, -ka], env)
        return lfilter([1 - kr], [1, -kr], y)

    env = follow(follow(np.abs(out), 0.004, 0.09), 0.02, 0.35) + 1e-9
    env_db = 20 * np.log10(env)
    over = np.maximum(env_db - (-26.0), 0.0)
    gain_db = -over * (1.0 - 1.0 / 4.0)
    gain_db = follow(follow(gain_db, 0.003, 0.12), 0.02, 0.3)
    out = out * 10 ** (gain_db / 20.0)
    out = np.tanh(out * 1.1) / np.tanh(1.1)
    peak = np.abs(out).max()
    if peak > 0:
        out = out / peak * 0.891          # -1.0 dBFS before widening

    # stereo: pad + arp get width, voice and impacts stay centred
    d = int(0.011 * sr)
    left = out.copy()
    right = np.concatenate([np.zeros(d), out[:-d]]) if d < len(out) else out.copy()
    width = 0.22 * (left - right)
    st = np.stack([left + width, right - width], axis=1)
    st /= max(1e-9, np.abs(st).max()) * 1.12   # lands at ~-1.0 dBFS
    wavfile.write(path, sr, (st * 32767).astype(np.int16))


def lerp(a, b, t):
    return a + (b - a) * t


def _render_slice(job):
    html_path, frames_dir, start, end, fps, w, h, scale = job
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": w * scale, "height": h * scale}, device_scale_factor=1)
        page.goto(Path(html_path).resolve().as_uri())
        page.evaluate("window.__ready")
        for i in range(start, end):
            page.evaluate("t => window.__draw(t)", i / fps)
            page.screenshot(path=str(Path(frames_dir) / f"{i:05d}.png"))
        ink = page.evaluate(
            "() => { const c = document.getElementById('c'), x = c.getContext('2d');"
            "const d = x.getImageData(0, 0, c.width, c.height).data; let s = 0;"
            "for (let i = 0; i < d.length; i += 400) s += d[i] + d[i+1] + d[i+2];"
            "return s / (d.length / 400) / 3; }"
        )
        browser.close()
    return ink


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default=str(HERE / "promo30.html"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=float, default=30.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--scale", type=int, default=1)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--audio-only", action="store_true",
                    help="rebuild the score and remux it onto an existing render (no frame work)")
    args = ap.parse_args()

    if args.audio_only:
        wav = Path(tempfile.gettempdir()) / "supears_score.wav"
        score(wav, args.seconds)
        tmp = Path(args.out).with_suffix(".remux.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(args.out), "-i", str(wav),
             "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-c:a", "aac", "-b:a", "192k", "-shortest",
             "-movflags", "+faststart", str(tmp)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tmp.replace(args.out)
        print(f"OK audio remuxed onto {args.out} ({Path(args.out).stat().st_size} bytes)")
        return 0

    total = int(round(args.seconds * args.fps))
    work = Path(tempfile.mkdtemp(prefix="supears_promo_"))
    frames = work / "f"
    frames.mkdir()

    src_html = Path(args.html)
    page_html = work / "page.html"
    html = inline_assets(src_html.read_text(encoding="utf-8"))
    flag_b64 = {f.stem: base64.b64encode(f.read_bytes()).decode()
                for f in sorted((HERE / "assets30" / "flags").glob("*.png"))}
    html = html.replace("const FLAGS = {};",
                        "const FLAG_B64 = " + json.dumps(flag_b64) + ";\nconst FLAGS = {};")
    html = html.replace("im.src = 'FLAG_' + n;",
                        "im.src = FLAG_B64[n] ? 'data:image/png;base64,' + FLAG_B64[n] : '';")
    page_html.write_text(html, encoding="utf-8")

    chunk = max(1, (total + args.workers - 1) // args.workers)
    jobs = []
    for s in range(0, total, chunk):
        e = min(total, s + chunk)
        jobs.append((str(page_html), str(frames), s, e, args.fps, args.width, args.height, args.scale))

    inks = []
    if args.workers > 1:
        with mp.Pool(min(args.workers, len(jobs))) as pool:
            inks = pool.map(_render_slice, jobs)
    else:
        inks = [_render_slice(j) for j in jobs]

    pngs = sorted(frames.glob("*.png"))
    assert len(pngs) == total, f"expected {total} frames, got {len(pngs)}"
    dark = [i for i, ink in enumerate(inks) if ink < 0.35]
    if dark:
        raise SystemExit(f"slices too dark (mean luminance): {inks}")

    wav = work / "score.wav"
    score(wav, args.seconds)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = ["-vf", f"scale={args.width}:{args.height}:flags=lanczos"] if args.scale != 1 else []
    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(args.fps), "-i", str(frames / "%05d.png"),
         "-i", str(wav), *vf, "-c:v", "libx264", "-preset", "slow", "-crf", "17",
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(out)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
    print(f"OK {out} {out.stat().st_size} bytes | {total} frames @{args.fps}fps | {dur}s | "
          f"{args.workers} workers | ink={[round(v,1) for v in inks]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
