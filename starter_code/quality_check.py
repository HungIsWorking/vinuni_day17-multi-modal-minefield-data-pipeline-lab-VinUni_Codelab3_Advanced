# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    content = document_dict.get('content', '')
    
    # TODO: Reject documents with 'content' length < 20 characters
    if not content or len(str(content)) < 20:
        return False
        
    # TODO: Reject documents containing toxic/error strings (e.g., 'Null pointer exception')
    toxic_strings = ['null pointer exception', 'error: 500', 'traceback (most recent call last)']
    content_lower = str(content).lower()
    for toxic in toxic_strings:
        if toxic in content_lower:
            return False
            
    # TODO: Flag discrepancies (e.g., if tax calculation comment says 8% but code says 10%)
    
    # Return True if pass, False if fail.
    return True
