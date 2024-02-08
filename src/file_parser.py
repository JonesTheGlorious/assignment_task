import ast
import re

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

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in file '{file_path}': {e}")