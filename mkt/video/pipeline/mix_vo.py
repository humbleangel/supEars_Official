"""Place the measured TTS clips at their absolute film times. No re-timing, ever."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
PLAN = {"hook": 0.00, "pain": 3.30, "brand": 8.80, "how1": 12.80, "how2": 17.30,
        "es": 20.90, "fr": 26.00, "de": 30.30, "ja": 35.10, "privacy": 39.60,
        "cpu": 44.90, "motto": 48.40, "free": 52.00, "cta2": 56.10}

timings = json.loads((HERE / "vo" / "timings.json").read_text(encoding="utf-8"))
by_id = {t["id"]: t for t in timings}
for extra in ("hook", "motto", "cta2", "user1", "user2"):
    f = HERE / "vo" / (extra + ".mp3")
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip()
    by_id[extra] = {"id": extra, "dur": round(float(d), 3)}
assert set(PLAN) <= set(by_id), f"missing durations: {set(PLAN) - set(by_id)}"

# prove no overlaps before building
order = sorted(PLAN, key=PLAN.get)
for a, b in zip(order, order[1:]):
    end_a = PLAN[a] + by_id[a]["dur"]
    assert end_a <= PLAN[b] + 1e-6, f"overlap: {a} ends {end_a:.2f}, {b} starts {PLAN[b]:.2f}"
    print(f"{a:8s} {PLAN[a]:5.2f} + {by_id[a]['dur']:.3f} = ends {end_a:5.2f}   next {b} at {PLAN[b]:5.2f}")

inputs, parts = [], []
for i, lid in enumerate(order):
    f = HERE / "vo" / (lid + ".mp3")
    assert f.exists() and f.stat().st_size > 1000, f"missing clip {f}"
    inputs += ["-i", str(f)]
    ms = int(round(PLAN[lid] * 1000))
    parts.append(f"[{i}]aresample=48000,adelay={ms}|{ms}[v{i}]")
parts.append("".join(f"[v{i}]" for i in range(len(order)))
             + f"amix=inputs={len(order)}:normalize=0:duration=longest[vout]")

out = HERE / "vo" / "vo_placed.wav"
subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(parts),
                "-map", "[vout]", "-t", "60", "-ac", "1", str(out)], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("OK", out, out.stat().st_size, "bytes")
