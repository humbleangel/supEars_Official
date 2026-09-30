# Failed / partial searches — all lead-research rounds (2026-09-30 UTC)

Do NOT redo — fix manually or accept. Concise log of what subagents failed.

## Hard failures (wrong data produced)
1. RU/UA micro hunt: 22 fabricated rows (formulaic info@city-studio domains, all NXDOMAIN) — PURGED from micro file.
2. TR micro hunt: 5 fabricated kurs rows (kapadokyadil et al., NXDOMAIN) — PURGED.
3. Cambridge rows (UK wave): Language Centre closed 2019, persons stale — marked DEAD.
4. UNC Córdoba dean: Graciela → Gloria Ferrero (name drift) — corrected, recheck mandate.
5. St Peter's Agustina Lacarte: left Head PYP role — marked STALE.
6. PSI Kyiv Rachel Caldwell: left Jul 2023 (now AIS Bucharest, already listed) — replaced with Trae Holland, email unconfirmed.
7. Surabaya Matthew Gaetano: left 2019 — replaced with info@ inbox, STALE.
8. Goethe Berlin Manuela Beck: replaced with Katja Kessing.
9. Surabaya admin@sis → info@sis (inbox fix).
10. Cinta Bahasa duplicate advisor row — deduped.
11. ID darmasiswa role was Minister, not program officer — flagged.
12. BH cmebh inbox = Conselho, not SMED outreach — 3 rows DEAD, use smed@.
13. UTRAMIG incorporated into UEMG 2023-2024 — presidency row STALE.
14. AM SEDUC 2024-2025 mandate turnover — STALE.
15. USP clinguas rotativa directorship — RECHECK.
16. Canopé Samuel Vitel email/person mismatch — replaced with generic contact.
17. ciep.fr domain retired — 2 rows STALE-domain.
18. TR bozok.edu.tr SERVFAIL 2026-09-30 — RECHECK.
19. IN Chattarji term ended / TISB Reynolds former principal — STALE.
20. MX Colegio Alemán person/email mismatch (Johanna Freyria) — RECHECK.

## Throttled (HTTP 429, needs manual recheck)
21. Wave-2 verify part 4: ~30 EG/SA/UAE/IN/PK rows never verified — flagged [UNVERIFIED] in file.

## Thin hunts (low yield, gaps later partially filled)
22. Micro UK/US/PL/RO: only 3 rows (UK); US + RO zero.
23. Micro CN/JP/KR/TW: only 6 rows (TW); CN + JP + KR zero.
24. Micro MENA: only 10 rows (EG-heavy; SA/UAE thin).
25. Micro CS/HU/EL/SV: zero HU + zero EL rows.
26. EL HI IT FR v12 hand-split wiped by v13 regen (pipeline lesson, fixed via `|` marker).

## Whole-batch unverified (agent could not confirm, kept with flags)
27. MX sweep: all 19 new rows [UNVERIFIED].
28. TH sweep: all 20 rows [UNVERIFIED].
29. RO sweep: most ISJ/CCD rows [UNVERIFIED]/[PARTIAL].
30. IT sweep: 12 CPIA/Dante/WSE rows [UNVERIFIED].
31. PT agrupamentos: 2 rows [UNVERIFIED].
32. JP sweep: 6 mandate/rotation rows [RECHECK].
33. KR sweep: IS Busan head + Yonsei inbox [RECHECK].
34. FR sweep: 8 person rows [UNVERIFIED person] (BM Lyon, Berlitz, ICS, ISP).
35. DE sweep: 5 shared/generic inbox rows [RECHECK].
36. NL sweep: Babel/ISA/UvA persons [RECHECK].
37. PL sweep: Early Stage person, UW prefix, Polenglot domain [RECHECK].
38. UK sweep: ISL/Bath roles unconfirmed, literacytrust inbox-only.
39. US sweep: NYC Schools roles + NYLC person [RECHECK].
40. SE sweep: ISSR head [RECHECK].
41. TR sweep: NEVU/Aksaray persons [reverify person].
42. ID sweep: darmasiswa + Cinta duplicates noted above.
43. EL sweep: 11 PDE/frontistiria/refugee rows [UNVERIFIED].
44. IN sweep: AIIS + British Council persons [RECHECK].
45. RU/UA sweeps: team-inbox rows, persons unverified by design.
46. VN delacour personal inbox — use enquiries@ for campaigns.
47. OIS Tomalin, USP, AM, BH items listed above (dupes of 12-14, kept once).

## Solo language-school round (no subagents for research; swarm assistants for drafting)
48. CL language-school emails (solo) — none found, schools phone/form only.
49. WSE/ICANA/Interlingua corporate emails (solo) — forms only.
50. inlingua FR contacts (solo) — phone only.
51. PT new language schools (solo) — only IH/Cambridge, already listed.
52. WSE France email (swarm) — form only.
53. WSE Italy email (swarm) — form only.
54. UK swarm 429s: Bell Cambridge, Studio Cambridge, British Council UK teaching centres, Kaplan UK, Language in London — RETRY SOLO.
55. US swarm: FLS International admissions email — RETRY SOLO.
56. PL swarm: Empik School email, British Council Poland email — RETRY SOLO.
57. Solo retry 2026-09-30: Bell/Studio Cambridge (transport error, backend throttled) — PENDING.
58. RO swarm: Eurolingua email, Fides Iași (only Bucharest published).
59. CS swarm: Glossa + Jipka named personal emails unfindable.
60. HU swarm: Hatos/Katedra/IH/BC/Origó/BME named persons unfindable (team inboxes kept).
61. EL swarm: Axios frontistiria + Ifestia language school do not exist in public sources.
62. SV swarm: SFI Malmö + SFI Göteborg dedicated provider emails unfindable.
63. UA swarm: Green Forest email (phones/form only); Nasha Shkola + Nota Bene are not language schools.
64. IN swarm: British Council India centres email (fetch blocked); VETA email (domains unreachable); Kota/Delhi coaching English wings (no verifiable page).
65. SA/UAE swarm: New Horizons Saudi KSA email; Al-Jazeera Academy KSA/UAE email (only Doha out of scope); BC/Eton/Berlitz named-person directs (general inboxes only).
66. CN swarm (rate-limited): Wall Street English China, EF China (phone only), New Oriental language emails.
67. JP swarm (rate-limited): KAI, Human Academy, Sendagaya, ECC, NOVA, Tokyo YMCA emails.
68. KR swarm (rate-limited): YBM, Pagoda, Hackers, Yonsei KLI, KU KLC, Hanyang IIE, EBS, Danuri emails.
69. VN swarm: British Council Vietnam email (fetch timed out, 429).
70. TH swarm: AUA, British Council Thailand, inlingua Bangkok, ECC Thailand emails.
71. ID swarm: EF Indonesia email (phones only); TBI email (site irretrievable).
72. TW swarm: KOJEN email (webform/phone only); Taipei European School email (site unreachable).
73. MY swarm: British Council Malaysia email (site unreachable); named persons EMS/Britannia/ELS/BC MY.
74. PH swarm: ENTIRE batch 429 — CPILS, CG, Philinter, CIA, EV, Cebu Languages + verifications — RETRY SOLO.
75. Solo PH retry 2026-09-30: 429 again — PENDING BACKOFF.
76. MY+SG catch-up (playbook sheets + SG leads + schedule slots): search backend 429 — PENDING BACKOFF, do not fabricate stats.
