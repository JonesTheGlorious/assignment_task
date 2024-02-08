import pytest
from src.relationship import identify_relationships

def test_identify_relationships():
    # Test case with sample functions
    functions = [('add', ['x', 'y'], ['x + y']), ('subtract', ['x', 'y'], ['x - y'])]
    relationships = identify_relationships(functions)
    expected_relationships = {
        'add': {'parameters': {'x', 'y'}, 'returns': {'x + y'}, 'related_functions': {'subtract'}, 'param_loose_ends': {'x', 'y'}, 'returns_loose_ends': {'y'}}, 'subtract': {'parameters': {'x', 'y'}, 'returns': {'x - y'}, 'related_functions': {'add'}, 'param_loose_ends': {'x', 'y'}, 'returns_loose_ends': {'y'}}
        }
    assert relationships == expected_relationships
    assert len(relationships) == 2