def identify_relationships(functions):
    try:
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
    except Exception as e:
        raise RuntimeError(f"Error identifying relationships: {e}")