"""build_lang.py — one command per language: VO (rate-fit) + spine synthesis +
placed + ring/peaks data. Then render + mix via existing scripts.
Usage: python build_lang.py es
PT spine (promo_invite_pt.html) is the master; per-lang spines are synthesized
by exact literal swaps (no template drift). Timeline identical for all langs.
"""
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from translations import LANG
from vo_polish import decode, polish, encode, probe

MASTER = HERE / "promo_invite_pt.html"
# PT slot durations (rate-fit targets)
SLOTS = {"hook": 3.35, "cats": 3.63, "how": 2.62, "testi": 3.04, "cta_m": 1.9}


def split_sentences(s):
    parts = re.split(r"(?<=[?!؟？！;;])\s*", s.strip())
    return [p for p in parts if p]


async def synth(text, voice, rate, dst):
    await edge_tts.Communicate(text, voice, rate=rate).save(str(dst))


async def gen_voice(lid, key, text, voice, target):
    dst = HERE / "vo_invite" / f"{lid}_{key}.mp3"
    await synth(text, voice, "+3%", dst)
    y = decode(dst)
    encode(polish(y), dst)
    d = probe(dst)
    if target and abs(d - target) > 0.35:
        rate = max(-30, min(30, round((d / target - 1) * 100)))
        await synth(text, voice, f"{rate:+d}%", dst)
        y = decode(dst)
        encode(polish(y), dst)
        d = probe(dst)
    assert d > 0.4, f"bad clip {dst}"
    print(f"  {lid}_{key}: {d:.2f}s (target {target})")
    return round(d, 3)


async def build_voices(lid):
    t = LANG[lid]
    durs = {}
    durs["hook"] = await gen_voice(lid, "hook", t["hook"], t["voiceM"], SLOTS["hook"])
    durs["cats"] = await gen_voice(lid, "cats", t["cats"], t["voiceM"], SLOTS["cats"])
    durs["how"] = await gen_voice(lid, "how", t["how"], t["voiceM"], SLOTS["how"])
    durs["testi"] = await gen_voice(lid, "testi", t["testi"], t["voiceF"], SLOTS["testi"])
    durs["cta_m"] = await gen_voice(lid, "cta_m", t["cta_m"], t["voiceM"], SLOTS["cta_m"])
    return durs


def split_how(s):
    parts = split_sentences(s)
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    return s, ""


