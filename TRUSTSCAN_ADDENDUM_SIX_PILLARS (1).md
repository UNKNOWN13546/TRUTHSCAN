# TRUSTSCAN — ADDENDUM: The Six-Pillar Trust Layer

> Append this to the TRUSTSCAN master prompt. Where the two conflict, this addendum wins.

## 0. WHY THIS ADDENDUM EXISTS

The hackathon theme: *build technology that makes digital interactions more transparent, reliable and trustworthy when content and identities can be manipulated.* Six pillars are required:

**Detect · Protect · Verify · Trace · Secure · Build Trust**

The base TrustScan covers **Secure** and **Build Trust** fully and **Detect** only as a stub. This addendum adds working versions of the rest and unifies everything under one idea.

## 1. THE UNIFYING IDEA: THE TRUST CASE

A user never thinks "I need module 3." They think **"something feels off."** So:

> The user drops in *anything* (message, screenshot, URL, QR, image, audio note, PDF, claim). TrustScan opens a **Trust Case**, routes it to every relevant pillar, and returns **one unified Trust Report** built on the shared Evidence contract.

Add to the Analysis schema:

```jsonc
{
  "case_id": "TS-A7F29",
  "pillars": {
    "detect":  { "status": "OK|NOT_RUN|UNAVAILABLE", "evidence_ids": [] },
    "protect": { "status": "...", "evidence_ids": [] },
    "verify":  { "status": "...", "evidence_ids": [] },
    "trace":   { "status": "...", "evidence_ids": [] },
    "secure":  { "status": "...", "evidence_ids": [] }
  },
  "attack_chain": [ /* ordered stages, see §8 */ ]
}
```

Evidence `source` gains: `Forensics`, `C2PA`, `FactCheck`, `ReverseImage`, `IdentityCheck`, `SIMSwapCheck`, `DocumentCheck`, `IntegritySeal`. Evidence `category` gains: `media_manipulation`, `missing_provenance`, `metadata_anomaly`, `document_tampering`, `signature_invalid`, `identity_impersonation`, `sim_swap_indicator`, `known_false_claim`, `first_seen_mismatch`.

All existing non-negotiables still apply. Add:

12. **Every pillar reports honestly:** `NOT_RUN`, `UNAVAILABLE`, `INCONCLUSIVE` are first-class results.
13. **"No indicators found" is never "authentic."** Absence of detection ≠ proof of authenticity. Say so in the UI.
14. **Detectors are probabilistic and beatable.** Show their limits inline; never present a detector output as a verdict.

---

## 2. DETECT — deepfakes, manipulated media, suspicious content

**Goal:** give layered, *explained* media-authenticity evidence, not a single magic score.

**Image analysis (build fully):** run these as independent analyzers, each emitting evidence:
1. **Provenance (C2PA / Content Credentials):** read manifests with the `c2pa-python` library. Report signer, edit history, and whether the signature validates. Missing credentials → `missing_provenance` at LOW severity only (most legit images have none).
2. **Metadata forensics:** EXIF anomalies (editing-software tags, stripped metadata + inconsistent dimensions, timestamps in the future, camera/GPS mismatch).
3. **Classical forensics:** Error Level Analysis heatmap, noise/JPEG-grid inconsistencies, copy-move detection via OpenCV feature matching. Render the ELA heatmap as an overlay ("Show Me Why" for images: highlight suspicious *regions* with boxes, each tied to an Evidence ID).
4. **Gemini Vision reasoning:** lighting/shadow inconsistencies, anatomy or text artifacts, context implausibility. Capped at MODERATE severity because it is opinion, not measurement.
5. **Pluggable ML detector:** `DeepfakeDetector` interface with a provider adapter (a Hugging Face image-classification model run locally, or a commercial API if a key exists). Verify the model card, licence and known limits before use, and display the model name plus its published limitations. If none is configured, return `DETECTOR_UNAVAILABLE`.

