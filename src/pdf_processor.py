import fitz
import pdfplumber
from pathlib import Path

def extract_text_blocks(pdf_path):
    """Extract text blocks with layout info from a PDF."""
    doc = fitz.open(pdf_path)
    blocks = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        fitz_blocks = page.get_text("dict")["blocks"]
        with pdfplumber.open(pdf_path) as pdf:
            plumber_page = pdf.pages[page_num]
            current_section = []
            for block in fitz_blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        current_section.append(text)
                        blocks.append({
                            "text": text,
                            "page": page_num + 1,
                            "font_size": span["size"],
                            "is_bold": bool(span["flags"] & 16),
                            "font": span["font"],
                            "y_position": span["bbox"][1],
                            "alignment": get_text_alignment(plumber_page, span["bbox"]),
                            "section_text": " ".join(current_section)
                        })
    
    doc.close()
    return blocks

def get_text_alignment(plumber_page, bbox):
    """Estimate text alignment using pdfplumber."""
    chars = plumber_page.chars
    for char in chars:
        if abs(char["x0"] - bbox[0]) < 1 and abs(char["y0"] - bbox[1]) < 1:
            return "center" if char["x0"] > plumber_page.width * 0.3 else "left"
    return "left"

def get_metadata(pdf_path):
    """Extract metadata for title detection."""
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    doc.close()
    return metadata