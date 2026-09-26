"""Tile N still PNGs into a labeled grid (filenames as captions). stdlib + ffmpeg only."""
import math
import subprocess
import sys
from pathlib import Path


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    pngs = sorted(src.glob("*.png"))
    if not pngs:
        print(f"contact_sheet: no PNGs in {src}", file=sys.stderr)
        return 1
    n = len(pngs)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    tw, th, bar = 480, 270, 30  # ponytail: fixed thumb size, bigger only if sheet illegible
    inputs, chains = [], []
    for i, p in enumerate(pngs):
        inputs += ["-loop", "1", "-i", str(p)]
        tag = p.name.replace("'", "").replace(":", "_")
        chains.append(f"[{i}:v]scale={tw}:{th}:force_original_aspect_ratio=decrease,"
                      f"pad={tw}:{th + bar}:(ow-iw)/2:(oh-ih-bar)/2:color=black,"
                      f"drawtext=text='{tag}':fontsize=14:fontcolor=white:"
                      f"x=(w-text_w)/2:y=h-{bar}+6[v{i}]")
    chains.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,tile={cols}x{rows}[t]")
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(chains),
           "-map", "[t]", "-frames:v", "1", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:  # no libfreetype / missing font: retry as plain grid
        plain = [c.split(",drawtext")[0] + f"[v{i}]" for i, c in enumerate(chains[:-1])]
        plain.append(chains[-1])
        subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(plain),
                        "-map", "[t]", "-frames:v", "1", str(out)], check=True)
        print(f"contact sheet (unlabeled, no drawtext) -> {out} [{n} tiles {cols}x{rows}]")
    else:
        print(f"contact sheet -> {out} [{n} tiles {cols}x{rows}]")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python contact_sheet.py <stills dir> <out png>")
        sys.exit(2)
    sys.exit(main())