**Audio / video (scope honestly):**
- Build the **audio path as an adapter + UI** (upload voice note → provider → evidence). Ship it wired to a real provider only if one is verified and available; otherwise `DETECTOR_UNAVAILABLE` with a clear message.
- Add a **voice-clone scam heuristic layer** that works without ML: "voice note from a 'family member' + urgent money request + new number" is evaluated in the *context* analyzer (Gemini + rules) as `social_engineering`.
- Video: frame-sampling scaffold that reuses the image analyzers on N frames. Label it experimental.

**Statuses:** `POTENTIALLY_MANIPULATED | NO_SIGNIFICANT_INDICATORS | INCONCLUSIVE | DETECTOR_UNAVAILABLE`. Never "100% fake." Always append: *"No indicators found does not prove authenticity."*

**UI:** image with region overlay + evidence list + "what each check can and can't tell you."

---

## 3. PROTECT — digital identity, impersonation, SIM swaps

Be precise: a hackathon web app can't see inside a telco. So Protect is built from four things that *are* feasible.

### 3.1 Impersonation Check ("Is this really who they say?")
- Input: claimed identity (bank / government / company / family member / recruiter) + the channel details (sender ID, phone number, email address, handle, domain).
- Rules + Gemini compare **claim vs channel**: display-name/domain mismatch, lookalike handles, free-mail domains used by "official" senders, WhatsApp business-vs-personal mismatch, new-number "Hi Mum" pattern, executive-impersonation (CEO fraud) patterns.
- Output: evidence (`identity_impersonation`) + a **"Verify out-of-band" plan**: how to contact the real entity via a channel *you* find independently.

### 3.2 SIM-Swap Risk Check
- **Self-check wizard** (no data leaves the browser): sudden loss of signal, unexpected "SIM changed / eSIM activation" messages, OTPs you didn't request, login alerts, password-reset emails, calls asking to "confirm" an OTP. Output a risk level with the specific indicators selected (evidence-based, deterministic).
- **Immediate-action playbook:** contact your operator from another phone, ask for the SIM/eSIM change log and to block the SIM, alert your bank and freeze UPI/cards, secure email and change credentials, report via **1930** and **cybercrime.gov.in**. Also mention India's **Sanchar Saathi** portal for checking connections issued in your name and reporting fraud. *Verify current features and URLs before shipping.*
- **Telco-grade path (optional adapter):** implement a `SimSwapProvider` interface modelled on the **CAMARA SIM Swap API** (network operators expose "was this number's SIM swapped recently?"). Use a **sandbox provider only if you can get real sandbox access; otherwise ship the interface + mock provider labelled "SIMULATED — operator integration required"** and explain how a bank would call it before releasing an OTP. Do not claim live operator data.

### 3.3 Credential Exposure Check (privacy-preserving)
- Password breach check using the **HIBP Pwned Passwords range API with k-anonymity**: hash client-side (SHA-1), send only the first 5 hex chars, match locally. The full password and full hash never leave the browser. Verify the current API terms.
- Email-breach lookup requires a paid HIBP key; make it optional and clearly marked.

### 3.4 Identity-Attack Guidance
"KYC/Aadhaar/PAN update" tricks, fake-official-call scripts, mule-account requests. Evidence-linked recommendations reuse the What Should I Do library.

---

## 4. VERIFY — documents, examination materials, credentials, content

This is where TrustScan becomes more than a scanner: it can also **issue** proof.

### 4.1 Document Authenticity Checker (PDF/image)
- PDF: parse metadata (creator/producer/mod-dates), incremental-update history, embedded fonts and text-layer vs rendered-image mismatch, hidden layers, and **cryptographic signature validation** (use `pyHanko`; report signer, certificate chain validity, and whether the document changed after signing).
- Image scans: ELA and copy-move (reuse §2), font/spacing inconsistency via Gemini Vision, and **edited-number detection** (compare regions around numerals and dates).
- Embedded QR/barcode: decode with the QR pipeline, then check the domain against an **issuer allowlist** (e.g. official government/university domains you configure) and flag mismatches. Never open the link.
- Output: `DocumentCheck` evidence + region overlay. Verdicts: `TAMPERING_INDICATORS | SIGNATURE_VALID | SIGNATURE_INVALID | INCONCLUSIVE`.

