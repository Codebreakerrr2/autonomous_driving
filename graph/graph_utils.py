from typing import Dict

from graph.node import LaneNode, Object_Node
from graph.nodes_types import NodeType
from graph.scene_graph import Graph
from interfaces.geometry import IDistanceCalculator, IPositionEstimator
from interfaces.graph import IGraphBuilder


class SimpleGraphBuilder(IGraphBuilder):
    def __init__(self, position_estimator: IPositionEstimator, distance_calculator: IDistanceCalculator):
        self.position_estimator = position_estimator
        self.distance_calculator = distance_calculator
        self.next_id = 0  # automatische Node-ID

    def build(self, perception_output: Dict) -> "Graph":
        """
        Baut einen Graphen aus perception output:
        perception_output = {
            "objects": [...],
            "lanes": [...]
        }
        """
        graph = Graph()

        #  Lane Nodes erstellen
        for lane in perception_output.get("lanes", []):
            lane_node = LaneNode(
                id=self.next_id,
                coordiantes=lane.get("coordinates", None),
                node_type=NodeType.GREENLANE
            )
            graph.add_node(lane_node)
            self.next_id += 1

        #  Object Nodes erstellen
        for obj in perception_output.get("objects", []):
            pos = self.position_estimator.estimate_3d(obj)
            obj_node = Object_Node(
                id=self.next_id,
                node_type=NodeType.UNKNOWN,
                x=pos[0] if pos else None,
                y=pos[1] if pos else None,
                z=pos[2] if pos else None
            )
            graph.add_node(obj_node)
            self.next_id += 1

        #  Edges erstellen (alle paarweise, z.B. für Abstand)
        node_ids = list(graph.nodes.keys())
        for i, id1 in enumerate(node_ids):
            for id2 in node_ids[i+1:]:
                node_a = graph.nodes[id1]
                node_b = graph.nodes[id2]
                dist = self.distance_calculator.compute(node_a, node_b)
                graph.add_edge(id1, id2, weight=dist)

        return graph
