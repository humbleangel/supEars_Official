"""Video QA analyzer: no long holds, no flat frames, no flashing, clean pre-drop silence.
Adopted from the reference workflow. Usage: python analyze_video.py <video.mp4> [drop_time]
Exit 0 = clean, 1 = findings. Prints a build-sheet-ready report.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HOLD_S = 2.0          # a static hold longer than this is flagged
DIFF_FLOOR = 1.6      # mean abs frame diff below this = hold (8-bit luma units)
FLAT_STD = 4.0        # frame std below this = flat frame
FLASH_MIN = 6         # luminance direction flips inside 1s = flashing
SIL_DB = -45.0        # pre-drop audio must stay below this


def decode_luma(video: Path, fps: float = 6.0):
    work = Path(tempfile.mkdtemp(prefix="qa_"))
    pat = work / "f_%05d.pgm"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
                    "-vf", f"fps={fps},format=gray,scale=480:270", "-f", "image2", str(pat)],
                   check=True)
    frames = []
    for f in sorted(work.glob("f_*.pgm")):
        raw = f.read_bytes()
        assert raw[:2] == b"P5", f"not P5: {f}"
        hdr_end = raw.index(b"255\n") + 4
        px = np.frombuffer(raw[hdr_end:], dtype=np.uint8).astype(np.float32)
        frames.append(px.reshape(270, 480))
    return np.stack(frames), fps


def decode_audio(video: Path, sr: int = 8000):
    work = Path(tempfile.mkdtemp(prefix="qa_"))
    raw = work / "a.raw"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-ac", "1", "-ar", str(sr),
                    "-f", "f32le", str(raw)], check=True)
    return np.fromfile(raw, dtype=np.float32), sr


def main() -> int:
    video = Path(sys.argv[1])
    drop = float(sys.argv[2]) if len(sys.argv) > 2 else None
    frames, fps = decode_luma(video)
    n = len(frames)
    diffs = np.array([np.abs(frames[i + 1] - frames[i]).mean() for i in range(n - 1)])
    stds = np.array([f.std() for f in frames])
    dt = 1.0 / fps

    findings = []
    # long holds
    hold = 0
    for i, d in enumerate(diffs):
        hold = hold + 1 if d < DIFF_FLOOR else 0
        if hold * dt >= HOLD_S and (i + 1 == len(diffs) or diffs[i + 1] >= DIFF_FLOOR):
            findings.append(f"HOLD {i*dt-hold*dt:.1f}-{(i+1)*dt:.1f}s "
                            f"({hold*dt:.1f}s static, diff {d:.2f})")
            hold = 0
    # flat frames
    for i, s in enumerate(stds):
        if s < FLAT_STD:
            findings.append(f"FLAT frame at {i*dt:.1f}s (std {s:.2f})")
    # flashing: luminance direction flips
    lum = frames.mean(axis=(1, 2))
    deriv = np.diff(lum)
    sgn = np.sign(deriv)
    for s0 in range(0, n - 1, int(fps)):
        seg = sgn[s0:s0 + int(fps)]
        flips = int(np.sum(seg[1:] * seg[:-1] < 0))
        if flips >= FLASH_MIN:
            findings.append(f"FLASH around {s0*dt:.1f}s ({flips} flips/s)")
    # pre-drop silence
    if drop is not None:
        y, sr = decode_audio(video)
        seg = y[int(max(0, drop - 0.6) * sr): int(drop * sr)]
        rms = float(np.sqrt((seg ** 2).mean())) if seg.size else 0.0
        db = 20 * np.log10(rms + 1e-9)
        if db > SIL_DB:
            findings.append(f"PRE-DROP NOISE at {drop:.2f}s ({db:.1f} dBFS > {SIL_DB})")
        else:
            print(f"pre-drop silence clean before {drop:.3f}s ({db:.1f} dBFS)")

    dur = n / fps
    print(f"QA {video.name}: {dur:.1f}s, {n} frames @ {fps}fps | "
          f"mean diff {diffs.mean():.2f}, min {diffs.min():.2f}, max {diffs.max():.2f}")
    if findings:
        print(f"FINDINGS ({len(findings)}):")
        for f in findings[:25]:
            print("  -", f)
        return 1
    print("clean: no long holds, no flat frames, no flashing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
