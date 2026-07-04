DANGEROUS_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "assistant:",
    "developer:",
    "execute shell",
    "rm -rf",
]


def is_safe_supplier(supplier: dict) -> bool:
    text = " ".join(str(v).lower() for v in supplier.values())

    return not any(pattern in text for pattern in DANGEROUS_PATTERNS)