def build_spine(lid):
    t = LANG[lid]
    src = MASTER.read_text(encoding="utf-8")
    pt = LANG["pt"]
    pt_hook = split_sentences(pt["hook"])
    tg_hook = split_sentences(t["hook"])
    assert len(pt_hook) == 3 and len(tg_hook) == 3, f"{lid}: hook must be 3 sentences"
    pt_how = ["Deixe seu comentário", "aqui embaixo ⬇"]
    tg_how = list(split_how(t["how"]))
    if tg_how[1]:
        tg_how[1] = tg_how[1] + " ⬇"
    pre = t["cta_m"].rstrip("，,、،")
    assert t["cta_full"].startswith(pre), f"{lid}: cta_full/cta_m mismatch"
    brand2 = t["cta_full"][len(pre):].strip()
    q = lambda s: json.dumps(s, ensure_ascii=False)  # JS-safe quoting
    # hook patterns are BARE text inside the spine's own quotes: escape, don't wrap
    esc = lambda s: s.replace("'", "\\'")
    subs = [
        ("Achou um bug?", esc(tg_hook[0])),
        ("Tem uma ideia?", esc(tg_hook[1])),
        ("Comenta aqui!", esc(tg_hook[2])),
        ("'Tua palavra'", q(t["cta_m"].rstrip("，,、،"))),
        ("'constrói o supEars.'", q(brand2)),
        ("'BUG', 'CRÍTICA', 'SUGESTÃO', 'ELOGIO'",
         ", ".join(q(c) for c in t["chips"])),
        ("'Deixe seu comentário'", q(tg_how[0])),
        ("'aqui embaixo ⬇'", q(tg_how[1])),
        ("'Essa orelha escreve tudo que eu falo!'", q(t["testi"])),
        ("'Seu comentário aqui! ✍️'", q(t["howcard"])),
        ("'Estreia · 10 de outubro de 2026'", q(t["date"])),
        ("'Fale livremente. (Link no 1º comentário)'", q(t["speak_sub"])),
        ("'@maria.ouve'", q(t["name"])),
        ("FLAG_B64.pt", f"FLAG_B64['{lid}']"),
        ("FLAGS.pt", f"FLAGS['{lid}']"),
        ("window.RAW_PT", "window.RAW"),
        ("window.PEAKS_PT", "window.PEAKS"),
        ("ring_raw_pt.js", f"ring_raw_{lid}.js"),
        ("peaks_pt.js", f"peaks_{lid}.js"),
    ]
    out = src
    for old, new in subs:
        assert out.count(old) >= 1, f"{lid}: literal not found: {old[:40]}"
        out = out.replace(old, new)
    dst = HERE / f"promo_invite_{lid}.html"
    dst.write_text(out, encoding="utf-8")
    # langpack (docs + flag code; spine carries strings inline)
    pack = {"id": lid, "flag": lid, "voices": {"M": t["voiceM"], "F": t["voiceF"]}}
    (HERE / f"langpack_{lid}.js").write_text(
        "window.PACK = " + json.dumps(pack, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"  spine {dst.name} + langpack_{lid}.js")


def build_data(lid):
    inv = HERE / "vo_invite"
    starts = {"open": 150, "testi": 3500, "hook": 6800, "cats": 10300,
              "how": 14000, "cta": 18000}
    files = {"open": HERE / "vo_invite" / "pt_open.mp3",
             "testi": inv / f"{lid}_testi.mp3", "hook": inv / f"{lid}_hook.mp3",
             "cats": inv / f"{lid}_cats.mp3", "how": inv / f"{lid}_how.mp3",
             "cta": inv / f"{lid}_cta.mp3"}
    # CTA = M lead + universal Ava stamp
    from build_cta_lib import assemble_cta
    cta_dur = assemble_cta(inv / f"{lid}_cta_m.mp3", files["cta"])
    tj = {}
    for key in ("hook", "cats", "how", "testi"):
        tj[key] = {"file": f"vo_invite/{lid}_{key}.mp3",
                   "dur": round(probe(inv / f"{lid}_{key}.mp3"), 3)}
    tj["cta"] = {"file": f"vo_invite/{lid}_cta.mp3", "dur": cta_dur}
    tj["open"] = {"file": "vo_invite/pt_open.mp3",
                  "dur": round(probe(inv / "pt_open.mp3"), 3)}
    (inv / f"{lid}_timings.json").write_text(
        json.dumps(tj, ensure_ascii=False, indent=2), encoding="utf-8")
    filt, inputs, labels = [], [], []
    gains = {"open": 4.0, "cats": 3.0}
    for i, key in enumerate(["open", "testi", "hook", "cats", "how", "cta"]):
        src = files[key]
        inputs += ["-i", str(src)]
        filt.append(f"[{i}:a]aresample=48000,adelay={starts[key]}|{starts[key]},"
                    f"volume={gains.get(key, 0.0):.1f}dB[s{i}]")
        labels.append(f"[s{i}]")
    n = len(labels)
    filt.append("".join(labels) + f"amix=inputs={n}:normalize=0,volume=+6dB,"
                f"alimiter=limit=0.89,apad=whole_dur=21[vox]")
    placed = inv / f"{lid}_placed.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
                    ";".join(filt), "-map", "[vox]", "-ar", "48000", "-ac", "1",
                    str(placed)], check=True)
    subprocess.run([sys.executable, str(HERE / "ring_raw.py"), str(placed),
                    f"ring_raw_{lid}.js", "window.RAW", "21", "60"], check=True)
    subprocess.run([sys.executable, str(HERE / "peaks_data.py"), str(placed),
                    f"peaks_{lid}.js", "window.PEAKS"], check=True)


async def main():
    lid = sys.argv[1]
    assert lid in LANG and lid != "pt", f"unknown lang {lid}"
    print(f"=== build {lid} ===")
    print("[1/3] voices…")
    await build_voices(lid)
    print("[2/3] spine…")
    build_spine(lid)
    print("[3/3] data…")
    build_data(lid)
    print(f"=== {lid} ready: render promo_invite_{lid}.html + mix_invite.py {lid} ===")


if __name__ == "__main__":
    asyncio.run(main())
