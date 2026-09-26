"""Phonk-style placeholder bed + click track on a shared 140BPM grid."""
import numpy as np
from scipy.io import wavfile

BPM = 140
BEAT = 60 / BPM
BAR = 4 * BEAT
S16 = BEAT / 4  # 16th


def _norm(x, peak=0.80):
    m = np.max(np.abs(x)) + 1e-12
    return (x / m * peak).astype(np.float32)


def _save(path, x, sr):
    wavfile.write(path, sr, (np.clip(_norm(x), -1, 1) * 32767).astype(np.int16))


def _tone(f, n, sr, decay=0.0, det=0.0):
    t = np.arange(n) / sr
    y = np.sin(2 * np.pi * f * t)
    if det:
        y = y + 0.5 * np.sin(2 * np.pi * f * (1 + det) * t)
    if decay:
        y = y * np.exp(-t * decay)
    return y.astype(np.float32)


def score_phonk(path, dur=60.0, sr=48000):
    n = int(dur * sr)
    y = np.zeros(n, dtype=np.float32)
    rng = np.random.default_rng(7)

    def add(sig, t0):
        i = int(round(t0 / BEAT) * BEAT * sr)  # quantize to grid
        i = max(0, min(i, n - 1))
        j = min(n, i + len(sig))
        y[i:j] += sig[: j - i]

    # (a) detuned 808 sub: A1 F1 C2 G1, one root per 2 bars
    for k, midi in enumerate([33, 29, 36, 31] * 8):
        t0 = k * 2 * BAR
        if t0 >= dur:
            break
        f = 440 * 2 ** ((midi - 69) / 12)
        L = min(int(2 * BAR * sr), n - int(t0 * sr))
        t = np.arange(L) / sr
        env = np.minimum(1, t / 0.01) * np.minimum(1, (2 * BAR - t) / 0.15 + 0.2)
        add((np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.007 * t)
             + 0.25 * np.sin(4 * np.pi * f * t)) * env * 0.5, t0)
    # (b) closed hats on 16ths, off-beat accents + 32nd rolls
    n16 = int(dur / S16)
    for k in range(n16):
        v = 0.9 if k % 4 == 2 else (0.5 if k % 2 else 0.32)
        L = int(0.045 * sr)
        h = rng.standard_normal(L).astype(np.float32) * np.exp(-np.arange(L) / (sr * 0.008))
        add(h * v * 0.35, k * S16)
        if k % 32 == 31 and k * S16 + S16 / 2 < dur:  # 32nd roll
            for r in (1, 2):
                add(h[: int(0.03 * sr)] * 0.3, k * S16 + r * S16 / 3)
    # (c) dark bell motif: sparse minor 2nds A4-Bb4
    b = 0
    while b * 4 * BAR < dur:
        t0 = b * 4 * BAR + 2 * BEAT
        for st, midi in enumerate([69, 70, 69]):
            f = 440 * 2 ** ((midi - 69) / 12)
            L = int(0.6 * sr)
            add((_tone(f, L, sr, 5) + 0.4 * _tone(f * 2, L, sr, 7)) * 0.22, t0 + st * BEAT)
        b += 1
    # (d) risers into targets (1s, start quantized)
    for end in (9.04, 17.44, 44.61, 53.10):
        if end > dur:
            continue
        L = int(1.0 * sr)
        t = np.arange(L) / sr
        sw = np.sin(2 * np.pi * (400 * t + 1800 * t ** 2)).astype(np.float32)
        nz = rng.standard_normal(L).astype(np.float32)
        add((sw * 0.25 + nz * 0.12) * (t / 1.0) ** 2, end - 1.0)
    # (e) drop-fill at 36.88: duck 0.4s then slam back
    g = np.ones(n, dtype=np.float32)
    a, d = int(36.88 * sr), int(0.4 * sr)
    if a < n:
        d = min(d, n - a)
        q = d // 4
        g[a:a + q] = np.linspace(1, 0.1, q)
        g[a + q:a + 3 * q] = 0.1
        g[a + 3 * q:a + d] = np.linspace(0.1, 1, d - 3 * q)
        y = y * g
    # (f) resolve + fade last 1.5s
    f0 = int(max(0, (dur - 1.5) * sr))
    y[f0:] *= np.linspace(1, 0, n - f0).astype(np.float32)
    _save(path, y, sr)


def click_track(path, dur=60.0, sr=48000):
    n = int(dur * sr)
    y = np.zeros(n, dtype=np.float32)
    nb = int(dur / BEAT) + 1
    for k in range(nb):
        bar = k % 4 == 0
        f = 3000 if bar else 2000
        a = 0.6 if bar else 0.35
        L = int(0.03 * sr)
        add_i = int(round(k * BEAT * sr))
        if add_i >= n:
            break
        j = min(n, add_i + L)
        t = np.arange(j - add_i) / sr
        y[add_i:j] += (np.sin(2 * np.pi * f * t) * np.exp(-t * 120) * a).astype(np.float32)
    _save(path, y, sr)


if __name__ == "__main__":
    click_track(r"mkt\video\pipeline\click.wav")
    score_phonk(r"mkt\video\pipeline\phonk_demo.wav")
