import pytest
from src.main import parse_python_file, identify_relationships, visualize_relationships

@pytest.fixture
def test_parse_python_file(example_python_code):
    functions = parse_python_file(example_python_code, naming_convention="_")
    assert len(functions) == 3
    assert ("add", ["x", "y"], ["x", "y"]) in functions
    assert ("subtract", ["x", "y"], ["x", "y"]) in functions
    assert ("multiply", ["x", "y"], ["x", "y"]) in functions

def test_identify_relationships():
    functions = [("add", ["x", "y"], ["x", "y"]),
                 ("subtract", ["x", "y"], ["x", "y"]),
                 ("multiply", ["x", "y"], ["x", "y"])]
    relationships = identify_relationships(functions)
    assert len(relationships) == 3

def test_visualize_relationships():
    relationships = {"add": {"parameters": {"x", "y"}, "returns": {"x", "y"}, "related_functions": {"subtract"}},
                     "subtract": {"parameters": {"x", "y"}, "returns": {"x", "y"}},
                     "multiply": {"parameters": {"x", "y"}, "returns": {"x", "y"}}}
    visualize_relationships(relationships, "test_visualize_relationships.png")
    # Add assertions to verify the generated PNG file if needed

if __name__ == "__main__":
    pytest.main()
