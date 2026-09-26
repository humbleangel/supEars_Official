"""V5 mix: phonk mashup ducked under main VO + the voice wall. Safe-write, limited, verified."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
BED = HERE / "mashup.wav"
MAIN = HERE / "vo" / "vo_placed.wav"
WALL = HERE / "wall.wav"

VIDEO = Path(sys.argv[1])
GRAPH = (
    "[1:a]aresample=48000,apad=whole_dur=60[bed];"
    "[2:a]aresample=48000,asplit=2[main][main2];"
    "[3:a]aresample=48000,volume=-5dB[wall];"
    "[bed][main]sidechaincompress=threshold=-20dB:ratio=6:attack=8:release=300[ducked];"
    "[ducked][main2]amix=inputs=2:normalize=0[premix];"
    "[premix][wall]amix=inputs=2:normalize=0,"
    "loudnorm=I=-14:TP=-2.0:LRA=9,alimiter=limit=0.85[mix]"
)

for p in (VIDEO, BED, MAIN, WALL):
    assert p.exists() and p.stat().st_size > 10000, f"missing/empty: {p}"

work = Path(tempfile.mkdtemp(prefix="v5mix_"))
vonly = work / "vonly.mp4"
out = work / "out.mp4"

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(VIDEO), "-map", "0:v", "-c:v", "copy",
                str(vonly)], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error",
                "-i", str(vonly), "-i", str(BED), "-i", str(MAIN), "-i", str(WALL),
                "-filter_complex", GRAPH, "-map", "0:v", "-map", "[mix]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                "-movflags", "+faststart", str(out)], check=True)
assert out.stat().st_size > 100000, "mix produced too small a file"
shutil.move(str(out), str(VIDEO))
print("OK", VIDEO, VIDEO.stat().st_size, "bytes")
