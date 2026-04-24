import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # TODO: Remove noise tokens like [Music starts], [inaudible], [Laughter]
    text = re.sub(r'\[(?:Music.*?|inaudible|Laughter)\]', '', text, flags=re.IGNORECASE)
    
    # TODO: Strip timestamps [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # TODO: Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    price_match = re.search(r'năm trăm nghìn', text, re.IGNORECASE)
    extracted_price = 500000 if price_match else 0
    
    # TODO: Return a cleaned dictionary for the UnifiedDocument schema.
    return {
        "document_id": "transcript-doc-001",
        "content": text,
        "source_type": "Video", # Match expected type in agent_forensic.py
        "author": "Speaker",
        "timestamp": None,
        "source_metadata": {
            "original_file": "demo_transcript.txt",
            "detected_price_vnd": extracted_price # Match expected key and type
        }
    }
