"""splice_cta.py — replace only the word 'supEars' in pt_cta.mp3 with the
AvaMultilingual winner take. Boundary = proportional prior refined by local
energy dip. 30ms crossfade, RMS-matched. Backup -> pt_cta_orig.mp3.
"""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
INV = HERE / "vo_invite"
CTA_TXT = "Tua palavra constrói o supEars."
AVA = HERE / "vo_brand" / "supEars_USAvaMultilingual_Supears.mp3"

SR = 48000


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def encode(y, dst):
    peak = float(np.abs(y).max())
    if peak > 0.99:
        y = y / peak * 0.99
    import tempfile
    raw = Path(tempfile.mkdtemp(prefix="spl_")) / "s.raw"
    (y * 32767).astype(np.int16).tofile(raw)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR),
                    "-ac", "1", "-i", str(raw), "-ar", "48000", "-ac", "1",
                    "-b:a", "192k", str(dst)], check=True)


def rms_win(y, i, w):
    seg = y[max(0, i - w):i + w]
    return float(np.sqrt((seg ** 2).mean() + 1e-12))


def main():
    cta = INV / "pt_cta.mp3"
    assert AVA.exists(), f"missing winner {AVA}"
    bak = INV / "pt_cta_orig.mp3"
    if not bak.exists():
        shutil.copy(cta, bak)
    a = decode(cta)
    b = decode(AVA)
    # trim ava edges (polish-style, light)
    w = SR // 100
    n = len(b) // w
    env = np.sqrt((b[:n * w].reshape(n, w) ** 2).mean(axis=1))
    loud = np.nonzero(20 * np.log10(env + 1e-12) > -42)[0]
    b = b[loud[0] * w - 240: (loud[-1] + 1) * w + 240]
    # RMS-match ava to cta voiced body
    ra = float(np.sqrt((a ** 2).mean())) or 1.0
    rb = float(np.sqrt((b ** 2).mean())) or 1.0
    b = b * min(3.0, ra / rb)
    # boundary: fixed 1.85s — mid-"o" vowel, before any Portuguese sibilant.
    # Antonio flows legato; the 30ms crossfade masks the vowel blend.
    cut = int(1.85 * SR)
    xf = int(0.03 * SR)
    left = a[:cut]
    j0, j1 = max(0, cut - xf), min(len(a), cut + xf)
    k = np.linspace(0, 1, j1 - j0) ** 2
    ov = j1 - j0
    seg_b = b[:ov] if len(b) >= ov else np.pad(b, (0, ov - len(b)))
    join = a[j0:j1] * (1 - k) + seg_b * k
    out = np.concatenate([left[:j0], join, b[ov:]])
    encode(out, cta)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(cta)],
                       capture_output=True, text=True, check=True)
    dur = round(float(r.stdout.strip()), 3)
    tj = INV / "pt_timings.json"
    rows = json.loads(tj.read_text(encoding="utf-8"))
    rows["cta"]["dur"] = dur
    tj.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK cta spliced @ {cut / SR:.2f}s, new dur {dur}s (backup pt_cta_orig.mp3)")


if __name__ == "__main__":
    main()
