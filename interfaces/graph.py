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


