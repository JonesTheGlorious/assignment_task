import ast
import os
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Visualize relationships between functions in a Python file.")
    # parser.add_argument("file_path", default= os.path.join(os.path.abspath(os.getcwd()), "resources/elementary.py"), help="Path to the Python file")
    parser.add_argument("--naming-convention", default="_", help="Naming convention pattern (default: _)")

    args = parser.parse_args()

    output_file = "function_relationships_graph.png"
    file_path = os.path.join(os.path.abspath(os.getcwd()), "resources/elementary.py")
    extracted_functions = parse_python_file(file_path, args.naming_convention)
    relationships = identify_relationships(extracted_functions)
    visualize_relationships(relationships, output_file)
    # for function in extracted_functions:
    #     print("Function Name:", function[0])
    #     print("Input Parameters:", function[1])
    #     print("Return Values:", function[2])
    #     print()
    # for name, info in relationships.items():
    #     print("Function:", name)
    #     print("Related Functions:", info.get('related_functions', []))
    #     print()

def parse_python_file(file_path, naming_convention):
    """
    Parse the Python file and extract function names, parameters, and return values.
    """
    with open(file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)

    functions = []

    def traverse(node):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            # Split function name based on naming convention
            split_function_name = re.split(naming_convention, function_name)
            if len(split_function_name) > 1:
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

def identify_relationships(functions):
    """
    Identify relationships between functions based on shared input parameters and return values.
    """
    relationships = {}
    for name, parameters, returns in functions:
        relationships[name] = {'parameters': set(parameters), 'returns': set(returns)}

    for name, info in relationships.items():
        for compare_func_name, compare_func_info in relationships.items():
            if name != compare_func_name:
                if info['parameters'] & compare_func_info['parameters'] or info['returns'] & compare_func_info['parameters']:
                    # Establishing a relationship between functions
                    if 'related_functions' not in info:
                        info['related_functions'] = set()
                    info['related_functions'].add(compare_func_name)

    return relationships

def visualize_relationships(relationships, output_file):
    """
    Visualize the relationships between functions as a graph and save it as a PNG file.
    """
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
    pos = nx.spring_layout(G, k=0.4, iterations=25)  # Layout algorithm
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Function Relationships Graph")
    plt.savefig(output_file)  # Save the plot as a PNG file on the output_file path
    plt.close()

if __name__ == '__main__':
    main()
