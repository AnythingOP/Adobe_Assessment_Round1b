import fitz
import numpy as np
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
import onnxruntime as ort
import os

class OCRHandler:
    def __init__(self, model_path="models/donut"):
        self.enabled = os.path.exists(model_path)
        if self.enabled:
            self.processor = DonutProcessor.from_pretrained(model_path)
            self.model = VisionEncoderDecoderModel.from_pretrained(model_path)
            self.ort_session = ort.InferenceSession(f"{model_path}/model.onnx")

    def process_scanned_pdf(self, pdf_path):
        """Extract text from scanned PDFs using Donut."""
        if not self.enabled:
            return []
        
        doc = fitz.open(pdf_path)
        blocks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            pixel_values = self.processor(img, return_tensors="pt").pixel_values
            outputs = self.ort_session.run(None, {"pixel_values": pixel_values.numpy()})[0]
            decoded_text = self.processor.batch_decode(outputs)[0]
            
            lines = decoded_text.split("\n")
            section_text = []
            for line in lines:
                text = line.strip()
                if text:
                    section_text.append(text)
                    blocks.append({
                        "text": text,
                        "page": page_num + 1,
                        "font_size": 12,
                        "is_bold": True,
                        "alignment": "left",
                        "y_position": 0,
                        "section_text": " ".join(section_text)
                    })
        
        doc.close()
        return blocks