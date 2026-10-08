# supEars wording standards — standing rules for public words

> Ordered by owner. Each rule is literal: obey exactly, no interpretation.
> New rules append below with date. Nothing here is retroactive history
> editing — internal docs keep their words; PUBLIC surfaces obey.

## Rule 1 — "engine", never "model" (owner, 2026-10-03 15:22 UTC)

- In every human-facing public word (release notes, site, video titles and
  descriptions, social posts, store copy), the speech-recognition software
  is called the **engine**. The word **model** (AI-model sense) never appears.
- Examples: "new Hindi engine" not "new Hindi model"; "engine download"
  not "model download"; "which engine is running" not "which model".
- EXCEPTIONS (stay exactly as they are):
  1. File and asset names (`model.safetensors`, `models-v1`,
     `pro-*-model.safetensors`, `models/` paths, config keys): renaming
     breaks downloads and the app. Never touch.
  2. Code identifiers and comments: internal, invisible. Never touch.
  3. The business term ("license model", "business model", "pricing model"):
     different word, different meaning. Stays.
  4. Proper names and quoted others ("Escuela Argentina Modelo", rival
     copy, seeker quotes): quote faithfully. Stays.
  5. Internal research/history docs: the record stays verbatim.
- Audit 2026-10-03: all marketing public surfaces (README, index.html +
  mirror, post texts, dev-video description, demand wall, landing) contain
  ZERO AI-model "model" — clean on arrival. App quality selector already
  shows Fast/Balance/Precise/PRO — clean. Open item: past GitHub release
  notes (dev-written) unchecked — owner/dev to verify.

## Rule 2 — describe, never announce (owner, 2026-10-08)

- Public words never say a feature "shipped", "is released", "is launched",
  or any dev-side announcement. We are the devs; the user is not a dev.
- Instead describe what the feature DOES in buyer words.
  Examples: "your words appear while you talk" not "streaming shipped";
  "it understands Portuguese" not "PT engine released".
- Applies to: site, README, release notes, video copy, social posts.
