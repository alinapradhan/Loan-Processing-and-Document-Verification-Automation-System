from typing import Optional

import cv2
import pytesseract
from paddleocr import PaddleOCR

from ocr.preprocess import preprocess_image


class OCREngine:
    def __init__(self, engine: str = "tesseract", tesseract_cmd: str = ""):
        self.engine = engine
        self.paddle_instance: Optional[PaddleOCR] = None

        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, file_bytes: bytes) -> str:
        image = preprocess_image(file_bytes)
        if image is None:
            return ""

        if self.engine == "paddle":
            if not self.paddle_instance:
                self.paddle_instance = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
            result = self.paddle_instance.ocr(image, cls=True)
            lines = []
            for block in result or []:
                for entry in block:
                    lines.append(entry[1][0])
            return "\n".join(lines)

        return pytesseract.image_to_string(image)

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        # Placeholder implementation: PDF OCR usually requires pdf2image conversion.
        # In production, convert each page to image, then call extract_text per page.
        return "PDF processing placeholder. Convert PDF pages to images for OCR."
