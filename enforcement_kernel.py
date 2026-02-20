"""
Enforcement Kernel Module

Responsibility:
- Mandatory enforcement choke point for all responses
- Validates output before returning to caller
- Non-bypassable - no flags, no degraded modes
- Replaces unsafe responses with safe error messages
"""

from guardrails import validate_output


class EnforcementKernel:
    """Enforcement choke point for output validation."""
    
    def enforce_output(self, response: str) -> str:
        """
        Validate and enforce output safety.
        
        Args:
            response: Response text to validate
        
        Returns:
            Original response if validation passes
        
        Raises:
            ValueError: If validation fails
        """
        result = validate_output(response)
        
        if not result.passed:
            raise ValueError(f"Output validation failed: {result.violations[0]}")
        
        return response
