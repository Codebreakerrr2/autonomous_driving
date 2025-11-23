from typing import Any, Dict, List
from ultralytics import YOLO
from interfaces.perception import IPerceptionModel


class YoloPerception(IPerceptionModel):
    def __init__(self, model_path: str = "yolov8s.pt", conf_threshold: float = 0.5):
        """
        Lädt ein vortrainiertes YOLOv8 Modell.
        """
        self.model = YOLO(model_path)  # lädt automatisch, wenn nicht vorhanden
        self.conf_threshold = conf_threshold

    def predict(self, frame: Any) -> Dict:
        """
        Nimmt ein Bild (np.array) und liefert ein standardisiertes Dictionary zurück:
        {
            "objects": [{"bbox": [x1, y1, x2, y2], "class": int, "confidence": float}, ...],
            "lanes": [],        # leer, da YOLO keine Lanes liefert
            "depth_map": None   # optional für andere Modelle
        }
        """
        results = self.model(frame)
        objects: List[Dict] = []

        for r in results:
            # r.boxes enthält alle Bounding Boxes
            for box in r.boxes:
                conf = float(box.conf[0].item())
                if conf < self.conf_threshold:
                    continue
                cls = int(box.cls[0].item())
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                objects.append({
                    "bbox": [x1, y1, x2, y2],
                    "class": cls,
                    "confidence": conf
                })

        return {
            "objects": objects,
            "lanes": [],
            "depth_map": None
        }
