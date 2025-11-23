from abc import ABC, abstractmethod
from typing import Any
from typing import Dict
class ICameraProvider(ABC):

    @abstractmethod
    def get_frame(self) -> Any:
        """
        Liefert einen einzelnen Frame zurück.
        Kann aus Kamera, Video oder Simulation kommen.
        """
        pass
a
    @abstractmethod
    class IControlOutput(ABC):

        @abstractmethod
        def send(self, commands: Dict) -> None:
            """
            Sendet Befehle an:
            - C-Programm
            - Microcontroller
            - UART
            - Bluetooth
            - Simulation
            """
            pass