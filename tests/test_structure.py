"""
Structural Regression Test

Responsibility:
- Enforces choke point architecture using AST analysis
- Verifies run_structural has NO direct return bypasses
- Ensures all returns route through _enforce_and_return
- Fails if enforcement choke point is removed or bypassed
"""

import ast
from pathlib import Path


def test_run_structural_enforces_choke_point():
    """
    Structural test: Verify run_structural only returns via _enforce_and_return.
    
    This test uses AST parsing to ensure the enforcement choke point is
    architecturally guaranteed, not convention-based.
    """
    # Load orchestrator.py
    orchestrator_path = Path(__file__).parent.parent / "orchestrator.py"
    with open(orchestrator_path) as f:
        source = f.read()
    
    # Parse AST
    tree = ast.parse(source)
    
    # Find Orchestrator class
    orchestrator_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Orchestrator":
            orchestrator_class = node
            break
    
    assert orchestrator_class is not None, "Orchestrator class not found"
    
    # Find run_structural method
    run_structural_method = None
    for item in orchestrator_class.body:
        if isinstance(item, ast.FunctionDef) and item.name == "run_structural":
            run_structural_method = item
            break
    
    assert run_structural_method is not None, "run_structural method not found"
    
    # Collect all Return nodes in run_structural
    returns = []
    for node in ast.walk(run_structural_method):
        if isinstance(node, ast.Return):
            returns.append(node)
    
    assert len(returns) > 0, "run_structural has no return statements"
    
    # Validate each return statement
    for return_node in returns:
        # Return must have a value (not bare return)
        assert return_node.value is not None, \
            "Found bare 'return' statement in run_structural"
        
        # Return value must be a function call
        assert isinstance(return_node.value, ast.Call), \
            f"Return statement must call a function, found: {ast.dump(return_node.value)}"
        
        # The call must be to an attribute (self._enforce_and_return)
        assert isinstance(return_node.value.func, ast.Attribute), \
            f"Return must call a method, found: {ast.dump(return_node.value.func)}"
        
        # The attribute must be _enforce_and_return
        assert return_node.value.func.attr == "_enforce_and_return", \
            f"Return must call _enforce_and_return, found: {return_node.value.func.attr}"
        
        # The object must be self
        assert isinstance(return_node.value.func.value, ast.Name), \
            "Method must be called on an object"
        
        assert return_node.value.func.value.id == "self", \
            f"Method must be called on 'self', found: {return_node.value.func.value.id}"
    
    # If we get here, all returns route through _enforce_and_return
    # This is the structural guarantee we're testing for


def test_run_advisory_has_direct_return():
    """
    Verify run_advisory has direct returns (demonstrates the contrast).
    
    This test confirms that advisory mode does NOT use the choke point,
    showing the architectural difference.
    """
    # Load orchestrator.py
    orchestrator_path = Path(__file__).parent.parent / "orchestrator.py"
    with open(orchestrator_path) as f:
        source = f.read()
    
    # Parse AST
    tree = ast.parse(source)
    
    # Find Orchestrator class
    orchestrator_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Orchestrator":
            orchestrator_class = node
            break
    
    assert orchestrator_class is not None, "Orchestrator class not found"
    
    # Find run_advisory method
    run_advisory_method = None
    for item in orchestrator_class.body:
        if isinstance(item, ast.FunctionDef) and item.name == "run_advisory":
            run_advisory_method = item
            break
    
    assert run_advisory_method is not None, "run_advisory method not found"
    
    # Collect all Return nodes in run_advisory
    returns = []
    for node in ast.walk(run_advisory_method):
        if isinstance(node, ast.Return):
            returns.append(node)
    
    assert len(returns) > 0, "run_advisory has no return statements"
    
    # Check if any return is a direct return (not through _enforce_and_return)
    has_direct_return = False
    for return_node in returns:
        if return_node.value is None:
            continue
        
        # Check if this is NOT a call to _enforce_and_return
        if isinstance(return_node.value, ast.Call):
            if isinstance(return_node.value.func, ast.Attribute):
                if return_node.value.func.attr == "_enforce_and_return":
                    continue  # This is a choke point return
        
        # This is a direct return
        has_direct_return = True
        break
    
    assert has_direct_return, \
        "run_advisory should have direct returns (not use enforcement choke point)"
