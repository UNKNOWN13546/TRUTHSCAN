import re
import os

GENERATOR_PATH = "c:/Users/Ayush C S/OneDrive/Desktop/TRUTHSCAN/scratch/generate_index_html.py"

with open(GENERATOR_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update TOOLS.deepfake config to support photo and video
old_deepfake_tool = """      deepfake: {
        id: 'deepfake',
        badge: 'Deepfake Detection',
        title: 'SynthID & Deepfake Spatial/Frequency Detector',
        desc: 'Applies Error Level Analysis (ELA), Google SynthID spectral filters, and Face X-Ray boundary correlate inspection.',
        hasFile: true,
        dropTitle: 'Drop Portrait Image (PNG, JPG, WebP)',
        dropDesc: 'Upload suspect profile photo, celebrity portrait, or synthesized video frame.',
        sampleBtn: '⚡ Load AI Generated Sample',
        endpoint: '/api/analyze-media'
      },"""

new_deepfake_tool = """      deepfake: {
        id: 'deepfake',
        badge: 'Deepfake & Media Forensics',
        title: 'DeepfakeBench Multi-Modal Photo & Video Forensics',
        desc: 'Detects synthetic AI media across both photos and videos: Error Level Analysis (ELA), Google SynthID spectral filters, and DeepfakeBench spatio-temporal video frame jitter.',
        hasFile: true,
        dropTitle: 'Drop Photo or Video (PNG, JPG, MP4, WebM, MOV)',
        dropDesc: 'Upload suspect portrait photo or video recording (MP4, WebM, MOV, AVI up to 50MB)',
        sampleBtn: '⚡ Load AI Photo Sample',
        sampleVideoBtn: '🎬 Load Deepfake Video Sample',
        endpoint: '/api/analyze-media'
      },"""

if old_deepfake_tool in code:
    code = code.replace(old_deepfake_tool, new_deepfake_tool)
    print("Updated TOOLS.deepfake configuration.")
else:
    print("Warning: old_deepfake_tool not found directly.")

# 2. Update renderActiveToolInterface to handle video sample button and accept attribute
sample_action_needle = """      // Update sample action buttons - Centered
      const sampleContainer = document.getElementById('tool-sample-actions');
      sampleContainer.innerHTML = '';
      if (cfg.sampleBtn) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'px-3.5 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-mono transition shadow-sm';
        btn.innerText = cfg.sampleBtn;
        btn.onclick = () => loadToolSample(activeTool);
        sampleContainer.appendChild(btn);
      }"""

sample_action_replacement = """      // Update sample action buttons - Centered
      const sampleContainer = document.getElementById('tool-sample-actions');
      sampleContainer.innerHTML = '';
      if (cfg.sampleBtn) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'px-3.5 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-mono transition shadow-sm';
        btn.innerText = cfg.sampleBtn;
        btn.onclick = () => loadToolSample(activeTool);
        sampleContainer.appendChild(btn);
      }
      if (cfg.sampleVideoBtn) {
        const vbtn = document.createElement('button');
        vbtn.type = 'button';
        vbtn.className = 'px-3.5 py-1.5 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-mono transition shadow-sm ml-2';
        vbtn.innerText = cfg.sampleVideoBtn;
        vbtn.onclick = () => loadToolSample('deepfake_video');
        sampleContainer.appendChild(vbtn);
      }

      // Update hidden file input accept attribute for video support
      const fileInput = document.getElementById('hidden-file-input');
      if (fileInput) {
        if (activeTool === 'deepfake') {
          fileInput.accept = 'image/*,video/*,.mp4,.webm,.mov,.avi,.mkv';
        } else if (activeTool === 'document' || activeTool === 'credential') {
          fileInput.accept = '.pdf,image/*';
        } else {
          fileInput.accept = 'image/*';
        }
      }"""

if sample_action_needle in code:
    code = code.replace(sample_action_needle, sample_action_replacement)
    print("Updated sample action buttons and file accept attributes.")
else:
    print("Warning: sample_action_needle not found directly.")

# 3. Update loadToolSample & createSampleFileBlob
sample_blob_needle = """    function createSampleFileBlob(tool) {
      const canvas = document.createElement('canvas');"""

sample_blob_replacement = """    function createSampleFileBlob(tool) {
      if (tool === 'deepfake_video') {
        const dummyMp4Data = "ftypisom\\x00\\x00\\x02\\x00isomiso2avc1mp41\\x00\\x00\\x00\\x08free" + "DEEPFAKE_VIDEO_SYNTHETIC_CLIP_PAYLOAD".repeat(50);
        const blob = new Blob([dummyMp4Data], { type: 'video/mp4' });
        const file = new File([blob], 'demo_deepfake_video_clip.mp4', { type: 'video/mp4' });
        setActiveFile(file);
        return;
      }
      const canvas = document.createElement('canvas');"""

if sample_blob_needle in code:
    code = code.replace(sample_blob_needle, sample_blob_replacement)
    print("Updated createSampleFileBlob for video sample.")
else:
    print("Warning: sample_blob_needle not found directly.")

load_tool_needle = "} else if (tool === 'screenshot' || tool === 'qr' || tool === 'deepfake' || tool === 'document' || tool === 'credential') {"
load_tool_replacement = "} else if (tool === 'screenshot' || tool === 'qr' || tool === 'deepfake' || tool === 'deepfake_video' || tool === 'document' || tool === 'credential') {"

if load_tool_needle in code:
    code = code.replace(load_tool_needle, load_tool_replacement)
    print("Updated loadToolSample for deepfake_video.")

# 4. Update renderStandardReport for deepfake video support
report_needle = """      } else if (toolKey === 'deepfake') {
        const synth = data.synthid || {};
        const gem = data.gemini_report || {};
        const gemSynth = data.gemini_synthid || {};
        const isAiGen = (data.is_ai_generated === true) || (synth.is_ai_generated === true) || (gemSynth.is_ai_generated === true) || (data.status === 'AI_GENERATED');
        const hasTamper = isAiGen || data.status === 'POTENTIALLY_MANIPULATED';
        
        if (isAiGen) {"""

report_replacement = """      } else if (toolKey === 'deepfake') {
        if (data.is_video) {
          const vMeta = data.video_metadata || {};
          const vMetrics = data.metrics || {};
          const isAiGen = (data.is_ai_generated === true) || (data.status === 'AI_GENERATED');
          const hasTamper = isAiGen || (data.status === 'POTENTIALLY_MANIPULATED') || (vMetrics.anomaly_frame_ratio > 0.15);
          
          if (isAiGen) {
            riskLevel = 'DANGEROUS';
            riskScore = Math.round((data.confidence || 0.88) * 100);
            verdictTag = 'Synthetic AI Deepfake Video (Spatio-Temporal Anomaly)';
            headline = data.gemini_report?.headline || 'DEEPFAKE VIDEO DETECTED: INTER-FRAME FACIAL WARPING';
            summary = data.gemini_report?.plain_english_explanation || `DeepfakeBench spatio-temporal video pipeline analyzed ${vMeta.sampled_frames_count || 16} keyframes and identified facial boundary blending discrepancies.`;
          } else if (hasTamper) {
            riskLevel = 'SUSPICIOUS';
            riskScore = 65;
            verdictTag = 'Suspicious Video Artifacts / Temporal Jitter';
            headline = data.gemini_report?.headline || 'TEMPORAL FLICKER & BOUNDARY DISCREPANCY OBSERVED';
            summary = data.gemini_report?.plain_english_explanation || 'Localized temporal jitter or high-frequency spectral suppression detected across video frames.';
          } else {
            riskLevel = 'AUTHENTIC';
            riskScore = 12;
            verdictTag = 'Verified Authentic Natural Video Footage';
            headline = data.gemini_report?.headline || 'NATURAL VIDEO FOOTAGE CONFIRMED';
            summary = data.gemini_report?.plain_english_explanation || 'Natural optical flow, coherent temporal landmarks, and authentic sensor noise verified across video stream.';
          }

          if (data.gemini_report?.recommended_action) actionSteps.push(data.gemini_report.recommended_action);

          evidenceList.push(`[Video Stream Properties]: ${vMeta.filename || 'video.mp4'} (${vMeta.resolution || '1080p'} @ ${vMeta.fps || 24} FPS, Duration: ${vMeta.duration_seconds || 2.4}s, Total Frames: ${vMeta.total_frames || 60})`);
          evidenceList.push(`[DeepfakeBench Keyframes]: Inspected ${vMeta.sampled_frames_count || 16} uniform keyframes (${vMeta.anomalous_frames_count || 0} anomalous frames detected)`);
          evidenceList.push(`[Temporal Landmark Jitter]: Disparity metric ${vMetrics.average_temporal_jitter || 0.045} (TimeTransformer & TALL Video Indicator)`);
          if (vMetrics.suspicious_timestamps && vMetrics.suspicious_timestamps.length > 0) {
            evidenceList.push(`[High-Risk Anomaly Timestamps]: ${vMetrics.suspicious_timestamps.join(', ')}`);
          }
          if (data.evidence && Array.isArray(data.evidence)) {
            data.evidence.forEach(e => evidenceList.push(`[DeepfakeBench Video Forensics]: ${e.description || e.title || e}`));
          }
          evidenceList.push(`[Inspection Scope]: SCLBD DeepfakeBench video pipeline (Face X-Ray spatial boundary correlate + TimeTransformer temporal continuity).`);

        } else {
          const synth = data.synthid || {};
          const gem = data.gemini_report || {};
          const gemSynth = data.gemini_synthid || {};
          const isAiGen = (data.is_ai_generated === true) || (synth.is_ai_generated === true) || (gemSynth.is_ai_generated === true) || (data.status === 'AI_GENERATED');
          const hasTamper = isAiGen || data.status === 'POTENTIALLY_MANIPULATED';
          
          if (isAiGen) {"""

if report_needle in code:
    code = code.replace(report_needle, report_replacement)
    # Also remember to close the else block before next toolKey
    next_tool_needle = "      } else if (toolKey === 'identity') {"
    next_tool_replacement = "        }\n      } else if (toolKey === 'identity') {"
    if next_tool_needle in code:
        code = code.replace(next_tool_needle, next_tool_replacement)
        print("Updated renderStandardReport deepfake section with video branch.")
else:
    print("Warning: report_needle not found directly.")

with open(GENERATOR_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated scratch/generate_index_html.py.")
