"""mix_v8.py — LONOWN bed + VO collage + whisper wall + synth SFX, with AUDIBILITY GATE.

The V7 lesson: never trust a mix you haven't measured. This script:
1. asserts every stem non-silent,
2. ducks bed+wall under VO (depth ~12-15 dB), carves dialogue room @300Hz/2.5kHz,
3. masters to -14 LUFS / -1.5 TP,
4. FAILS unless every VO window in the FINAL measures >= +6 dB over bed-only floor.

Usage: python mix_v8.py <video.mp4>   (replaces its audio, safe-write)
"""
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
LONOWN = Path(r"C:\Users\777\Downloads\LONOWN - AVANGARD (Slowed).wav")
VOX = HERE / "vo_collage.wav"
WALL = HERE / "wall.wav"
BED_START = 130.0
TOTAL = 30.0


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
    video = Path(sys.argv[1])
    assert video.exists(), f"missing {video}"
    for p in (LONOWN, VOX, WALL):
        assert p.exists() and p.stat().st_size > 20000, f"missing/small stem: {p}"
    for name, p in (("LONOWN", LONOWN), ("VOX", VOX), ("WALL", WALL)):
        r = rms_db(p)  # full-file: wall starts with silence, must not false-trip
        assert r > -50, f"stem silent: {name} ({r:.1f} dBFS)"
        print(f"stem {name}: full-file RMS {r:.1f} dBFS")

    work = Path(tempfile.mkdtemp(prefix="v8mix_"))
    sfx = work / "sfx.wav"
    # synth SFX with numpy -> wav via ffmpeg raw
    sr = 48000
    n = int(TOTAL * sr)
    y = np.zeros(n, dtype=np.float64)

    def place(sig, at):
        i = int(at * sr)
        j = min(n, i + len(sig))
        y[i:j] += sig[: j - i]

    d = int(1.4 * sr)
    ph = np.cumsum(2 * np.pi * (60 * (28 / 60) ** (np.arange(d) / d)) / sr)
    place(0.9 * np.sin(ph) * np.exp(-3 * np.arange(d) / d), 6.0)
    d = int(2.0 * sr)
    nz = np.random.default_rng(7).standard_normal(d)
    riser = np.cumsum(nz)
    riser /= max(1e-9, np.abs(riser).max())
    k = np.linspace(0.05, 1.0, d)
    place(0.35 * riser * k ** 2, 25.0)
    ph2 = np.cumsum(2 * np.pi * np.linspace(220, 880, d) / sr)
    place(0.15 * np.sin(ph2) * k ** 2, 25.0)
    d = int(0.35 * sr)
    place(0.8 * np.sin(2 * np.pi * 50 * np.arange(d) / sr) * np.exp(-9 * np.arange(d) / d), 0.05)
    peak = np.abs(y).max()
    if peak > 0:
        y /= peak
    raw = work / "sfx.raw"
    (y * 32767).astype(np.int16).tofile(raw)
    run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(sr), "-ac", "1",
         "-i", str(raw), str(sfx)])

    graph = (
        f"[1:a]aresample=48000,atrim={BED_START}:{BED_START + TOTAL},asetpts=PTS-STARTPTS,"
        f"volume=-12dB,equalizer=f=300:t=q:w=1:g=-4,equalizer=f=2500:t=q:w=1.5:g=-4,"
        f"afade=t=in:st=0:d=0.8,afade=t=out:st={TOTAL - 1.5}:d=1.5[bed];"
        f"[2:a]aresample=48000,volume=+7dB,asplit=2[vox][voxsc];"
        f"[3:a]aresample=48000,atrim=15:45,asetpts=PTS-STARTPTS,volume=-12dB[wall];"
        f"[4:a]aresample=48000,volume=-8dB[sfx];"
        f"[bed][wall]amix=inputs=2:normalize=0[music];"
        f"[music][voxsc]sidechaincompress=threshold=-24dB:ratio=5:attack=15:release=500[ducked];"
        # VOX MUST be mixed back in: the sidechain detector consumes it without passing audio
        f"[ducked][vox][sfx]amix=inputs=3:normalize=0,"
        f"loudnorm=I=-14:TP=-1.5:LRA=9[mix]"
    )
    vomap = work / "vonly.mp4"
    out = work / "out.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-map", "0:v", "-c:v", "copy", str(vomap)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vomap), "-i", str(LONOWN), "-i", str(VOX),
         "-i", str(WALL), "-i", str(sfx), "-filter_complex", graph, "-map", "0:v", "-map", "[mix]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
         "-movflags", "+faststart", str(out)])
    assert out.stat().st_size > 200000, "mix too small"

    # ---- AUDIBILITY GATE on the final ----
    fin = work / "final.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-map", "0:a", "-c:a", "copy", str(fin)])
    floor = min(rms_db(fin, ss=2.5, t=0.6), rms_db(fin, ss=17.5, t=0.6))
    print(f"bed-only floor: {floor:.1f} dBFS")
    cues = json.loads((HERE / "collage_cues.js").read_text(encoding="utf-8")
                      .replace("window.COLLAGE = ", "").rstrip().rstrip(";"))
    vox_spans = [(0.0, 2.42), (3.2, 7.33), (18.2, 23.07), (23.2, 28.34), (27.0, 29.4)]
    vox_spans += [(h["start"], h["start"] + h["dur"]) for h in cues["hits"]]
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

    import shutil
    shutil.move(str(out), str(video))
    print("OK", video, video.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
