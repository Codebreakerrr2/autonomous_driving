from graph.nodes_types import NodeType


class Object_Node:
    def __init__(self, id, node_type=NodeType.UNKNOWN ,x=None,y=None,z=None):
        self.id = id
        self.type = node_type
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Node(id={self.id}, type={self.type})"

class LaneNode:
    def __init__(self, id, node_type = NodeType.GREENLANE, coordiantes = None):
        self.id = id
        self.coordiantes = coordiantes
        self.type = node_type
