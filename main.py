from pathlib import Path
import json
import fitz  # PyMuPDF
from src.pdf_processor import extract_text_blocks, get_metadata
from src.heading_detector import detect_headings, extract_title
from src.semantic_analyzer import SemanticAnalyzer
from src.output_formatter import save_output

def is_text_layer_pdf(pdf_path):
    """Check if PDF has a text layer."""
    doc = fitz.open(pdf_path)
    for page_num in range(min(1, len(doc))):
        text = doc[page_num].get_text().strip()
        if text:
            doc.close()
            return True
    doc.close()
    return False

def main():
    # Use the directory where main.py is located as the base
    base_dir = Path(__file__).parent

    # Relative input/output paths
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Read input.json
    input_json_path = input_dir / "input.json"
    if not input_json_path.exists():
        print(f"❌ Error: '{input_json_path}' does not exist.")
        return

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    documents = input_data.get("documents", [])
    persona = input_data.get("persona", {})
    job_to_be_done = input_data.get("job_to_be_done", {})

    semantic_analyzer = SemanticAnalyzer()
    all_sections = []

    # Process each PDF
    for doc in documents:
        pdf_path = input_dir / doc["filename"]
        provided_title = doc.get("title", "")

        if not pdf_path.exists():
            print(f"⚠️ Warning: File '{pdf_path}' not found. Skipping.")
            continue

        if not is_text_layer_pdf(pdf_path):
            print(f"⚠️ Warning: {doc['filename']} is not a text-layer PDF. Skipping (no OCR available).")
            continue

        blocks = extract_text_blocks(pdf_path)
        metadata = get_metadata(pdf_path)
        outline = detect_headings(blocks)

        for section in outline:
            section["document"] = doc["filename"]

        all_sections.extend(outline)

    # Rank sections based on job-to-be-done
    ranked_sections = semantic_analyzer.rank_sections(all_sections, job_to_be_done.get("task", ""))

    # Save output
    output_path = output_dir / "output.json"
    save_output(documents, persona, job_to_be_done, ranked_sections, output_path)
    print(f"✅ Output saved to: {output_path}")

if __name__ == "__main__":
    main()
