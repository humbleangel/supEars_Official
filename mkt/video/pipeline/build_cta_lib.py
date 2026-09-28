"""build_cta_lib.py — universal CTA assembly: M lead (no brand word) + Ava stamp.
M cut at last block above -50dB + 80ms (keeps soft speech, kills digital black
— the -40dB floor ate syllables, -55 keeps hiss; -50 is the middle path proven
against PT data). Ava: first-sample trim + profile tail trim. 40ms xf join.
"""
import subprocess
from pathlib import Path

import numpy as np

SR = 48000
AVA = Path(__file__).parent / "vo_brand" / "supEars_USAvaMultilingual_Supears.mp3"


def decode(p):
    from vo_polish import decode as _d
    return _d(p)


def assemble_cta(m_path, dst):
    from vo_polish import encode, probe
    m = decode(Path(m_path))
    w = 4800
    n = len(m) // w
    prof = np.sqrt(m[:n * w].reshape(n, w) ** 2).mean(axis=1)
    loud = np.nonzero(20 * np.log10(prof + 1e-12) > -50)[0]
    assert len(loud) > 5, f"M clip silent: {m_path}"
    m = m[:min(len(m), (loud[-1] + 1) * w + int(0.08 * SR))]
    a = decode(AVA)
    first = int(np.nonzero(np.abs(a) > 0.02)[0][0])
    nn = len(a) // w
    pa = np.sqrt(a[:nn * w].reshape(nn, w) ** 2).mean(axis=1)
    la = np.nonzero(20 * np.log10(pa + 1e-12) > -40)[0]
    a = a[max(0, first - int(0.02 * SR)):min(len(a), (la[-1] + 1) * w + int(0.08 * SR))]
    ra = float(np.sqrt((m ** 2).mean())) or 1.0
    rb = float(np.sqrt((a ** 2).mean())) or 1.0
    a = a * min(3.0, ra / rb)
    f = int(0.01 * SR)
    m[-f:] *= np.linspace(1, 0, f)
    a[:f] *= np.linspace(0, 1, f)
    xf = int(0.04 * SR)
    k = np.linspace(0, 1, xf) ** 2
    out = np.concatenate([m[:-xf], m[-xf:] * (1 - k) + a[:xf] * k, a[xf:]])
    encode(out, Path(dst))
    d = probe(Path(dst))
    assert d > 1.0, "cta assembly too short"
    print(f"  cta assembled: {d:.2f}s")
    return round(d, 3)
