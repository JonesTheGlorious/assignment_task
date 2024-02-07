import argparse
import ast
import re
import os
import networkx as nx
import matplotlib.pyplot as plt
from tests.test_scripts import visualize_relationships

def parse_python_file(file_path, naming_convention):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        tree = ast.parse(code)

        functions = []

        def traverse(node):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                # Split function name based on naming convention
                split_function_name = re.split(naming_convention, function_name)
                if len(split_function_name) == 1 or (len(split_function_name) > 1 and any(split_function_name)):
                    parameters = [arg.arg for arg in node.args.args]
                    returns = []
                    for statement in node.body:
                        if isinstance(statement, ast.Return):
                            if isinstance(statement.value, ast.Name):
                                returns.append(statement.value.id)
                            elif isinstance(statement.value, ast.Tuple):
                                returns.extend([elt.id for elt in statement.value.elts if isinstance(elt, ast.Name)])
                    functions.append((' '.join(split_function_name), parameters, returns))

            for child in ast.iter_child_nodes(node):
                traverse(child)

        traverse(tree)

        return functions

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in file '{file_path}': {e}")

def identify_relationships(functions):
    try:
        relationships = {}
        for name, parameters, returns in functions:
            relationships[name] = {'parameters': set(parameters), 'returns': set(returns)}

        for name, info in relationships.items():
            for other_name, other_info in relationships.items():
                if name != other_name:
                    if info['parameters'] & other_info['parameters'] or info['returns'] & other_info['parameters']:
                        # Establishing a relationship between functions
                        if 'related_functions' not in info:
                            info['related_functions'] = set()
                        info['related_functions'].add(other_name)

        return relationships
    except Exception as e:
        raise RuntimeError(f"Error identifying relationships: {e}")

def visualize_relationships(relationships, output_file):
    try:
        G = nx.DiGraph()

        # Add nodes for each function
        for name in relationships:
            G.add_node(name)

        # Add edges based on relationships
        for name, info in relationships.items():
            related_functions = info.get('related_functions', [])
            for related_function in related_functions:
                G.add_edge(name, related_function)

        # Visualize the graph
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)  # Layout algorithm
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
        plt.title("Function Relationships Graph")
        plt.savefig(output_file)  # Save the plot as a PNG file
        plt.close()
    except Exception as e:
        raise RuntimeError(f"Error visualizing relationships: {e}")

def main():
    parser = argparse.ArgumentParser(description="Visualize relationships between functions in a Python file.")
    parser.add_argument("file_path",nargs='?', default=os.path.join(os.path.abspath(os.getcwd()), "resources/elementary.py"), help="Path to the Python file")
    parser.add_argument("--naming-convention", default="_", help="Naming convention pattern (default: _)")

    args = parser.parse_args()

    try:
        extracted_functions = parse_python_file(args.file_path, args.naming_convention)
        relationships = identify_relationships(extracted_functions)
        output_file = "function_relationships_graph.png"
        visualize_relationships(relationships, output_file)
        print("Graph visualization saved as 'function_relationships_graph.png'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
