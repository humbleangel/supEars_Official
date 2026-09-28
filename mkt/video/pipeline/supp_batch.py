"""supp_batch.py — 'supEars' pronunciation battery: voices x spellings.
Writes vo_brand/*.mp3 + brand_playlist.m3u for VLC A/B picking.
"""
import asyncio
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
OUT = HERE / "vo_brand"

VOICES = [
    "en-US-AriaNeural", "en-US-AvaNeural", "en-US-AvaMultilingualNeural",
    "en-US-JennyNeural", "en-US-EmmaNeural", "en-US-MichelleNeural",
    "en-GB-LibbyNeural", "en-GB-MaisieNeural", "en-AU-NatashaNeural",
    "en-IE-EmilyNeural",
    "en-US-GuyNeural", "en-US-BrianNeural", "en-US-AndrewMultilingualNeural",
    "en-US-DavisNeural", "en-US-ChristopherNeural", "en-GB-RyanNeural",
]
SPELLINGS = ["supEars", "Supears"]


async def main():
    OUT.mkdir(exist_ok=True)
    valid = {v["ShortName"] for v in await edge_tts.list_voices()}
    tracks = []
    for voice in VOICES:
        if voice not in valid:
            print(f"SKIP {voice} (not available)")
            continue
        tag = voice.replace("en-", "").replace("-", "").replace("Neural", "")
        for sp in SPELLINGS:
            dst = OUT / f"supEars_{tag}_{sp}.mp3"
            await edge_tts.Communicate(sp, voice).save(str(dst))
            assert dst.stat().st_size > 2000, f"empty {dst}"
            tracks.append(dst.name)
            print(f"ok {dst.name}")
    m3u = OUT / "brand_playlist.m3u"
    m3u.write_text("\n".join(tracks) + "\n", encoding="utf-8")
    print(f"OK {len(tracks)} clips + {m3u.name}")


if __name__ == "__main__":
    asyncio.run(main())
