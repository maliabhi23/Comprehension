import networkx as nx


def generate_graph(relations):
    graph = nx.DiGraph()

    for relation in relations:
        graph.add_edge(
            relation["source"],
            relation["target"],
            relation=relation["relation"]
        )

    return graph