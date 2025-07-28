import json
from pathlib import Path
from datetime import datetime

def save_output(documents, persona, job_to_be_done, ranked_sections, output_path):
    """Save output in required JSON format."""
    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona["role"],
            "job_to_be_done": job_to_be_done["task"],
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [
            {
                "document": section["document"],
                "section_title": section["section_title"],
                "importance_rank": section["importance_rank"],
                "page_number": section["page_number"]
            } for section in ranked_sections
        ],
        "subsection_analysis": [
            {
                "document": section["document"],
                "refined_text": section["refined_text"],
                "page_number": section["page_number"]
            } for section in ranked_sections
        ]
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)