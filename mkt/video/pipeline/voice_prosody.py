"""voice_prosody.py — regenerate the 5 EN anchors, same voices/words, per-line
rate+patch prosody (edge-tts escapes SSML, so prosody goes through rate/pitch
params instead). A/B table printed; durations must stay near originals.
"""
import asyncio
import subprocess
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
VO = HERE / "vo"

# file: (voice, text, rate, pitch) — subtle broadcast shaping, never cartoon
ANCHORS = {
    "hook.mp3": ("en-US-GuyNeural",
                 "Are you tired of paying subscriptions to talk?",
                 "-5%", "+0Hz"),
    "brand_F.mp3": ("en-US-AriaNeural",
                    "supEars. The Ear that writes what it hears.",
                    "+2%", "+0Hz"),
    "privacy.mp3": ("en-US-GuyNeural",
                    "One hundred percent offline. No account. No cloud.",
                    "-8%", "-20Hz"),
    "how_F.mp3": ("en-US-AriaNeural",
                  "Tap the ear. Speak. Read what it writes.",
                  "+4%", "+0Hz"),
    "cta2.mp3": ("en-US-GuyNeural",
                 "supEars. Public release October tenth.",
                 "-3%", "+0Hz"),
}


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def main():
    for fname, (voice, text, rate, pitch) in ANCHORS.items():
        dst = VO / fname
        old_dur = probe(dst) if dst.exists() else -1
        await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(dst))
        new_dur = probe(dst)
        assert dst.stat().st_size > 5000 and new_dur > 0.5, f"regen failed: {fname}"
        flag = "  <-- CHECK" if old_dur > 0 and abs(new_dur - old_dur) > 1.5 else ""
        print(f"{fname}: {old_dur:.2f}s -> {new_dur:.2f}s rate={rate} pitch={pitch}{flag}")
    print("anchors regenerated with prosody shaping")


if __name__ == "__main__":
    asyncio.run(main())
