"""gen_invite_boards.py — storyboard HTML for the 25 INVITATION videos:
supEars invites users (in their own language) to drop a comment with bugs,
impressions, critiques, suggestions, compliments. No video until approved.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from collage import GENDER  # noqa: E402

# id: (language, hook native, cta native, voice, gender via GENDER)
INVITES = [
    ("pt", "Portuguese", "Achou um bug? Tem uma ideia? Comenta aqui!",
     "Tua palavra constrói o supEars.", "pt-BR-AntonioNeural"),
    ("es", "Spanish", "¿Viste un error? ¿Tienes una idea? ¡Comenta!",
     "Tus palabras construyen supEars.", "es-ES-ElviraNeural"),
    ("fr", "French", "Un bug ? Une idée ? Dites-le en commentaire !",
     "Vos mots construisent supEars.", "fr-FR-HenriNeural"),
    ("de", "German", "Bug gefunden? Idee gehabt? Schreib's in die Kommentare!",
     "Deine Worte bauen supEars.", "de-DE-KatjaNeural"),
    ("it", "Italian", "Hai trovato un bug? Hai un'idea? Commenta!",
     "Le tue parole costruiscono supEars.", "it-IT-DiegoNeural"),
    ("ru", "Russian", "Нашёл ошибку? Есть идея? Напиши в комментариях!",
     "Твои слова создают supEars.", "ru-RU-SvetlanaNeural"),
    ("zh", "Chinese", "发现漏洞？有想法？请在评论区告诉我们！",
     "你的话语塑造 supEars。", "zh-CN-YunxiNeural"),
    ("ja", "Japanese", "バグを見つけた？アイデアがある？コメントで教えて！",
     "あなたの声がsupEarsを作る。", "ja-JP-NanamiNeural"),
    ("ko", "Korean", "버그를 찾았어? 아이디어 있어? 댓글로 알려줘!",
     "당신의 말이 supEars를 만듭니다.", "ko-KR-InJoonNeural"),
    ("nl", "Dutch", "Bug gevonden? Idee? Laat het weten in de reacties!",
     "Jouw woorden bouwen supEars.", "nl-NL-FennaNeural"),
    ("pl", "Polish", "Znalazłeś błąd? Masz pomysł? Napisz w komentarzu!",
     "Twoje słowa budują supEars.", "pl-PL-MarekNeural"),
    ("tr", "Turkish", "Hata mı buldun? Fikrin mi var? Yoruma yaz!",
     "Sözlerin supEars'ı inşa ediyor.", "tr-TR-EmelNeural"),
    ("uk", "Ukrainian", "Знайшов помилку? Маєш ідею? Напиши в коментарях!",
     "Твої слова творять supEars.", "uk-UA-OstapNeural"),
    ("hi", "Hindi", "बग मिला? कोई आइडिया है? कमेंट में बताओ!",
     "आपके शब्द supEars बनाते हैं।", "hi-IN-SwaraNeural"),
    ("ar", "Arabic", "وجدت خطأ؟ عندك فكرة؟ اكتب في التعليقات!",
     "كلماتك تبني supEars.", "ar-SA-HamedNeural"),
    ("id", "Indonesian", "Nemu bug? Punya ide? Tulis di komentar!",
     "Kata-katamu membangun supEars.", "id-ID-GadisNeural"),
    ("vi", "Vietnamese", "Thấy lỗi? Có ý tưởng? Hãy bình luận!",
     "Lời của bạn xây dựng supEars.", "vi-VN-NamMinhNeural"),
    ("ro", "Romanian", "Ai găsit un bug? Ai o idee? Scrie în comentarii!",
     "Cuvintele tale construiesc supEars.", "ro-RO-AlinaNeural"),
    ("el", "Greek", "Βρήκες σφάλμα; Έχεις ιδέα; Γράψε στα σχόλια!",
     "Τα λόγια σου χτίζουν το supEars.", "el-GR-NestorasNeural"),
    ("sv", "Swedish", "Hittat en bugg? Har du en idé? Kommentera!",
     "Dina ord bygger supEars.", "sv-SE-SofieNeural"),
    ("cs", "Czech", "Našel jsi chybu? Máš nápad? Napiš do komentářů!",
     "Tvá slova staví supEars.", "cs-CZ-AntoninNeural"),
    ("hu", "Hungarian", "Találtál egy hibát? Van ötleted? Írd meg kommentben!",
     "Szavaid építik a supEars-t.", "hu-HU-NoemiNeural"),
    ("th", "Thai", "เจอบั๊ก? มีไอเดีย? คอมเมนต์บอกเรา!",
     "คำพูดของคุณสร้าง supEars", "th-TH-NiwatNeural"),
    ("ur", "Urdu", "بگ ملا؟ کوئی آئیڈیا ہے؟ کمنٹ میں بتاؤ!",
     "آپ کے الفاظ supEars بناتے ہیں۔", "ur-PK-UzmaNeural"),
    ("en", "English", "Spotted a bug? Got an idea? Comment below!",
     "Your words build supEars.", "en-US-AvaNeural"),
]

CATS = ["BUG", "IMPRESSION", "CRITIQUE", "SUGGESTION", "COMPLIMENT"]


def card(lid, lang, hook, cta, voice):
    gender = GENDER.get(voice, "?")
    cats = " · ".join(CATS)
    return f"""
