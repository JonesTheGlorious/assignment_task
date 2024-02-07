import networkx as nx
import matplotlib.pyplot as plt

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