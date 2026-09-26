"""Multi-track phonk mashup on a locked 140 BPM grid (35 bars = 60.000s)."""
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.signal import butter, lfilter

D = Path(r"C:\Users\777\Downloads")
HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
SR = 48000
BPM = 140.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
TOTAL = 35 * BAR                       # 60.000s
work = Path(tempfile.mkdtemp(prefix="mash_"))

TRACKS = [
    "MONTAGEM TOMADA.wav",
    "sub_clair-brazilian-phonk-577761.mp3",
    "EEYUH! x Fluxxwave.mp3",
    "NUNCA MUDA (Slowed).wav",
    "LONOWN - AVANGARD (Slowed).wav",
    "Matushka Ultrafunk.wav",
    "Ogryzek - GLORY (PHONK).wav",
    "sosin-phonk-music-beat-580409.mp3",
]


def decode(p: Path, sr: int = 22050) -> np.ndarray:
    raw = work / (p.stem[:20] + f"_{sr}.raw")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(sr),
                    "-f", "f32le", str(raw)], check=True)
    return np.fromfile(raw, dtype=np.float32)


def onset_env(y: np.ndarray, sr: int, hop: int = 512) -> np.ndarray:
    fr = y[: len(y) // hop * hop].reshape(-1, hop)
    spec = np.abs(np.fft.rfft(fr * np.hanning(hop), axis=1))
    flux = np.maximum(0, np.diff(np.log1p(spec), axis=0)).sum(axis=1)
    env = flux - flux.mean()
    return np.maximum(env, 0)


def bpm_of(y: np.ndarray, sr: int) -> tuple[float, float]:
    """Interval-histogram: robust against subharmonics."""
    hop = 512
    env = onset_env(y, sr, hop)
    sf = sr / hop
    if env.size < 64:
        return 0.0, 0.0
    thr = env.mean() + 0.6 * env.std()
    peaks = [i for i in range(1, env.size - 1)
             if env[i] >= env[i - 1] and env[i] > env[i + 1] and env[i] > thr]
    if len(peaks) < 8:
        return 0.0, 0.0
    hist = {}
    for a_i, a in enumerate(peaks):
        for b in peaks[a_i + 1: a_i + 40]:
            dt = (b - a) / sf
            while dt < 0.30:
                dt *= 2
            while dt > 0.60:
                dt /= 2
            bpm = round(60.0 / dt)
            hist[bpm] = hist.get(bpm, 0) + 1
    if not hist:
        return 0.0, 0.0
    best = max(hist, key=lambda k: hist[k])
    # refine +-3 bpm with a fine correlation on the envelope
    best_f, best_v = float(best), -1e9
    for bpm in np.arange(best - 3, best + 3.01, 0.25):
        lag = int(round(60.0 / bpm * sf))
        if lag < 1 or lag >= env.size:
            continue
        v = float(np.dot(env[:-lag], env[lag:]) / (env.size - lag))
        if v > best_v:
            best_v, best_f = v, float(bpm)
    return best_f, best_v


def refit(bpm: float, lo: float = 0.82, hi: float = 1.22) -> tuple[float, float]:
    """Return (tempo factor to 140, folded bpm) trying x1, x2, x0.5."""
    cands = []
    for m in (1.0, 2.0, 0.5):
        b = bpm * m
        f = BPM / b
        if lo <= f <= hi:
            cands.append((abs(f - 1.0), f, b))
    if not cands:
        return 0.0, bpm
    cands.sort()
    return cands[0][1], cands[0][2]


def kick_phase(track: np.ndarray, sr: int) -> float:
    hop = 256
    fr = track[: len(track) // hop * hop].reshape(-1, hop)
    spec = np.abs(np.fft.rfft(fr * np.hanning(hop), axis=1))
    freqs = np.fft.rfftfreq(hop, 1 / sr)
    kb = (freqs >= 40) & (freqs <= 130)
    k = np.maximum(0, np.diff(spec[:, kb].sum(axis=1)))
    k /= k.max() + 1e-9
    sf = sr / hop
    a, b = int(1.0 * sf), int(min(len(k) / sf, 40.0) * sf)
    seg = k[a:b]
    best_ph, best_v = 0.0, -1.0
    for ms in range(0, int(BEAT * 1000), 5):
        ph = ms / 1000.0
        idx = ((np.arange(0, len(seg) / sf, BEAT) * sf) + int(ph * sf)).astype(int)
        idx = idx[(idx >= 0) & (idx < len(seg))]
        if idx.size == 0:
            continue
        v = float(seg[idx].mean())
        if v > best_v:
            best_v, best_ph = v, ph
    return best_ph


def stretch(p: Path, factor: float) -> Path:
    out = work / (p.stem[:20] + f"_x{factor:.4f}.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p),
                    "-filter:a", f"atempo={factor:.6f}", "-ar", str(SR), "-ac", "1", str(out)],
                   check=True)
    return out


def load48(p: Path) -> np.ndarray:
    raw = work / (p.stem[:20] + "_48.raw")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR),
                    "-f", "f32le", str(raw)], check=True)
    return np.fromfile(raw, dtype=np.float32)


