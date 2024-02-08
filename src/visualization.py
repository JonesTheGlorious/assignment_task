import networkx as nx
import matplotlib.pyplot as plt

def visualize_relationships(relationships, output_file):
    """
    Visualizes the relationships between functions as a graph.

    Args:
        relationships (dict): A dictionary containing relationships between functions.
                              Each key is a function name, and the corresponding value
                              is a dictionary containing information about related functions.
        output_file (str): The filename for the output graph image.

    Returns:
        None
    """
    try:
        #Creates directed graph
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
        pos = nx.spring_layout(G, k=0.35, iterations=25)  # Layout algorithm
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
        plt.title("Function Relationships Graph")
        plt.savefig(output_file)  # Save the plot as a PNG file with output_file name
        plt.close()
    except Exception as e:
        raise RuntimeError(f"Error visualizing relationships: {e}")