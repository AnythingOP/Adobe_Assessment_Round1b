from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from scipy.spatial.distance import cosine
import os

class SemanticAnalyzer:
    def __init__(self, model_path="models/minilm"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)
    
    def get_embedding(self, text):
        """Generate text embedding using MiniLM."""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def is_vegetarian_and_gluten_free(self, text):
        """Filter for vegetarian and gluten-free content."""
        non_veg_keywords = ["chicken", "beef", "pork", "fish", "meat", "bacon", "sausage"]
        gluten_keywords = ["flour", "wheat", "pasta", "macaroni", "bread", "barley", "semolina", "couscous"]
        text_lower = text.lower()
        return (not any(keyword in text_lower for keyword in non_veg_keywords) and
                not any(keyword in text_lower for keyword in gluten_keywords))

    def rank_sections(self, sections, job_description):
        """Rank sections by relevance, filtering for vegetarian/gluten-free."""
        job_embedding = self.get_embedding(job_description)
        ranked_sections = []
        
        for section in sections:
            section_text = section["section_text"]
            if not self.is_vegetarian_and_gluten_free(section_text):
                continue
            section_embedding = self.get_embedding(section_text)
            similarity = 1 - cosine(job_embedding, section_embedding)
            ranked_sections.append({
                "document": section["document"],
                "page_number": section["page"],
                "section_title": section["text"],
                "importance_rank": similarity,
                "refined_text": section_text[:500]
            })
        
        # Sort by similarity and assign integer ranks
        ranked_sections.sort(key=lambda x: x["importance_rank"], reverse=True)
        for i, section in enumerate(ranked_sections, 1):
            section["importance_rank"] = i
        
        return ranked_sections[:5]  # Top 5 sections