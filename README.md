# Enforcement Boundary Architecture

## Why I Built This

This repo documents an adversarial audit of a production AI agent system that revealed a fail-open control boundary.

Guardrails existed, but they returned booleans that callers could ignore. That meant unsafe operations could still execute if a caller skipped a check, logged a warning, or implemented fallback logic.

A boundary that can be bypassed by ignoring a boolean is not a boundary.

The system was refactored to enforce boundaries structurally instead of by convention.

---

## The Problem: Advisory Enforcement

The original architecture used advisory guardrails:

- Input sanitization returned a result object that callers were expected to check
- Lifecycle transitions returned `False` on policy violations
- Output validation could log failures without blocking responses

This design delegates enforcement to the caller.  
If the caller ignores the result, enforcement disappears.

This is a fail-open design.

---

## The Architectural Correction

The system was redesigned so unsafe operations are **structurally impossible** to execute, not just discouraged.

### Mandatory Enforcement Choke Point

All return paths route through a single enforcement method that validates output before any response reaches the caller. Structural tests detect any direct return that bypasses this choke point.

### Exception-Based Blocking

Policy violations raise exceptions instead of returning booleans:

- Lifecycle violations raise `TransitionError`
- Critical input violations raise `SecurityError`
- Exceptions are not caught or suppressed
- Execution halts immediately on violation

Unsafe operations cannot continue past the control boundary.

---

## Control Boundary Structure

```
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
```

Unsafe output cannot bypass this boundary.

---

## Regression Defense

Structural tests enforce the boundary:

- Detect direct return bypasses
- Fail if exceptions are replaced with boolean returns
- Break CI if enforcement is removed

Tests verify structural enforcement, not full behavioral coverage.

---

## Enforcement Boundaries

**Input Boundary**
- Enforces sanitization against injection and unsafe patterns
- Exception-based blocking in critical paths
- Fail-closed status: Partial

**Output Boundary**
- Response validation before returning to caller
- Mandatory choke point
- Fail-closed status: Yes

**Lifecycle Boundary**
- Approved state transitions only
- Exception raised on policy violation
- Fail-closed status: Yes

---

## Demo

Run the reference implementation:

```bash
python demo.py
```

Before: Guardrails return booleans; caller may ignore violations  
After: Violations raise exceptions; execution halts at the control boundary

The difference is architectural: advisory checks rely on caller discipline; structural enforcement makes unsafe operations impossible to execute.

---

## What This Is

This is a reference implementation demonstrating enforcement boundary design:

- Fail-closed control boundaries
- Mandatory enforcement choke points
- Exception-based blocking
- Regression tests that protect the boundary

This is not a full agent system.  
This is the enforcement layer.
