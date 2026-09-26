"""The cue sheet: single source of truth for picture and sound.
Build -> validate -> print storyboard. Nothing renders until violations == 0.
"""
import json
from pathlib import Path

HERE = Path(r"D:\WORK_B\PRJS\supEars_Official\mkt\video\pipeline")
OUT = HERE / "cue_sheet.json"

BPM = 140.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
DUR = 60.0

CHAPTERS = [
    ("HOOK", 0.0, 8.571), ("MECH", 8.571, 20.571), ("WALL", 20.571, 39.429),
    ("PRIVACY", 39.429, 44.571), ("PROOF", 44.571, 53.143), ("CTA", 53.143, 60.0),
]

VO = [
    ("hook", 0.00, 2.424), ("pain", 3.30, 4.008), ("brand", 8.80, 3.528),
    ("how1", 12.80, 4.152), ("how2", 17.30, 2.784), ("es", 20.90, 4.728),
    ("fr", 26.00, 4.008), ("de", 30.30, 4.440), ("ja", 35.10, 4.056),
    ("privacy", 39.60, 4.872), ("cpu", 44.90, 3.240), ("motto", 48.40, 3.264),
    ("free", 52.00, 3.744), ("cta2", 56.10, 2.400),
]

TEXTS = [
    ("hook", "Are you tired of paying subscriptions to talk?", "en", 0.00, 3.20, "hero", 470),
    ("pain1", "You pay every month.", "en", 3.30, 7.10, "hero", 470),
    ("pain2", "to type one sentence.", "en", 5.00, 7.10, "sub", 600),
    ("quote1", "\u201cWindows speech recognition accuracy was too low.\u201d", "en", 7.30, 8.50, "quote", 1010),
    ("brand", "The Ear that understands your language.", "en", 8.80, 12.30, "claim", 870),
    ("quote2", "\u201cLocal offline speech recognition. No internet needed.\u201d", "en", 9.95, 11.95, "quote", 1010),
    ("mech1", "Click.", "en", 12.80, 14.30, "hero3", 750),
    ("mech2", "Speak.", "en", 14.30, 15.80, "hero3", 750),
    ("mech3", "Magic.", "en", 15.80, 17.30, "hero3", 750),
    ("cry", "Escape the Subscriptions Trap.", "en", 18.00, 20.40, "cry", 540),
    ("draft1", "Fale no seu idioma.", "pt", 15.20, 17.10, "draft", 0),
    ("draft2", "Speak in your own native language.", "en", 15.90, 17.30, "draft", 0),
    ("es", "Habla en espa\u00f1ol.", "es", 20.75, 25.55, "hero", 350),
    ("es_sub", "supEars escribe en ingl\u00e9s.", "en", 22.15, 25.55, "sub", 620),
    ("es_win", "Email to my boss, in English.", "en", 22.35, 25.55, "window", 0),
    ("fr", "Parlez fran\u00e7ais.", "fr", 25.85, 29.95, "hero", 350),
    ("fr_sub", "supEars \u00e9crit en anglais.", "en", 27.25, 29.95, "sub", 620),
    ("fr_win", "Message: I'm running late, see you at nine.", "en", 27.45, 29.95, "window", 0),
    ("quote3", "\u201cI searched for voice-to-text without a subscription.\u201d", "en", 27.80, 29.80, "quote", 1010),
    ("de", "Sprich Deutsch.", "de", 30.15, 34.60, "hero", 350),
    ("de_sub", "Keine Cloud, kein Abo.", "en", 31.55, 34.60, "sub", 620),
    ("de_win", "Invoice the client on Friday.", "en", 31.75, 34.60, "window", 0),
    ("quote4", "\u201c200 hours of sermons must become text.\u201d", "en", 32.40, 34.40, "quote", 1010),
    ("ja", "\u65e5\u672c\u8a9e\u3067\u8a71\u3059\u3002", "ja", 34.95, 37.45, "hero", 350),
    ("ja_sub", "\u82f1\u8a9e\u3067\u66f8\u304f\u3002", "en", 36.35, 39.00, "sub", 620),
    ("ja_win", "Meeting notes, translated.", "en", 36.55, 39.00, "window", 0),
    ("claim", "25 languages in. English out.", "en", 37.60, 39.40, "claim", 190),
    ("priv1", "100% offline.", "en", 39.50, 44.40, "hero", 480),
    ("priv2", "No account. No cloud.", "en", 41.40, 44.40, "sub", 690),
    ("proof1", "Runs on old CPUs.", "en", 44.90, 48.00, "claim", 170),
    ("proof2", "No graphics card.", "en", 46.20, 48.00, "sub", 244),
    ("motto", "Escape the Big Tech Corps Subscriptions Traps.", "en", 48.40, 51.60, "claim", 540),
    ("proof3", "30 days free. No credit card.", "en", 52.00, 55.50, "claim", 964),
    ("uc1", "\u201cI have so much typing. I can't cope.\u201d", "en", 52.30, 55.20, "quote", 700),
    ("cta1", "supEars", "en", 56.10, 60.00, "brand", 808),
    ("cta2", "Public release \u00b7 October 10, 2026", "en", 56.50, 60.00, "sub", 890),
    ("cta3", "100% offline \u00b7 no account \u00b7 no cloud", "en", 57.00, 60.00, "sub", 942),
    ("cta4", "Developed by HumbleAngel", "en", 57.40, 60.00, "sub", 982),
]

