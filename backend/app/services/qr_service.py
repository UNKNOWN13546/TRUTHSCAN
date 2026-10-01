"""
QR Decoder Service:
Uses OpenCV and pyzbar to safely extract payloads from QR codes
without automatically opening or navigating to the target URL.
"""
import io
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional

class QRService:
    @staticmethod
    def decode_qr(image_bytes: bytes) -> Dict[str, Any]:
        """
        Decodes QR payload safely via OpenCV QRCodeDetector.
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return {"found": False, "error": "Unable to decode image format."}

            detector = cv2.QRCodeDetector()
            data, bbox, straight_qrcode = detector.detectAndDecode(img)

            if bbox is not None and data:
                return {
                    "found": True,
                    "payload": data,
                    "is_url": data.lower().startswith("http://") or data.lower().startswith("https://") or data.lower().startswith("upi://"),
                    "safety_notice": "QR extracted securely. Target URL will NOT be opened automatically."
                }
            else:
                return {
                    "found": False,
                    "payload": "",
                    "is_url": False,
                    "notice": "No valid QR code pattern detected in the uploaded frame."
                }
        except Exception as e:
            return {
                "found": False,
                "error": str(e)
            }
