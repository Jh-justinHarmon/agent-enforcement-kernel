"""
Guardrails Module

Responsibility:
- Input sanitization against prompt injection, jailbreak attempts, and code injection
- Output validation for sensitive data exposure and safety violations
- Returns structured result objects with violation details
"""

from dataclasses import dataclass
from typing import List


class SecurityError(Exception):
    """Raised when strict enforcement detects a security violation."""
    pass


@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    passed: bool
    violations: List[str]
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"


def sanitize_input(query: str, strict: bool = False) -> GuardrailResult:
    """
    Sanitize input against injection patterns.
    
    Args:
        query: Input text to sanitize
        strict: If True, raises SecurityError on violation. If False, returns result.
    
    Returns:
        GuardrailResult when strict=False
    
    Raises:
        SecurityError when strict=True and violation detected
    """
    violations = []
    risk_level = "LOW"
    
    # Check for prompt injection patterns
    injection_patterns = [
        "ignore previous instructions",
        "disregard all",
        "system:",
        "assistant:",
        "<script>",
        "eval(",
        "exec(",
    ]
    
    query_lower = query.lower()
    for pattern in injection_patterns:
        if pattern in query_lower:
            violations.append(f"Injection pattern detected: {pattern}")
            risk_level = "HIGH"
    
    # Check for excessive length (potential DoS)
    if len(query) > 10000:
        violations.append("Query exceeds maximum length")
        risk_level = "MEDIUM"
    
    passed = len(violations) == 0
    result = GuardrailResult(passed=passed, violations=violations, risk_level=risk_level)
    
    if strict and not passed:
        raise SecurityError(f"Input blocked: {violations[0]}")
    
    return result


def validate_output(response: str) -> GuardrailResult:
    """
    Validate output for sensitive data exposure.
    
    Args:
        response: Output text to validate
    
    Returns:
        GuardrailResult with validation status
    """
    violations = []
    risk_level = "LOW"
    
    # Check for PII patterns
    pii_patterns = [
        ("SSN", r"\d{3}-\d{2}-\d{4}"),
        ("credit card", r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}"),
        ("API key", r"sk-[a-zA-Z0-9]{32,}"),
    ]
    
    import re
    for name, pattern in pii_patterns:
        if re.search(pattern, response):
            violations.append(f"Potential {name} exposure detected")
            risk_level = "CRITICAL"
    
    # Check for excessive output (potential resource exhaustion)
    if len(response) > 50000:
        violations.append("Response exceeds safe length")
        risk_level = "MEDIUM"
    
    passed = len(violations) == 0
    return GuardrailResult(passed=passed, violations=violations, risk_level=risk_level)
