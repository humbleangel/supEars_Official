# -*- coding: utf-8 -*-
"""translations.py — all 25 invitation languages. PT baseline first, then Wave-1
swarms (ES/FR/DE/IT/NL/EN, RU/UK/PL/CS/HU/EL, ZH/JA/KO/VI/TH/ID, AR/HI/UR/TR/RO/SV).
Schema per lang: voiceM/F, hook (3 sentences), cta_full (ends with brand),
cta_m (no brand + trailing comma), cats (spoken 4), chips[4] (short!),
how, testi, howcard, date, speak_sub, name (viewer handle, localized).
"""
LANG = {
    "pt": {
        "voiceM": "pt-BR-AntonioNeural", "voiceF": "pt-BR-FranciscaNeural",
        "hook": "Achou um bug? Tem uma ideia? Comenta aqui!",
        "cta_full": "Tua palavra constrói o supEars",
        "cta_m": "Tua palavra constrói o,",
        "cats": "Bugs, críticas, sugestões ou elogios.",
        "chips": ["BUGS", "CRÍTICAS", "SUGESTÕES", "ELOGIOS"],
        "name": "@maria.ouve",
        "how": "Deixe seu comentário aqui embaixo",
        "testi": "Essa orelha traduz e escreve tudo que eu falo!",
        "testi_en": "This ear translates and writes everything I say!",
        "howcard": "Seu comentário aqui! ✍️",
        "date": "Estreia · 10 de outubro de 2026",
        "speak_sub": "Fale livremente. (Link no 1º comentário)",
    },
}

# Wave-1 swarms below (merged at import). Do not edit by hand.
# NOTE: importers must have this dir on sys.path (build_lang.py does).
from lang_a import LANG_A
from lang_b import LANG_B
from lang_c import LANG_C
from lang_d import LANG_D

LANG.update(LANG_A)
LANG.update(LANG_B)
LANG.update(LANG_C)
LANG.update(LANG_D)
assert len(LANG) == 25, f"want 25 langs, have {len(LANG)}"
