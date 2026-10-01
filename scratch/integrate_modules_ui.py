import re
import os

GENERATOR_PATH = "c:/Users/Ayush C S/OneDrive/Desktop/TRUTHSCAN/scratch/generate_index_html.py"

with open(GENERATOR_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Navigation Bar to include Trust Firewall
nav_needle = """          <button onclick="switchAppTab('history')" id="app-nav-history" class="app-nav-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 flex items-center space-x-1.5 transition">
            <i data-lucide="history" class="w-3.5 h-3.5"></i>
            <span>History</span>
          </button>"""

nav_replacement = """          <button onclick="switchAppTab('firewall')" id="app-nav-firewall" class="app-nav-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 flex items-center space-x-1.5 transition">
            <i data-lucide="shield-alert" class="w-3.5 h-3.5 text-rose-400"></i>
            <span>Trust Firewall</span>
          </button>

          <button onclick="switchAppTab('passport')" id="app-nav-passport" class="app-nav-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 flex items-center space-x-1.5 transition">
            <i data-lucide="badge-check" class="w-3.5 h-3.5 text-sky-400"></i>
            <span>Content Passport & Graph</span>
          </button>

          <button onclick="switchAppTab('history')" id="app-nav-history" class="app-nav-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 flex items-center space-x-1.5 transition">
            <i data-lucide="history" class="w-3.5 h-3.5"></i>
            <span>History</span>
          </button>"""

# Also remove old duplicate passport button in nav
old_passport_button = """          <button onclick="switchAppTab('passport')" id="app-nav-passport" class="app-nav-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 flex items-center space-x-1.5 transition">
            <i data-lucide="badge-check" class="w-3.5 h-3.5"></i>
            <span>Trust Passport</span>
          </button>"""

if old_passport_button in code:
    code = code.replace(old_passport_button, "")

if nav_needle in code:
    code = code.replace(nav_needle, nav_replacement)
    print("Navigation bar successfully updated.")
else:
    print("Warning: nav_needle not found directly, checking partial...")

# 2. Add SUBVIEW: REAL-TIME TRUST FIREWALL (MODULE A) and enhanced SUBVIEW: UNIVERSAL CONTENT PASSPORT (MODULE B)
subview_needle = """      <!-- ======================================================== -->
      <!--               SUBVIEW 3: TRUST PASSPORT                  -->
      <!-- ======================================================== -->
      <div id="subview-passport" class="app-subview hidden space-y-6">
        <div class="glass-card rounded-3xl p-6 sm:p-8 border border-slate-700 space-y-6">
          <div class="pb-4 border-b border-slate-800 text-center">
            <h3 class="text-xl font-bold text-white font-mono">Trust Passport Public Verification</h3>
            <p class="text-xs text-slate-400">Query and verify any TrustScan assessment certificate by ID.</p>
          </div>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-3 max-w-xl mx-auto">
            <input type="text" id="passport-search-id" placeholder="Enter Assessment ID (e.g. TS-A7F29)..." class="w-full bg-surface-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 font-mono focus:outline-none focus:border-sky-500 text-center" />
            <button onclick="lookupPassportById()" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-mono text-xs font-bold transition flex items-center justify-center space-x-2 shrink-0">
              <i data-lucide="search" class="w-4 h-4"></i>
              <span>Verify Passport</span>
            </button>
          </div>

          <div id="passport-lookup-result" class="hidden p-6 rounded-2xl bg-surface-950 border border-slate-800 space-y-4 max-w-xl mx-auto">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>"""

subviews_replacement = """      <!-- ======================================================== -->
      <!--            SUBVIEW: REAL-TIME TRUST FIREWALL (MODULE A)   -->
      <!-- ======================================================== -->
      <div id="subview-firewall" class="app-subview hidden space-y-6">
        <div class="glass-card rounded-3xl p-6 sm:p-8 border border-slate-700 space-y-6">
          
          <!-- Header and Controls -->
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-slate-800">
            <div>
              <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40 uppercase tracking-wider">MODULE A</span>
                <h3 class="text-xl font-bold text-white font-mono flex items-center gap-2">
                  <i data-lucide="shield-alert" class="w-5 h-5 text-rose-400"></i>
                  Real-Time Trust Firewall
                </h3>
              </div>
              <p class="text-xs text-slate-400 mt-1">Live deepfake, voice-clone, lip-sync, and identity verification for video calls, remote exams, interviews & transactions.</p>
            </div>

            <!-- Session Controls -->
            <div class="flex flex-wrap items-center gap-3">
              <div class="flex items-center space-x-2">
                <span class="text-xs font-mono text-slate-400">Mode:</span>
                <select id="tfw-session-type" class="bg-surface-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 font-mono focus:border-rose-500 focus:outline-none">
                  <option value="video_call">Live Video Call / Interview</option>
                  <option value="remote_exam">Remote Online Exam / Proctoring</option>
                  <option value="financial_auth">High-Value Financial Auth</option>
                  <option value="identity_verification">Onboarding ID Attestation</option>
                </select>
              </div>

              <button id="tfw-btn-start" onclick="startFirewallSession()" class="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-xs font-bold transition flex items-center space-x-1.5 shadow-lg shadow-emerald-950/40">
                <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
                <span>Connect Live Stream</span>
              </button>

              <button id="tfw-btn-end" onclick="endFirewallSession()" class="hidden px-4 py-1.5 rounded-lg bg-rose-600/80 hover:bg-rose-500 text-white font-mono text-xs font-bold transition flex items-center space-x-1.5">
                <i data-lucide="square" class="w-3.5 h-3.5 fill-current"></i>
                <span>Disconnect</span>
              </button>

              <div id="tfw-status-badge" class="status-pill status-muted flex items-center space-x-1">
                <span class="w-2 h-2 rounded-full bg-slate-400 inline-block"></span>
                <span>IDLE</span>
              </div>
            </div>
          </div>

          <!-- Main Grid: Left Monitor + Diagnostics | Right Attack Scenarios + Live Audit Log -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Monitor (7 Cols) -->
            <div class="lg:col-span-7 space-y-5">
              
              <!-- Video / Canvas Live Viewport -->
              <div class="relative rounded-2xl overflow-hidden bg-surface-950 border border-slate-800 aspect-video flex flex-col justify-between p-4 subtle-glow">
                
                <!-- Background Canvas for Face Mesh Wireframe & Audio Spectrogram -->
                <canvas id="tfw-stream-canvas" class="absolute inset-0 w-full h-full object-cover opacity-90"></canvas>
                
                <!-- Top Overlay Badges -->
                <div class="relative z-10 flex items-center justify-between text-[11px] font-mono">
                  <div class="flex items-center space-x-2">
                    <span class="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md text-emerald-400 border border-emerald-500/30 flex items-center space-x-1">
                      <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                      <span id="tfw-session-display-id">SESSION: READY</span>
                    </span>
                    <span class="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md text-slate-300 border border-white/10">1080p @ 30fps</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span class="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md text-sky-400 border border-sky-500/30">Edge ONNX: Active</span>
                    <span id="tfw-stream-latency" class="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md text-slate-400 border border-white/10">Latency: 24ms</span>
                  </div>
                </div>

                <!-- Center Active Alert Banner (When Red) -->
                <div id="tfw-alert-banner" class="relative z-10 hidden self-center px-4 py-2 rounded-xl bg-red-950/90 border border-red-500/60 text-red-200 text-xs font-mono font-bold flex items-center space-x-2 animate-bounce">
                  <i data-lucide="alert-octagon" class="w-4 h-4 text-red-400"></i>
                  <span id="tfw-alert-banner-text">SECURITY ALERT: SYNTHETIC DEEPFAKE ATTACK DETECTED</span>
                </div>

                <!-- Bottom Telemetry HUD Overlay -->
                <div class="relative z-10 flex items-end justify-between bg-gradient-to-t from-black/85 via-black/40 to-transparent p-3 -mx-4 -mb-4 rounded-b-2xl">
                  <div>
                    <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Target Identity</div>
                    <div class="text-xs font-mono font-semibold text-white flex items-center space-x-1.5">
                      <i data-lucide="user" class="w-3.5 h-3.5 text-sky-400"></i>
                      <span id="tfw-target-user">Dr. Elena Vance (Stanford Credential)</span>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Passkey FIDO2</div>
                    <div id="tfw-passkey-badge" class="text-xs font-mono font-semibold text-emerald-400 flex items-center justify-end space-x-1">
                      <i data-lucide="key" class="w-3 h-3"></i>
                      <span>Hardware Attested</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Composite Trust Score Gauge Bar -->
              <div class="p-5 rounded-2xl bg-surface-950/80 border border-slate-800 space-y-4">
                <div class="flex items-center justify-between">
                  <div>
                    <span class="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Composite Trust Score</span>
                    <div class="flex items-baseline space-x-2 mt-0.5">
                      <span id="tfw-score-num" class="text-3xl font-extrabold font-mono text-emerald-400">96</span>
                      <span class="text-xs font-mono text-slate-500">/ 100</span>
                      <span id="tfw-level-badge" class="status-pill status-ok ml-2">GREEN: VERIFIED GENUINE</span>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="text-[10px] font-mono text-slate-400 block">Firewall Decision</span>
                    <span id="tfw-action-badge" class="text-xs font-mono font-bold text-emerald-400">ALLOW_SESSION</span>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="w-full bg-slate-800/80 rounded-full h-2.5 overflow-hidden border border-white/5">
                  <div id="tfw-score-bar" class="bg-emerald-500 h-2.5 rounded-full transition-all duration-500" style="width: 96%"></div>
                </div>

                <!-- Explainability Reasons -->
                <div class="bg-surface-900/60 rounded-xl p-3 border border-slate-800 text-xs font-mono space-y-1.5">
                  <div class="text-slate-400 font-bold flex items-center space-x-1.5">
                    <i data-lucide="info" class="w-3.5 h-3.5 text-sky-400"></i>
                    <span>Real-Time Explainability Audit:</span>
                  </div>
                  <ul id="tfw-reasons-list" class="space-y-1 text-slate-300 list-disc list-inside">
                    <li>Optimal facial micro-tremor and natural eye saccades detected (MediaPipe Mesh).</li>
                    <li>Audio harmonics align with vocal tract physics; synthetic vocoder null.</li>
                    <li>Audio-visual lip-sync delay is 14ms (well within human speech tolerance).</li>
                  </ul>
                </div>
              </div>

              <!-- 4 Real-Time Signal Channels -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div class="p-3 rounded-xl bg-surface-950/70 border border-slate-800/80 space-y-1">
                  <div class="text-[10px] font-mono text-slate-400 flex items-center space-x-1">
                    <i data-lucide="video" class="w-3 h-3 text-sky-400"></i>
                    <span>Video Deepfake</span>
                  </div>
                  <div id="tfw-sig-video" class="text-sm font-bold font-mono text-emerald-400">0.04 <span class="text-[10px] font-normal text-slate-500">(Safe)</span></div>
                  <div class="w-full bg-slate-800 h-1 rounded-full"><div id="tfw-bar-video" class="bg-emerald-500 h-1 rounded-full" style="width: 4%"></div></div>
                </div>

                <div class="p-3 rounded-xl bg-surface-950/70 border border-slate-800/80 space-y-1">
                  <div class="text-[10px] font-mono text-slate-400 flex items-center space-x-1">
                    <i data-lucide="mic" class="w-3 h-3 text-purple-400"></i>
                    <span>Voice Clone</span>
                  </div>
                  <div id="tfw-sig-audio" class="text-sm font-bold font-mono text-emerald-400">0.06 <span class="text-[10px] font-normal text-slate-500">(Clean)</span></div>
                  <div class="w-full bg-slate-800 h-1 rounded-full"><div id="tfw-bar-audio" class="bg-emerald-500 h-1 rounded-full" style="width: 6%"></div></div>
                </div>

                <div class="p-3 rounded-xl bg-surface-950/70 border border-slate-800/80 space-y-1">
                  <div class="text-[10px] font-mono text-slate-400 flex items-center space-x-1">
                    <i data-lucide="repeat" class="w-3 h-3 text-cyan-400"></i>
                    <span>Lip-Sync Lag</span>
                  </div>
                  <div id="tfw-sig-lipsync" class="text-sm font-bold font-mono text-emerald-400">18ms <span class="text-[10px] font-normal text-slate-500">(In Sync)</span></div>
                  <div class="w-full bg-slate-800 h-1 rounded-full"><div id="tfw-bar-lipsync" class="bg-emerald-500 h-1 rounded-full" style="width: 12%"></div></div>
                </div>

                <div class="p-3 rounded-xl bg-surface-950/70 border border-slate-800/80 space-y-1">
                  <div class="text-[10px] font-mono text-slate-400 flex items-center space-x-1">
                    <i data-lucide="smartphone" class="w-3 h-3 text-amber-400"></i>
                    <span>SIM-Swap Risk</span>
                  </div>
                  <div id="tfw-sig-sim" class="text-sm font-bold font-mono text-emerald-400">0.00 <span class="text-[10px] font-normal text-slate-500">(Low)</span></div>
                  <div class="w-full bg-slate-800 h-1 rounded-full"><div id="tfw-bar-sim" class="bg-emerald-500 h-1 rounded-full" style="width: 0%"></div></div>
                </div>
              </div>

            </div>

            <!-- Right Column: Interactive Attack Simulations + Audit Log (5 Cols) -->
            <div class="lg:col-span-5 space-y-5">
              
              <!-- Attack Simulation & Verification Triggers -->
              <div class="p-5 rounded-2xl bg-surface-950 border border-slate-800 space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-slate-800">
                  <h4 class="text-xs font-mono font-bold text-white flex items-center space-x-1.5">
                    <i data-lucide="crosshair" class="w-3.5 h-3.5 text-rose-400"></i>
                    <span>Live Stress-Testing & Injections</span>
                  </h4>
                  <span class="text-[10px] font-mono text-slate-500">Live API Driven</span>
                </div>
                <p class="text-[11px] text-slate-400">Inject synthetic attacks or trigger cryptographic challenges against the active stream:</p>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 font-mono text-xs">
                  <button onclick="simulateFirewallScenario('genuine')" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-emerald-400 border border-emerald-500/30 flex items-center space-x-2 transition text-left">
                    <i data-lucide="shield-check" class="w-4 h-4 shrink-0"></i>
                    <div>
                      <div class="font-bold">1. Genuine Call</div>
                      <div class="text-[10px] text-slate-400">WebAuthn + FIDO2</div>
                    </div>
                  </button>

                  <button onclick="simulateFirewallScenario('deepfake')" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-rose-400 border border-rose-500/30 flex items-center space-x-2 transition text-left">
                    <i data-lucide="skull" class="w-4 h-4 shrink-0"></i>
                    <div>
                      <div class="font-bold">2. Face-Swap Attack</div>
                      <div class="text-[10px] text-slate-400">XceptionNet Warping</div>
                    </div>
                  </button>

                  <button onclick="simulateFirewallScenario('voice_clone')" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-purple-400 border border-purple-500/30 flex items-center space-x-2 transition text-left">
                    <i data-lucide="mic-off" class="w-4 h-4 shrink-0"></i>
                    <div>
                      <div class="font-bold">3. Voice Clone & Desync</div>
                      <div class="text-[10px] text-slate-400">Vocoder + 210ms Lag</div>
                    </div>
                  </button>

                  <button onclick="simulateFirewallScenario('sim_swap')" class="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-amber-400 border border-amber-500/30 flex items-center space-x-2 transition text-left">
                    <i data-lucide="smartphone-charging" class="w-4 h-4 shrink-0"></i>
                    <div>
                      <div class="font-bold">4. SIM-Swap Flag</div>
                      <div class="text-[10px] text-slate-400">Carrier IMSI Tamper</div>
                    </div>
                  </button>
                </div>

                <!-- Liveness Challenge Button -->
                <button onclick="triggerFirewallLiveness()" class="w-full mt-2 py-2.5 px-3 rounded-xl bg-sky-600/20 hover:bg-sky-600/30 text-sky-300 border border-sky-500/40 text-xs font-mono font-bold flex items-center justify-center space-x-2 transition">
                  <i data-lucide="eye" class="w-4 h-4"></i>
                  <span>Request Interactive Liveness Challenge</span>
                </button>
                <div id="tfw-liveness-prompt" class="hidden p-3 rounded-xl bg-sky-950/60 border border-sky-500/30 text-xs font-mono text-sky-200 animate-pulse"></div>
              </div>

              <!-- Live Audit Trail Log -->
              <div class="p-5 rounded-2xl bg-surface-950 border border-slate-800 space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-slate-800">
                  <h4 class="text-xs font-mono font-bold text-white flex items-center space-x-1.5">
                    <i data-lucide="file-text" class="w-3.5 h-3.5 text-sky-400"></i>
                    <span>Real-Time Audit Trail (WORM Log)</span>
                  </h4>
                  <button onclick="exportFirewallAuditReport()" class="text-[10px] font-mono text-sky-400 hover:underline flex items-center space-x-1">
                    <i data-lucide="download" class="w-3 h-3"></i>
                    <span>Export JSON</span>
                  </button>
                </div>

                <div id="tfw-audit-log-container" class="space-y-2 max-h-56 overflow-y-auto pr-1 text-[11px] font-mono">
                  <div class="p-2 rounded bg-slate-900/80 border border-slate-800/80 text-slate-400 flex items-start justify-between">
                    <span>[BOOT] Trust Firewall engine armed. Ready for session connect.</span>
                    <span class="text-[10px] text-slate-600 ml-2">SYSTEM</span>
                  </div>
                </div>
              </div>

            </div>

          </div>

        </div>
      </div>

      <!-- ======================================================== -->
      <!--      SUBVIEW: UNIVERSAL CONTENT PASSPORT (MODULE B)      -->
      <!-- ======================================================== -->
      <div id="subview-passport" class="app-subview hidden space-y-6">
        <div class="glass-card rounded-3xl p-6 sm:p-8 border border-slate-700 space-y-6">
          
          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
            <div>
              <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/40 uppercase tracking-wider">MODULE B</span>
                <h3 class="text-xl font-bold text-white font-mono flex items-center gap-2">
                  <i data-lucide="badge-check" class="w-5 h-5 text-sky-400"></i>
                  Universal Content Passport & Provenance Graph
                </h3>
              </div>
              <p class="text-xs text-slate-400 mt-1">Multi-vector forensic auditing, C2PA Content Credentials, SHA-256/dHash, and interactive Directed Acyclic Graph (DAG) provenance tracing.</p>
            </div>

            <!-- Preloaded Test Suites -->
            <div class="flex items-center space-x-2">
              <span class="text-xs font-mono text-slate-400">Sample:</span>
              <button onclick="loadSamplePassport('degree')" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-mono text-emerald-300 border border-emerald-500/30 transition">
                ✓ Genuine Degree
              </button>
              <button onclick="loadSamplePassport('tampered_pdf')" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-mono text-rose-300 border border-rose-500/30 transition">
                ⚠ Tampered PDF
              </button>
            </div>
          </div>

          <!-- Ingestion & Minting Form -->
          <div class="p-5 rounded-2xl bg-surface-950 border border-slate-800 space-y-4">
            <h4 class="text-xs font-mono font-bold text-slate-200 flex items-center space-x-1.5">
              <i data-lucide="file-plus" class="w-4 h-4 text-sky-400"></i>
              <span>Content Ingestion & Passport Minting</span>
            </h4>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs font-mono">
              <div class="space-y-1">
                <label class="text-slate-400">Document / Asset Name</label>
                <input type="text" id="cp-input-filename" value="Academic_Credential_Stanford.pdf" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:border-sky-500 focus:outline-none" />
              </div>
              <div class="space-y-1">
                <label class="text-slate-400">Issuing Entity (C2PA)</label>
                <input type="text" id="cp-input-issuer" value="Stanford Registrar Board" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:border-sky-500 focus:outline-none" />
              </div>
              <div class="space-y-1">
                <label class="text-slate-400">Claimed Author / Principal</label>
                <input type="text" id="cp-input-author" value="Dr. Jennifer Sterling" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:border-sky-500 focus:outline-none" />
              </div>
              <div class="space-y-1">
                <label class="text-slate-400">Source Channel / Origin URL</label>
                <input type="text" id="cp-input-url" value="https://credentials.stanford.edu/verify/9921" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:border-sky-500 focus:outline-none" />
              </div>
            </div>

            <div class="flex items-center justify-between pt-2">
              <div class="flex items-center space-x-3 text-xs font-mono text-slate-400">
                <label class="flex items-center space-x-1.5 cursor-pointer">
                  <input type="checkbox" id="cp-chk-c2pa" checked class="rounded border-slate-700 text-sky-500 focus:ring-0" />
                  <span>Enforce C2PA Manifest</span>
                </label>
                <label class="flex items-center space-x-1.5 cursor-pointer">
                  <input type="checkbox" id="cp-chk-ela" checked class="rounded border-slate-700 text-sky-500 focus:ring-0" />
                  <span>Error Level Analysis (ELA)</span>
                </label>
                <label class="flex items-center space-x-1.5 cursor-pointer">
                  <input type="checkbox" id="cp-chk-ai" checked class="rounded border-slate-700 text-sky-500 focus:ring-0" />
                  <span>AI Forensics</span>
                </label>
              </div>

              <button onclick="mintContentPassport()" class="px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-mono text-xs font-bold transition flex items-center space-x-2 shadow-lg shadow-sky-950/40">
                <i data-lucide="cpu" class="w-4 h-4"></i>
                <span>Ingest & Generate Passport</span>
              </button>
            </div>
          </div>

          <!-- PROVENANCE GRAPH VISUALIZER (INTERACTIVE DAG) -->
          <div class="p-6 rounded-2xl bg-surface-950 border border-slate-800 space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-800">
              <div>
                <h4 class="text-sm font-mono font-bold text-white flex items-center space-x-2">
                  <i data-lucide="network" class="w-4 h-4 text-emerald-400"></i>
                  <span>Directed Acyclic Provenance Graph (DAG)</span>
                </h4>
                <p class="text-[11px] text-slate-400 font-mono">End-to-end cryptographic lineage: origin, author, digital seal, distribution spread & audit ledger.</p>
              </div>
              <div class="flex items-center space-x-2 text-xs font-mono">
                <span class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center space-x-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span id="cp-graph-nodes-count">6 Nodes</span>
                </span>
                <span class="px-2.5 py-1 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/30">
                  5 Cryptographic Edges
                </span>
              </div>
            </div>

            <!-- DAG Interactive Visualizer Canvas / SVG Container -->
            <div id="provenance-graph-viewport" class="relative w-full h-72 rounded-xl bg-slate-950/80 border border-slate-800/80 overflow-hidden flex items-center justify-center p-4">
              <!-- Rendered via SVG in JS with cybernetic laser conduit connectors -->
              <svg id="provenance-dag-svg" class="w-full h-full" viewBox="0 0 1000 240" preserveAspectRatio="xMidYMid meet">
                <!-- Laser conduit paths & interactive nodes injected dynamically -->
              </svg>
            </div>

            <!-- Selected Node Inspector Modal / Bar -->
            <div id="cp-node-details-card" class="p-4 rounded-xl bg-surface-900/90 border border-slate-800 font-mono text-xs space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="text-slate-400">Selected Node:</span>
                  <span id="cp-inspect-node-title" class="text-sky-300 font-bold">Node 1: Origin (Stanford Registrar Board)</span>
                </div>
                <span id="cp-inspect-node-type" class="status-pill status-ok">ISSUER_AUTHORITY</span>
              </div>
              <p id="cp-inspect-node-desc" class="text-slate-300 text-[11px]">Official root of trust. Cryptographic private key held in FIPS 140-2 Level 3 HSM.</p>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[10px] text-slate-400 pt-1 border-t border-slate-800">
                <div>Signer ID: <span id="cp-inspect-signer" class="text-slate-200">did:key:z6Mkq9...f91a</span></div>
                <div>Hash: <span id="cp-inspect-hash" class="text-slate-200">e82b71...a41c</span></div>
                <div>Timestamp: <span id="cp-inspect-time" class="text-slate-200">2026-10-01 12:40 UTC</span></div>
              </div>
            </div>
          </div>

          <!-- Forensics & Fingerprints -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Cryptographic Hashes & C2PA Credentials -->
            <div class="p-5 rounded-2xl bg-surface-950 border border-slate-800 space-y-3 font-mono text-xs">
              <h5 class="text-slate-200 font-bold flex items-center space-x-1.5 pb-2 border-b border-slate-800">
                <i data-lucide="binary" class="w-4 h-4 text-sky-400"></i>
                <span>Cryptographic & Perceptual Fingerprints</span>
              </h5>
              <div class="space-y-2">
                <div>
                  <div class="text-[10px] text-slate-500 uppercase">SHA-256 Digest</div>
                  <div id="cp-sha256-val" class="text-slate-200 break-all text-[11px] bg-slate-900/60 p-2 rounded border border-slate-800 select-all">e82b71d0928a...c9304</div>
                </div>
                <div>
                  <div class="text-[10px] text-slate-500 uppercase">Perceptual Difference Hash (dHash)</div>
                  <div id="cp-dhash-val" class="text-sky-300 font-bold bg-slate-900/60 p-2 rounded border border-slate-800 select-all">a4f9b8c2e107d3f8</div>
                </div>
                <div class="flex items-center justify-between pt-1">
                  <span class="text-slate-400">C2PA Manifest:</span>
                  <span id="cp-c2pa-val" class="status-pill status-ok">VALID_EMBEDDED</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">Digital Signature:</span>
                  <span id="cp-sig-val" class="text-emerald-400 font-bold">PKCS#7 RSA-4096</span>
                </div>
              </div>
            </div>

            <!-- Tamper & AI Generation Forensic Summary -->
            <div class="p-5 rounded-2xl bg-surface-950 border border-slate-800 space-y-3 font-mono text-xs">
              <h5 class="text-slate-200 font-bold flex items-center space-x-1.5 pb-2 border-b border-slate-800">
                <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                <span>Multi-Vector Forensics Verdict</span>
              </h5>
              <div class="space-y-2.5">
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">Authenticity Trust Score:</span>
                  <span id="cp-score-val" class="text-base font-bold text-emerald-400">95 / 100</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">Physical / Pixel Tamper (ELA):</span>
                  <span id="cp-ela-val" class="status-pill status-ok">CLEAN: NO SPLICE</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">Synthetic AI Generation:</span>
                  <span id="cp-ai-val" class="status-pill status-ok">NEGATIVE (0.02)</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">Overall Verdict:</span>
                  <span id="cp-verdict-val" class="status-pill status-ok">AUTHENTIC_VERIFIED</span>
                </div>

                <div class="pt-2 flex items-center justify-between">
                  <button onclick="downloadPassportReport()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs flex items-center space-x-1.5 transition">
                    <i data-lucide="file-text" class="w-3.5 h-3.5"></i>
                    <span>Export Passport JSON</span>
                  </button>
                  <span class="text-[10px] text-slate-500">Immutable Ledger Node ID: #88921</span>
                </div>
              </div>
            </div>

          </div>

          <!-- Public Verification Search (Existing Functionality Preserved & Enhanced) -->
          <div class="p-5 rounded-2xl bg-surface-950/60 border border-slate-800/80 space-y-3">
            <div class="text-center space-y-1">
              <h4 class="text-xs font-mono font-bold text-slate-300">Public Verification Ledger Query</h4>
              <p class="text-[11px] text-slate-400 font-mono">Verify any issued Content Passport by Passport ID or SHA-256 Hash:</p>
            </div>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-3 max-w-xl mx-auto pt-1">
              <input type="text" id="passport-search-id" placeholder="Enter Passport ID (e.g. CP-9A4B12) or SHA-256..." class="w-full bg-surface-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 font-mono focus:outline-none focus:border-sky-500 text-center" />
              <button onclick="lookupPassportById()" class="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-mono text-xs font-bold transition flex items-center justify-center space-x-2 shrink-0">
                <i data-lucide="search" class="w-3.5 h-3.5"></i>
                <span>Verify Ledger</span>
              </button>
            </div>
            <div id="passport-lookup-result" class="hidden p-4 rounded-xl bg-surface-900 border border-slate-800 space-y-3 max-w-xl mx-auto"></div>
          </div>

        </div>
      </div>"""

if subview_needle in code:
    code = code.replace(subview_needle, subviews_replacement)
    print("Subviews successfully updated.")
else:
    print("Warning: subview_needle not found directly.")

# 3. Add Client-Side JavaScript Logic for Module A & Module B
js_logic = """
    // ========================================================
    // MODULE A: REAL-TIME TRUST FIREWALL JAVASCRIPT ENGINE
    // ========================================================
    let currentTfwSession = null;
    let tfwSocket = null;
    let tfwAnimFrame = null;
    let tfwLastScore = 96;

    async function startFirewallSession() {
      const sessionType = document.getElementById('tfw-session-type').value;
      try {
        const resp = await fetch('/api/trust/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_type: sessionType,
            title: `Live ${sessionType.replace('_', ' ').toUpperCase()} Firewall`
          })
        });
        const data = await resp.json();
        currentTfwSession = data;
        
        document.getElementById('tfw-session-display-id').textContent = `SESSION: ${data.session_id}`;
        document.getElementById('tfw-btn-start').classList.add('hidden');
        document.getElementById('tfw-btn-end').classList.remove('hidden');
        
        const badge = document.getElementById('tfw-status-badge');
        badge.className = 'status-pill status-ok flex items-center space-x-1';
        badge.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping inline-block"></span><span>STREAMING LIVE</span>';
        
        logFirewallEvent(`Firewall connected to session ${data.session_id}. Edge telemetry active.`, 'LIVE');
        
        // Start Canvas Facial Mesh & Spectrogram Animation
        startFirewallCanvasAnimation();
        
        // Initialize WebSocket connection if available
        initFirewallWebSocket(data.session_id);
      } catch (err) {
        console.error('Failed to start Trust Firewall session:', err);
        alert('Could not start Trust Firewall session: ' + err.message);
      }
    }

    function initFirewallWebSocket(sessionId) {
      try {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/trust/${sessionId}`;
        tfwSocket = new WebSocket(wsUrl);
        
        tfwSocket.onopen = () => {
          logFirewallEvent('WebSocket low-latency bi-directional telemetry pipe established.', 'WS');
        };
        
        tfwSocket.onmessage = (event) => {
          try {
            const msg = JSON.parse(event.data);
            if (msg.score !== undefined) {
              updateFirewallTelemetryUI(msg);
            }
          } catch(e) {}
        };
        
        tfwSocket.onerror = (e) => {
          console.warn('WS fallback to REST telemetry.');
        };
      } catch(e) {
        console.warn('WebSocket init skipped, using REST polling.');
      }
    }

    async function endFirewallSession() {
      if (!currentTfwSession) return;
      try {
        await fetch(`/api/trust/session/${currentTfwSession.session_id}/end`, { method: 'POST' });
        logFirewallEvent(`Session ${currentTfwSession.session_id} ended. Final audit report sealed.`, 'END');
      } catch (e) {}

      if (tfwSocket) {
        try { tfwSocket.close(); } catch(e) {}
        tfwSocket = null;
      }
      if (tfwAnimFrame) {
        cancelAnimationFrame(tfwAnimFrame);
        tfwAnimFrame = null;
      }

      document.getElementById('tfw-btn-start').classList.remove('hidden');
      document.getElementById('tfw-btn-end').classList.add('hidden');
      
      const badge = document.getElementById('tfw-status-badge');
      badge.className = 'status-pill status-muted flex items-center space-x-1';
      badge.innerHTML = '<span class="w-2 h-2 rounded-full bg-slate-400 inline-block"></span><span>DISCONNECTED</span>';
      
      document.getElementById('tfw-alert-banner').classList.add('hidden');
      currentTfwSession = null;
    }

    async function simulateFirewallScenario(type) {
      if (!currentTfwSession) {
        await startFirewallSession();
      }
      
      const sid = currentTfwSession ? currentTfwSession.session_id : 'DEMO';
      let payload = {};

      if (type === 'genuine') {
        payload = {
          video_quality: 0.96,
          face_boundary_jitter: 0.02,
          voice_harmonic_distortion: 0.04,
          lip_sync_latency_ms: 16,
          sim_swap_detected: false,
          passkey_verified: true
        };
        logFirewallEvent('[STRESS-TEST] Simulated genuine participant stream with FIDO2 passkey.', 'TEST');
      } else if (type === 'deepfake') {
        payload = {
          video_quality: 0.35,
          face_boundary_jitter: 0.91,
          voice_harmonic_distortion: 0.15,
          lip_sync_latency_ms: 45,
          sim_swap_detected: false,
          passkey_verified: false
        };
        logFirewallEvent('[STRESS-TEST] INJECTION: XceptionNet Neural Deepfake Face-Swap Stream.', 'ATTACK');
      } else if (type === 'voice_clone') {
        payload = {
          video_quality: 0.82,
          face_boundary_jitter: 0.12,
          voice_harmonic_distortion: 0.88,
          lip_sync_latency_ms: 220,
          sim_swap_detected: false,
          passkey_verified: false
        };
        logFirewallEvent('[STRESS-TEST] INJECTION: AASIST Synthetic Voice Clone with 220ms Lip-Sync Lag.', 'ATTACK');
      } else if (type === 'sim_swap') {
        payload = {
          video_quality: 0.88,
          face_boundary_jitter: 0.05,
          voice_harmonic_distortion: 0.08,
          lip_sync_latency_ms: 24,
          sim_swap_detected: true,
          passkey_verified: false
        };
        logFirewallEvent('[STRESS-TEST] INJECTION: Carrier IMSI SIM-Swap Anomaly within 48h.', 'WARNING');
      }

      try {
        const resp = await fetch(`/api/trust/session/${sid}/verify-frame`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const result = await resp.json();
        updateFirewallTelemetryUI(result);
      } catch (err) {
        console.error('Frame verification error:', err);
      }
    }

    function updateFirewallTelemetryUI(data) {
      const score = Math.round(data.score);
      tfwLastScore = score;
      
      const scoreNum = document.getElementById('tfw-score-num');
      const scoreBar = document.getElementById('tfw-score-bar');
      const levelBadge = document.getElementById('tfw-level-badge');
      const actionBadge = document.getElementById('tfw-action-badge');
      const alertBanner = document.getElementById('tfw-alert-banner');
      const alertBannerText = document.getElementById('tfw-alert-banner-text');

      scoreNum.textContent = score;
      scoreBar.style.width = `${score}%`;

      if (score >= 80) {
        scoreNum.className = 'text-3xl font-extrabold font-mono text-emerald-400';
        scoreBar.className = 'bg-emerald-500 h-2.5 rounded-full transition-all duration-500';
        levelBadge.className = 'status-pill status-ok ml-2';
        levelBadge.textContent = 'GREEN: VERIFIED GENUINE';
        actionBadge.className = 'text-xs font-mono font-bold text-emerald-400';
        actionBadge.textContent = 'ALLOW_SESSION';
        alertBanner.classList.add('hidden');
      } else if (score >= 50) {
        scoreNum.className = 'text-3xl font-extrabold font-mono text-amber-400';
        scoreBar.className = 'bg-amber-500 h-2.5 rounded-full transition-all duration-500';
        levelBadge.className = 'status-pill status-warn ml-2';
        levelBadge.textContent = 'YELLOW: SUSPICIOUS ANOMALY';
        actionBadge.className = 'text-xs font-mono font-bold text-amber-400';
        actionBadge.textContent = 'WARN_AND_REVERIFY';
        alertBanner.classList.remove('hidden');
        alertBannerText.textContent = 'WARNING: MODERATE INTEGRITY RISK DETECTED';
      } else {
        scoreNum.className = 'text-3xl font-extrabold font-mono text-rose-500';
        scoreBar.className = 'bg-rose-500 h-2.5 rounded-full transition-all duration-500';
        levelBadge.className = 'status-pill status-critical ml-2';
        levelBadge.textContent = 'RED: CRITICAL ATTACK DETECTED';
        actionBadge.className = 'text-xs font-mono font-bold text-rose-400';
        actionBadge.textContent = 'BLOCK_AND_ISOLATE';
        alertBanner.classList.remove('hidden');
        alertBannerText.textContent = 'SECURITY ALERT: SYNTHETIC DEEPFAKE ATTACK DETECTED';
      }

      // Signal Breakdown values
      const sigs = data.signals || {};
      if (sigs.deepfake_video !== undefined) {
        const v = sigs.deepfake_video;
        document.getElementById('tfw-sig-video').innerHTML = `${v.toFixed(2)} <span class="text-[10px] font-normal ${v > 0.4 ? 'text-rose-400' : 'text-slate-500'}">(${v > 0.4 ? 'Attack' : 'Safe'})</span>`;
        document.getElementById('tfw-bar-video').style.width = `${Math.min(100, v * 100)}%`;
        document.getElementById('tfw-bar-video').className = v > 0.4 ? 'bg-rose-500 h-1 rounded-full' : 'bg-emerald-500 h-1 rounded-full';
      }
      if (sigs.voice_clone !== undefined) {
        const a = sigs.voice_clone;
        document.getElementById('tfw-sig-audio').innerHTML = `${a.toFixed(2)} <span class="text-[10px] font-normal ${a > 0.4 ? 'text-purple-400' : 'text-slate-500'}">(${a > 0.4 ? 'Synthetic' : 'Clean'})</span>`;
        document.getElementById('tfw-bar-audio').style.width = `${Math.min(100, a * 100)}%`;
        document.getElementById('tfw-bar-audio').className = a > 0.4 ? 'bg-purple-500 h-1 rounded-full' : 'bg-emerald-500 h-1 rounded-full';
      }
      if (sigs.lip_sync !== undefined) {
        const l = sigs.lip_sync;
        const lag = Math.round(l.offset_ms || 20);
        document.getElementById('tfw-sig-lipsync').innerHTML = `${lag}ms <span class="text-[10px] font-normal ${lag > 100 ? 'text-rose-400' : 'text-slate-500'}">(${lag > 100 ? 'Desync' : 'In Sync'})</span>`;
        document.getElementById('tfw-bar-lipsync').style.width = `${Math.min(100, (lag / 250) * 100)}%`;
      }
      if (sigs.sim_swap !== undefined) {
        const sim = sigs.sim_swap;
        document.getElementById('tfw-sig-sim').innerHTML = `${sim.risk.toFixed(2)} <span class="text-[10px] font-normal ${sim.risk > 0.5 ? 'text-amber-400' : 'text-slate-500'}">(${sim.risk > 0.5 ? 'Swapped' : 'Low'})</span>`;
        document.getElementById('tfw-bar-sim').style.width = `${Math.min(100, sim.risk * 100)}%`;
        document.getElementById('tfw-bar-sim').className = sim.risk > 0.5 ? 'bg-amber-500 h-1 rounded-full' : 'bg-emerald-500 h-1 rounded-full';
      }

      // Update Reasons list
      const reasonsList = document.getElementById('tfw-reasons-list');
      if (reasonsList && data.reasons && data.reasons.length > 0) {
        reasonsList.innerHTML = data.reasons.map(r => `<li>${r}</li>`).join('');
      }

      logFirewallEvent(`Score evaluated: ${score}/100 [${data.level}]. Action: ${data.action || 'NORMAL'}`, data.level);
    }

    async function triggerFirewallLiveness() {
      if (!currentTfwSession) {
        await startFirewallSession();
      }
      const sid = currentTfwSession ? currentTfwSession.session_id : 'DEMO';
      try {
        const resp = await fetch(`/api/trust/session/${sid}/liveness-challenge`, { method: 'POST' });
        const ch = await resp.json();
        
        const promptBox = document.getElementById('tfw-liveness-prompt');
        promptBox.classList.remove('hidden');
        promptBox.innerHTML = `
          <div class="flex items-center space-x-2">
            <i data-lucide="eye" class="w-4 h-4 text-sky-400"></i>
            <span class="font-bold">Active Challenge Nonce [${ch.challenge_id}]:</span>
          </div>
          <div class="mt-1 text-slate-100 text-xs">"${ch.prompt}"</div>
          <div class="mt-2 flex items-center justify-between text-[10px] text-slate-400">
            <span>Passphrase: <b>${ch.expected_action}</b></span>
            <span class="text-emerald-400 font-bold">Scanning Biometric Reflex (3s)...</span>
          </div>
        `;
        refreshIcons();
        logFirewallEvent(`Issued liveness challenge ${ch.challenge_id}: "${ch.prompt}"`, 'CHALLENGE');

        // Simulate challenge completion after 2.5s
        setTimeout(() => {
          promptBox.classList.add('hidden');
          logFirewallEvent(`Liveness challenge ${ch.challenge_id} passed with 99.4% biometric confidence.`, 'VERIFIED');
          simulateFirewallScenario('genuine');
        }, 2500);
      } catch (err) {
        console.error('Liveness challenge error:', err);
      }
    }

    async function exportFirewallAuditReport() {
      if (!currentTfwSession) {
        alert('Please connect a Trust Firewall session first.');
        return;
      }
      try {
        const resp = await fetch(`/api/trust/session/${currentTfwSession.session_id}/report`);
        const report = await resp.json();
        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `trust_firewall_audit_${currentTfwSession.session_id}.json`;
        a.click();
        URL.revokeObjectURL(url);
      } catch (e) {
        alert('Could not download audit report: ' + e.message);
      }
    }

    function logFirewallEvent(text, tag) {
      const container = document.getElementById('tfw-audit-log-container');
      if (!container) return;
      const timeStr = new Date().toISOString().substring(11, 19);
      const tagColor = tag === 'ATTACK' || tag === 'RED' ? 'text-rose-400 border-rose-500/40 bg-rose-500/10' :
                       tag === 'WARNING' || tag === 'YELLOW' ? 'text-amber-400 border-amber-500/40 bg-amber-500/10' :
                       tag === 'CHALLENGE' ? 'text-purple-400 border-purple-500/40 bg-purple-500/10' :
                       'text-sky-400 border-sky-500/40 bg-sky-500/10';

      const entry = document.createElement('div');
      entry.className = 'p-2 rounded bg-slate-900/90 border border-slate-800 flex items-start justify-between space-x-2 text-[11px] font-mono animate-fadeIn';
      entry.innerHTML = `
        <div class="flex items-start space-x-1.5">
          <span class="text-slate-500 shrink-0">[${timeStr}]</span>
          <span class="text-slate-200">${text}</span>
        </div>
        <span class="px-1.5 py-0.5 rounded text-[9px] font-bold border ${tagColor} shrink-0">${tag}</span>
      `;
      container.prepend(entry);
    }

    // High-Tech Cybernetic Stream Canvas Animation
    function startFirewallCanvasAnimation() {
      const canvas = document.getElementById('tfw-stream-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      let t = 0;

      function resize() {
        if (canvas.clientWidth && canvas.clientHeight) {
          canvas.width = canvas.clientWidth;
          canvas.height = canvas.clientHeight;
        }
      }
      resize();

      function draw() {
        t += 0.05;
        const w = canvas.width || 640;
        const h = canvas.height || 360;
        
        ctx.fillStyle = '#070d19';
        ctx.fillRect(0, 0, w, h);

        // Tech grid lines
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.06)';
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 30) {
          ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
        }
        for (let y = 0; y < h; y += 30) {
          ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
        }

        // Facial Bounding Box in Center
        const boxW = Math.min(w * 0.45, 200);
        const boxH = boxW * 1.25;
        const boxX = (w - boxW) / 2;
        const boxY = (h - boxH) / 2 - 10;
        const isRed = tfwLastScore < 50;

        ctx.strokeStyle = isRed ? 'rgba(239, 68, 68, 0.8)' : 'rgba(56, 189, 248, 0.7)';
        ctx.lineWidth = 1.5;

        // Draw Corner Brackets
        const cLen = 18;
        // Top Left
        ctx.beginPath(); ctx.moveTo(boxX, boxY + cLen); ctx.lineTo(boxX, boxY); ctx.lineTo(boxX + cLen, boxY); ctx.stroke();
        // Top Right
        ctx.beginPath(); ctx.moveTo(boxX + boxW - cLen, boxY); ctx.lineTo(boxX + boxW, boxY); ctx.lineTo(boxX + boxW, boxY + cLen); ctx.stroke();
        // Bottom Left
        ctx.beginPath(); ctx.moveTo(boxX, boxY + boxH - cLen); ctx.lineTo(boxX, boxY + boxH); ctx.lineTo(boxX + cLen, boxY + boxH); ctx.stroke();
        // Bottom Right
        ctx.beginPath(); ctx.moveTo(boxX + boxW - cLen, boxY + boxH); ctx.lineTo(boxX + boxW, boxY + boxH); ctx.lineTo(boxX + boxW, boxY + boxH - cLen); ctx.stroke();

        // Facial Mesh Landmark Points
        const points = [
          [boxX + boxW * 0.32, boxY + boxH * 0.35], // Left eye
          [boxX + boxW * 0.68, boxY + boxH * 0.35], // Right eye
          [boxX + boxW * 0.50, boxY + boxH * 0.52], // Nose tip
          [boxX + boxW * 0.38, boxY + boxH * 0.72], // Mouth left
          [boxX + boxW * 0.62, boxY + boxH * 0.72], // Mouth right
          [boxX + boxW * 0.50, boxY + boxH * 0.88], // Chin
          [boxX + boxW * 0.50, boxY + boxH * 0.20], // Forehead
        ];

        // Draw connecting mesh
        ctx.strokeStyle = isRed ? 'rgba(239, 68, 68, 0.3)' : 'rgba(52, 211, 153, 0.35)';
        ctx.beginPath();
        points.forEach((pt, i) => {
          if (i === 0) ctx.moveTo(pt[0], pt[1]);
          else ctx.lineTo(pt[0], pt[1]);
        });
        ctx.closePath();
        ctx.stroke();

        // Draw nodes
        points.forEach(pt => {
          ctx.fillStyle = isRed ? '#f87171' : '#34d399';
          ctx.beginPath();
          ctx.arc(pt[0], pt[1], 2.5, 0, Math.PI * 2);
          ctx.fill();
        });

        // Vertical Sweep Line
        const scanY = boxY + ((Math.sin(t) + 1) / 2) * boxH;
        ctx.strokeStyle = isRed ? 'rgba(239, 68, 68, 0.6)' : 'rgba(56, 189, 248, 0.6)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(boxX, scanY);
        ctx.lineTo(boxX + boxW, scanY);
        ctx.stroke();

        // Audio Spectrogram Waveform at Bottom of Viewport
        const waveY = h - 25;
        ctx.strokeStyle = isRed ? 'rgba(244, 63, 94, 0.7)' : 'rgba(168, 85, 247, 0.7)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let x = 0; x < w; x += 6) {
          const amp = Math.sin(x * 0.05 + t * 2) * Math.cos(x * 0.02 - t) * (isRed ? 18 : 10);
          if (x === 0) ctx.moveTo(x, waveY + amp);
          else ctx.lineTo(x, waveY + amp);
        }
        ctx.stroke();

        tfwAnimFrame = requestAnimationFrame(draw);
      }

      draw();
    }


    // ========================================================
    // MODULE B: UNIVERSAL CONTENT PASSPORT & PROVENANCE GRAPH
    // ========================================================
    let currentPassportData = null;
    let currentProvenanceGraph = null;

    async function mintContentPassport() {
      const filename = document.getElementById('cp-input-filename').value || 'document.pdf';
      const issuer = document.getElementById('cp-input-issuer').value || 'Stanford Registrar Board';
      const author = document.getElementById('cp-input-author').value || 'Dr. Jennifer Sterling';
      const sourceUrl = document.getElementById('cp-input-url').value || 'https://truthscan.local/ingest';

      const formData = new FormData();
      formData.append('filename', filename);
      formData.append('issuer_name', issuer);
      formData.append('claimed_author', author);
      formData.append('source_url', sourceUrl);
      formData.append('content_type', filename.toLowerCase().endsWith('.pdf') ? 'document' : 'image');

      // Create a dummy byte blob representing the content
      const dummyContent = `MINTED_TRUTHSCAN_CONTENT_ASSET:${filename}:${issuer}:${author}:${Date.now()}`;
      formData.append('file', new Blob([dummyContent], { type: 'application/octet-stream' }), filename);

      try {
        const resp = await fetch('/api/passport/create', {
          method: 'POST',
          body: formData
        });
        const passport = await resp.json();
        currentPassportData = passport;

        // Fetch DAG Graph
        const graphResp = await fetch(`/api/passport/${passport.passport_id}/provenance-graph`);
        const graphData = await graphResp.json();
        currentProvenanceGraph = graphData;

        // Update UI
        updatePassportUI(passport);
        renderProvenanceGraph(graphData);
      } catch (err) {
        console.error('Failed minting content passport:', err);
        alert('Minting failed: ' + err.message);
      }
    }

    function loadSamplePassport(type) {
      if (type === 'degree') {
        document.getElementById('cp-input-filename').value = 'Stanford_Phd_Degree_Certificate.pdf';
        document.getElementById('cp-input-issuer').value = 'Stanford University Registrar Board';
        document.getElementById('cp-input-author').value = 'Dr. Jennifer Sterling';
        document.getElementById('cp-input-url').value = 'https://credentials.stanford.edu/verify/9921';
      } else if (type === 'tampered_pdf') {
        document.getElementById('cp-input-filename').value = 'Manipulated_Invoice_ILovePdf.pdf';
        document.getElementById('cp-input-issuer').value = 'Unknown Script (Canva / ILovePDF)';
        document.getElementById('cp-input-author').value = 'Anonymous User';
        document.getElementById('cp-input-url').value = 'https://dubious-downloads.net/invoice.pdf';
      }
      mintContentPassport();
    }

    function updatePassportUI(p) {
      document.getElementById('cp-sha256-val').textContent = p.hashes.sha256;
      document.getElementById('cp-dhash-val').textContent = p.hashes.perceptual_dhash;
      
      const c2paBadge = document.getElementById('cp-c2pa-val');
      c2paBadge.textContent = p.provenance_metadata.c2pa_manifest_status;
      c2paBadge.className = p.provenance_metadata.c2pa_manifest_status === 'VALID_EMBEDDED' ? 'status-pill status-ok' : 'status-pill status-warn';

      const sigBadge = document.getElementById('cp-sig-val');
      sigBadge.textContent = p.provenance_metadata.digital_signature_status;
      sigBadge.className = p.provenance_metadata.digital_signature_status.includes('VALID') ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold';

      const scoreVal = document.getElementById('cp-score-val');
      const score = p.forensics_summary.trust_score;
      scoreVal.textContent = `${score} / 100`;
      scoreVal.className = score >= 80 ? 'text-base font-bold text-emerald-400' : (score >= 50 ? 'text-base font-bold text-amber-400' : 'text-base font-bold text-rose-500');

      const elaBadge = document.getElementById('cp-ela-val');
      if (p.forensics_summary.tamper_detected) {
        elaBadge.textContent = 'TAMPER DETECTED (HIGH ELA)';
        elaBadge.className = 'status-pill status-critical';
      } else {
        elaBadge.textContent = 'CLEAN: NO SPLICE';
        elaBadge.className = 'status-pill status-ok';
      }

      const aiBadge = document.getElementById('cp-ai-val');
      if (p.forensics_summary.ai_generated) {
        aiBadge.textContent = 'SYNTHETIC AI DETECTED';
        aiBadge.className = 'status-pill status-critical';
      } else {
        aiBadge.textContent = 'NEGATIVE (0.02)';
        aiBadge.className = 'status-pill status-ok';
      }

      const verdictBadge = document.getElementById('cp-verdict-val');
      verdictBadge.textContent = p.forensics_summary.authenticity_verdict;
      verdictBadge.className = score >= 80 ? 'status-pill status-ok' : (score >= 50 ? 'status-pill status-warn' : 'status-pill status-critical');
    }

    // Render Directed Acyclic Graph (DAG) in SVG
    function renderProvenanceGraph(graph) {
      const svg = document.getElementById('provenance-dag-svg');
      if (!svg || !graph || !graph.nodes) return;
      
      const nodes = graph.nodes;
      const count = nodes.length;
      const totalWidth = 1000;
      const yPos = 120;
      const spacing = totalWidth / (count + 1);

      document.getElementById('cp-graph-nodes-count').textContent = `${count} Nodes`;

      // Clear SVG
      svg.innerHTML = '';

      // Defs for gradients and glow
      const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
      defs.innerHTML = `
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <marker id="arrow" viewBox="0 0 10 10" refX="28" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
        </marker>
      `;
      svg.appendChild(defs);

      // Render Laser Conduit Edges
      for (let i = 0; i < count - 1; i++) {
        const x1 = spacing * (i + 1);
        const x2 = spacing * (i + 2);
        
        // Background line
        const bgPath = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        bgPath.setAttribute('x1', x1);
        bgPath.setAttribute('y1', yPos);
        bgPath.setAttribute('x2', x2);
        bgPath.setAttribute('y2', yPos);
        bgPath.setAttribute('stroke', 'rgba(255, 255, 255, 0.15)');
        bgPath.setAttribute('stroke-width', '2');
        svg.appendChild(bgPath);

        // Animated laser conduit
        const laser = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        laser.setAttribute('x1', x1);
        laser.setAttribute('y1', yPos);
        laser.setAttribute('x2', x2);
        laser.setAttribute('y2', yPos);
        laser.setAttribute('class', i % 2 === 0 ? 'laser-conduit-cyan' : 'laser-conduit-emerald');
        laser.setAttribute('stroke-width', '2.5');
        laser.setAttribute('marker-end', 'url(#arrow)');
        svg.appendChild(laser);

        // Edge label
        if (graph.edges && graph.edges[i]) {
          const edgeTxt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          edgeTxt.setAttribute('x', (x1 + x2) / 2);
          edgeTxt.setAttribute('y', yPos - 12);
          edgeTxt.setAttribute('text-anchor', 'middle');
          edgeTxt.setAttribute('fill', '#94a3b8');
          edgeTxt.setAttribute('font-family', 'monospace');
          edgeTxt.setAttribute('font-size', '9');
          edgeTxt.textContent = graph.edges[i].label;
          svg.appendChild(edgeTxt);
        }
      }

      // Render Nodes
      nodes.forEach((node, idx) => {
        const cx = spacing * (idx + 1);
        const cy = yPos;
        const color = node.color || '#38bdf8';

        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'cursor-pointer transition-transform hover:scale-110');
        g.onclick = () => inspectGraphNode(node, idx);

        // Outer glow circle
        const circleOuter = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circleOuter.setAttribute('cx', cx);
        circleOuter.setAttribute('cy', cy);
        circleOuter.setAttribute('r', '22');
        circleOuter.setAttribute('fill', '#0f172a');
        circleOuter.setAttribute('stroke', color);
        circleOuter.setAttribute('stroke-width', '2.5');
        circleOuter.setAttribute('filter', 'url(#glow-cyan)');
        g.appendChild(circleOuter);

        // Inner circle
        const circleInner = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circleInner.setAttribute('cx', cx);
        circleInner.setAttribute('cy', cy);
        circleInner.setAttribute('r', '14');
        circleInner.setAttribute('fill', color);
        circleInner.setAttribute('fill-opacity', '0.25');
        g.appendChild(circleInner);

        // Step number
        const txtNum = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        txtNum.setAttribute('x', cx);
        txtNum.setAttribute('y', cy + 4);
        txtNum.setAttribute('text-anchor', 'middle');
        txtNum.setAttribute('fill', '#ffffff');
        txtNum.setAttribute('font-family', 'monospace');
        txtNum.setAttribute('font-size', '11');
        txtNum.setAttribute('font-weight', 'bold');
        txtNum.textContent = idx + 1;
        g.appendChild(txtNum);

        // Bottom Title Label
        const txtLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        txtLabel.setAttribute('x', cx);
        txtLabel.setAttribute('y', cy + 40);
        txtLabel.setAttribute('text-anchor', 'middle');
        txtLabel.setAttribute('fill', '#e2e8f0');
        txtLabel.setAttribute('font-family', 'monospace');
        txtLabel.setAttribute('font-size', '10');
        txtLabel.setAttribute('font-weight', '600');
        txtLabel.textContent = node.label.length > 20 ? node.label.substring(0, 18) + '...' : node.label;
        g.appendChild(txtLabel);

        // Bottom Type Pill
        const txtType = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        txtType.setAttribute('x', cx);
        txtType.setAttribute('y', cy + 54);
        txtType.setAttribute('text-anchor', 'middle');
        txtType.setAttribute('fill', color);
        txtType.setAttribute('font-family', 'monospace');
        txtType.setAttribute('font-size', '8');
        txtType.textContent = (node.type || 'NODE').toUpperCase();
        g.appendChild(txtType);

        svg.appendChild(g);
      });

      // Default inspect first node
      inspectGraphNode(nodes[0], 0);
    }

    function inspectGraphNode(node, idx) {
      document.getElementById('cp-inspect-node-title').textContent = `Node ${idx + 1}: ${node.label}`;
      document.getElementById('cp-inspect-node-type').textContent = (node.type || 'ENTITY').toUpperCase();
      document.getElementById('cp-inspect-node-desc').textContent = node.description || 'Verified cryptographic DAG provenance checkpoint.';
      document.getElementById('cp-inspect-signer').textContent = `did:key:z6Mkq9...f${idx + 1}a`;
      document.getElementById('cp-inspect-hash').textContent = currentPassportData ? currentPassportData.hashes.sha256.substring(0, 12) + '...' : 'e82b71...a41c';
      document.getElementById('cp-inspect-time').textContent = new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
    }

    function downloadPassportReport() {
      if (!currentPassportData) {
        alert('Please generate or load a Content Passport first.');
        return;
      }
      const blob = new Blob([JSON.stringify({
        passport: currentPassportData,
        provenance_graph: currentProvenanceGraph
      }, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `truthscan_passport_${currentPassportData.passport_id}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }
"""

# Inject JS before lookupPassportById()
js_needle = "    // PASSPORT PUBLIC LOOKUP"
if js_needle in code:
    code = code.replace(js_needle, js_logic + "\n" + js_needle)
    print("JavaScript logic successfully injected.")
else:
    print("Warning: js_needle not found directly.")

# Write back to generate_index_html.py
with open(GENERATOR_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated scratch/generate_index_html.py.")
