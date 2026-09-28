"""mix_v9.py — ONE soundtrack (LONOWN) + voice collage. No wall, no SFX, no mashup.

Owner rule: single audio track philosophy — the bed is LONOWN only, voices ride over it.
Same audibility gate as v8: every VO window must measure >= +6 dB over bed-only floor.

Usage: python mix_v9.py <video.mp4>   (replaces its audio, safe-write)
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
LONOWN = Path(r"C:\Users\777\Downloads\LONOWN - AVANGARD (Slowed).wav")
VOX = HERE / "vo_collage.wav"


def run(cmd):
    subprocess.run(cmd, check=True)


def rms_db(path, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    if t is not None:
        cmd += ["-t", str(t)]
    cmd += ["-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    y = np.frombuffer(raw, dtype=np.float32)
    if y.size < 100:
        return -99.0
    return 10 * math.log10(float((y ** 2).mean()) + 1e-12)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--seconds", type=float, default=30.0)
    ap.add_argument("--bed-start", type=float, default=130.0)
    a = ap.parse_args()
    TOTAL, BED_START = float(a.seconds), float(a.bed_start)
    video = Path(a.video)
    assert video.exists(), f"missing {video}"
    for name, p in (("LONOWN", LONOWN), ("VOX", VOX)):
        assert p.exists() and p.stat().st_size > 20000, f"missing/small stem: {p}"
        r = rms_db(p)
        assert r > -50, f"stem silent: {name} ({r:.1f} dBFS)"
        print(f"stem {name}: full-file RMS {r:.1f} dBFS")

    work = Path(tempfile.mkdtemp(prefix="v9mix_"))
    graph = (
        f"[1:a]aresample=48000,atrim={BED_START}:{BED_START + TOTAL},asetpts=PTS-STARTPTS,"
        f"volume=-12dB,equalizer=f=300:t=q:w=1:g=-4,equalizer=f=2500:t=q:w=1.5:g=-4,"
        f"afade=t=in:st=0:d=0.8,afade=t=out:st={TOTAL - 1.5}:d=1.5[bed];"
        f"[2:a]aresample=48000,volume=+7dB,asplit=2[vox][voxsc];"
        f"[bed][voxsc]sidechaincompress=threshold=-24dB:ratio=5:attack=15:release=500[ducked];"
        f"[ducked][vox]amix=inputs=2:normalize=0,"
        f"loudnorm=I=-14:TP=-1.5:LRA=9[mix]"
    )
    vomap = work / "vonly.mp4"
    out = work / "out.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-map", "0:v", "-c:v", "copy", str(vomap)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vomap), "-i", str(LONOWN), "-i", str(VOX),
         "-filter_complex", graph, "-map", "0:v", "-map", "[mix]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
         "-movflags", "+faststart", str(out)])
    assert out.stat().st_size > 200000, "mix too small"

    fin = work / "final.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-map", "0:a", "-c:a", "copy", str(fin)])
    cues = json.loads((HERE / "collage_cues.js").read_text(encoding="utf-8")
                      .replace("window.COLLAGE = ", "").rstrip().rstrip(";"))
    vox_spans = sorted(cues["spans"])
    # floor = first two coverage gaps >= 0.6s (dynamic: works for 15/30/60)
    gaps = []
    prev = 0.0
    for s, e in vox_spans + [[TOTAL, TOTAL]]:
        if s - prev >= 0.6:
            gaps.append((prev + 0.05, min(0.6, s - prev - 0.1)))
        prev = max(prev, e)
    assert len(gaps) >= 2, "no clean bed-only gaps for floor measurement"
    floor = min(rms_db(fin, ss=g[0], t=g[1]) for g in gaps[:2])
    print(f"bed-only floor: {floor:.1f} dBFS (gaps {gaps[:2]})")
    worst, worst_s = 99.0, None
    for s, e in vox_spans:
        w = rms_db(fin, ss=s + 0.15, t=max(0.3, e - s - 0.3))
        margin = w - floor
        print(f"VO {s:5.2f}-{e:5.2f}: {w:6.1f} dBFS  (margin {margin:+5.1f} dB)")
        if margin < worst:
            worst, worst_s = margin, s
    assert worst >= 6.0, f"AUDIBILITY GATE FAILED: worst margin {worst:+.1f} dB @ {worst_s}"
    print(f"AUDIBILITY GATE PASSED: worst margin {worst:+.1f} dB, floor {floor:.1f} dBFS")

    vd = subprocess.run(["ffmpeg", "-v", "error", "-i", str(fin), "-af", "volumedetect",
                         "-f", "null", "-"], capture_output=True, text=True)
    for line in vd.stderr.splitlines():
        if "max_volume" in line:
            print("peak:", line.strip())
            assert "n/a" not in line and float(line.split(":")[1].split()[0]) < -1.0, "peak too hot"

    shutil.move(str(out), str(video))
    print("OK", video, video.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
