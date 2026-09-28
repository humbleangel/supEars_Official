import subprocess
import numpy as np

raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", "mkt/video/pipeline/vo/brand.mp3",
     "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
    capture_output=True).stdout
y = np.frombuffer(raw, dtype=np.float32)
print("samples:", y.size)
w = 1600
for i in range(0, len(y), w):
    seg = y[i:i + w]
    db = 10 * np.log10((seg ** 2).mean() + 1e-12)
    print(f"{i / 16000:4.1f}s {db:6.1f} dB")