### 4.2 Exam Integrity Seal (examination materials)
Purpose: let an institution prove a question paper, answer key or result sheet is the **original, unaltered version**, and detect leaked or modified copies.
- **Issuer flow:** upload a file → compute `SHA-256` of the bytes, plus a **perceptual hash** (for images/PDF pages, so re-photographed or re-scanned copies still match approximately) → sign the manifest `{issuer, title, sha256, phash[], issued_at, valid_from, valid_until}` with **Ed25519** (issuer key generated server-side for the demo) → return a **Seal** (JSON + QR).
- **Verifier flow:** upload/scan a copy → exact hash match = `ORIGINAL_UNMODIFIED`; perceptual near-match = `MATCHES_ORIGINAL_WITH_MODIFICATIONS_OR_REPHOTO` (show diff regions); no match = `NOT_RECOGNISED`; signature bad = `SEAL_INVALID`.
- **Time-lock idea:** seal validity window lets a verifier see a "leak check": a matching copy appearing *before* `valid_from` is flagged for the issuer. State plainly that this shows a copy is *recognised*, not who leaked it.
- Store only the manifest and hashes, never the document.

### 4.3 Credential Verification
- Implement a small **verifiable-credential-style** flow: issuer signs a credential (JSON: subject, degree/certificate, issuer, dates) with Ed25519; holder shares a QR/link; verifier checks signature, expiry, and **revocation list** (a simple signed list). Model the shape on W3C Verifiable Credentials but say "VC-style, simplified."
- Demo issuer + demo credentials clearly labelled as demonstration data.
- Also support **decoding and sanity-checking** official QR credentials in the wild (issuer-domain allowlist), without claiming to validate government systems it cannot reach. Only claim validation if you actually verify a signature.

### 4.4 Content Verification
C2PA verification (see §2) and Trust Passport verification (base spec).

---

## 5. TRACE — origins and spread of misinformation

Be honest: no tool can see WhatsApp forward chains. TrustScan traces what is publicly traceable and gives users a structured way to reason about the rest.

### 5.1 Claim Extraction
Gemini extracts **atomic, checkable claims** from a message/screenshot (structured JSON; each claim tied to `exact_match` and grounded like other evidence). It separates factual claims from opinion and flags emotional-manipulation wording.

### 5.2 Fact-Check Lookup
Query the **Google Fact Check Tools API** (`claims:search`) for each claim; show publisher, rating, review date, and link. Verify the current endpoint, key setup and quotas in the official docs. Sources: `FactCheck`. Coverage of local-language and very recent claims is limited, so say "no matching fact-check found," never "claim is true."

### 5.3 Image Provenance / First-Seen
For images: reverse-image lookup through an official API that supports it (e.g. Google Cloud Vision **Web Detection** — verify availability and terms; do not scrape). Report pages with matching or partially matching images, and **earliest known appearance** where the provider exposes dates. Flag `first_seen_mismatch` (e.g. an "urgent photo from today's event" that appeared years ago). Sources: `ReverseImage`.

### 5.4 Provenance Trail (UI)
A vertical timeline: *first known appearance → fact-checks → C2PA history → matches → this submission*, each node showing source and confidence and **"what we could not see."**

### 5.5 Spread Estimate (privacy-safe, opt-in)
Because Trust Passports carry a signed case ID, allow the user to *optionally* publish an anonymous **"claim fingerprint"** (hash of a normalised claim, no content) to a tiny aggregate counter, so the app can show **"this claim pattern has been checked N times on TrustScan."** Explicit consent, no content or identity stored. This is a demonstration of community signal, not a measurement of internet-wide spread. Label it that way.

