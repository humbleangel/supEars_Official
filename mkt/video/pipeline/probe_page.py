import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
html = (HERE / "promo_invite_pt.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(args=["--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": 540, "height": 960})
    pg.goto(html)
    pg.evaluate("window.__ready")
    info = pg.evaluate("""() => ({
      peaks: typeof window.PEAKS_PT,
      peaksN: window.PEAKS_PT ? window.PEAKS_PT.mn.length : -1,
      ring: typeof window.RING_PT,
      crestComplete: document.getElementById('crest').complete,
      crestW: document.getElementById('crest').naturalWidth,
      flagPt: !!document.getElementById('crest'),
    })""")
    print(info)
    pg.evaluate("t => window.__draw(t)", 5.5)
    pg.screenshot(path=r"C:\Users\777\AppData\Local\Temp\opencode\probe55.png")
    b.close()
print("probe still saved")
