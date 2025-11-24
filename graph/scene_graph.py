# graph/graph.py

class Graph:
    def __init__(self):
        self.nodes = {}     # id -> Node
        self.edges = {}     # (id1, id2) -> weight

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, id1, id2, weight=1.0):
        self.edges[(id1, id2)] = weight
        self.edges[(id2, id1)] = weight  # undirected graph

    def neighbors(self, node_id):
        return [nid2 for (nid1, nid2) in self.edges.keys() if nid1 == node_id]

    def get_edge_weight(self, id1, id2):
        return self.edges.get((id1, id2), None)

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"
