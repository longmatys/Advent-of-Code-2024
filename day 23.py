import os
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def draw_graph(G, subgraph):
    plt.figure(figsize=(10, 8))  # Set the figure size
    nx.draw(
        G,
        with_labels=True,           # Show node labels
        node_color=["red" if node in subgraph else "lightblue" for node in G.nodes()],     # Set node color
        edge_color="gray",          # Set edge color
        node_size=500,              # Set node size
        font_size=10                # Set font size for labels
    )

    # Save the graph as an image
    # plt.savefig("graph.png", format="PNG")
    plt.show()


# Find all triangles
def find_triangles(graph, filter=None):
    triangles = set()
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        for n1, n2 in combinations(neighbors, 2):  # Check pairs of neighbors
            if graph.has_edge(n1, n2):  # If neighbors are connected, it's a triangle
                triangle = tuple(sorted([node, n1, n2]))  # Sort to avoid duplicates
                filter_values = [node for node in triangle if node[0] == filter]
                if filter and len(filter_values)==0:
                    continue
                triangles.add(triangle)
    return triangles


def work(data):
    G = nx.Graph()
    for node1, node2 in [edge.split('-') for edge in data]:
        G.add_edge(node1, node2)
    print(list(nx.connected_components(G)))

    triangles = find_triangles(G, 't')
    print(f'Found {len(triangles)} triangles starting with t')

    # Find all cliques
    cliques = list(nx.find_cliques(G))
    # Find the largest clique
    largest_clique = max(cliques, key=len)
    print(f'Found largest clique with len of {len(largest_clique)}: {",".join(sorted(largest_clique))}')
    subset_nodes = largest_clique

    # Create a subgraph with only the subset of nodes
    subgraph = G.subgraph(subset_nodes)
    #draw_graph(G, subgraph)
    

def main():
    # Get the name of the Python script

    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'

    with open(input_file) as f:
        data = [line.strip() for line in f]
        res = work(data)


if __name__ == '__main__':
    main()
