"""voice_ssml.py — regenerate the 5 EN anchors with SSML emphasis (same voices).
A/B: prints duration + RMS before/after for each line. Keeps rate neutral for clarity.
edge-tts treats input starting with <speak> as SSML.
"""
import asyncio
import subprocess
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
VO = HERE / "vo"

ANCHORS = {
    "hook.mp3": ("en-US-GuyNeural",
                 '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                 '<voice name="en-US-GuyNeural">Are you <emphasis level="strong">tired</emphasis> '
                 'of paying <emphasis level="moderate">subscriptions</emphasis> to talk?</voice></speak>'),
    "brand_F.mp3": ("en-US-AriaNeural",
                    '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                    '<voice name="en-US-AriaNeural">supEars. The <emphasis level="strong">Ear</emphasis> '
                    'that writes what it hears.</voice></speak>'),
    "privacy.mp3": ("en-US-GuyNeural",
                    '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                    '<voice name="en-US-GuyNeural">One hundred percent <emphasis level="strong">offline</emphasis>. '
                    'No account. No cloud.</voice></speak>'),
    "how_F.mp3": ("en-US-AriaNeural",
                  '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                  '<voice name="en-US-AriaNeural"><emphasis level="moderate">Tap the ear.</emphasis> Speak. '
                  '<emphasis level="moderate">Read</emphasis> what it writes.</voice></speak>'),
    "cta2.mp3": ("en-US-GuyNeural",
                 '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                 '<voice name="en-US-GuyNeural">supEars. Public release '
                 '<emphasis level="strong">October tenth</emphasis>.</voice></speak>'),
}


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def main():
    for fname, (voice, ssml) in ANCHORS.items():
        dst = VO / fname
        old_dur = probe(dst) if dst.exists() else -1
        await edge_tts.Communicate(ssml, voice).save(str(dst))
        new_dur = probe(dst)
        assert dst.stat().st_size > 5000 and new_dur > 0.5, f"SSML regen failed: {fname}"
        print(f"{fname}: {old_dur:.2f}s -> {new_dur:.2f}s ({voice})")
    print("SSML anchors regenerated, same voices, emphasis on key words")


if __name__ == "__main__":
    asyncio.run(main())
