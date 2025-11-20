from nodes_types import NodeType

class SceneGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def clear(self):
        self.nodes = []
        self.edges = []

    # ------------------------
    # ADD LANE NODES
    # ------------------------
    def add_lanes(self, lanes):
      pass

    # ------------------------
    # ADD OBJECTS
    # ------------------------
    def add_objects(self, objects, depth=None):
        for oid, obj in enumerate(objects):
            # compute 3D center if depth map exists
            if depth is not None:
                x1, y1, x2, y2 = obj["bbox"]
                   cx = int((x1+x2)/2)
                cy = int((y1+y2)/2)
                z = float(depth[cy, cx])
                pos = (cx, cy, z)
            else:
                pos = None

            self.nodes.append({
                "id": f"obj_{oid}",
                "type": NodeType.OBJECT,
                "class": obj["type"],
                "bbox": obj["bbox"],
                "pos": pos,
            })

    # ------------------------
    # CAR NODE
    # ------------------------
    def set_car_state(self, pos, heading):
        self.nodes.append({
            "id": "car",
            "type": NodeType.CAR,
            "pos": pos,
            "heading": heading
        })

    # ------------------------
    # BUILD EDGES
    # ------------------------
    def build_edges(self):
        self.edges = []
        # create edges for:
        # car -> nearest lane
        # car -> nearest object
        # object -> lane intersections
        pass

    # ------------------------
    # Extract data for Decision Module
    # ------------------------
    def extract_car_state(self):
        for n in self.nodes:
            if n["type"] == NodeType.CAR:
                return n
        return {}

    def extract_surrounding(self):
        # distance to nearest object ahead etc.
        return {}
