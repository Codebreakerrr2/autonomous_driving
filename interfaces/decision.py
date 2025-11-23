from abc import ABC, abstractmethod
from typing import Any, Dict

class IDecisionModule(ABC):

    @abstractmethod
    def decide(self, world_model: Any) -> Dict:
        """
        Liefert Steuerbefehle:
        {
            "steering": float,
            "throttle": float
        }
        """
        pass
