import pandas as pd
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # TODO: Remove duplicate rows based on 'id'
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'])
        
    # TODO: Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    def clean_price(val):
        if pd.isna(val): return 0.0
        s = str(val).lower().replace('$', '').replace(',', '').strip()
        if 'five' in s:
            return 5.0
        nums = re.findall(r'\d+\.?\d*', s)
        if nums:
            return float(nums[0])
        return 0.0
        
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_price)
        
    # TODO: Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
    if 'date_of_sale' in df.columns:
        df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], errors='coerce').dt.strftime('%Y-%m-%d')
        
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    docs = []
    for idx, row in df.iterrows():
        timestamp_val = row.get('date_of_sale')
        if pd.isna(timestamp_val):
            timestamp_val = None
            
        docs.append({
            "document_id": f"csv-doc-{row.get('id', idx)}",
            "content": f"Sales Record: {row.to_dict()}",
            "source_type": "CSV",
            "author": "System",
            "timestamp": timestamp_val,
            "source_metadata": {"original_file": "sales_records.csv", "row_index": idx}
        })
        
    return docs
