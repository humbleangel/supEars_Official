import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from playwright.sync_api import sync_playwright
from scipy.io import wavfile

W, H, FPS, N = 640, 360, 24, 24

HTML = """<html><body style="margin:0;background:#000">
<canvas id="c" width="640" height="360"></canvas>
<script>
const x = document.getElementById('c').getContext('2d');
function draw(t) {
  x.fillStyle = '#000'; x.fillRect(0, 0, 640, 360);
  x.fillStyle = '#73f2bd'; x.font = 'bold 48px Arial'; x.fillText('supEars', 40, 90);
  x.fillStyle = '#ffffff'; x.fillRect(40, 130, t * 20, 44);
  x.fillStyle = '#999999'; x.font = '16px Arial'; x.fillText('frame ' + t, 40, 220);
}
draw(0);
</script></body></html>"""


def main() -> int:
    out = Path(tempfile.mkdtemp(prefix="supears_smoke_"))
    frames = out / "f"
    frames.mkdir()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H})
        page.set_content(HTML)
        for i in range(N):
            page.evaluate("t => draw(t)", i)
            page.screenshot(path=str(frames / f"{i:04d}.png"))
        ink = page.evaluate(
            "() => { const d = x.getImageData(0, 0, 640, 360).data;"
            "let s = 0; for (let i = 0; i < d.length; i += 4) s += d[i] + d[i+1] + d[i+2];"
            "return s / (d.length / 4) / 3; }"
        )
        browser.close()

    assert ink > 1.0, f"frames look blank (mean luminance {ink:.2f})"

    pngs = sorted(frames.glob("*.png"))
    assert len(pngs) == N, f"expected {N} frames, got {len(pngs)}"

    sr = 44100
    t = np.arange(int(sr * N / FPS)) / sr
    tone = (0.2 * np.sin(2 * np.pi * (220 + 330 * t) * t) * np.exp(-1.5 * t) * 32767).astype(np.int16)
    wavfile.write(out / "tone.wav", sr, tone)

    mp4 = out / "smoke.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
         "-i", str(out / "tone.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-shortest", str(mp4)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    assert mp4.exists() and mp4.stat().st_size > 2000, "encode produced no usable file"
    print(f"OK {mp4} {mp4.stat().st_size} bytes | {N} canvas frames @ {FPS}fps = {N / FPS:.2f}s | numpy/scipy tone muxed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
