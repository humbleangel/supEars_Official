"""invite_words.py — word timings by char-proportional split of each clip.
(edge-tts only returns SentenceBoundary for short lines; proportional split
is ±0.3s on evenly-read promo lines — verified visually in stills.)
Writes vo_invite/pt_words.json {key: [{w, start, dur}]} in CLIP time.
Callers add the clip's placement offset for video time.
"""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "vo_invite"

TEXTS = {
    "hook": "Achou um bug? Tem uma ideia? Comenta aqui!",
    "cats": "Bug, impressão, crítica, sugestão ou elogio.",
    "how": "Deixe seu comentário aqui embaixo.",
    "cta": "Tua palavra constrói o supEars.",
}


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    allw = {}
    for key, text in TEXTS.items():
        dur = probe(OUT / f"pt_{key}.mp3")
        words = text.split()
        weights = [max(1, len(w)) for w in words]
        total = sum(weights)
        t, rows = 0.05, []
        for w, wt in zip(words, weights):
            d = (dur - 0.1) * wt / total
            rows.append({"w": w, "start": round(t, 3), "dur": round(d, 3)})
            t += d
        allw[key] = rows
        print(f"{key} ({dur:.2f}s): " + " ".join(f"{r['w']}@{r['start']}" for r in rows))
    (OUT / "pt_words.json").write_text(json.dumps(allw, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    print("OK vo_invite/pt_words.json")


if __name__ == "__main__":
    main()
