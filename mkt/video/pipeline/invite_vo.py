"""invite_vo.py — invitation VO per language (hook/cats/how/cta), polished + probed.
Usage: python invite_vo.py pt
Table extends to all 25 after PT baseline approval.
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
OUT = HERE / "vo_invite"

# lang: (voice, hook, cats, how, cta)
LINES = {
    "pt": ("pt-BR-AntonioNeural",
           "Achou um bug? Tem uma ideia? Comenta aqui!",
           "Erro, impressão, crítica, sugestão ou elogio.",
           "Deixe seu comentário aqui embaixo.",
           "Tua palavra constrói o supEars."),
}

from vo_polish import decode, polish, encode, probe  # noqa: E402


async def synth(text, voice, dst):
    await edge_tts.Communicate(text, voice, rate="+3%").save(str(dst))


async def main():
    lang = sys.argv[1]
    voice, hook, cats, how, cta = LINES[lang]
    OUT.mkdir(exist_ok=True)
    parts = {}
    for key, text in (("hook", hook), ("cats", cats), ("how", how), ("cta", cta)):
        dst = OUT / f"{lang}_{key}.mp3"
        await synth(text, voice, dst)
        y = decode(dst)
        encode(polish(y), dst)
        d = probe(dst)
        assert d > 0.4, f"bad clip {dst}"
        parts[key] = {"file": str(dst), "dur": round(d, 3)}
        print(f"{lang}_{key}: {d:.2f}s")
    (OUT / f"{lang}_timings.json").write_text(json.dumps(parts, ensure_ascii=False, indent=2),
                                              encoding="utf-8")
    print(f"OK vo_invite/{lang}.*")


if __name__ == "__main__":
    asyncio.run(main())
