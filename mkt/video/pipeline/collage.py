"""collage.py — overlapping M/F voice collage with verification + JS cues for the spine.

Usage: python collage.py --seconds 30
Reads vo/timings.json (EN anchors) + vo2/timings.json (language hits), places anchors at
fixed beat times and cascades language hits with OVERLAP (next starts before prev ends),
alternating M/F strictly. Writes vo_collage.wav + collage_cues.js (spine syncs text to voice).
Fails loudly if any stem is silent.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
VO = HERE / "vo"
VO2 = HERE / "vo2"

# voice -> gender (from voice2.py VOICES + en-US-GuyNeural M / AriaNeural F)
GENDER = {
    "pt-BR-AntonioNeural": "M", "es-ES-ElviraNeural": "F", "fr-FR-HenriNeural": "M",
    "de-DE-KatjaNeural": "F", "it-IT-DiegoNeural": "M", "ru-RU-SvetlanaNeural": "F",
    "zh-CN-YunxiNeural": "M", "ja-JP-NanamiNeural": "F", "ko-KR-InJoonNeural": "M",
    "nl-NL-FennaNeural": "F", "pl-PL-MarekNeural": "M", "tr-TR-EmelNeural": "F",
    "uk-UA-OstapNeural": "M", "hi-IN-SwaraNeural": "F", "ar-SA-HamedNeural": "M",
    "id-ID-GadisNeural": "F", "vi-VN-NamMinhNeural": "M", "ro-RO-AlinaNeural": "F",
    "el-GR-NestorasNeural": "M", "sv-SE-SofieNeural": "F", "cs-CZ-AntoninNeural": "M",
    "hu-HU-NoemiNeural": "F", "th-TH-NiwatNeural": "M", "ur-PK-UzmaNeural": "F",
    "en-US-BrianNeural": "M", "en-US-AvaNeural": "F",
    "en-US-GuyNeural": "M", "en-US-AriaNeural": "F",
}

# EN anchors: (file, start, level_db) — strict M/F alternation, matched to visual beats
ANCHORS_30 = [
    ("hook.mp3", 0.0, 0),       # M hook over HOOK beat
    ("brand_F.mp3", 3.2, 0),    # F brand over BATTLE CRY
    ("privacy.mp3", 18.2, 0),   # M privacy over PRIVACY beat
    ("how_F.mp3", 23.2, 0),     # F how over HOW cards
    ("cta2.mp3", 27.0, 0),      # M cta over END CARD tail
]
# 60s pilgrimage: trap (hook+brand), full 26-voice cascade, proof, release
ANCHORS_60 = [
    ("hook.mp3", 0.0, 0),
    ("brand_F.mp3", 4.2, 0),
    ("privacy.mp3", 38.8, 0),
    ("how_F.mp3", 44.6, 0),
    ("cta2.mp3", 55.3, 0),
]
ORDER_60 = ["pt", "es", "fr", "de", "it", "ru", "zh", "ja", "ko", "nl",
            "pl", "tr", "uk", "hi", "ar", "id", "vi", "ro", "el", "sv",
            "cs", "hu", "th", "ur", "en1", "en2"]
# language-hit cascade windows: (t_start, t_end, overlap)
# window 2 removed: 18.5-23.2 is a deliberate solo-anchor breath after the dense cascade
WINDOWS_30 = [(6.0, 16.2, 1.1)]
# short hits first (dense collage), strict M/F alternation preserved by the picker
ORDER_30 = ["uk", "ur", "cs", "ro", "ko", "tr", "zh", "ja", "ar", "sv",
            "pl", "hu", "nl", "el", "th", "id", "hi", "vi",
            "pt", "es", "fr", "de", "it", "ru", "en1", "en2"]


def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def rms_db(path, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    if t is not None:
        cmd += ["-t", str(t)]
    cmd += ["-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    if len(raw) < 100:
        return -99.0
    import struct
    n = len(raw) // 4
    import numpy as np
    y = np.frombuffer(raw, dtype=np.float32, count=n)
    import math
    v = float((y ** 2).mean())
    return 10 * math.log10(v + 1e-12)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=30)
    a = ap.parse_args()
    total = float(a.seconds)

    en_durs = {}
    dur_by_path = {}
    for f in VO.glob("*.mp3"):
        d = probe_dur(f)
        en_durs[f.name] = d
        dur_by_path[str(f)] = d
    hits = json.loads((VO2 / "timings.json").read_text(encoding="utf-8"))
    for h in hits:
        p = VO2 / f"{h['id']}.mp3"
        assert p.exists() and p.stat().st_size > 5000, f"missing/small: {p}"
        r = rms_db(p)
        assert r > -50, f"silent source: {p} ({r:.1f} dBFS)"
        h["gender"] = GENDER[h["voice"]]
        dur_by_path[str(p)] = h["dur"]

    if total == 30:
        anchors, windows = ANCHORS_30, WINDOWS_30
    elif total == 15:
        anchors = [("hook.mp3", 0.0, 0), ("brand_F.mp3", 2.6, 0), ("cta2.mp3", 12.2, 0)]
        windows = [(5.0, 11.8, 0.9)]
    elif total == 60:
        anchors, windows = ANCHORS_60, [(8.8, 37.5, 1.3)]
    else:
        print("only 15/30/60 wired", file=sys.stderr)
        sys.exit(2)

    placed = []  # (src_path, start, level_db, label, gender)
    for fname, start, lvl in anchors:
        src = VO / fname
        assert src.exists(), f"missing anchor {src}"
        g = "F" if fname.endswith("_F.mp3") else "M"
        placed.append((src, start, lvl, fname.replace(".mp3", ""), g))

    order = ORDER_60 if total == 60 else (
        ["pt", "es", "fr", "de", "it", "ru", "zh", "ja", "ko", "nl",
         "pl", "tr", "uk", "hi", "ar", "id", "vi", "ro", "el", "sv",
         "cs", "hu", "th", "ur", "en1", "en2"] if total != 30 else ORDER_30)
    by_id = {h["id"]: h for h in hits}
    anchor_starts = [s for _, s, _ in anchors]
    anchor_gender = [("F" if f.endswith("_F.mp3") else "M") for f, _, _ in anchors]
    anchor_spans = [(s, s + en_durs[f]) for f, s, _ in anchors]
    last_gender = None
    cues = []
    oi = 0
    for ws, we, ov in windows:
        # seed alternation from the last anchor at/before this window,
        # then carry across previously placed hits
        seed = [g for (s, g) in zip(anchor_starts, anchor_gender) if s <= ws + 0.5]
        last_gender = seed[-1] if seed else None
        for _, s, lvl, _, g in placed:
            if ws - 3.0 <= s <= ws + 0.5 and lvl < 0:
                last_gender = g
        t = ws
        iters = 0
        while t < we and oi < len(order) and iters < 400:
            iters += 1
            h = by_id[order[oi]]
            if h["gender"] == last_gender:
                oi += 1
                continue  # strict alternation, try next voice at same t
            e = t + h["dur"]
            mud = max([min(e, ae) - max(t, aas) for aas, ae in anchor_spans] + [0.0])
            if mud > 1.2:
                t += 0.4
                continue  # slide past the anchor, retry same voice later
            if any(abs(t - s) < 0.4 for s in anchor_starts):
                t += 0.45
                continue  # never co-start with an anchor
            last_gender = h["gender"]
            oi += 1
            placed.append((VO2 / f"{h['id']}.mp3", round(t, 3), -4, h["id"], h["gender"]))
            cues.append({"id": h["id"], "lang": h["lang"], "gender": h["gender"],
                         "start": round(t, 3), "dur": h["dur"]})
            t += h["dur"] - ov
    # post-pass safety net: drop any hit still overlapping an anchor by >1.2s
    def placed_end(p):
        src, s, _, label, _ = p
        return s + dur_by_path[str(src)]

    keep = []
    for p in placed:
        src, s, lvl, label, g = p
        if lvl == 0:
            keep.append(p)  # anchors always stay
            continue
        e = placed_end(p)
        clash = any(min(e, ae) - max(s, aas) > 1.2 for aas, ae in anchor_spans)
        if clash:
            print(f"drop muddy hit: {label} @ {s}")
            cues = [c for c in cues if c["id"] != label]
        else:
            keep.append(p)
    placed = keep

    # render: pad each to total, gain, mix in ONE amix (normalize=0) + compensate +6dB on VO
    import math as _math
    work = Path(tempfile.mkdtemp(prefix="collage_"))
    inputs, filt, mixlabels = [], [], []
    for i, (src, start, lvl, label, g) in enumerate(placed):
        inputs += ["-i", str(src)]
        ms = int(round(start * 1000))
        if lvl < 0:
            # unify loudness: language hits target -17 dBFS, anchors -15 (foreground)
            file_r = rms_db(src)
            gain = max(-2.0, min(8.0, -17.0 - file_r))
        else:
            file_r = rms_db(src)
            gain = max(-2.0, min(8.0, -15.0 - file_r))
        filt.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms},volume={gain:.1f}dB[s{i}]")
        mixlabels.append(f"[s{i}]")
    n = len(placed)
    filt.append("".join(mixlabels) + f"amix=inputs={n}:normalize=0,volume=+6dB,"
                f"alimiter=limit=0.89,apad=whole_dur={total}[vox]")
    out = HERE / "vo_collage.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt),
                    "-map", "[vox]", "-ar", "48000", "-ac", "1", str(out)], check=True)
    assert out.stat().st_size > 50000, "collage render too small"
    r = rms_db(out)
    assert r > -45, f"collage silent ({r:.1f} dBFS)"

    # per-hit audibility prediction: each hit window must contain energy
    print(f"{'start':>6} {'dur':>5} {'g':>1}  {'label':<8} {'winRMS':>7}")
    for src, start, lvl, label, g in sorted(placed, key=lambda p: p[1]):
        dur = dur_by_path[str(src)]
        w = rms_db(out, ss=start + 0.15, t=min(dur - 0.2, total - start - 0.2))
        flag = "" if w > -45 else "  <-- SILENT!"
        print(f"{start:6.2f} {dur:5.2f} {g:>1}  {label:<8} {w:7.1f}{flag}")
        assert w > -45, f"placed hit silent in mix: {label} @ {start}"

    js = HERE / "collage_cues.js"
    anchor_rows = [{"id": f.replace(".mp3", ""), "start": s, "dur": round(en_durs[f], 3)}
                   for f, s, _ in anchors]
    js.write_text("window.COLLAGE = " + json.dumps(
        {"anchors": anchor_rows, "hits": cues,
         "spans": [[s, s + d] for s, d in
                   [(a["start"], a["dur"]) for a in anchor_rows] +
                   [(h["start"], h["dur"]) for h in cues]]},
        ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"OK {out} ({out.stat().st_size}B) + {js}, {len(placed)} placed, {len(cues)} lang hits")


if __name__ == "__main__":
    main()
