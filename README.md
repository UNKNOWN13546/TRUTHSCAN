# TRUTHSCAN 360
### Explainable Digital Trust & Safety Platform
> **Detect • Protect • Verify • Trace • Secure • Build Trust**

TRUTHSCAN 360 is an explainable AI security platform designed to help users evaluate whether digital messages, screenshots, URLs, payment QR codes, documents, viral claims, and identities can be trusted. Rather than giving a blind "safe" or "scam" label, TRUTHSCAN shows **grounded evidence, highlights suspicious phrases, and provides actionable safety guidance**.

---

## 🚀 Live Features & Modalities

| Modality / Tool | Core Capability | Security & Reasoning Engine |
| :--- | :--- | :--- |
| **1. Text Scanner** | SMS, WhatsApp, and email phishing detection | Gemini Multimodal + Coercion Urgency Analyzer |
| **2. Screenshot Scanner** | Fake payment receipts, chat tampering, and UI spoofing | OCR + Gemini Vision + Forensic Heuristics |
| **3. URL Analyzer** | Multi-vendor threat scan and domain brand impersonation | 92-Engine VirusTotal Intelligence + 10-Step Gemini DOM Audit |
| **4. QR Analyzer** | Static / Dynamic UPI payment traps and intent analysis | NPCI UPI Protocol Decoder + Deep-link Risk Parser |
| **5. Claim Tracing** | Viral misinformation decomposition and fact-checking | Atomic Claim Extraction + IFCN Fact-Check Service |
| **6. Document Verification** | Official university receipts, certificates & presentation decks | **8-Step Forensic Protocol** (AST Stream, Metadata, Fonts, Images) |
| **7. Examination Seal** | Tamper detection on institutional exam papers | Ed25519 Cryptographic Signatures + Perceptual dHash |
| **8. Identity Protection** | Cellular takeover and SIM-swap risk assessment | CAMARA API Mock + Telecom Indicator Risk Engine |
| **9. Deepfake & Image Forensics**| Synthetic AI images and copy-move cloning detection | Error Level Analysis (ELA) + Google DeepMind SynthID Forensics |
| **10. Case Orchestrator** | Multi-vector coordinated fraud investigation | Unified Case Vault + Cross-Signal Correlation |

---

## 🔬 The 8-Step Forensic Document Authenticity Protocol

When any document (PDF or image) is submitted for verification, TRUTHSCAN executes an 8-step forensic audit:

1. **Step 1 - Read Content:** Analyzes text streams, tables, layout formatting, spelling typos, split words, and mathematical coherence.
2. **Step 2 - Inspect Metadata:** Measures `Producer`, `Creator`, `Author`, `Title`, `CreationDate`, `ModDate`, and software classification (`FPDF` = server billing script, `Canva` = human design suite, `Acrobat` = manual editor).
3. **Step 3 - Check Fonts:** Distinguishes embedded CID Type 0 font subsets from core PostScript standard 14 Type 1 fonts.
4. **Step 4 - Check Images:** Evaluates real selectable text layers vs. flattened raster pages and identifies full-page 16:9 background canvases.
5. **Step 5 - Check Timestamps:** Correlates file creation metadata against timestamps printed inside the document body.
6. **Step 6 - Fingerprint Analysis:** Differentiates human typographical cues from programmatic templates and detects metadata tags (`containsAiGeneratedContent: Yes`).
7. **Step 7 - Cross-Check:** Verifies institutional registry domains (e.g. `nitte.edu.in`), student registration identifiers, and monetary receipts.
8. **Step 8 - Verify Claims:** Assesses whether technical, financial, or architectural claims are verifiable, plausible, or unsupported.

---

## 🛠️ Architecture & Tech Stack

```text
User Input (Text, Screenshot, URL, QR, PDF Document)
   │
   ▼
[ FastAPI Backend Gateway ] (app/main.py)
   │
   ├── Forensic Analyzers: Error Level Analysis (ELA) & SynthID Watermark Engine
   ├── Telecom Engine: CAMARA SIM-Swap & HIBP k-Anonymity Breach Range API
   ├── Document Engine: PyPDF AST Stream Parser & Font/Image Inspector
   ├── Web Intelligence: VirusTotal 92-Engine API + Safe Crawler
   │
   ▼
[ Google Gemini Multimodal Reasoning Engine ] (gemini-3.5-flash / gemini-3.6-flash)
   │
   ▼
[ Universal Final Trust Report ]
   ├── Threat Severity Gauge (0 to 100)
   ├── One-Line Forensic Verdict
   ├── Grounded Evidence Vault
   ├── "Show Me Why" Exact Phrase Highlighting
   └── Contextual Action Plan ("What Should I Do?")
```

- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **AI Core:** Google GenAI SDK (`google-genai`), Gemini 3.5 / 3.6 Flash
- **Computer Vision & Forensics:** Pillow (PIL), NumPy, PyPDF
- **Frontend:** Responsive Glassmorphism UI, Tailwind CSS, Lucide Icons, Vanilla ES6+
- **Security & Privacy:** Ed25519 Cryptographic Signatures, SHA-256 Hashes, Zero-Knowledge selective disclosure concepts

---

## 🏁 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/UNKNOWN13546/TRUTHSCAN.git
cd TRUTHSCAN
```

### 2. Configure Environment Secrets
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your-google-gemini-api-key"
VIRUSTOTAL_API_KEY="your-virustotal-api-key"   # Optional (fallback telemetry included)
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Run the Platform
Double-click `start_trustscan.bat` or run:
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:
- **Landing Page:** `http://127.0.0.1:8000`
- **Active Workspace Application:** `http://127.0.0.1:8000/app`

---

## 👥 Hackathon Details
- **Project Name:** TRUTHSCAN 360
- **Track:** Track 2 — Trust in a Synthetic World
- **Team Name:** DUOBYTE
- **Team Members:** AYUSH C S, HAIMA KRISHNA
