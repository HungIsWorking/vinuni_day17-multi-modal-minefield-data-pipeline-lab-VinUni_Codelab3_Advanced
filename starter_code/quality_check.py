# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

import json
import re


TOXIC_PATTERNS = [
    "null pointer exception",
    "traceback (most recent call last)",
    "segmentation fault",
    "fatal error",
    "stack overflow",
    "index out of range",
    "keyerror",
    "valueerror",
    "typeerror",
]


def _safe_to_text(document_dict):
    """Convert any input object to searchable text without raising errors."""
    if isinstance(document_dict, dict):
        try:
            return json.dumps(document_dict, ensure_ascii=False, default=str)
        except Exception:
            return str(document_dict)
    return str(document_dict)


def _has_tax_rate_discrepancy(search_text):
    """Detect obvious mismatches between stated tax/VAT rates and code rates."""
    lines = search_text.splitlines()
    tax_lines = [line for line in lines if re.search(r"\b(tax|vat)\b", line, flags=re.IGNORECASE)]

    if not tax_lines:
        return False

    tax_text = "\n".join(tax_lines)

    percent_values = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", tax_text)]

    assigned_rates = [
        float(x)
        for x in re.findall(
            r"(?:tax_rate|vat_rate|tax|vat)\s*=\s*(\d+(?:\.\d+)?)",
            tax_text,
            flags=re.IGNORECASE,
        )
    ]
    code_percent_from_decimal = [value * 100 if value <= 1 else value for value in assigned_rates]

    observed_rates = percent_values + code_percent_from_decimal
    if len(observed_rates) < 2:
        return False

    normalized = {round(rate, 2) for rate in observed_rates}
    return len(normalized) > 1

def run_quality_gate(document_dict):
    # Gate 1: Reject missing/very short content.
    content = str(document_dict.get("content", "")).strip() if isinstance(document_dict, dict) else ""
    if len(content) < 20:
        return False

    search_text = _safe_to_text(document_dict).lower()

    # Gate 2: Reject toxic/error artifacts.
    if any(pattern in search_text for pattern in TOXIC_PATTERNS):
        return False

    # Gate 3: Flag semantic discrepancy in tax/VAT logic.
    if _has_tax_rate_discrepancy(search_text):
        return False

    return True
