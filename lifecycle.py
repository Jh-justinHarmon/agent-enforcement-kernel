"""
Lifecycle Module

Responsibility:
- Manages agent state transitions (Active → Guarded → Passive → Retired)
- Enforces approval requirements for state changes
- Raises TransitionError on policy violations (fail-closed enforcement)
"""


class TransitionError(Exception):
    """Raised when a state transition violates policy."""
    pass


def apply_transition(current_state: str, requires_approval: bool, approved: bool) -> str:
    """
    Apply a state transition with approval enforcement.
    
    Args:
        current_state: Current state of the agent
        requires_approval: Whether this transition requires approval
        approved: Whether approval was granted
    
    Returns:
        New state after successful transition
    
    Raises:
        TransitionError: If approval is required but not granted
    """
    if requires_approval and not approved:
        raise TransitionError(
            f"Transition from {current_state} requires approval but none was provided"
        )
    
    # Transition logic would go here
    # For demonstration, we just return a placeholder
    return current_state
