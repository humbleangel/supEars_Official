"""Voice wall v2: 24 language voices + 2 real-user voices across the WALL chapter (21.2-46s)."""
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import scipy.io.wavfile as wf

HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
SR = 48000
DUR = 60.0
START, STAG = 21.2, 0.55
work = Path(tempfile.mkdtemp(prefix="wall2_"))

timings = json.loads((HERE / "vo2" / "timings.json").read_text(encoding="utf-8"))
ids = [t["id"] for t in timings if t["id"] not in ("en1", "en2")]

plan = [(tid, START + i * STAG, 0.7 if i % 2 == 0 else -0.7, -13.0) for i, tid in enumerate(ids)]
plan.append(("user1", 25.90, 0.5, -9.0))
plan.append(("user2", 30.90, -0.5, -9.0))

out = np.zeros((int(DUR * SR), 2), dtype=np.float64)


def load48(p: Path) -> np.ndarray:
    raw = work / "t.raw"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR),
                    "-f", "f32le", str(raw)], check=True)
    return np.fromfile(raw, dtype=np.float32)


for tid, st, pan, peak_db in plan:
    f = HERE / "vo2" / f"{tid}.mp3"
    if not f.exists():
        f = HERE / "vo" / f"{tid}.mp3"
    if not f.exists():
        print("skip missing", tid)
        continue
    y = load48(f).astype(np.float64)
    y /= max(1e-9, np.abs(y).max())
    y *= 10 ** (peak_db / 20.0)
    n = y.size
    fade = int(0.06 * SR)
    y[:fade] *= np.linspace(0, 1, fade)
    y[-fade:] *= np.linspace(1, 0, fade)
    gl = np.sqrt((1 - pan) / 2 + 0.0) if False else (1 - max(0, pan) * 0.5)
    gl = 1.0 - max(0.0, pan) * 0.5
    gr = 1.0 - max(0.0, -pan) * 0.5
    i0 = int(st * SR)
    end = min(out.shape[0], i0 + n)
    out[i0:end, 0] += y[: end - i0] * gl
    out[i0:end, 1] += y[: end - i0] * gr

t = np.arange(out.shape[0]) / SR
env = np.ones_like(t)
env[t >= 36.5] = np.linspace(1.0, 0.55, int((t >= 36.5).sum()))
env[t >= 44.0] = np.linspace(0.55, 0.0, int((t >= 44.0).sum()))
out *= env[:, None]

peak = np.abs(out).max()
out = out / peak * 0.95
wf.write(HERE / "wall.wav", SR, (out * 32767).astype(np.int16))
(HERE / "wall_manifest.json").write_text(json.dumps(
    [{"id": i, "start": round(s, 2), "pan": p, "peak_db": d} for i, s, p, d in plan], indent=1))

buckets = []
for s0 in range(21, 37):
    m = (t >= s0) & (t < s0 + 1)
    active = sum(1 for _, st, _, _ in plan if st <= s0 < st + 4.0)
    buckets.append(active)
print(f"OK wall.wav peak {20*np.log10(peak/peak):.1f} dBFS (normalized 0.95), "
      f"voices per second {buckets}, max {max(buckets)}")
