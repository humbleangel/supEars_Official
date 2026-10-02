#!/usr/bin/env python3
"""Upload that day's supEars invite Shorts to YouTube (hybrid path B).

Only uploads what you name explicitly -- no bulk, no surprises:
    python upload_shorts.py --only DE IT NL        # dry-run plan (default)
    python upload_shorts.py --only DE IT NL --go   # real private upload

No --only  ->  dry-run plan for all remaining (not yet live) languages.
Uploads go up as PRIVATE (unaudited API projects are private-locked anyway);
flip to public in Studio, one click per video, and post the 1st comment there.

Needs (owner, once): Google Cloud project + YouTube Data API v3 enabled +
OAuth client (Desktop) saved as client_secrets.json. Secrets NEVER enter git.
"""
import argparse
import datetime
import glob
import os
import re
import sys

# Windows consoles default to cp1252, which chokes on Cyrillic/CJK titles.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.dirname(HERE)
POST_TEXTS = os.path.join(VIDEO_DIR, "post_texts_25langs.txt")
LOG_FILE = os.path.join(HERE, "upload_log.txt")

# Invite Shorts already live on the channel -- never re-upload these.
LIVE = {"ES", "FR", "JA", "KO", "EN"}

CATEGORY_SCIENCE_TECH = "28"
DEFAULT_LINK = "https://github.com/humbleangel/supEars_Official/releases"

# BCP-47 for snippet language flags (upload language == video language).
BCP47 = {"PT": "pt", "DE": "de", "IT": "it", "NL": "nl", "RU": "ru",
         "UK": "uk", "PL": "pl", "CS": "cs", "HU": "hu", "EL": "el",
         "ZH": "zh", "JA": "ja", "VI": "vi", "TH": "th", "ID": "id",
         "AR": "ar", "HI": "hi", "UR": "ur", "TR": "tr", "RO": "ro",
         "SV": "sv"}

# Evergreen English tags backing every upload (titles/descriptions already
# carry the native-language discovery; these cover EN search).
BASE_TAGS = ["supEars", "shorts", "offline dictation", "voice typing",
             "speech to text", "no subscription", "windows app",
             "indie dev"]


def parse_post_texts(path):
    """Parse post_texts_25langs.txt -> {LANG: {title, description, comment}}."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out = {}
    blocks = re.split(r"\n-{10,}\n", text)
    for b in blocks:
        m = re.match(r"\s*\[([A-Z]{2})\]", b)
        if not m:
            continue
        lang = m.group(1)
        title = re.search(r"^TITLE:\s*(.+)$", b, re.M)
        desc = re.search(r"^DESCRIPTION:\s*\n(.*?)^FIRST COMMENT:",
                         b, re.M | re.S)
        comment = re.search(r"^FIRST COMMENT:\s*\n(.*)$", b, re.M | re.S)
        out[lang] = {
            "title": title.group(1).strip() if title else "",
            "description": desc.group(1).strip() if desc else "",
            "comment": comment.group(1).strip() if comment else "",
        }
    return out


def resolve_file(lang):
    """Newest 12fps nightdrive companion for a language, or None."""
    pat = os.path.join(VIDEO_DIR, "*-invite-%s-nightdrive-*-12fps.mp4"
                       % lang.lower())
    cands = glob.glob(pat)
    if not cands:
        return None

    def version(p):
        m = re.search(r"-v(\d+)-12fps\.mp4$", p)
        return int(m.group(1)) if m else -1

    return sorted(cands, key=lambda p: (version(p), p))[-1]


def plan(meta, langs, link):
    """Build (and validate) the upload plan. Returns list of dicts."""
    items = []
    for lang in langs:
        if lang not in meta:
            sys.exit("unknown language '%s' (not in %s)"
                     % (lang, os.path.basename(POST_TEXTS)))
        if len(meta[lang]["title"]) > 100:
            sys.exit("title over 100 chars for %s -- fix post texts first"
                     % lang)
        f = resolve_file(lang)
        if not f:
            sys.exit("no 12fps file found for %s -- render it first" % lang)
        desc = meta[lang]["description"].replace("[LINK]", link)
        if "#Shorts" not in desc and "#shorts" not in desc:
            desc += "\n#Shorts"
        native_tags = re.findall(r"#(\w+)", desc, re.UNICODE)
        tags = list(dict.fromkeys(BASE_TAGS + native_tags))[:30]
        items.append({"lang": lang, "file": f,
                      "title": meta[lang]["title"],
                      "description": desc, "tags": tags,
                      "bcp47": BCP47.get(lang, lang.lower()),
                      "comment": meta[lang]["comment"].replace("[LINK]", link)})
    return items


def do_upload(items, secrets):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    token_path = os.path.join(HERE, "token.json")
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secrets, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    yt = build("youtube", "v3", credentials=creds)

    for it in items:
        body = {"snippet": {"title": it["title"],
                            "description": it["description"],
                            "tags": it["tags"],
                            "categoryId": CATEGORY_SCIENCE_TECH,
                            "defaultLanguage": it["bcp47"],
                            "defaultAudioLanguage": it["bcp47"]},
                "status": {"privacyStatus": "private",
                           "selfDeclaredMadeForKids": False}}
        media = MediaFileUpload(it["file"], chunksize=-1, resumable=True)
        req = yt.videos().insert(part=",".join(body.keys()),
                                 body=body, media_body=media)
        resp = None
        while resp is None:
            try:
                _, resp = req.next_chunk()
            except HttpError as e:
                if e.resp.status in (500, 502, 503, 504):
                    continue  # resumable: retry, it picks up where it left off
                raise
        vid = resp["id"]
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%d %H:%M UTC")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("%s  %s  %s  %s\n"
                    % (stamp, it["lang"],
                       os.path.basename(it["file"]), vid))
        print("[%s] PRIVATE  https://youtu.be/%s" % (it["lang"], vid))
        print("  Studio flip -> public, then 1st comment:\n  %s\n"
              % it["comment"].replace("\n", "\n  "))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", nargs="+", metavar="LANG",
                    help="that day's languages, e.g. --only DE IT NL")
    ap.add_argument("--go", action="store_true",
                    help="real upload (default is dry-run plan)")
    ap.add_argument("--link", default=DEFAULT_LINK,
                    help="download URL replacing [LINK]")
    ap.add_argument("--secrets", default=os.path.join(HERE,
                                                      "client_secrets.json"),
                    help="OAuth client JSON (never in git)")
    a = ap.parse_args()

    meta = parse_post_texts(POST_TEXTS)
    langs = [l.upper() for l in a.only] if a.only else \
        [l for l in meta if l not in LIVE]

    print("live, skipped: %s" % " ".join(sorted(LIVE)))
    items = plan(meta, langs, a.link)
    for it in items:
        print("[%s] %s\n  %s" % (it["lang"], it["title"],
                                 os.path.basename(it["file"])))
    if not a.go:
        print("\ndry-run: %d video(s) ready. Add --go to upload as private."
              % len(items))
        return
    if not os.path.exists(a.secrets):
        sys.exit("missing %s -- owner creates the Cloud project first" %
                 a.secrets)
    do_upload(items, a.secrets)


if __name__ == "__main__":
    main()
