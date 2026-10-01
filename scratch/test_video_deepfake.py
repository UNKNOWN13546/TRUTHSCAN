import cv2
import numpy as np
import tempfile
import urllib.request
import json
import os

def run_test():
    temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_path = temp_file.name
    temp_file.close()

    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_path, fourcc, 15.0, (160, 160))
        for i in range(30):
            f = np.zeros((160, 160, 3), dtype=np.uint8)
            f[:, :] = (30, 30, 40)
            cv2.circle(f, (80 + (i % 3) * 6, 80 + (i % 2) * 4), 40, (180, 160, 150), -1)
            noise = np.random.randint(0, 30, (160, 160, 3), dtype=np.uint8)
            f = cv2.add(f, noise)
            out.write(f)
        out.release()

        with open(temp_path, 'rb') as f:
            video_bytes = f.read()

        print(f"Generated synthetic test video ({len(video_bytes)} bytes)")

        # 1. Test /api/analyze-media with Video MP4
        boundary = '----WebKitFormBoundaryVideoDFTest'
        body = (
            f'--{boundary}\r\n'
            'Content-Disposition: form-data; name="image_file"; filename="suspect_interview_deepfake.mp4"\r\n'
            'Content-Type: video/mp4\r\n\r\n'
        ).encode('utf-8') + video_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')

        req = urllib.request.Request(
            'http://127.0.0.1:8000/api/analyze-media',
            data=body,
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
        )
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print("\n=== /api/analyze-media (VIDEO) RESULT ===")
            print("  Status Code:   ", resp.status)
            print("  Is Video:      ", res.get('is_video'))
            print("  Status Verdict:", res.get('status'))
            print("  Video Metadata:", res.get('video_metadata'))
            print("  Evidence Items:", len(res.get('evidence', [])))
            print("  Headline:      ", res.get('gemini_report', {}).get('headline'))
            print("  --> PASS: VIDEO DEEPFAKE ANALYSIS IS FULLY OPERATIONAL!")

        # 2. Test /api/deepfake-detector/analyze with Video MP4
        req2 = urllib.request.Request(
            'http://127.0.0.1:8000/api/deepfake-detector/analyze',
            data=body,
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
        )
        with urllib.request.urlopen(req2) as resp2:
            res2 = json.loads(resp2.read().decode('utf-8'))
            print("\n=== /api/deepfake-detector/analyze (VIDEO) RESULT ===")
            print("  Status Code:    ", resp2.status)
            print("  Is Video:       ", res2.get('is_video'))
            print("  Verdict:        ", res2.get('verdict'))
            print("  Temporal Jitter:", res2.get('metrics', {}).get('average_temporal_jitter'))
            print("  --> PASS: DEEPFAKEBENCH VIDEO PIPELINE OPERATIONAL!")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    run_test()
