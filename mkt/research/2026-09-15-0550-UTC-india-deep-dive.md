# India deep-dive: Hindi/Hinglish dictation — owner-supplied leads

> Filed 2026-09-15 05:50 UTC. Owner proved the last round shallow with 4 links — all four investigated below, plus bonus finds from the same threads. Honest admission: our competitor map missed the entire India-native layer. Internal document, not public copy.

## 1. r/developersIndia thread: "Looking for Speech to Text for Hindi" (FULL capture via archive API)

- Thread: https://www.reddit.com/r/developersIndia/comments/1tdieq5/looking_for_a_speech_to_text_tool_for_hindi/ (1.5M-sub community, flair: Suggestions, 9 comments).
- OP (Product Manager): tried WisprFlow + ChatGPT mic — *"they record the entire audio, then transcribe it to words."* Wants **words appearing AS he speaks** (train-of-thought, speak in bits and pieces). Follow-up: *"most apps process the text altogether to generate context and then display."*
- Best answers: (a) Tech Lead: *"WisprFlow actually does live transcription under the hood, unfortunately they don't show it"* — the capability exists, the UX hides it; (b) Azure Speech streams Hindi well (OSS alt: whisper-streaming); *"Hinglish is trickier though"*; (c) test with messy Hindi/Hinglish samples, not clean English demos; (d) second seeker: *"I am also looking for one such tool"* — OP never found one (*"Nope, not yet"*).
- Noise in thread: DictaFlow shill ($7/mo, "Hindi natively, local mode" — same outfit behind the "Wispr accuracy problems" SEO article; treat claims as marketing), removed lecsync shill, dead Freeflow links.
- **Takeaway: the LIVE gap is real and unsolved.** Users don't want record-then-transcribe; they want visible words while speaking. Nobody in India's largest dev community could name a Hindi tool that does it.

## 2. ElevenLabs Scribe — Hindi benchmark king (file/API, NOT at-cursor)

- Hindi page: https://elevenlabs.io/speech-to-text/hindi. Scribe v1 Hindi WER: **5.5% vs Whisper Large v3 33.3%**, Deepgram Nova 2 19.0%, Gemini Flash 2.5 5.2%. 600M speakers, Khariboli/Braj/Awadhi/Bhojpuri accents noted. 99 langs; Hindi in "Excellent ≤5% WER" tier, but Punjabi/Urdu only "Good", most Indian regional langs lower.
- Price: **$0.40/hr audio**, API-first. Real-time version "will be released soon" — i.e. batch today.
- **Takeaway: adjacent, not direct** (upload-file/API, no at-cursor paste, no Windows float). Two lessons: (a) Whisper-based rivals are beatable 6× on Hindi with the right model — our Hindi accuracy bar must be Scribe, not Whisper; (b) Scribe's per-language WER table is the template for honest per-language accuracy claims at alpha.

## 3. Kapwing — Hindi transcript generator (creator subtitles, NOT dictation)

- Hindi tool page: https://www.kapwing.com/tools/transcribe/hindi — upload video → Hindi transcript/subtitles, web-based. Pricing ~$16/mo Pro, $50/mo Business.
- **Takeaway: adjacent** (creator subtitle workflow, cloud, no live input, no paste). Relevant only as (a) the tool our future YouTube workflow might use for Hindi captions, (b) proof of Hindi demand in creator tooling.

## 4. Quill Flow — the Hinglish-native rival we missed (iPhone keyboard)

- Blog: https://quillflow.app/blog/best-dictation-app-hinglish (Flow Studios, Indian founder, Mar 2026). Hinglish as first-class input mode (no language switching), Roman-script output, **India-specific pricing**, iPhone keyboard (WhatsApp/Notes/Gmail anywhere), Mac/Android waitlist. Publishes comparison pages vs Apple, Wispr Flow, Aqua, Gboard — aggressive SEO exactly as our playbook prescribes.
- Representative claim table: Apple mangles Hindi-in-English-mode and vice versa; Google better but inconsistent; Quill most reliable *because it expects mixing*.
- **Takeaway: closest thing to a direct India rival — but iOS-only, no Windows.** Zero overlap with our Windows float today; watch their Mac waitlist. Learn: India pricing + Hinglish-first messaging + comparison-page SEO.

## 5. Bonus micro-competitors from the same threads (all new vs our map)

| Name | What | Price | Overlap |
|---|---|---|---|
| DictaFlow ($7/mo) | Hold-to-talk, Hindi native, "local mode", Mac/Win/iOS/Android-via-Telegram | $7/mo Pro | Direct-ish; aggressive SEO + Reddit shilling — watch |
| Voicedash | "Live dictation layer", cleanup (per thread rec) | ? (unverified) | Possible direct; needs verification |
| SpeakType (OSS, MIT) | Offline Mac, WhisperKit, hotkey-paste; wants Hindi/Indian-English help + **Windows port** | $0 | Future Windows rival OR contributor pool |
| Dicta (nitintf/dicta, OSS) | Tauri+Rust Mac app, local whisper.cpp + cloud options incl. ElevenLabs; Hindi listed | $0 | Same lane, Mac-only |
| BolNote | Hindi/Marathi/English voice → WhatsApp formatting | ? | Niche, no overlap |
| Freeflow (mrinalwadhwa, OSS) | Batch like Wispr per OP | $0 | Dead end (batch, links dying) |
| Azure Speech / whisper-streaming / SimulStreaming / lecsync | Streaming infra pieces | varies/OSS | Tech paths if we ever do live-streaming |

## 6. What this changes (corrections to prior research)

1. **We missed the India-native layer entirely** (Quill, DictaFlow, Voicedash, SpeakType, Dicta, BolNote). Owner right: round was shallow outside US/EU.
2. **New #1 India feature: LIVE visible words** — streaming display while speaking, not just fast batch paste. Product question for dev/owner: does supEars stream partials live or paste on release? Our landing's word-by-word animation already promises the feeling — the product must match before we claim it.
3. **Hindi accuracy bar = Scribe 5.5%, not Whisper 33%** — never benchmark ourselves against Whisper alone.
4. **Per-language honesty wins**: Scribe-style WER table per language at alpha; no fake "100% accuracy".
5. **Other markets need the same treatment** — owner flagged "lot more on others": Brazil, Japan, Indonesia next. Propose one deep-dive per priority market, same method (local sub + local founders + local pricing).

---
*Filed 2026-09-15 05:50 UTC · cost 0 · no public post. Method: direct webfetch + Arctic Shift public archive API for Reddit (Reddit walls scrapers; websearch API 429).*
