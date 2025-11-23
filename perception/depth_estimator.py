from typing import Any, Dict
import torch
import cv2
from interfaces.perception import IPerceptionModel


class DepthPerception(IPerceptionModel):
    def __init__(self, model_type: str = "MiDaS_small"):
        """
        Lädt ein vortrainiertes MiDaS Depth Estimation Modell.
        model_type kann z.B. sein: "DPT_Large", "DPT_Hybrid", "MiDaS_small"
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # MiDaS Modell laden
        self.midas = torch.hub.load("intel-isl/MiDaS", model_type)
        self.midas.to(self.device)
        self.midas.eval()

        # Transformationspipeline
        self.transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform if "DPT" in model_type else torch.hub.load("intel-isl/MiDaS", "transforms").small_transform

    def predict(self, frame: Any) -> Dict:
        """
        Nimmt ein Bild (np.array BGR) und liefert ein standardisiertes Dictionary:
        {
            "objects": [],        # leer
            "lanes": [],          # leer
            "depth_map": np.array # Depth Map
        }
        """
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_tensor = self.transform(img).to(self.device)

        with torch.no_grad():
            prediction = self.midas(input_tensor)
            depth_map = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False
            ).squeeze().cpu().numpy()

        return {
            "objects": [],
            "lanes": [],
            "depth_map": depth_map
        }