### 5.6 Misinformation Guidance
"Pause before you share" checklist: source, date, corroboration, emotional trigger, plus a one-tap **Share a correction** message.

---

## 6. SECURE — phishing, scams, fraud (already specified)

Keep all base-spec features (text, screenshot, URL, QR, VirusTotal, rules, risk engine, What Should I Do). Add: **mule-account and refund-scam patterns**, **loan-app harassment/blackmail** patterns, and **UPI collect-request** parsing.

---

## 7. BUILD TRUST — the transparent-AI layer (make this a visible feature, not a footnote)

Judges reward this pillar when it is *demonstrable*. Build:

1. **"How we decided" panel** on every result: rules fired, sources used, sources unavailable.
2. **Limits Card** for every analyzer: *what this check can detect, what it cannot, known failure modes.*
3. **Model & Data Card** page (`/about`): models used, data sent to third parties (Gemini, VirusTotal, Fact Check, Vision), retention (none), known biases (language coverage, image-quality effects), and the fact that detectors can be evaded.
4. **Evaluation transparency:** ship a labelled golden set in `/eval`, a script that computes per-class precision/recall and a confusion matrix, and a **live "Reliability" page** that shows those numbers. Only report numbers you actually computed, on the test set you actually have, and state its size and limits.
5. **Uncertainty as UI:** `INCONCLUSIVE` is celebrated, not hidden ("Better to say we're unsure than to guess").
6. **User control:** per-service consent toggles (VirusTotal, Fact Check, Vision), a "local-only mode," and one-click history wipe.
7. **Human-in-the-loop:** "Report wrong result" button that stores a hash + label locally for the eval loop (never content).
8. **Accessibility & language:** the multilingual and low-literacy design from the base spec (icons + short sentences + read-aloud via the browser's speech synthesis).

---

## 8. ATTACK CHAIN VIEW (the cross-pillar wow)

Real fraud is a *sequence*. Correlate evidence across pillars into a single narrative:

```
1 CONTACT        fake bank SMS, lookalike sender          (Secure/Protect)
2 MANIPULATION   urgency + authority + AI voice note      (Secure/Detect)
3 CREDENTIAL     OTP request, phishing page               (Secure)
4 TAKEOVER       SIM-swap indicators, login alerts        (Protect)
5 CASH-OUT       UPI collect / mule account               (Secure)
6 COVER          fake reassurance, request to stay silent (Secure)
```

The UI shows which stages this case touches and **which stage the user can still break**. Mapping is deterministic (category → stage table) with Gemini used only to write the one-sentence summary. It turns six modules into one story the jury remembers.

---

## 9. NEW ENDPOINTS

```
POST /api/analyze-media        image | audio | video → Detect
POST /api/check-identity       { claimed_entity, channel_details } → Protect
POST /api/sim-swap/self-check  { indicators[] } → Protect (local rules)
POST /api/sim-swap/lookup      { msisdn_hash? } → provider adapter (mock unless real access)
POST /api/breach/password-range { prefix } → proxied k-anonymity (or do it client-side)
POST /api/verify-document      pdf | image → Verify
POST /api/seal/issue           file → Seal
POST /api/seal/verify          file + seal → Verify
POST /api/credential/issue     demo issuer
POST /api/credential/verify    credential → Verify
POST /api/extract-claims       text|image → Trace
POST /api/fact-check           { claims[] } → Trace
POST /api/image-provenance     image → Trace
POST /api/case                 multi-input → Trust Case (orchestrator)
GET  /api/reliability          eval metrics
```

All keep the shared Evidence contract, the error envelope, rate limits and consent flags.

---

## 10. NEW PROJECT FOLDERS

```
backend/app/services/
  forensics_service.py        # ELA, copy-move, EXIF
  c2pa_service.py
  identity_service.py         # impersonation rules
  simswap_service.py          # self-check + provider interface (+ mock)
  breach_service.py           # k-anonymity
  document_service.py         # pdf checks, pyHanko
  seal_service.py             # Ed25519 seals + phash
  credential_service.py       # VC-style issue/verify/revoke
  claim_service.py            # extraction
  factcheck_service.py        # Google Fact Check Tools
  provenance_service.py       # reverse image adapter
  case_orchestrator.py        # routes inputs to pillars
  attack_chain.py             # category → stage mapping
frontend/src/pages/
  MediaAuthenticity.tsx  IdentityShield.tsx  DocumentVerify.tsx
  ExamSeal.tsx  Credentials.tsx  ClaimTrace.tsx  Reliability.tsx  About.tsx
```

---

## 11. UPDATED BUILD ORDER

1. **Tier 1–3 of the base spec** (text, Gemini, evidence, risk, Show Me Why, URL/VT, screenshot, QR, passport, history).
2. **Tier A:** Trust Case orchestrator + Attack Chain + Build-Trust panels (How we decided, Limits, About).
3. **Tier B (Verify):** Exam Integrity Seal + document checker. *These are the most original, most demonstrable, least API-dependent.*
4. **Tier C (Detect):** image forensics + C2PA + Gemini vision + pluggable detector, region overlay.
5. **Tier D (Protect):** impersonation check + SIM-swap self-check wizard + password k-anonymity.
6. **Tier E (Trace):** claim extraction + Fact Check + reverse-image provenance + Provenance Trail.
7. **Tier F:** audio adapter, video scaffold, credential flow, claim-fingerprint counter.

Rule: **a pillar that is visible and honest beats a pillar that is broad and fake.** If time runs out, ship Tier A–C beautifully and present D–F as working-but-limited with their Limits Cards.

---

## 12. UPDATED DEMO SCRIPT (2.5 minutes, one story)

**Story:** *"Riya's father gets a WhatsApp voice note, his 'son' is in trouble, plus a link and a bank alert."*

1. **Secure (0:00):** paste the bank SMS → HIGH → highlights → OTP explanation.
2. **Detect (0:30):** upload the photo attached to the plea → forensic overlay + C2PA "no credentials" + honest INCONCLUSIVE/POTENTIALLY_MANIPULATED.
3. **Trace (0:55):** reverse-image provenance → *"this photo first appeared in 2021"* + a fact-check hit on the claim.
4. **Protect (1:15):** SIM-swap self-check ("I lost signal an hour ago") → HIGH → action playbook; impersonation check on the "new number."
5. **Verify (1:35):** upload the "fee receipt" PDF → signature invalid + edited digits flagged. Then the **Exam Seal**: verify an original (✅), a re-photographed copy (⚠ modified), and a tampered one (❌).
6. **Attack Chain (2:00):** the full six-stage narrative, with "you can still stop it here."
7. **Build Trust (2:15):** open Reliability + About: *real precision/recall, every limit disclosed.* Close: **"TrustScan doesn't just tell you what to trust. It shows you why, and lets you prove it."**

---

## 13. DEFINITION OF DONE (additions)

- [ ] Every pillar is reachable from one home screen and from the Trust Case flow.
- [ ] Each pillar returns `NOT_RUN / UNAVAILABLE / INCONCLUSIVE` correctly when its dependency is missing.
- [ ] Exam Seal: original, rephotographed and tampered copies each produce a distinct, correct result.
- [ ] No pillar claims capabilities it lacks (SIM-swap mock is labelled SIMULATED; missing detectors say so).
- [ ] The Reliability page shows only metrics computed by the included eval script.
- [ ] Attack Chain view renders for at least two golden cases.

Build Tier 1–3 first, then continue through Tiers A–F, running and showing the result of each before starting the next.
