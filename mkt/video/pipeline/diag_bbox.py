import subprocess
import sys
import numpy as np

names = sys.argv[1:] or ["mkt/video/026-promo-v9-60s.mp4", "mkt/video/022-promo-v6-60s.mp4",
                         "mkt/video/024-promo-v8-30s.mp4"]
ss = "7"
if names and names[0].replace(".", "", 1).isdigit():
    ss = names.pop(0)
for name in names:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", ss, "-i", name, "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", name],
        capture_output=True, text=True).stdout.strip()
    w, h = [int(v) for v in p.split(",")]
    img = np.frombuffer(raw, dtype=np.uint8).reshape(h, w, 3)
    lum = img.astype(float).mean(axis=2)
    ys, xs = np.nonzero(lum > 8)
    print(f"{name}: {w}x{h}  content x:[{xs.min()}-{xs.max()}] y:[{ys.min()}-{ys.max()}]")
