import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # TODO: Use the 'ast' module to find docstrings for functions
    docs_content = []
    try:
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    node_name = getattr(node, 'name', 'Module')
                    docs_content.append(f"Entity: {node_name}\\nDocstring: {docstring}")
    except SyntaxError:
        pass
        
    # TODO: (Optional/Advanced) Use regex to find business rules in comments like "# Business Logic Rule 001"
    rules = re.findall(r'#\s*(Business Logic Rule.*?)$', source_code, re.MULTILINE)
    for rule in rules:
        docs_content.append(f"Business Rule: {rule}")
        
    # TODO: Return a dictionary for the UnifiedDocument schema.
    return {
        "document_id": "legacy-code-001",
        "content": "\\n\\n".join(docs_content),
        "source_type": "Code",
        "author": "Legacy Developer",
        "timestamp": None,
        "source_metadata": {
            "original_file": "legacy_pipeline.py",
            "entities_extracted": len(docs_content)
        }
    }
