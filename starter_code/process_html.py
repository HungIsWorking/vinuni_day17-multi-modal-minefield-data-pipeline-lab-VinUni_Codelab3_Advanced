from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # TODO: Use BeautifulSoup to find the table with id 'main-catalog'
    # TODO: Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    docs = []
    table = soup.find('table', id='main-catalog')
    if table:
        rows = table.find_all('tr')
        for idx, row in enumerate(rows[1:]): # skip header
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 3:
                product_name = cols[0].get_text(strip=True)
                description = cols[1].get_text(strip=True)
                price_str = cols[2].get_text(strip=True)
                
                # Handling 'N/A' or 'Liên hệ' in the price column
                if price_str.lower() in ['n/a', 'liên hệ', 'lien he']:
                    price = None
                else:
                    price = price_str
                    
                content = f"Product: {product_name} | Description: {description} | Price: {price}"
                docs.append({
                    "document_id": f"html-doc-{idx}",
                    "content": content,
                    "source_type": "HTML",
                    "author": "Catalog System",
                    "timestamp": None,
                    "source_metadata": {"original_file": "product_catalog.html", "product_name": product_name}
                })
                
    return docs
