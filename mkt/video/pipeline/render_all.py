"""One-command full pipeline for the 60s v6 promo. Orchestrates existing scripts only."""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
STILLS = "0,3.4,8.8,12.8,18.0,20.75,26.0,30.3,35.1,39.5,44.9,53.1"
DEFAULT_OUT = str(HERE.parent / "022-promo-v6-60s.mp4")


def run(cmd, step):
    """Run a step, echo output, abort with a clear message on failure."""
    r = subprocess.run([str(c) for c in cmd], cwd=HERE, capture_output=True, text=True)
    print(f"--- [{step}] $ {' '.join(str(c) for c in cmd)}\n{r.stdout}{r.stderr}")
    if r.returncode != 0:
        sys.exit(f"ABORT [{step}]: exit {r.returncode}\n{r.stdout}{r.stderr}")
    return r


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser(description="Full 60s v6 promo pipeline: cues->voice->bed->wall->stills->frames->mix->qa->contact.")
    ap.add_argument("--skip-bed", action="store_true", help="reuse mashup.wav after verifying 60.0s via ffprobe")
    ap.add_argument("--skip-stills", action="store_true", help="skip stills + contact sheet")
    ap.add_argument("--out", default=DEFAULT_OUT, help="final mp4 path")
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    r = run([PY, "build_cues.py"], "cues")  # 1
    if "readability violations: []" not in r.stdout:
        sys.exit(f"ABORT [cues]: readability violations not clean:\n{r.stdout}")
    run([PY, "mix_vo.py"], "voice")  # 2

    bed = HERE / "mashup.wav"  # 3
    if args.skip_bed:
        d = duration(bed)
        if abs(d - 60.0) > 0.1:
            sys.exit(f"ABORT [bed]: --skip-bed refused, mashup.wav is {d:.3f}s (want 60.0s)")
        print(f"--- [bed] skipped, reusing mashup.wav ({d:.3f}s)")
    else:
        run([PY, "mashup.py"], "bed")
    run([PY, "wallmix2.py"], "wall")  # 4

    stills_dir = Path(tempfile.mkdtemp(prefix="stills_"))  # 5
    if not args.skip_stills:
        r = run([PY, "render-promo.py", "--html", "promo_v6.html",
                 "--stills", STILLS, "--out", stills_dir], "stills")
        printed = [l.strip() for l in r.stdout.splitlines() if l.strip().endswith(".png")]
        missing = [p for p in printed if not Path(p).exists()]
        pngs = list(stills_dir.glob("*.png"))
        if len(pngs) < len(STILLS.split(",")):
            missing.append(f"expected {len(STILLS.split(','))} PNGs, found {len(pngs)} in {stills_dir}")
        if missing:
            sys.exit(f"ABORT [stills]: missing stills:\n" + "\n".join(missing))
    else:
        print("--- [stills] skipped")

    run([PY, "render-promo.py", "--html", "promo_v6.html", "--seconds", "60",  # 6
         "--fps", "30", "--score60", "--out", out], "frames")
    run([PY, "mix_v5.py", out], "mix")  # 7

    r = subprocess.run([PY, "analyze_video.py", str(out)], cwd=HERE,  # 8 (warn-only on PRE-DROP)
                       capture_output=True, text=True)
    print(f"--- [qa] $ analyze_video.py {out}\n{r.stdout}{r.stderr}")
    findings = [l for l in r.stdout.splitlines() if l.strip().startswith("-")]
    hard = [f for f in findings if any(k in f for k in ("HOLD", "FLAT", "FLASH"))]
    if hard:
        sys.exit(f"ABORT [qa]: hard findings:\n" + "\n".join(hard))
    if any("PRE-DROP" in f for f in findings):
        print("WARN [qa]: PRE-DROP findings (non-blocking)")
    elif r.returncode != 0:
        sys.exit(f"ABORT [qa]: unexpected findings:\n{r.stdout}")

    if not args.skip_stills:  # 9
        contact = out.with_name(out.stem + "_contact.png")
        run([PY, "contact_sheet.py", stills_dir, contact], "contact")
    print(f"OK pipeline complete -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
