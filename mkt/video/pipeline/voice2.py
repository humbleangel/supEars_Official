"""voice2.py — multilingual voice wall: one real-use-case phrase per language.

Synthesizes each LINES phrase with edge-tts (alternating male/female neural
voices, varied rate), resamples to 48 kHz mono mp3 via ffmpeg, measures each
clip with ffprobe, writes vo2/timings.json and prints a table sorted by id.
"""
import asyncio
import json
import subprocess
import tempfile
from pathlib import Path

import edge_tts

BASE = Path(__file__).parent
OUT = BASE / "vo2"

# id | lang | voice-language | text
LINES = [
    ("pt", "pt-BR", "pt-BR", "Anota aí: reunião amanhã às três com o cliente."),
    ("es", "es-ES", "es-ES", "Escribe un correo a mi jefe, en inglés."),
    ("fr", "fr-FR", "fr-FR", "Écris un message pour dire que je suis en retard."),
    ("de", "de-DE", "de-DE", "Schreib eine E-Mail an den Kunden, bitte auf Englisch."),
    ("it", "it-IT", "it-IT", "Scrivi una nota: comprare il pane domani."),
    ("ru", "ru-RU", "ru-RU", "Напиши письмо клиенту, пожалуйста."),
    ("zh", "zh-CN", "zh-CN", "把这段话翻译成英文。"),
    ("ja", "ja-JP", "ja-JP", "明日の会議のメモを書いて。"),
    ("ko", "ko-KR", "ko-KR", "이메일을 영어로 써 줘."),
    ("nl", "nl-NL", "nl-NL", "Schrijf een bericht naar de klant."),
    ("pl", "pl-PL", "pl-PL", "Napisz wiadomość do klienta."),
    ("tr", "tr-TR", "tr-TR", "Müşteriye bir e-posta yaz."),
    ("uk", "uk-UA", "uk-UA", "Напиши лист клієнту."),
    ("hi", "hi-IN", "hi-IN", "यह बात अंग्रेज़ी में लिखो।"),
    ("ar", "ar-SA", "ar-SA", "اكتب رسالة إلى العميل."),
    ("id", "id-ID", "id-ID", "Tulis pesan untuk klien."),
    ("vi", "vi-VN", "vi-VN", "Viết tin nhắn cho khách hàng."),
    ("ro", "ro-RO", "ro-RO", "Scrie un mesaj clientului."),
    ("el", "el-GR", "el-GR", "Γράψε ένα μήνυμα στον πελάτη."),
    ("sv", "sv-SE", "sv-SE", "Skriv ett meddelande till kunden."),
    ("cs", "cs-CZ", "cs-CZ", "Napiš zprávu klientovi."),
    ("hu", "hu-HU", "hu-HU", "Írj üzenetet az ügyfélnek."),
    ("th", "th-TH", "th-TH", "เขียนข้อความถึงลูกค้า"),
    ("ur", "ur-PK", "ur-PK", "کلائنٹ کو پیغام لکھو۔"),
    ("en1", "en-US", "en-US", "Reply to Maria that I'll be there in twenty minutes."),
    ("en2", "en-US", "en-US", "Add a note: invoice the client on Friday."),
]

# male/female alternates down the list; rate cycles +0%..+12% with no neighbours equal
VOICES = {
    "pt": "pt-BR-AntonioNeural",  "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-HenriNeural",    "de": "de-DE-KatjaNeural",
    "it": "it-IT-DiegoNeural",    "ru": "ru-RU-SvetlanaNeural",
    "zh": "zh-CN-YunxiNeural",    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-InJoonNeural",   "nl": "nl-NL-FennaNeural",
    "pl": "pl-PL-MarekNeural",    "tr": "tr-TR-EmelNeural",
    "uk": "uk-UA-OstapNeural",    "hi": "hi-IN-SwaraNeural",
    "ar": "ar-SA-HamedNeural",    "id": "id-ID-GadisNeural",
    "vi": "vi-VN-NamMinhNeural",  "ro": "ro-RO-AlinaNeural",
    "el": "el-GR-NestorasNeural", "sv": "sv-SE-SofieNeural",
    "cs": "cs-CZ-AntoninNeural",  "hu": "hu-HU-NoemiNeural",
    "th": "th-TH-NiwatNeural",    "ur": "ur-PK-UzmaNeural",
    "en1": "en-US-BrianNeural",   "en2": "en-US-AvaNeural",
}


def rate_for(i):
    return f"+{(i * 5 + 3) % 13}%"


async def synth(text, voice, rate, dst):
    await edge_tts.Communicate(text, voice, rate=rate).save(str(dst))


def resample(src, dst):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-ar", "48000",
                    "-ac", "1", "-b:a", "192k", str(dst)], check=True)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    voices = {v["ShortName"] for v in await edge_tts.list_voices()}
    subs, rows = 0, []
    with tempfile.TemporaryDirectory() as td:
        for i, (lid, lang, vlang, text) in enumerate(LINES):
            voice = VOICES[lid]
            if voice not in voices:
                pool = sorted(n for n in voices if n.startswith(vlang + "-"))
                assert pool, f"no voice available for {vlang}"
                voice = pool[0]
                subs += 1
                print(f"SUB {lid}: wanted {VOICES[lid]}, using {voice}")
            rate = rate_for(i)
            raw = Path(td) / f"{lid}.raw.mp3"
            await synth(text, voice, rate, raw)
            out = OUT / f"{lid}.mp3"
            resample(raw, out)
            size, dur = out.stat().st_size, probe(out)
            assert size > 0, f"{lid}: empty file"
            assert dur > 0.3, f"{lid}: too short ({dur}s)"
            rows.append({"id": lid, "lang": lang, "voice": voice, "rate": rate,
                         "file": f"vo2/{lid}.mp3", "dur": round(dur, 3)})
    rows.sort(key=lambda r: r["id"])
    (OUT / "timings.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    w = max(len(r["id"]) for r in rows)
    for r in rows:
        print(f'{r["id"]:<{w}}  {r["lang"]:<5}  {r["voice"]:<26}  {r["rate"]:>4}  {r["dur"]:7.3f}s')
    total = sum(r["dur"] for r in rows)
    print(f'{len(rows)} clips, total {total:.2f}s, {subs} substitution(s), '
          f'all files non-empty and >0.3s, timings.json written')


if __name__ == "__main__":
    asyncio.run(main())
