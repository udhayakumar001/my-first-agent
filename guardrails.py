import re

# ==========================================
# PATTERNS & CONFIG
# ==========================================

# PII Patterns
PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
}

# Prompt Injection Patterns
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above)\s+instructions",
    r"system\s*:\s*override",
    r"disregard\s+(the\s+)?system\s+prompt",
    r"you\s+are\s+now\s+a\s+unrestricted",
    r"jailbreak",
    r"DAN\s+mode",
    r"forget\s+(all\s+)?your\s+rules",
]

# Max length guardrail
MAX_INPUT_LENGTH = 4000


# ==========================================
# PII REDACTION
# ==========================================

def redact_pii(text: str) -> str:
    """Detects and redacts sensitive PII from text."""
    sanitized = text
    for pii_type, pattern in PII_PATTERNS.items():
        sanitized = re.sub(pattern, f"[{pii_type}_REDACTED]", sanitized)
    return sanitized


# ==========================================
# INPUT GUARDRAILS
# ==========================================

def validate_input(user_input: str):
    """
    Validates user input.
    Returns: (is_safe: bool, sanitized_input: str, block_reason: str)
    """
    if not user_input or not user_input.strip():
        return False, "", "Empty input provided."

    if len(user_input) > MAX_INPUT_LENGTH:
        return False, "", f"Input exceeds maximum allowed length of {MAX_INPUT_LENGTH} characters."

    # Check for Prompt Injection Attacks
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False, "", "Input blocked: Potential prompt injection detected."

    # Redact PII
    sanitized_input = redact_pii(user_input)

    return True, sanitized_input, ""


# ==========================================
# OUTPUT GUARDRAILS
# ==========================================

def validate_output(output_text: str):
    """
    Validates AI generated output.
    Returns: (is_safe: bool, sanitized_output: str, block_reason: str)
    """
    if not output_text:
        return True, "", ""

    # Ensure output doesn't contain leaked PII
    sanitized_output = redact_pii(output_text)

    return True, sanitized_output, ""