def rms_windows(y: np.ndarray, win_s: float = 1.0) -> np.ndarray:
    w = int(win_s * SR)
    return np.sqrt((y[: len(y) // w * w].reshape(-1, w) ** 2).mean(axis=1))


print("== measuring ==")
info = {}
for name in TRACKS:
    p = D / name
    if not p.exists():
        print(f"MISSING {name}")
        continue
    y22 = decode(p)
    bpm, strength = bpm_of(y22, 22050)
    factor, folded = refit(bpm)
    if factor == 0.0:
        print(f"discard {name:44s} bpm={bpm:6.2f} (no fold lands in 0.82-1.22)")
        continue
    stretched = stretch(p, factor)
    # two-pass lock: correct from what the stretched file actually measures
    y22b = decode(stretched)
    bpm2, s2 = bpm_of(y22b, 22050)
    if bpm2 > 0 and abs(bpm2 - BPM) > 2.5:
        corr = BPM / bpm2
        if 0.8 <= corr <= 1.25:
            factor *= corr
            stretched = stretch(p, factor)
            y22b = decode(stretched)
            bpm2, s2 = bpm_of(y22b, 22050)
    if bpm2 > 0 and abs(bpm2 - BPM) > 3.5:
        print(f"discard {name:44s} still off after 2 passes: {bpm2:.2f}")
        continue
    y48 = load48(stretched)
    ph = kick_phase(y48, SR)
    energy = float(np.sqrt((y48 ** 2).mean()))
    info[name] = dict(y=y48, phase=ph, energy=energy, bpm=bpm2, factor=factor)
    print(f"keep    {name:44s} bpm={bpm:6.2f}->{bpm2:6.2f} x{factor:.4f} "
          f"phase={ph:.3f}s energy={energy:.3f} peak={s2:.1f}")

if not info:
    raise SystemExit("no usable tracks")

by_energy = sorted(info, key=lambda k: -info[k]["energy"])
print("\n== arrangement ==")
master = by_energy[0]
hard1 = by_energy[1] if len(by_energy) > 1 else by_energy[0]
hard2 = by_energy[2] if len(by_energy) > 2 else hard1
calm = by_energy[-1]

plan = [
    (0, 5, master, "hook"),                 # 0.000 - 8.571
    (5, 12, hard1, "mech"),                 # 8.571 - 20.571
    (12, 23, None, "wall"),                 # 20.571 - 39.429
    (23, 26, calm, "privacy"),              # 39.429 - 44.571
    (26, 31, None, "proof"),                # 44.571 - 53.143
    (31, 35, master, "cta"),                # 53.143 - 60.000
]
master_y = info[master]["y"]
rms = rms_windows(master_y)
loud5 = int(np.argmax(np.convolve(rms, np.ones(5) / 5, "valid")))
master_off = max(0.0, loud5 - 1.0)
print(f"master={master} energy={info[master]['energy']:.3f} start offset {master_off:.2f}s")

out = np.zeros(int(TOTAL * SR) + SR)
manifest = []


def place(at_bar: int, bars: int, track: str, src_off: float, tag: str, lp: float = 0.0):
    y = info[track]["y"]
    i0 = int(src_off * SR)
    m = int(bars * BAR * SR) + int(0.06 * SR)
    seg = y[i0:i0 + m]
    if seg.size < m:
        seg = np.pad(seg, (0, m - seg.size))
    if lp > 0:
        b, a = butter(2, lp)
        seg = lfilter(b, a, seg).astype(np.float32)
    dst = int(at_bar * BAR * SR)
    end = min(len(out), dst + seg.size)
    out[dst:end] += seg[: end - dst]
    manifest.append({"start": round(at_bar * BAR, 3), "end": round((at_bar + bars) * BAR, 3),
                     "track": track, "src_offset": round(src_off, 3), "bars": bars, "tag": tag})


for at, to, track, tag in plan:
    bars = to - at
    if tag == "wall":
        k = 0
        for b in range(at, to, 2):
            nb = min(2, to - b)
            t = hard1 if k % 2 == 0 else hard2
            place(b, nb, t, info[t]["phase"] + (k % 2) * 2 * BAR, tag)
            k += 1
    elif tag == "proof":
        k = 0
        for b in range(at, to, 2):
            nb = min(2, to - b)
            t = hard2 if k % 2 == 0 else hard1
            place(b, nb, t, info[t]["phase"] + (k % 2) * 2 * BAR, tag)
            k += 1
    elif tag == "privacy":
        place(at, bars, calm, info[calm]["phase"], tag, lp=0.02)
    elif tag == "cta":
        place(at, bars - 1, master, master_off, tag)
        b, a = butter(2, 0.03)
        tail = lfilter(b, a, master_y[int(master_off * SR): int(master_off * SR) + int(BAR * SR)]).astype(np.float32)
        dst = int((at + bars - 1) * BAR * SR)
        out[dst:dst + tail.size] += tail * 0.7
    elif tag == "hook":
        place(at, bars, master, master_off, tag)
    else:
        place(at, bars, track, info[track]["phase"], tag)

# section-boundary stabs
for at, to, track, tag in plan[1:]:
    src = info[hard2]["y"]
    ph = info[hard2]["phase"]
    stab = src[int(ph * SR): int((ph + 0.45) * SR)]
    dst = int(at * BAR * SR)
    env = np.exp(-np.arange(stab.size) / (0.12 * SR)).astype(np.float32)
    out[dst:dst + stab.size] += (stab * env * 0.55)[: len(out) - dst]

out = out[: int(TOTAL * SR)]
out = np.tanh(out * 0.9) / np.tanh(0.9)
out /= max(1e-9, np.abs(out).max()) * 1.05
fade = int(1.2 * SR)
out[-fade:] *= np.linspace(1, 0, fade) ** 1.3
wav = HERE / "mashup.wav"
import scipy.io.wavfile as wf
wf.write(wav, SR, (out * 32767).astype(np.int16))
(HERE / "mashup_manifest.json").write_text(json.dumps(manifest, indent=1))
print(f"\nOK {wav} {wav.stat().st_size} bytes, {len(out)/SR:.3f}s, peak {20*np.log10(np.abs(out).max()):.2f} dBFS")
print(json.dumps(manifest[:6], indent=1))