COUNTERS = [
    ("languages", "LANGUAGES", 20.90, 39.00, 1, 25),
    ("free_days", "DAYS FREE", 52.00, 55.70, 0, 30),
]

SFX = [
    ("boom", 0.00, "sub"), ("boom2", 3.30, "sub"), ("whip", 5.00, "whip"),
    ("push", 6.60, "impact"), ("brand", 8.80, "shimmer"), ("click1", 12.80, "click"),
    ("click2", 14.30, "click"), ("click3", 15.80, "click"), ("type", 15.20, "ticks"),
    ("cry", 18.00, "impact"), ("claim", 37.60, "shimmer"), ("whoosh", 20.571, "whip"), ("iris", 39.429, "iris"),
    ("motto", 48.40, "impact"), ("riser", 55.20, "riser"), ("slam", 56.10, "impact"),
]

CAMERA = [
    (0.00, 0, 0, 1.16, 0, "io"), (3.30, -70, 26, 1.46, 0, "out"), (5.00, 0, 0, 1.02, 0, "io"),
    (6.60, 0, 0, 2.70, 0, "in"), (7.40, 0, 40, 1.02, 0, "out"), (8.571, -40, 0, 1.05, 0, "io"),
    (11.30, 150, -34, 1.34, 0, "out"), (14.60, -160, 26, 1.24, 0, "io"), (17.50, 120, -30, 1.30, 0, "io"),
    (20.571, 0, 0, 1.02, 0, "io"), (24.00, -40, 20, 1.40, 0, "out"), (28.00, -110, 46, 1.22, 0, "io"),
    (32.00, 90, -42, 1.34, 0, "io"), (36.00, 0, 0, 1.50, 0, "out"), (39.429, 0, 0, 1.26, 0, "io"),
    (43.00, 0, 0, 1.04, 0, "out"), (44.571, 0, 0, 1.00, 0, "io"), (46.50, -80, 34, 1.26, 0, "out"),
    (50.00, 50, -24, 1.14, 0, "io"), (53.143, 0, 0, 1.00, 0, "io"), (56.50, 0, 0, 1.07, 0, "out"),
    (60.00, 0, 0, 1.00, 0, "io"),
]

MIN_ON_SCREEN = 1.2
MAX_HERO_CHARS = 50
MAX_SUB_CHARS = 64
STYLE_LIMIT = {"quote": 64}


def ch(t):
    for name, a, b in CHAPTERS:
        if a <= t < b:
            return name
    return "CTA"


