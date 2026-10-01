"""
Forensics Service: Error Level Analysis (ELA), EXIF metadata inspection,
OpenCV Copy-Move detection, and regional tampering heatmaps.
"""
import io
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from typing import Tuple, List, Dict, Any
from app.schemas import EvidenceItem

class ForensicsService:
    @staticmethod
    def inspect_exif(image_bytes: bytes) -> Tuple[Dict[str, Any], List[EvidenceItem]]:
        evidence = []
        metadata = {}
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                raw_exif = img.getexif()
                if not raw_exif:
                    evidence.append(EvidenceItem(
                        source="Forensics",
                        category="metadata_anomaly",
                        severity="LOW",
                        title="Stripped EXIF Metadata",
                        description="Image has stripped metadata. While common in messaging apps, it prevents camera provenance verification.",
                        limits_and_disclaimer="WhatsApp, Telegram, and social platforms recompress and strip EXIF by default."
                    ))
                else:
                    for tag_id, value in raw_exif.items():
                        metadata[str(tag_id)] = str(value)
                    # Check editing software clues
                    software_str = str(raw_exif.get(305, "")).lower()
                    if any(sw in software_str for sw in ["photoshop", "gimp", "canva", "pixlr", "procreate"]):
                        evidence.append(EvidenceItem(
                            source="Forensics",
                            category="metadata_anomaly",
                            severity="HIGH",
                            title=f"Editing Software Tag Detected: {software_str}",
                            description=f"EXIF indicates the image was manipulated or exported through graphics software ({software_str}).",
                            limits_and_disclaimer="Indicates post-processing software; does not prove malicious intent."
                        ))
        except Exception as e:
            metadata["error"] = str(e)
            
        return metadata, evidence

    @staticmethod
    def generate_ela(image_bytes: bytes, quality: int = 90, scale: int = 15) -> Tuple[bytes, List[EvidenceItem], List[List[float]]]:
        """
        Error Level Analysis: re-saves image at fixed JPEG quality and calculates difference.
        Uncompressed/edited regions show elevated error levels.
        """
        evidence = []
        suspicious_boxes = []
        try:
            orig = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            buffer = io.BytesIO()
            orig.save(buffer, 'JPEG', quality=quality)
            buffer.seek(0)
            resaved = Image.open(buffer)

            # Compute difference
            diff = ImageChops.difference(orig, resaved)
            extrema = diff.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            if max_diff == 0:
                max_diff = 1
            scale_val = 255.0 / max_diff
            diff = ImageEnhance.Brightness(diff).enhance(scale_val)

            # Convert to numpy for OpenCV contour hotspot detection
            diff_cv = cv2.cvtColor(np.array(diff), cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(diff_cv, 180, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            h, w = diff_cv.shape
            hotspot_count = 0
            for c in contours:
                area = cv2.contourArea(c)
                if 250 < area < (w * h * 0.4):  # filter noise and full backgrounds
                    x, y, cw, ch = cv2.boundingRect(c)
                    suspicious_boxes.append([round(y / h, 3), round(x / w, 3), round((y + ch) / h, 3), round((x + cw) / w, 3)])
                    hotspot_count += 1

            if hotspot_count > 0:
                evidence.append(EvidenceItem(
                    source="Forensics",
                    category="media_manipulation",
                    severity="HIGH" if hotspot_count > 2 else "MODERATE",
                    title="Compression Inconsistency Hotspots (ELA)",
                    description=f"Error Level Analysis revealed {hotspot_count} region(s) with significantly different compression artifacts, typical of spliced or pasted elements.",
                    bounding_box=suspicious_boxes[0] if suspicious_boxes else None,
                    confidence=0.82,
                    limits_and_disclaimer="ELA can produce false positives on high-contrast edges and multiple sequential resaves."
                ))

            out_buf = io.BytesIO()
            diff.save(out_buf, format="JPEG")
            return out_buf.getvalue(), evidence, suspicious_boxes
        except Exception as e:
            return b"", [EvidenceItem(
                source="Forensics",
                category="media_manipulation",
                severity="INFO",
                title="ELA Processing Note",
                description=f"Could not compute ELA: {str(e)}",
                limits_and_disclaimer="ELA requires readable RGB pixel data."
            )], []

    @staticmethod
    def detect_copy_move(image_bytes: bytes) -> List[EvidenceItem]:
        """
        OpenCV ORB feature matching to detect duplicated cloned elements within the same image.
        """
        evidence = []
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return evidence

            orb = cv2.ORB_create(nfeatures=1200)
            kp, des = orb.detectAndCompute(img, None)
            if des is not None and len(des) > 20:
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
                matches = bf.knnMatch(des, des, k=2)
                
                cloned_points = 0
                for match_pair in matches:
                    if len(match_pair) == 2:
                        m, n = match_pair
                        # Lowe's ratio test, exclude self-match
                        if m.distance < 0.65 * n.distance and m.queryIdx != m.trainIdx:
                            pt1 = kp[m.queryIdx].pt
                            pt2 = kp[m.trainIdx].pt
                            dist = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
                            if dist > 35:  # must not be adjacent pixels
                                cloned_points += 1

                if cloned_points > 12:
                    evidence.append(EvidenceItem(
                        source="Forensics",
                        category="media_manipulation",
                        severity="HIGH",
                        title="Copy-Move Cloning Detected",
                        description=f"Identified {cloned_points} matching feature clusters across separate regions, indicating cloned, stamped, or duplicated elements.",
                        confidence=0.85,
                        limits_and_disclaimer="Repetitive patterns (e.g. wallpapers, fences, tiled textures) can yield natural duplicate keypoints."
                    ))
        except Exception:
            pass
        return evidence
