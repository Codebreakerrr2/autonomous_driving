import math
from interfaces.geometry import IDistanceCalculator, IPositionEstimator
import numpy as np


class DepthPositionEstimator(IPositionEstimator):
    """
    Nimmt eine Depth-Map + YOLO-Bounding-Box und erzeugt (x, y, z).
    """
    def __init__(self, fx, fy, cx, cy):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.depth_map = None

    def update_depth(self, depth_map: np.ndarray):
        self.depth_map = depth_map

    def estimate_3d(self, node):
        if self.depth_map is None:
            return None

        # Mittelpunkt der Bounding Box holen
        u = int((node.x1 + node.x2) / 2)
        v = int((node.y1 + node.y2) / 2)

        depth = float(self.depth_map[v, u])
        if depth <= 0:
            return None

        # Reale Welt Koordinaten hier eventuell kamera etc kalibieren
        X = (u - self.cx) * depth / self.fx
        Y = (v - self.cy) * depth / self.fy
        Z = depth

        return X, Y, Z

    # ob das sinn macht?

class EuclideanDistance(IDistanceCalculator):

        def compute(self, a, b) -> float:
            if None in (a.x, a.y, a.z, b.x, b.y, b.z):
                return float("inf")

            dx = a.x - b.x
            dy = a.y - b.y
            dz = a.z - b.z

            return math.sqrt(dx * dx + dy * dy + dz * dz)
