#!/usr/bin/env python3
"""wallmix.py - build wall.wav: the 60 s stereo 48 kHz "wall of voices" layer.

24 vo2 clips stagger into the LANGUAGES chapter (17.1-33.5 s) at -13 dBFS peaks with
L/R pan rotation, duck to a -20 dBFS bed after 34 s, fade 47-49 s; en1/en2 join at
37.2/39.6 s at -9 dBFS. Jitter is md5-derived (no RNG). Usage: python wallmix.py
"""
import hashlib, json, math, re, subprocess
from pathlib import Path

PIPE = Path(__file__).resolve().parent
VO2, OUT, MANIFEST = PIPE / "vo2", PIPE / "wall.wav", PIPE / "wall_manifest.json"
BODY, BED = PIPE / "wall_body.tmp.wav", PIPE / "wall_bed.tmp.wav"
SR, TOTAL, START, STEP, JIT = 48000, 60.0, 17.1, 0.62, 0.2
PEAK_WALL, PEAK_EN, BED_DB = -13.0, -9.0, -20.0
BED_AT, DUCK_END, BED_END, FADE = 34.0, 36.0, 47.0, 2.0
FADE_S, LIMIT, BED_LEN = 0.06, 0.9, BED_END + FADE - BED_AT
DUCK = 10 ** ((BED_DB - PEAK_WALL) / 20)  # bus gain while holding the bed
SALT, DEPTHS = "wall:v1:", (0.70, 0.55, 0.82)  # 3-step pan rotation; even index = left


def run(args, check=True):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise SystemExit("ffmpeg failed: " + " ".join(map(str, args)) + "\n" + r.stderr[-1500:])
    return r


def peak_db(path):
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", run(
        ["ffmpeg", "-hide_banner", "-i", path, "-af", "volumedetect", "-f", "null", "-"]).stderr)
    if not m:
        raise SystemExit(f"volumedetect failed on {path}")
    return float(m.group(1))


def sched(i, cid):
    h = int(hashlib.md5((SALT + cid).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    s = max(START, min(33.5, START + i * STEP + (h * 2 - 1) * JIT))
    p = DEPTHS[(i // 2) % 3]
    return s, (-p if i % 2 == 0 else p)


def clip(idx, cid, dur, start, p, peak):
    th, ms = (p + 1) * math.pi / 4, round(start * 1000)
    g = peak - peak_db(VO2 / f"{cid}.mp3")
    return (f"[{idx}:a]aresample={SR},aformat=channel_layouts=mono,volume={g:.2f}dB,"
            f"pan=stereo|c0={math.cos(th):.3f}*c0|c1={math.sin(th):.3f}*c0,"
            f"afade=t=in:st=0:d={FADE_S},afade=t=out:st={dur - FADE_S:.3f}:d={FADE_S},"
            f"adelay={ms}|{ms}[w{idx}]")


def main():
    timings = json.loads((VO2 / "timings.json").read_text(encoding="utf-8"))
    missing = [t["id"] for t in timings if not (PIPE / t["file"]).exists()]
    print("source clips missing (skipped):", ", ".join(missing) if missing else "none")
    pieces, parts = [], []
    wall = [t for t in timings if t["id"] not in ("en1", "en2") and t["id"] not in missing]
    for i, t in enumerate(wall):
        s, p = sched(i, t["id"])
        pieces.append({"id": t["id"], "start": round(s, 3), "pan": round(p, 2),
                       "peak_db": PEAK_WALL, "dur": float(t["dur"])})
        parts.append(clip(i, t["id"], float(t["dur"]), s, p, PEAK_WALL))
    durs = {t["id"]: float(t["dur"]) for t in timings}
    en_parts = []
    for idx, cid, s, p in ((2, "en1", 37.2, -0.70), (3, "en2", 39.6, 0.70)):
        pieces.append({"id": cid, "start": s, "pan": p, "peak_db": PEAK_EN, "dur": durs[cid]})
        en_parts.append(clip(idx, cid, durs[cid], s, p, PEAK_EN))
    n = len(wall)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         *sum([["-i", VO2 / f"{t['id']}.mp3"] for t in wall], []),
         "-filter_complex",
         ";".join(parts) + ";" + "".join(f"[w{i}]" for i in range(n)) +
         f"amix=inputs={n}:normalize=0:duration=longest[out]",
         "-map", "[out]", "-ac", "2", "-ar", SR, "-c:a", "pcm_s16le", "-t", "35", BODY])
    d_ms = round(BED_AT * 1000)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", BODY, "-af",
         f"atrim=start={START}:end={START + BED_LEN:.1f},asetpts=PTS-STARTPTS,"
         f"volume={BED_DB - PEAK_WALL}dB,afade=t=out:st={BED_LEN - FADE:.1f}:d={FADE},"
         f"adelay={d_ms}|{d_ms}", "-ac", "2", "-ar", SR, "-c:a", "pcm_s16le", BED])
    expr = f"if(lt(t,{BED_AT}),1,if(lt(t,{DUCK_END}),1-{1 - DUCK:.6f}*(t-{BED_AT})/2,{DUCK:.6f}))"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", BODY, "-i", BED, "-i", VO2 / "en1.mp3", "-i", VO2 / "en2.mp3",
         "-filter_complex",
         ";".join(en_parts) + f";[0:a]volume=volume='{expr}':eval=frame[wall];"
         "[wall][1:a][w2][w3]amix=inputs=4:normalize=0:duration=longest,"
         f"alimiter=limit={LIMIT}:level=disabled,apad[out]",
         "-map", "[out]", "-ac", "2", "-ar", SR, "-c:a", "pcm_s16le", "-t", str(TOTAL), OUT])
    BODY.unlink(), BED.unlink()
    pieces.sort(key=lambda p: p["start"])
    MANIFEST.write_text(json.dumps([{k: p[k] for k in ("id", "start", "pan", "peak_db")}
                                    for p in pieces], indent=2), encoding="utf-8")
    # verify: format, peak, and overlap density per 1 s bucket
    st = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                         "stream=sample_rate,channels", "-of", "json", OUT]).stdout)["streams"][0]
    dur = float(json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "json", OUT]).stdout)["format"]["duration"])
    pk = peak_db(OUT)
    ok = st["channels"] == 2 and int(st["sample_rate"]) == SR and abs(dur - TOTAL) <= 0.05 and pk <= -0.5
    print(f"wall.wav: {st['channels']}ch {st['sample_rate']} Hz {dur:.3f} s peak {pk:.1f} dBFS -> "
          + ("OK" if ok else "FAIL"))
    iv = [(p["start"], p["start"] + p["dur"]) for p in pieces if p["id"] not in ("en1", "en2")]
    print("overlaps per 1 s bucket, 10 ms sampling (wall clips only):")
    lo, hi = 99, 0
    for s0 in range(17, 34):
        cs = [sum(1 for a, b in iv if a <= s0 + k / 100 < b) for k in range(100)]
        if 18 <= s0 <= 32:
            lo, hi = min(lo, max(cs)), max(hi, max(cs))
        print(f"  {s0:2d}-{s0 + 1:2d}s  min {min(cs)}  max {max(cs)}")
    print(f"steady-window bucket maxima (18-32 s): min {lo}, max {hi}; the 17 s ramp-in and 33 s "
          "dissolve fall below 3 by construction of the 0.62 s stagger")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
