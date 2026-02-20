"""
Orchestrator Module

Responsibility:
- Main entry point for user queries
- Routes all return paths through enforcement choke point
- Implements _enforce_and_return() as mandatory exit point
- Calls guardrails for input sanitization
"""

from guardrails import sanitize_input
from enforcement_kernel import EnforcementKernel


class Orchestrator:
    """Main orchestrator demonstrating advisory vs structural enforcement."""
    
    def __init__(self):
        self.kernel = EnforcementKernel()
    
    def _enforce_and_return(self, response: str) -> str:
        """
        Mandatory enforcement choke point.
        All structural returns MUST route through this method.
        
        Args:
            response: Response to validate and return
        
        Returns:
            Validated response
        
        Raises:
            ValueError: If output validation fails
        """
        return self.kernel.enforce_output(response)
    
    def run_advisory(self, query: str) -> str:
        """
        Advisory enforcement pattern - guardrails return booleans.
        Caller may ignore violations and continue execution.
        
        Args:
            query: User query
        
        Returns:
            Response (may be unsafe if guardrails ignored)
        """
        # Check input guardrail (advisory mode)
        result = sanitize_input(query, strict=False)
        
        # Caller could ignore this and continue
        # This demonstrates the weakness of advisory enforcement
        if not result.passed:
            # Log violation but continue anyway
            pass
        
        # Process query (placeholder)
        response = f"Processed: {query}"
        
        # Direct return - no enforcement choke point
        return response
    
    def run_structural(self, query: str) -> str:
        """
        Structural enforcement pattern - all returns through choke point.
        Guardrails raise exceptions, execution halts on violation.
        
        Args:
            query: User query
        
        Returns:
            Validated response
        
        Raises:
            SecurityError: If input validation fails
            ValueError: If output validation fails
        """
        # Check input guardrail (strict mode - raises on violation)
        sanitize_input(query, strict=True)
        
        # Process query (placeholder)
        response = f"Processed: {query}"
        
        # ALL returns MUST route through enforcement choke point
        return self._enforce_and_return(response)