<section class="card" id="v-{lid}">
  <header>
    <img class="flag" src="../pipeline/assets30/flags/{lid}.png" alt="{lid} flag"
         onerror="this.style.display='none'">
    <div>
      <h2>{lang} <span class="lid">[{lid}]</span></h2>
      <p class="meta">VO <code>{voice}</code> ({gender}) · record at production · native lines = draft</p>
      <p class="native">“{hook}”</p>
      <p class="en">→ {cta}</p>
    </div>
    <div class="status">
      <label><input type="checkbox"> native OK</label>
      <label><input type="checkbox"> board OK</label>
      <label><input type="checkbox"> produced</label>
    </div>
  </header>
  <table>
    <tr><th>beat</th><th>visual</th><th>text on screen</th><th>audio</th></tr>
    <tr><td><b>0–3s · HOOK</b></td><td>Ear ring pulses red. Hook slams word-by-word.</td>
        <td class="line">{hook}</td><td>VO hook (native), LONOWN bed low</td></tr>
    <tr><td><b>3–8s · FIVE DOORS</b></td><td>Five chips pop staggered: bug / impression / critique / suggestion / compliment.</td>
        <td class="line">{cats}</td><td>VO reads the five (native), bed ducks</td></tr>
    <tr><td><b>8–12s · HOW</b></td><td>Comment-bubble graphic + cursor click. Ring settles emerald.</td>
        <td class="line">Drop a comment below ⬇</td><td>VO how (native): where to comment</td></tr>
    <tr><td><b>12–15s · WHY + CTA</b></td><td>CTA line + supEars + flag + Oct 10, 2026.</td>
        <td class="line">{cta}<br><em>supEars · Public release Oct 10, 2026</em></td>
        <td>VO cta (native), bed tail</td></tr>
  </table>
</section>"""


def main():
    outdir = HERE.parent / "storyboards"
    outdir.mkdir(exist_ok=True)
    cards = [card(*row) for row in INVITES]
    nav = " ".join(f"<a href='#v-{r[0]}'>{r[0]}</a>" for r in INVITES)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>supEars invitation videos — storyboard (25 languages)</title>
<style>
  body {{ font-family: "Segoe UI", system-ui, sans-serif; background: #0b0f0e; color: #eaf2ee;
         margin: 0; padding: 24px; }}
  a {{ color: #7af0be; }}
  .top, nav {{ max-width: 1100px; margin: 0 auto 24px; }}
  nav {{ line-height: 2; }}
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
  <h1>supEars invitation videos — storyboard · 25 languages</h1>
  <p>Goal: invite every user, <b>in their own language</b>, to <b>drop a comment</b> with
  bugs, impressions, critiques, suggestions, compliments. Format: <b>15s vertical 9:16</b>.
  Music: <code>LONOWN - AVANGARD (Slowed)</code> only. Native hook/CTA lines are
  <b>draft</b> — tick <b>native OK</b> per language, then <b>board OK</b>. No video until approved.</p>
</div>
<nav>{nav}</nav>
{''.join(cards)}
</body>
</html>"""
    dst = outdir / "feedback-invite-25.html"
    dst.write_text(html, encoding="utf-8")
    print(f"OK {dst} ({len(cards)} boards)")


if __name__ == "__main__":
    main()
