"""V4 final mix: phonk bed (locked grid) ducked under the placed VO, loudnorm master, mux.
Usage: python mix_final.py <rendered-mp4>"""
import subprocess
import sys
from pathlib import Path

HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
PHONK = Path(r"C:\Users\777\Downloads\MONTAGEM TOMADA.wav")
VO = HERE / "vo" / "vo_placed.wav"
OFFSET = 2.319  # phase-locked downbeat (measured 8.7x on-grid kick contrast)

out_mp4 = Path(sys.argv[1])
tmp = out_mp4.with_suffix(".remux.mp4")
subprocess.run(
    ["ffmpeg", "-y",
     "-i", str(out_mp4),
     "-ss", f"{OFFSET:.3f}", "-t", "60", "-i", str(PHONK),
     "-i", str(VO),
     "-filter_complex",
     "[1:a]aresample=48000,apad=whole_dur=60[bed];"
     "[2:a]aresample=48000[voice];"
     "[bed][voice]sidechaincompress=threshold=-21dB:ratio=5:attack=8:release=320[ducked];"
     "[ducked][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[mix]",
     "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
     "-shortest", "-movflags", "+faststart", str(tmp)],
    check=True)
tmp.replace(out_mp4)
print("OK", out_mp4, out_mp4.stat().st_size, "bytes")
