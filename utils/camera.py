import cv2
import os
from typing import Any, Dict

from interfaces.io import ICameraProvider


class FlexibleCameraProvider(ICameraProvider):
    """
    Liefert Frames aus:
    - Video-Datei
    - Bilder-Ordner
    - Webcam
    """
    def __init__(self, source: str = "0"):
        """
        source:
            - int-String oder int → Webcam
            - Pfad zu Video-Datei
            - Pfad zu Bilder-Ordner
        """
        self.frames = []
        self.index = 0
        self.cap = None

        if source.isdigit():  # Webcam
            self.cap = cv2.VideoCapture(int(source))
            if not self.cap.isOpened():
                raise ValueError(f"Webcam {source} konnte nicht geöffnet werden.")

        elif os.path.isfile(source):  # Video-Datei
            self.cap = cv2.VideoCapture(source)
            if not self.cap.isOpened():
                raise ValueError(f"Video {source} konnte nicht geöffnet werden.")

        elif os.path.isdir(source):  # Bilder-Ordner
            files = sorted(os.listdir(source))
            self.frames = [os.path.join(source, f) for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            if not self.frames:
                raise ValueError(f"Keine Bilder im Ordner {source} gefunden.")

        else:
            raise ValueError(f"Quelle {source} unbekannt.")

    def get_frame(self) -> Any:
        # Video / Webcam
        if self.cap:
            ret, frame = self.cap.read()
            if not ret:
                return None
            return frame

        # Bilder-Ordner
        if self.frames:
            if self.index >= len(self.frames):
                return None
            frame_path = self.frames[self.index]
            frame = cv2.imread(frame_path)
            self.index += 1
            return frame

    class IControlOutput(ICameraProvider.IControlOutput):
        def send(self, commands: Dict) -> None:
            print(f"FlexibleCameraProvider: ControlOutput send: {commands}")
