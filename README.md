# Enforcement Boundary Architecture

This repository documents an adversarial audit of a production AI agent system that revealed advisory guardrails at the control boundary. Input enforcement returned booleans that callers could ignore, allowing unsafe operations to proceed. The architectural correction introduced structural enforcement through mandatory choke points, exception-based blocking, and regression tests that fail if enforcement is removed.

## The Problem: Advisory Enforcement

The original architecture implemented guardrails that returned boolean results rather than blocking execution.

- Input sanitization returned a result object that callers were expected to check.
- Lifecycle transitions returned `False` on policy violations.
- Output validation could log failures without preventing responses from being returned.

This pattern delegates enforcement to the caller. If the caller ignores the return value, logs the failure, or implements fallback logic, the guardrail becomes advisory.

A control boundary that can be crossed by ignoring a boolean is not a boundary. Enforcement must be structural—unsafe operations must be impossible to execute regardless of caller discipline.

## The Architectural Correction

The system was refactored to enforce control boundaries structurally rather than by convention.

### Mandatory Enforcement Choke Point

All return paths route through a single enforcement method that validates output before any response reaches the caller. Structural tests detect any direct return that bypasses this choke point.

### Exception-Based Blocking

Policy violations raise exceptions instead of returning booleans.

- Lifecycle transitions raise `TransitionError`.
- Critical input paths raise `SecurityError`.
- Exceptions are not caught or suppressed.

Execution halts immediately on violation.

### Control Boundary Structure

User Query
    ↓
Orchestrator
    ↓
Business Logic
    ↓
Enforcement Choke Point
    ↓
Output Validation
    ↓
Return to User

Unsafe output cannot bypass this boundary.

### Regression Defense

Structural tests:

- Detect direct return bypasses.
- Fail if exceptions are replaced with boolean returns.
- Break CI if enforcement is removed.

## Enforcement Boundaries

### Input Boundary

**Enforces:** Sanitization against injection and unsafe patterns.  
**Mechanism:** Exception-based blocking in critical paths; conditional enforcement in some orchestrator paths.  
**Fail-closed status:** Partial.

### Output Boundary

**Enforces:** Response validation before returning to caller.  
**Mechanism:** Mandatory choke point; validation cannot be skipped.  
**Fail-closed status:** Yes.

### Lifecycle Boundary

**Enforces:** Approved state transitions.  
**Mechanism:** Exception raised on policy violation; no degraded modes.  
**Fail-closed status:** Yes.

## Demo

Run the reference implementation:

python demo.py

**Before:** Guardrails return booleans; caller may ignore violations.  
**After:** Violations raise exceptions; execution halts at the control boundary.

The difference is architectural: advisory checks rely on caller discipline; structural enforcement makes unsafe operations impossible to execute.

## Verification & Regression Defense

Tests verify structural enforcement, not full behavioral coverage.

They confirm:

- All returns route through the enforcement choke point.
- Policy violations raise exceptions.
- Removing enforcement breaks CI.

They do not guarantee complete runtime path coverage. Behavioral monitoring remains necessary.

## What This Is Not

This is not a production security framework.  
This is not a complete agent system.  
This is a reference implementation demonstrating enforcement boundary design.
