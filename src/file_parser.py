import ast
import re

def parse_python_file(file_path, naming_convention):
    """
    Parses the provided Python file to extract function information.

    Args:
        file_path (str): The path to the Python file to be parsed.
        naming_convention (str): The naming convention used for function names.

    Returns:
        list: A list of tuples, each containing function name, parameters, and return values.
    """
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        tree = ast.parse(code)

        functions = []

        # Function to traverse the AST and extract function information
        def traverse(node):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                # Split function name based on naming convention
                split_function_name = re.split(naming_convention, function_name)
                if len(split_function_name) > 1:
                    # Extract function parameters
                    parameters = [arg.arg for arg in node.args.args]
                    returns = []
                    for statement in node.body:
                        if isinstance(statement, ast.Return):
                            #checks if the return type is a name or a tuple and appends to return based on type.
                            if isinstance(statement.value, ast.Name):
                                returns.append(statement.value.id)
                            elif isinstance(statement.value, ast.Tuple):
                                returns.extend([elt.id for elt in statement.value.elts if isinstance(elt, ast.Name)])
                    # Append function information to the list
                    functions.append((' '.join(split_function_name), parameters, returns))
            
            # Recursively traverse child nodes in the AST
            for child in ast.iter_child_nodes(node):
                traverse(child)

        traverse(tree)

        return functions

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in file '{file_path}': {e}")