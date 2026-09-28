"""ring_data.py — the app's ring recipe (paint.rs) fed with the REAL voice energy.

For each video frame (30fps): take the 50ms of VO mix BEFORE frame time,
bucket into 120 buckets, keep the loudest signed sample per bucket (exactly
like paint_circular_waveform), quantize to int8. Plus per-frame RMS level
for the 16 energy bars (paint_waveform). Writes ring_data.js.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
FPS = 30
POINTS = 120
WIN_S = 0.05


def main():
    seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
    vox = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "vo_collage.wav"
    out_name = sys.argv[3] if len(sys.argv) > 3 else "ring_data.js"
    var = sys.argv[4] if len(sys.argv) > 4 else "window.RING"
    assert vox.exists(), f"missing VO {vox}"
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(vox), "-ac", "1", "-ar", "48000",
         "-f", "f32le", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, dtype=np.float32).copy()
    sr = 48000
    nframes = int(seconds * FPS)
    win_n = int(WIN_S * sr)
    # ENVELOPE (not raw shape): rectify + 25 Hz lowpass over the whole file,
    # normalize to the 99th percentile — syllabic energy, smooth by physics.
    # The 120 ring points then breathe with the voice instead of tracing
    # glottal cycles (which reads as thorns at cinematic scale).
    from scipy.signal import lfilter
    a = 1 - __import__("math").exp(-2 * __import__("math").pi * 25 / sr)
    env_all = lfilter([a], [1, -(1 - a)], np.abs(y).astype(np.float64))
    norm = float(np.percentile(env_all, 99)) or 1.0
    env_all = np.clip(env_all / norm, 0, 1)
    bands, levels = [], []
    held = [0] * POINTS
    for f in range(nframes):
        t = f / FPS
        end = min(int(t * sr), len(y))
        start = max(0, end - win_n)
        tail = y[start:end]
        seg = env_all[start:end]
        if seg.size < POINTS:
            bands.extend([0] * POINTS)
            levels.append(0.0)
            continue
        idx = (np.arange(POINTS + 1) * seg.size / POINTS).astype(int)
        row = []
        for i in range(POINTS):
            blk = seg[idx[i]:max(idx[i + 1], idx[i] + 1)]
            row.append(int(round(float(blk.mean()) * 127)))
        # peak-meter release so the breath flows between syllables
        if f == 0:
            held = row
        else:
            held = [h if v > h else h + (v - h) * 0.25 for h, v in zip(held, row)]
        bands.extend(held)
        lv = float(np.sqrt((tail ** 2).mean())) if tail.size else 0.0
        levels.append(round(lv if f == 0 else max(lv, levels[-1] * 0.7), 4))
    hot = sum(1 for v in levels if v > 0.02)
    js = HERE / out_name
    js.write_text(var + " = ", encoding="utf-8")
    with open(js, "a", encoding="utf-8") as f:
        json.dump({"fps": FPS, "points": POINTS, "bands": bands, "levels": levels}, f)
        f.write(";\n")
    print(f"OK {js} ({js.stat().st_size}B): {nframes} frames, {hot} hot "
          f"({hot / nframes * 100:.0f}% speaking)")
    assert hot > nframes * 0.3, "ring data mostly silent — wrong VO file?"


if __name__ == "__main__":
    main()
