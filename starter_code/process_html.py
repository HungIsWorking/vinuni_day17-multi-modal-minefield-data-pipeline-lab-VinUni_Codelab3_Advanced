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
    # HTML table columns: [0] Mã SP | [1] Tên sản phẩm | [2] Danh mục | [3] Giá niêm yết | [4] Tồn kho | [5] Đánh giá
    table = soup.find('table', id='main-catalog')
    if table:
        rows = table.find_all('tr')
        for idx, row in enumerate(rows[1:]): # skip header
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 4:
                product_id   = cols[0].get_text(strip=True)   # Mã SP   e.g. "SP-001"
                product_name = cols[1].get_text(strip=True)   # Tên sản phẩm
                category     = cols[2].get_text(strip=True)   # Danh mục
                price_str    = cols[3].get_text(strip=True)   # Giá niêm yết ← was cols[2] (BUG)
                
                # Handling 'N/A' or 'Liên hệ' in the price column
                if price_str.lower() in ['n/a', 'liên hệ', 'lien he']:
                    price = None
                else:
                    price = price_str
                    
                content = f"Product: {product_id} | Name: {product_name} | Category: {category} | Price: {price}"
                docs.append({
                    "document_id": f"html-doc-{idx}",
                    "content": content,
                    "source_type": "HTML",
                    "author": "Catalog System",
                    "timestamp": None,
                    "source_metadata": {"original_file": "product_catalog.html", "product_name": product_id}
                })
                
    return docs
