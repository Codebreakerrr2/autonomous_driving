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

