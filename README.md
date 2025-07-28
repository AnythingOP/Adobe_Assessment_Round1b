Round 1B: Persona-Driven Document Intelligence
This solution extracts and prioritizes vegetarian, gluten-free dinner menu sections from 9 PDFs for a Food Contractor, outputting results in JSON format.
Setup

Python: 3.10
Dependencies: Listed in requirements.txt
Models: MiniLM-L6-v2 (models/minilm/)
Docker: AMD64-compatible, offline execution

Installation

Install dependencies:pip install -r requirements.txt


Download MiniLM-L6-v2:mkdir -p models/minilm
python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2').save_pretrained('models/minilm'); AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2').save_pretrained('models/minilm')"



Input

Place PDFs and input.json in input/.
Example input.json:{
  "documents": [{"filename": "Dinner Ideas - Sides_2.pdf", "title": "Dinner Ideas - Sides_2"}],
  "persona": {"role": "Food Contractor"},
  "job_to_be_done": {"task": "Prepare a vegetarian buffet-style dinner menu..."}
}



Running Locally

Place inputs in input/.
Run: python main.py.
Check output/output.json.

Docker Execution

Build:docker build --platform linux/amd64 -t mysolutionname:test .


Run:docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:test



Assumptions

Handles text-layer PDFs with PyMuPDF/pdfplumber.
Skips non-text-layer PDFs (no OCR included).
Supports multilingual text via Unicode.
Total model size ~150MB, processing time <60 seconds.

Notes

Modular code for future reuse.
Keep repository private until the deadline.
