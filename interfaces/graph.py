# graph/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, Any

from graph.node import Object_Node


class IGraphBuilder(ABC):

    @abstractmethod
    def build(self, perception_output: Dict) -> Any:
        """
        Wandelt die Perception-Daten in ein internes Weltmodell um.
        Kann ein Graph, JSON, Node-Map etc sein.
        """
        pass


from abc import ABC, abstractmethod
from typing import Any, Tuple

class IPositionEstimator(ABC):
    @abstractmethod
    def estimate_3d(self, detection: Any) -> Tuple[float, float, float] | None:
        """
        Wandelt Pixel-Detection in (x, y, z) um.
        Kann Depth Map, Stereo, Lidar etc nutzen.
        """
        pass

# graph/interfaces.py


class IDistanceCalculator(ABC):
    @abstractmethod
    def compute(self, node_a: Object_Node, node_b: Object_Node) -> float:
        pass