def validate(sheet):
    v = []
    txt = sheet["texts"]
    for c in txt:
        d = c["end"] - c["start"]
        if d < MIN_ON_SCREEN:
            v.append(f"{c['id']}: on screen {d:.2f}s < {MIN_ON_SCREEN}s")
    for c in txt:
        lim = STYLE_LIMIT.get(c["style"], MAX_HERO_CHARS if c["style"] in
                              ("hero", "hero3", "cry", "claim", "brand") else MAX_SUB_CHARS)
        if len(c["text"]) > lim:
            v.append(f"{c['id']}: {len(c['text'])} chars > {lim} ({c['style']})")
    heroes = sorted([c for c in txt if c["style"] in ("hero", "hero3", "claim", "cry")],
                    key=lambda c: c["start"])
    for a, b in zip(heroes, heroes[1:]):
        if b["start"] < a["end"]:
            v.append(f"hero overlap: {a['id']} ends {a['end']:.2f}, {b['id']} starts {b['start']:.2f}")
    vo_starts = [x["start"] for x in sheet["vo"]] + [s["at"] for s in sheet["sfx"]]
    for c in heroes:
        if not any(abs(c["start"] - s) <= 0.65 for s in vo_starts):
            v.append(f"{c['id']}: no voice/sfx near {c['start']:.2f}")
    vos = sorted(sheet["vo"], key=lambda s: s["start"])
    for a, b in zip(vos, vos[1:]):
        if b["start"] < a["start"] + a["dur"] + 0.25:
            v.append(f"VO overlap: {a['id']} ends {a['start']+a['dur']:.2f}, {b['id']} at {b['start']:.2f}")
    for s in sheet["vo"]:
        if ch(s["start"]) != s["chapter"]:
            v.append(f"VO {s['id']} starts in {ch(s['start'])}, declared {s['chapter']}")
    for c in txt:
        if ch(c["start"]) != c["chapter"]:
            v.append(f"{c['id']} starts in {ch(c['start'])}, declared {c['chapter']}")
    ts = [k["t"] for k in sheet["camera"]]
    if ts != sorted(ts) or ts[0] != 0.0 or ts[-1] != DUR:
        v.append("camera keys must start at 0, end at 60, strictly increasing")
    for c in sheet["counters"]:
        if c["end"] <= c["start"]:
            v.append(f"counter {c['id']} has no window")
    return v


def build():
    return {
        "meta": {"fps": 30, "duration": DUR, "bpm": BPM, "beat": round(BEAT, 5),
                 "bar": round(BAR, 5), "resolution": [1920, 1080], "render": [960, 540],
                 "music": "mashup.wav (6 tracks @141)", "wall": "wall.wav (26 voices)",
                 "vo": "vo/vo_placed.wav (14 lines)"},
        "chapters": [{"name": n, "start": a, "end": b} for n, a, b in CHAPTERS],
        "vo": [{"id": i, "chapter": ch(s), "start": s, "dur": d, "file": f"vo/{i}.mp3"} for i, s, d in VO],
        "texts": [{"id": i, "chapter": ch(s), "text": t, "lang": l, "start": s, "end": e,
                   "style": st, "y": y, "snap": round(s / BEAT) * BEAT} for i, t, l, s, e, st, y in TEXTS],
        "counters": [{"id": i, "label": l, "start": s, "end": e, "from": a, "to": b}
                     for i, l, s, e, a, b in COUNTERS],
        "sfx": [{"id": i, "at": t, "kind": k, "snap": round(t / BEAT) * BEAT} for i, t, k in SFX],
        "camera": [{"t": t, "x": xx, "y": yy, "z": z, "rot": r, "ease": e} for t, xx, yy, z, r, e in CAMERA],
    }


def main():
    sheet = build()
    violations = validate(sheet)
    OUT.write_text(json.dumps(sheet, indent=1), encoding="utf-8")
    print(f"cue sheet -> {OUT.name}")
    print(f"chapters {len(sheet['chapters'])}, texts {len(sheet['texts'])}, vo {len(sheet['vo'])}, "
          f"sfx {len(sheet['sfx'])}, counters {len(sheet['counters'])}, camera keys {len(sheet['camera'])}")
    print(f"readability violations: {violations}")
    print()
    cur = None
    for c in sheet["texts"]:
        if c["chapter"] != cur:
            cur = c["chapter"]
            ch_row = next(x for x in sheet["chapters"] if x["name"] == cur)
            print(f"--- {cur}  {ch_row['start']:.2f}-{ch_row['end']:.2f} ---")
        print(("  %6.2f-%6.2f  %-7s  %s" % (c["start"], c["end"], c["style"], c["text"])).encode("ascii", "replace").decode())
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
