import pytest
from src.relationship import identify_relationships

def test_identify_relationships():
    # Test case with sample functions
    functions = [('add', ['x', 'y'], ['x + y']), ('subtract', ['x', 'y'], ['x - y'])]
    relationships = identify_relationships(functions)
    expected_relationships = {
        'add': {'parameters': {'x', 'y'}, 'returns': {'x + y'}, 'related_functions': 
        {'subtract'}}, 'subtract': {'parameters': {'x', 'y'}, 'returns': {'x - y'}, 'related_functions': {'add'}}
    }
    assert relationships == expected_relationships
    assert len(relationships) == 2