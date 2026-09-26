import asyncio, json, subprocess
from pathlib import Path
import edge_tts
BASE = Path(__file__).resolve().parent
SRC = BASE / "vo_lines.json"
OUT = BASE / "vo"
async def one(e):
    tmp = OUT / (e["id"] + ".tmp.mp3")
    dst = OUT / (e["id"] + ".mp3")
    await edge_tts.Communicate(e["text"], e["voice"], rate=e.get("rate", "+0%")).save(str(tmp))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-ar", "48000", str(dst)], check=True)
    tmp.unlink(missing_ok=True)
    print(f"ok {e['id']}", flush=True)
async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines = json.loads(SRC.read_text(encoding="utf-8"))
    for e in lines:
        try:
            await one(e)
        except Exception as ex:
            print(f"FAIL {e['id']}: {ex}")
            raise
asyncio.run(main())
