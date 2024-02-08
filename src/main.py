import argparse
import os
from file_parser import parse_python_file
from relationship import identify_relationships
from visualization import visualize_relationships

def main():
    parser = argparse.ArgumentParser(description="Visualize relationships between functions in a Python file.")
    parser.add_argument("file_path", nargs='?', default=os.path.join(os.path.abspath(os.getcwd()), "resources/elementary.py"), help="Path to the Python file")
    parser.add_argument("--naming-convention", nargs='?', default="_", help="Naming convention pattern (default: _)")
    parser.add_argument("output_file", nargs='?', default="function_relationships_graph.png", help="name of the resulting output file")

    args = parser.parse_args()

    try:
        extracted_functions = parse_python_file(args.file_path, args.naming_convention)
        relationships = identify_relationships(extracted_functions)
        visualize_relationships(relationships, args.output_file)
        print("Graph visualization saved as " + args.output_file)
    except Exception as e:
        print(f"Error: {e}")
    


if __name__ == "__main__":
    main()
