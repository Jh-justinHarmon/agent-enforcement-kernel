"""
Lifecycle Test Module

Responsibility:
- Verifies lifecycle transitions raise exceptions on policy violations
- Tests that TransitionError is raised, not return False
- Confirms no try/except blocks suppress enforcement exceptions
- Validates fail-closed enforcement behavior
"""

import pytest
from lifecycle import apply_transition, TransitionError


def test_lifecycle_blocks_unapproved_transition():
    """Test that apply_transition raises TransitionError when approval is missing."""
    with pytest.raises(TransitionError) as exc_info:
        apply_transition(
            current_state="ACTIVE",
            requires_approval=True,
            approved=False
        )
    
    assert "requires approval" in str(exc_info.value)
    assert "ACTIVE" in str(exc_info.value)


def test_lifecycle_allows_approved_transition():
    """Test that apply_transition succeeds when approval is granted."""
    # Should not raise
    result = apply_transition(
        current_state="ACTIVE",
        requires_approval=True,
        approved=True
    )
    
    assert result == "ACTIVE"  # Placeholder returns current state


def test_lifecycle_allows_transition_without_approval_requirement():
    """Test that transitions not requiring approval succeed without approval."""
    # Should not raise
    result = apply_transition(
        current_state="ACTIVE",
        requires_approval=False,
        approved=False
    )
    
    assert result == "ACTIVE"
