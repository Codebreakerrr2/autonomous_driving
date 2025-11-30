import torch
import cv2
import numpy as np
from typing import Any, Dict

from interfaces.perception import IPerceptionModel


class DepthPerception(IPerceptionModel):
    def __init__(self, model_type: str = "MiDaS_small"):
        """
        Lädt das MiDaS Depth-Modell über Torch Hub.
        model_type kann sein: "MiDaS_small", "DPT_Large", "DPT_Hybrid"
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # MiDaS Model laden
        self.midas = torch.hub.load("intel-isl/MiDaS", model_type)
        self.midas.to(self.device)
        self.midas.eval()

        # Die zugehörigen Transforms laden
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if model_type in ["DPT_Large", "DPT_Hybrid"]:
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform


    def predict(self, frame: Any) -> Dict:
        """
        Nimmt ein RGB-Image (numpy array) und liefert:
        {
            "objects": [],
            "lanes": [],
            "depth_map": np.ndarray(H, W)
        }
        """

        # BGR → RGB (falls OpenCV-Bilder genutzt werden)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Transformieren + Tensor erstellen
        input_tensor = self.transform(img).to(self.device)

        with torch.no_grad():
            prediction = self.midas(input_tensor)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = prediction.cpu().numpy()

        return {
            "objects": [],
            "lanes": [],
            "depth_map": depth_map
        }

#test test
# run_depth_video.py
import cv2
import numpy as np
import os
from perception.depth_estimator import DepthPerception

def visualize_depth(depth_map: np.ndarray) -> np.ndarray:
    # Normalisiere auf 0..255 und Colormap anwenden
    dmin, dmax = np.nanmin(depth_map), np.nanmax(depth_map)
    if not np.isfinite(dmin) or not np.isfinite(dmax) or dmax == dmin:
        norm = np.zeros_like(depth_map, dtype=np.uint8)
    else:
        norm = ((depth_map - dmin) / (dmax - dmin) * 255.0).astype(np.uint8)
    color = cv2.applyColorMap(norm, cv2.COLORMAP_MAGMA)
    return color

def main(video_path: str, out_path: str = None, model_type: str = "MiDaS_small", show_window: bool = True):
    # Initialisiere Depth-Model (lädt MiDaS via torch.hub)
    print("Lade Depth-Modell (MiDaS)... das kann beim ersten Lauf dauern (Download + Cache).")
    depth_model = DepthPerception(model_type=model_type)
    print("Modell geladen.")

    cap = cv2.VideoCapture("/Users/usman/PycharmProjects/SelfDrivingCar/data/knuff1.mp4")
    if not cap.isOpened():
        raise RuntimeError(f"Kann Video nicht öffnen: {video_path}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = None
    if out_path is not None:
        # Output Video hat gleiche Größe wie Input, wir speichern RGB overlay
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(out_path, fourcc, cap.get(cv2.CAP_PROP_FPS) or 20.0, (w*2, h))

    frame_idx = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1

            # Depth vorhersagen
            out = depth_model.predict(frame)
            depth_map = out["depth_map"]  # numpy array, shape (H,W)

            # Visualisierung
            depth_vis = visualize_depth(depth_map)
            # Side-by-side original + depth
            combined = np.hstack([frame, depth_vis])

            if show_window:
                cv2.imshow("Frame | Depth", combined)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if writer is not None:
                writer.write(combined)

            if frame_idx % 50 == 0:
                print(f"Processed {frame_idx} frames...")

    finally:
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
        print("Fertig.")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("video", help="Pfad zum Video (z.B. video.mp4)")
    p.add_argument("--out", help="Optional: speichere Overlay-Video", default=None)
    p.add_argument("--model", help="MiDaS model_type (MiDaS_small, DPT_Large, DPT_Hybrid)", default="MiDaS_small")
    p.add_argument("--no-show", help="Fenster nicht anzeigen (headless)", action="store_true")
    args = p.parse_args()
    main(args.video, args.out, args.model, not args.no_show)
#to run  cd /Users/usman/PycharmProjects/SelfDrivingCar python -m perception.depth_estimator /Users/usman/PycharmProjects/SelfDrivingCar/data/knuff1.mp4