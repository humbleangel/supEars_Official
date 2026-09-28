"""mix_invite.py — LONOWN (single track) + placed invitation VO. Same gate rules.
Usage: python mix_invite.py <video.mp4> <lang> [--seconds 15]
VO placed from vo_invite/<lang>_timings.json at fixed map (hook/cats/how/cta).
"""
import argparse
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
BED15 = 142.0  # hottest 18s window (was 146 for 15s)

# lang: [(key, start)] — PT shifted +3.0s for the opener (rest untouched)
PLACES = {
    "pt": [("hook", 3.1), ("cats", 6.6), ("how", 11.0), ("cta", 15.0)],
}


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
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("lang")
    ap.add_argument("--seconds", type=float, default=15.0)
    a = ap.parse_args()
    TOTAL = float(a.seconds)
    video, lang = Path(a.video), a.lang
    assert video.exists()
    tj = json.loads((HERE / "vo_invite" / f"{lang}_timings.json").read_text(encoding="utf-8"))
    work = Path(tempfile.mkdtemp(prefix="inv_"))
    # place VO
    inputs, filt, labels = [], [], []
    spans = []
    for i, (key, start) in enumerate(PLACES[lang]):
        src = HERE / "vo_invite" / f"{lang}_{key}.mp3"
        assert src.exists() and src.stat().st_size > 3000, f"missing {src}"
        inputs += ["-i", str(src)]
        ms = int(round(start * 1000))
        filt.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms}[s{i}]")
        labels.append(f"[s{i}]")
        spans.append((start, start + tj[key]["dur"]))
    n = len(spans)
    filt.append("".join(labels) + f"amix=inputs={n}:normalize=0,volume=+6dB,"
                f"alimiter=limit=0.89,apad=whole_dur={TOTAL}[vox]")
    vox = work / "vox.wav"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt),
         "-map", "[vox]", "-ar", "48000", "-ac", "1", str(vox)])
    assert rms_db(vox) > -45, "placed VO silent"

    graph = (
        f"[1:a]aresample=48000,atrim={BED15}:{BED15 + TOTAL},asetpts=PTS-STARTPTS,"
        f"volume=-7dB,equalizer=f=300:t=q:w=1:g=-4,equalizer=f=2500:t=q:w=1.5:g=-4,"
        f"afade=t=in:st=0:d=0.6,afade=t=out:st={TOTAL - 1.2}:d=1.2[bed];"
        f"[2:a]aresample=48000,volume=+7dB,asplit=2[vox][voxsc];"
        f"[bed][voxsc]sidechaincompress=threshold=-24dB:ratio=6:attack=15:release=500[ducked];"
        f"[ducked][vox]amix=inputs=2:normalize=0,"
        f"loudnorm=I=-14:TP=-1.5:LRA=9[mix]"
    )
    vomap = work / "vonly.mp4"
    out = work / "out.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-map", "0:v", "-c:v", "copy", str(vomap)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vomap), "-i", str(LONOWN), "-i", str(vox),
         "-filter_complex", graph, "-map", "0:v", "-map", "[mix]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
         "-movflags", "+faststart", str(out)])
    fin = work / "final.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-map", "0:a", "-c:a", "copy", str(fin)])
    gaps, prev = [], 0.0
    for s, e in sorted(spans) + [[TOTAL, TOTAL]]:
        if s - prev >= 0.6:
            gaps.append((prev + 0.05, min(0.6, s - prev - 0.1)))
        prev = max(prev, e)
    floor = min(rms_db(fin, ss=g[0], t=g[1]) for g in gaps[:2]) if len(gaps) >= 2 else -30.0
    # stem-truth gate: ducked-bed-only render (real vox drives sidechain,
    # silence takes its place in the mix) vs +7dB vox stem, per window.
    bedonly = work / "bedonly.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vomap), "-i", str(LONOWN),
         "-i", str(vox), "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono:d={TOTAL}",
         "-filter_complex",
         f"[1:a]aresample=48000,atrim={BED15}:{BED15 + TOTAL},asetpts=PTS-STARTPTS,"
         f"volume=-7dB,equalizer=f=300:t=q:w=1:g=-4,equalizer=f=2500:t=q:w=1.5:g=-4[bed];"
         f"[2:a]aresample=48000,volume=+7dB[voxsc];"
         f"[3:a]aresample=48000[null];"
         f"[bed][voxsc]sidechaincompress=threshold=-24dB:ratio=6:attack=15:release=500[ducked];"
         f"[ducked][null]amix=inputs=2:normalize=0,"
         f"loudnorm=I=-14:TP=-1.5:LRA=9[mix]",
         "-map", "[mix]", "-c:a", "pcm_s16le", "-ar", "16000", str(bedonly)])
    worst = 99.0
    for s, e in sorted(spans):
        w = rms_db(fin, ss=s + 0.1, t=max(0.3, e - s - 0.2))
        vb = rms_db(vox, ss=s + 0.1, t=max(0.3, e - s - 0.2)) + 7.0
        bb = rms_db(bedonly, ss=s + 0.1, t=max(0.3, e - s - 0.2))
        stem_margin = vb - bb
        worst = min(worst, stem_margin)
        print(f"VO {s:4.1f}-{e:4.1f}: final {w - floor:+5.1f} dB / stem {stem_margin:+5.1f} dB")
    assert worst >= 6.0, f"AUDIBILITY GATE FAILED ({worst:+.1f} dB)"
    print(f"GATE PASSED (worst stem margin {worst:+.1f} dB, floor {floor:.1f})")
    shutil.move(str(out), str(video))
    print("OK", video, video.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
