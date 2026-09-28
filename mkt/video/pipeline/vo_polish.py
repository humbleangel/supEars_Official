"""vo_polish.py — de-robot the voice clips with numpy (deterministic):
cut leading silence (keep 30ms), trailing (keep 80ms), shrink internal
pauses >0.25s to 0.12s. Then re-probe and rewrite vo/timings.json +
vo2/timings.json. In-place (git restores on disaster).
"""
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
SR = 48000
SIL_DB = -42.0
WIN = SR // 100  # 10 ms
LEAD_KEEP = int(0.03 * SR)
TRAIL_KEEP = int(0.08 * SR)
PAUSE_MAX = 0.25
PAUSE_KEEP = 0.12


def decode(src: Path) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", str(SR),
         "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def silent_mask(y: np.ndarray) -> np.ndarray:
    n = len(y) // WIN
    if n == 0:
        return np.zeros(0, dtype=bool)
    w = y[:n * WIN].reshape(n, WIN)
    rms = np.sqrt((w ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(rms) < SIL_DB


def spans(mask: np.ndarray):
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def polish(y: np.ndarray) -> np.ndarray:
    nwin = len(y) // WIN
    y = y[:nwin * WIN]
    mask = silent_mask(y)
    cuts = []  # (win_start, win_end) to DELETE
    for a, b in spans(mask):
        dur = (b - a) * WIN / SR
        if a == 0:
            keep = LEAD_KEEP // WIN
            if b > keep:
                cuts.append((0, b - keep))
        elif b == nwin or (b == len(mask)):
            keep = TRAIL_KEEP // WIN
            if b - a > keep:
                cuts.append((b - keep, b))
        elif dur > PAUSE_MAX:
            keep = int(PAUSE_KEEP * SR) // WIN
            cuts.append((a, b - keep))
    if not cuts:
        return y
    keep_mask = np.ones(nwin, dtype=bool)
    for a, b in cuts:
        keep_mask[a:b] = False
    return y[np.repeat(keep_mask, WIN)[:len(y)]]


def encode(y: np.ndarray, dst: Path):
    work = Path(tempfile.mkdtemp(prefix="polish_"))
    raw = work / "p.raw"
    peak = float(np.abs(y).max())
    if peak > 0.99:
        y = y / peak * 0.99
    (y * 32767).astype(np.int16).tofile(raw)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR),
                    "-ac", "1", "-i", str(raw), "-ar", "48000", "-ac", "1",
                    "-b:a", "192k", str(dst)], check=True)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def refresh_timings(d: Path):
    tj = d / "timings.json"
    rows = json.loads(tj.read_text(encoding="utf-8"))
    for r in rows:
        f = r.get("file", "")
        p = HERE / f if "/" in f else d / f
        if not p.exists():
            p = d / f.split("/")[-1]
        r["dur"] = round(probe(p), 3)
    tj.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return rows


def main():
    saved = 0.0
    for d in (HERE / "vo", HERE / "vo2"):
        for mp3 in sorted(d.glob("*.mp3")):
            if mp3.name.startswith("vo_"):
                continue
            old_dur = probe(mp3)
            y = decode(mp3)
            assert y.size > SR // 4, f"decode failed: {mp3}"
            p = polish(y)
            assert len(p) > SR // 4, f"polish destroyed {mp3}"
            encode(p, mp3)
            new_dur = probe(mp3)
            saved += old_dur - new_dur
            print(f"{d.name}/{mp3.name}: {old_dur:.2f}s -> {new_dur:.2f}s")
    for d in (HERE / "vo", HERE / "vo2"):
        rows = refresh_timings(d)
        print(f"{d.name}/timings.json refreshed ({len(rows)} rows)")
    print(f"polish done, {saved:.1f}s of dead air removed")


if __name__ == "__main__":
    main()
