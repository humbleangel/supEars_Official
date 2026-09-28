"""ring_raw.py — paint.rs VERBATIM math, fed with our real VO (the owner's proposal):
per frame: 50ms window -> 120 buckets, loudest SIGNED sample per bucket
(paint_circular_waveform), RMS level (rms_tail), NO smoothing anywhere.
Usage: python ring_raw.py <wav> <out.js> <var> <seconds> <fps> [--smooth N]
smooth N = causal moving average over N frames (tames jitter, keeps it live).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def main():
    src = Path(sys.argv[1])
    out_name, var, seconds, fps = sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    smooth = int(sys.argv[7]) if len(sys.argv) > 7 and sys.argv[6] == "--smooth" else 0
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", "48000",
         "-f", "f32le", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, dtype=np.float32).copy()
    sr = 48000
    nframes = int(seconds * fps)
    win_n = int(0.05 * sr)
    bands, levels = [], []
    for f in range(nframes):
        end = min(int(f / fps * sr), len(y))
        tail = y[max(0, end - win_n):end]
        if tail.size < 120:
            bands.extend([0] * 120)
            levels.append(0.0)
            continue
        idx = (np.arange(121) * tail.size / 120).astype(int)
        row = []
        for i in range(120):
            seg = tail[idx[i]:max(idx[i + 1], idx[i] + 1)]
            k = int(np.argmax(np.abs(seg)))
            peak = float(seg[k])
            row.append(int(round(max(-1.0, min(1.0, peak * 1.2)) * 127)))
        bands.extend(row)
        levels.append(round(float(np.sqrt((tail ** 2).mean())), 4))
    if smooth > 1:
        k = smooth
        lv = np.array(levels)
        levels = [round(float(lv[max(0, i - k + 1):i + 1].mean()), 4) for i in range(len(lv))]
        bd = np.array(bands, dtype=np.float32).reshape(-1, 120)
        acc = np.zeros_like(bd)
        run = np.zeros(120, dtype=np.float32)
        for i in range(len(bd)):
            run += bd[i]
            if i >= k:
                run -= bd[i - k]
            acc[i] = run / min(i + 1, k)
        bands = [int(round(v)) for v in acc.reshape(-1)]
    js = Path(__file__).parent / out_name
    js.write_text(var + " = " + json.dumps(
        {"fps": fps, "bands": bands, "levels": levels}) + ";\n", encoding="utf-8")
    hot = sum(1 for v in levels if v > 0.02)
    print(f"OK {js} ({js.stat().st_size}B): {nframes} frames@{fps}fps, {hot} hot")


if __name__ == "__main__":
    main()
