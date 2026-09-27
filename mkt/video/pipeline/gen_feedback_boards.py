"""gen_feedback_boards.py — storyboard HTML for the 25 feedback videos (one per
language), generated from the real VO inventory (voice2.py LINES + VOICES,
vo2/timings.json, collage.py GENDER). No video production — review first.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from voice2 import LINES, VOICES  # noqa: E402
from collage import GENDER  # noqa: E402

ENGLISH = {
    "pt": "Meeting tomorrow at three with the client.",
    "es": "Write an email to my boss, in English.",
    "fr": "Running late — write them a message.",
    "de": "Email the client, please in English.",
    "it": "Note: buy bread tomorrow.",
    "ru": "Please write to the client.",
    "zh": "Translate this into English.",
    "ja": "Write up tomorrow's meeting notes.",
    "ko": "Write the email in English.",
    "nl": "Message the customer.",
    "pl": "Message the client.",
    "tr": "Email the customer.",
    "uk": "Write to the client.",
    "hi": "Write this in English.",
    "ar": "Message the client.",
    "id": "Message the client.",
    "vi": "Message the customer.",
    "ro": "Message the client.",
    "el": "Message the customer.",
    "sv": "Message the customer.",
    "cs": "Message the client.",
    "hu": "Message the client.",
    "th": "Message the customer.",
    "ur": "Message the client.",
    "en1": "English, as spoken.",
    "en2": "English, as spoken.",
}
LANGNAME = {"pt": "Portuguese", "es": "Spanish", "fr": "French", "de": "German",
            "it": "Italian", "ru": "Russian", "zh": "Chinese", "ja": "Japanese",
            "ko": "Korean", "nl": "Dutch", "pl": "Polish", "tr": "Turkish",
            "uk": "Ukrainian", "hi": "Hindi", "ar": "Arabic", "id": "Indonesian",
            "vi": "Vietnamese", "ro": "Romanian", "el": "Greek", "sv": "Swedish",
            "cs": "Czech", "hu": "Hungarian", "th": "Thai", "ur": "Urdu",
            "en1": "English (1)", "en2": "English (2)"}

timings = {r["id"]: r for r in
           json.loads((HERE / "vo2" / "timings.json").read_text(encoding="utf-8"))}

BEATS = [
    ("0–2s · HOOK", "User's face / phone screen, dim. Native pain line types on.",
     "native", "VO native, dry then LONOWN bed fades under"),
    ("2–9s · DEMO", "supEars ring: waveform dances WITH the voice (data-driven). "
     "Native line flies in word-by-word, then English translation stamps below it.",
     "native + EN", "VO native foreground, bed ducked −12 dB"),
    ("9–12s · PROOF", "Ring settles emerald. Chips: 100% OFFLINE · NO CLOUD.",
     "chips", "bed breathes, tail of VO"),
    ("12–15s · CTA", "supEars + flag + Public release Oct 10, 2026.",
     "brand", "bed tail + end tick"),
]


def card(lid, lang, text):
    t = timings[lid]
    voice = t["voice"]
    gender = GENDER.get(voice, "?")
    flag = f"assets30/flags/{lid[:2]}.png"
    rows = []
    for i, (beat, visual, track, audio) in enumerate(BEATS):
        line = {"native": text, "native + EN": f"{text}<br><em>{ENGLISH[lid]}</em>",
                "chips": "100% OFFLINE · NO CLOUD · NO ACCOUNT",
                "brand": "supEars · Oct 10, 2026"}[track]
        rows.append(
            f"<tr><td><b>{beat}</b></td><td>{visual}</td>"
            f"<td class='line'>{line}</td><td>{audio}</td></tr>")
    return f"""
<section class="card" id="v-{lid}">
  <header>
    <img class="flag" src="../pipeline/{flag}" alt="{lid} flag"
         onerror="this.style.display='none'">
    <div>
      <h2>{LANGNAME.get(lid, lid)} <span class="lid">[{lid}]</span></h2>
      <p class="meta">voice <code>{voice}</code> ({gender}) · clip {t['dur']}s · rate {t['rate']}</p>
      <p class="native">“{text}”</p>
      <p class="en">→ {ENGLISH[lid]}</p>
    </div>
    <div class="status">
      <label><input type="checkbox"> board OK</label>
      <label><input type="checkbox"> produced</label>
    </div>
  </header>
  <table>
    <tr><th>beat</th><th>visual</th><th>text on screen</th><th>audio</th></tr>
    {''.join(rows)}
  </table>
</section>"""


def main():
    outdir = HERE.parent / "storyboards"
    outdir.mkdir(exist_ok=True)
    cards = [card(lid, lang, text) for lid, lang, _, text in LINES]
    nav = " ".join(f"<a href='#v-{lid}'>{lid}</a>" for lid, _, _, _ in LINES)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>supEars feedback videos — storyboard (25 languages)</title>
<style>
  body {{ font-family: "Segoe UI", system-ui, sans-serif; background: #0b0f0e; color: #eaf2ee;
         margin: 0; padding: 24px; }}
  a {{ color: #7af0be; }}
  .top {{ max-width: 1100px; margin: 0 auto 24px; }}
  .top code {{ color: #e7c15a; }}
  nav {{ max-width: 1100px; margin: 0 auto 24px; line-height: 2; }}
  nav a {{ margin-right: 10px; }}
  .card {{ max-width: 1100px; margin: 0 auto 20px; background: #101614;
          border: 1px solid #1f2b26; border-radius: 12px; padding: 18px 20px; }}
  .card header {{ display: flex; gap: 16px; align-items: flex-start; }}
  .flag {{ width: 92px; border-radius: 6px; border: 1px solid #333; }}
  h2 {{ margin: 0 0 4px; font-size: 22px; }}
  .lid {{ color: #8fa79b; font-size: 14px; }}
  .meta {{ margin: 0 0 8px; color: #8fa79b; font-size: 13px; }}
  .meta code {{ color: #e7c15a; }}
  .native {{ margin: 4px 0; font-size: 18px; }}
  .en {{ margin: 0; color: #e7c15a; }}
  .status {{ margin-left: auto; white-space: nowrap; font-size: 14px; }}
  .status label {{ display: block; margin-bottom: 6px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }}
  th, td {{ border: 1px solid #24332d; padding: 8px 10px; vertical-align: top; text-align: left; }}
  th {{ background: #16211d; color: #7af0be; }}
  td.line {{ font-size: 15px; }}
  td.line em {{ color: #e7c15a; font-style: normal; }}
  @media print {{ body {{ background: #fff; color: #000; }} .card {{ break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="top">
  <h1>supEars feedback videos — storyboard · 25 languages</h1>
  <p>Format: <b>15s vertical 9:16</b> (Shorts / Reels / TikTok), 16:9 cutdown on approval.
  One user, one request, one proof: the user speaks, the ring dances <b>with their real
  voice energy</b>, their words land in English. Music: <code>LONOWN - AVANGARD (Slowed)</code>
  only, ducked under VO. No video production until boards are approved — tick
  <b>board OK</b> per language.</p>
</div>
<nav>{nav}</nav>
{''.join(cards)}
</body>
</html>"""
    dst = outdir / "feedback-25.html"
    dst.write_text(html, encoding="utf-8")
    print(f"OK {dst} ({len(cards)} boards)")


if __name__ == "__main__":
    main()
