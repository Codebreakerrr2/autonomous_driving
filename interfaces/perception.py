from abc import ABC, abstractmethod
from typing import Any, Dict

class IPerceptionModel(ABC):

    @abstractmethod
    def predict(self, frame: Any) -> Dict:
        """
        Nimmt ein Bild und gibt
        ein standardisiertes Ergebnis zurück.
        Beispiel:
        {
            "objects": [...],
            "lanes": [...],
            "confidence": 0.92
        }
        """
        pass
