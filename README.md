# TRUTHSCAN 360
### Explainable Digital Trust, Real-Time Firewall & Content Provenance Platform
> **Detect • Protect • Verify • Trace • Secure • Build Trust**

[![Live Web App](https://img.shields.io/badge/Live%20Demo-truthscan--eta.vercel.app-0284c7?style=for-the-badge&logo=vercel)](https://truthscan-eta.vercel.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-TRUTHSCAN-10b981?style=for-the-badge&logo=github)](https://github.com/UNKNOWN13546/TRUTHSCAN)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python%203.12-38bdf8?style=for-the-badge&logo=fastapi)](https://github.com/UNKNOWN13546/TRUTHSCAN)

🌐 **Live Production Deployment:** [https://truthscan-eta.vercel.app/](https://truthscan-eta.vercel.app/)  
📂 **Source Code Repository:** [https://github.com/UNKNOWN13546/TRUTHSCAN](https://github.com/UNKNOWN13546/TRUTHSCAN)

---

## 📌 Executive Overview

**TRUTHSCAN 360** is an enterprise-grade digital trust, media forensics, and real-time cognitive safety platform. Instead of giving users opaque, binary "real" or "fake" labels, TRUTHSCAN performs multi-vector forensic audits, exposes explainable evidence, highlights exact manipulated phrases or pixel boundaries, and provides cryptographic provenance.

The platform bridges real-time behavioral streams with immutable content lineage:
1. **10 Specialized Modalities:** Phishing text, tampered payment screenshots, malicious URLs, UPI payment QR traps, viral claim debunking, 8-step PDF document forensics, institutional exam seals, telecom SIM-swap detection, deepfake image forensics, and unified multi-vector fraud case orchestration.
2. **MODULE A — Real-Time Trust Firewall:** Live trust verification for video calls, remote proctored exams, interviews, and financial transactions with sub-30ms latency, optical face-swap detection, AASIST voice clone detection, lip-sync audio-visual desync alerts, WebAuthn/FIDO2 passkey verification, and interactive liveness challenges.
3. **MODULE B — Universal Content Passport + Provenance Graph:** Cryptographic SHA-256 + perceptual `dHash` fingerprinting, C2PA Content Credentials auditing, Error Level Analysis (ELA) tamper detection, and an interactive Directed Acyclic Graph (DAG) tracing content origin, revisions, cryptographic signatures, distribution spread, and ledger verification.

---

## 🏛️ Comprehensive System Architecture

```mermaid
flowchart TD
    classDef client fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef gateway fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#f8fafc;
    classDef firewall fill:#3f1d24,stroke:#f43f5e,stroke-width:2px,color:#f8fafc;
    classDef passport fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc;
    classDef engine fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#f8fafc;
    classDef storage fill:#172554,stroke:#60a5fa,stroke-width:1px,color:#f8fafc;

    subgraph CLIENT_LAYER ["1. Presentation & Client Layer (Next.js / Glassmorphism UI)"]
        UI_DASH["Interactive Workspace (/app)"]:::client
        UI_FIREWALL["Trust Firewall Live HUD (Canvas Face Mesh & Audio Waves)"]:::client
        UI_PASSPORT["Content Passport & DAG Visualizer (SVG Conduits)"]:::client
        UI_PUBLIC["Public Verification Ledger (/verify/:id)"]:::client
    end

    subgraph API_GATEWAY ["2. Gateway & Routing Layer (FastAPI / ASGI)"]
        GW_HTTP["REST API Router (JSON / Multipart)"]:::gateway
        GW_WS["WebSocket Telemetry Server (/ws/trust/:sessionId)"]:::gateway
        GW_AUTH["WebAuthn & FIDO2 Identity Assertion"]:::gateway
    end

    subgraph MODULE_A ["3. MODULE A: Real-Time Trust Firewall"]
        TFW_ENGINE["Risk Composite Engine (0-100 Score)"]:::firewall
        TFW_VIDEO["Video Deepfake Detector (XceptionNet / Face Jitter)"]:::firewall
        TFW_AUDIO["Voice Clone Detector (AASIST Harmonic Vocoder)"]:::firewall
        TFW_SYNC["Lip-Sync Latency Correlator (SyncNet Threshold)"]:::firewall
        TFW_CHALLENGE["Biometric Liveness Challenge (Nonce Reflex)"]:::firewall
        TFW_AUDIT["WORM Session Audit Trail (JSON Export)"]:::firewall
    end

    subgraph MODULE_B ["4. MODULE B: Universal Content Passport & Provenance Graph"]
        CP_INGEST["Multi-Vector Content Ingestion (PDF, PNG, JPG, URL)"]:::passport
        CP_HASH["Dual Hasher: Cryptographic SHA-256 + Perceptual dHash"]:::passport
        CP_C2PA["C2PA Manifest & PKCS#7 Digital Signature Verifier"]:::passport
        CP_FORENSICS["Tamper Engine: ELA Pixel Splicing + AI Detection"]:::passport
        CP_DAG["Directed Acyclic Graph (DAG) Lineage Generator"]:::passport
    end

    subgraph CORE_ENGINES ["5. Specialized Fraud & Forensics Engines"]
        ENG_DOC["8-Step Document Forensics Protocol (PyPDF AST, Fonts, Metadata)"]:::engine
        ENG_GEMINI["Google Gemini Multimodal AI (gemini-3.5/3.6-flash)"]:::engine
        ENG_TELECOM["Telecom SIM-Swap & CAMARA Risk Engine"]:::engine
        ENG_URL["92-Engine VirusTotal + Safe Web Crawler"]:::engine
        ENG_UPI["NPCI UPI Intent Protocol & QR Parser"]:::engine
    end

    subgraph STORAGE_LAYER ["6. Cryptographic Ledger & Audit Persistence"]
        DB_POSTGRES["PostgreSQL / In-Memory Session & Passport Store"]:::storage
        LEDGER_DAG["Cryptographic DAG Node Registry (did:key Signers)"]:::storage
        ZK_PROOF["Zero-Knowledge Selective Disclosure Engine"]:::storage
    end

    %% Client to Gateway
    UI_DASH --> GW_HTTP
    UI_FIREWALL <--> GW_WS
    UI_FIREWALL --> GW_HTTP
    UI_PASSPORT --> GW_HTTP
    UI_PUBLIC --> GW_HTTP

    %% Gateway to Modules
    GW_WS --> TFW_ENGINE
    GW_HTTP --> TFW_ENGINE
    GW_HTTP --> CP_INGEST
    GW_HTTP --> CORE_ENGINES
    GW_AUTH --> TFW_ENGINE

    %% Module A Internal Flow
    TFW_ENGINE --> TFW_VIDEO
    TFW_ENGINE --> TFW_AUDIO
    TFW_ENGINE --> TFW_SYNC
    TFW_ENGINE --> TFW_CHALLENGE
    TFW_ENGINE --> TFW_AUDIT
    TFW_AUDIT --> DB_POSTGRES

    %% Module B Internal Flow
    CP_INGEST --> CP_HASH
    CP_HASH --> CP_C2PA
    CP_C2PA --> CP_FORENSICS
    CP_FORENSICS --> CP_DAG
    CP_DAG --> LEDGER_DAG
    CP_DAG --> DB_POSTGRES

    %% Core Engines Flow
    CORE_ENGINES --> ENG_GEMINI
    ENG_DOC --> CP_INGEST
    ENG_TELECOM --> TFW_ENGINE
    LEDGER_DAG --> ZK_PROOF
```

---

## 🔍 How Each Layer Works in Detail

### 1. Presentation & Client Layer
- **Live Video & Telemetry HUD:** Uses an HTML5 canvas overlay to render real-time facial landmark nodes, corner bounding brackets, biometric scanning lasers, and a responsive audio spectrogram.
- **Interactive SVG DAG Visualizer:** Renders the 6-stage provenance lineage with cybernetic laser conduit animations (`laser-conduit-cyan`, `laser-conduit-emerald`) and clickable node inspection cards.
- **Glassmorphism Design System:** Built with Tailwind CSS, Lucide icons, dark-mode radial lighting, and micro-animations for zero UI stutter.

### 2. Module A — Real-Time Trust Firewall
Operates in closed-loop cycles during live video calls, interviews, proctored exams, or financial transactions:
1. **Telemetry Streaming:** The client captures media frames and audio buffers, streaming them over `WebSocket /ws/trust/{sessionId}` (or low-latency REST fallback).
2. **Deepfake Video Analysis:** Measures face-boundary jitter, high-frequency neural artifacts, and eye saccade patterns.
3. **Voice Clone & Lip-Sync:** AASIST spectral harmonic inspection detects synthetic text-to-speech vocoders. SyncNet cross-correlation flags lip-motion/audio desync exceeding $100\text{ms}$.
4. **Passkey & SIM-Swap Assertion:** FIDO2 WebAuthn assertions grant trust bonuses; recent carrier IMSI modifications trigger automated risk penalties.
5. **Composite Scoring:** Evaluates a weighted $0 - 100$ score with explainability:
   - 🟢 **GREEN ($\ge 80$):** `ALLOW_SESSION` — Verified authentic, optimal biometric micro-tremors.
   - 🟡 **YELLOW ($50 - 79$):** `WARN_AND_REVERIFY` — Mild latency anomaly or unverified device attestation.
   - 🔴 **RED ($< 50$):** `BLOCK_AND_ISOLATE` — Critical synthetic face-swap or voice clone detected.
6. **Liveness Challenge Engine:** Sends randomized biometric nonces (*e.g., "Blink twice and turn head right"*) with timeout verification.
7. **Tamper-Evident WORM Audit Log:** Appends every event chronologically for instant JSON audit export.

### 3. Module B — Universal Content Passport & Provenance Graph
Verifies and traces documents, academic certificates, exam papers, and media assets:
1. **Multi-Vector Ingestion:** Ingests raw PDFs, images, URLs, or text payloads.
2. **Dual-Hash Fingerprinting:**
   - **SHA-256 Digest:** Provides bit-exact cryptographic integrity validation.
   - **Perceptual dHash:** Gradient difference hashing ($8 \times 8$ resized grayscale matrix) tracks visual identity across re-encodings, resizing, and compressions.
3. **C2PA & Digital Signatures:** Verifies PKCS#7 digital signatures, X.509 certificate chains, and C2PA Content Credentials manifests.
4. **Tamper Forensics (ELA & AI):** Error Level Analysis identifies spliced pixel regions, resaved JPEG compression blocks, and AI generator footprints (`containsAiGeneratedContent: Yes`).
5. **Directed Acyclic Graph (DAG) Generation:** Constructs a connected 6-node provenance pipeline:
   $$\text{Origin Authority} \longrightarrow \text{Author of Record} \longrightarrow \text{Master Asset} \longrightarrow \text{C2PA Seal} \longrightarrow \text{Transit Platform} \longrightarrow \text{TruthScan Ledger}$$
6. **Public Ledger Verification:** Anyone can query any passport by ID (e.g. `CP-A7F29`) or SHA-256 hash to view the cryptographic proof without accessing sensitive document contents.

### 4. The 8-Step Forensic Document Protocol
When official receipts, degrees, or PDFs are uploaded:
1. **Step 1 - Content Inspection:** Typographical anomalies, split words, unnatural math/date mismatches.
2. **Step 2 - Metadata Extraction:** Producer classification (`Canva` = human design, `FPDF`/`ReportLab` = automated billing script, `iLovePDF` = post-generation editor).
3. **Step 3 - Font Hierarchy:** Standard 14 PostScript fonts vs. embedded CID Type 0 subsets.
4. **Step 4 - Image Forensics:** Real text selectable layers vs. flattened raster scans.
5. **Step 5 - Timestamp Cross-Reference:** Creation date vs. printed document datelines.
6. **Step 6 - Machine vs. Human Fingerprints:** Template repetition and synthetic metadata flags.
7. **Step 7 - Institutional Cross-Check:** Registry domain matching and student roll verification.
8. **Step 8 - Verifiable Claims:** Plausibility audit of technical or academic assertions.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend Framework** | HTML5, Tailwind CSS, Three.js (Magic Rings Canvas), Lucide Icons, Vanilla ES6+ |
| **Backend & Routing** | Python 3.12, FastAPI, Uvicorn (ASGI), WebSockets (`websockets`) |
| **AI Reasoning Core** | Google GenAI SDK (`google-genai`), Gemini 3.5 / 3.6 Flash |
| **Computer Vision & Forensics**| Pillow (PIL), NumPy, PyPDF (AST Stream Parsing), Custom ELA Engine |
| **Cryptographic Primitives** | Ed25519 Signatures, SHA-256, Perceptual dHash, C2PA Manifests, WebAuthn/FIDO2 |
| **Deployment & Hosting** | Vercel (Edge Frontend), Python ASGI Server (Local / Cloud Docker) |

---

## 🚀 Quickstart & Setup Guide

### 1. Clone Repository
```bash
git clone https://github.com/UNKNOWN13546/TRUTHSCAN.git
cd TRUTHSCAN
```

### 2. Configure Environment Variables
Create a `.env` file in the root or `backend/` directory:
```env
GEMINI_API_KEY="your-google-gemini-api-key"
VIRUSTOTAL_API_KEY="your-virustotal-api-key"  # Optional
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Run Integration Tests
```bash
python backend/tests/test_modules_ab.py
```
*(Validates Trust Firewall session lifecycle, attack simulations, Content Passport generation, and DAG provenance graph).*

### 5. Launch the Application
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open your browser:
- **Web App Workspace:** `http://127.0.0.1:8000/app`
- **Trust Firewall HUD:** `http://127.0.0.1:8000/app` $\rightarrow$ Click **Trust Firewall** tab
- **Content Passport & DAG:** `http://127.0.0.1:8000/app` $\rightarrow$ Click **Content Passport & Graph** tab
- **Live Vercel Deployment:** [https://truthscan-eta.vercel.app/](https://truthscan-eta.vercel.app/)

---

## 👥 Hackathon Details & Credits
- **Project:** TRUTHSCAN 360
- **Track:** Track 2 — Trust in a Synthetic World
- **Team:** DUOBYTE
- **Team Members:** AYUSH C S, HAIMA KRISHNA
- **Live URL:** [https://truthscan-eta.vercel.app/](https://truthscan-eta.vercel.app/)
- **Repository:** [https://github.com/UNKNOWN13546/TRUTHSCAN](https://github.com/UNKNOWN13546/TRUTHSCAN)
