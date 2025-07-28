def detect_headings(blocks):
    """Detect headings (H1, H2, H3) and associate section text."""
    outline = []
    
    for block in blocks:
        text = block["text"]
        font_size = block["font_size"]
        is_bold = block["is_bold"]
        alignment = block["alignment"]
        y_position = block["y_position"]
        
        # Heuristic rules for headings (tuned for recipes)
        if font_size > 14 and is_bold and (alignment == "center" or y_position < 100):
            level = "H1"
        elif 12 <= font_size <= 14 and is_bold and (alignment == "left" or y_position < 150):
            level = "H2"
        elif 10 <= font_size < 12 and is_bold:
            level = "H3"
        else:
            continue
        
        outline.append({
            "level": level,
            "text": text,
            "page": block["page"],
            "section_text": block["section_text"]
        })
    
    return outline

def extract_title(blocks, metadata, provided_title):
    """Use provided title from input.json."""
    return provided_title if provided_title else metadata.get("title", "Unknown Title")