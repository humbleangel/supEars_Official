"""peaks_data.py — true-sample peaks for the scrolling waveform strip.
Per 10 ms: (min, max) int16 over the placed VO mix -> peaks_<lang>.js.
The strip draws the voice's own shape scrolling under a playhead.
Usage: python peaks_data.py mkt/video/pipeline/vo_invite/pt_placed.wav peaks_pt.js
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def main():
    src = Path(sys.argv[1])
    out_name = sys.argv[2]
    var = sys.argv[3] if len(sys.argv) > 3 else "window.PEAKS_PT"
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", "48000",
         "-f", "s16le", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    sr, step = 48000, 480  # 10 ms
    n = len(y) // step
    mn = [round(float(y[i * step:(i + 1) * step].min()), 4) for i in range(n)]
    mx = [round(float(y[i * step:(i + 1) * step].max()), 4) for i in range(n)]
    js = Path(__file__).parent / out_name
    js.write_text(var + " = " + json.dumps({"mn": mn, "mx": mx}) + ";\n", encoding="utf-8")
    hot = sum(1 for a, b in zip(mn, mx) if abs(a) + abs(b) > 0.02)
    print(f"OK {js} ({js.stat().st_size}B): {n} pairs, {hot} hot")


if __name__ == "__main__":
    main()
