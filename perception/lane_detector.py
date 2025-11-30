from interfaces.perception import IPerceptionModel
from typing import Any, Dict, List, Tuple
import torch
import cv2
import os
from utils.common import get_model, merge_config
from data.dataset import LaneTestDataset
import torchvision.transforms as transforms
import numpy as np
import tqdm

class LaneDetection(IPerceptionModel):
    def __init__(self, model_path: str = "Ultra-Fast-Lane-Detection.pth", dataset: str = "CULane"):
        # Config laden
        args, cfg = merge_config()
        cfg.test_model = model_path
        cfg.dataset = dataset
        cfg.batch_size = 1
        self.cfg = cfg

        # Model laden
        self.net = get_model(cfg)
        state_dict = torch.load(cfg.test_model, map_location='cpu')['model']
        compatible_state_dict = {}
        for k, v in state_dict.items():
            if 'module.' in k:
                compatible_state_dict[k[7:]] = v
            else:
                compatible_state_dict[k] = v
        self.net.load_state_dict(compatible_state_dict, strict=False)
        self.net.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net.to(self.device)

        # Transform
        self.img_transforms = transforms.Compose([
            transforms.Resize((int(cfg.train_height / cfg.crop_ratio), cfg.train_width)),
            transforms.ToTensor(),
            transforms.Normalize((0.485,0.456,0.406), (0.229,0.224,0.225))
        ])

    def predict(self, frame: Any) -> Dict:
        """
        frame: np.ndarray BGR
        return: dict mit lane pixel koords
        """
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_tensor = self.img_transforms(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            pred = self.net(input_tensor)

        # pred2coords von UFLD
        lanes: List[List[Tuple[int,int]]] = []
        loc_row = pred['loc_row'].cpu()
        loc_col = pred['loc_col'].cpu()
        exist_row = pred['exist_row'].cpu()
        exist_col = pred['exist_col'].cpu()

        row_anchor = self.cfg.row_anchor
        col_anchor = self.cfg.col_anchor
        H, W, _ = frame.shape

        for lane_idx in range(loc_row.shape[-1]):
            tmp = []
            for k in range(loc_row.shape[1]):
                if exist_row[0,k,lane_idx]:
                    idx = loc_row[0,:,k,lane_idx].argmax()
                    x = int(idx / (loc_row.shape[0]-1) * W)
                    y = int(row_anchor[k] * H)
                    tmp.append((x,y))
            lanes.append(tmp)

        return {"objects": [], "lanes": lanes, "confidence": 1.0}  # confidence dummy

# --- Main Demo ---
if __name__ == "__main__":
    lane_detector = LaneDetection(model_path="ufld_culane.pth")  # hier Pfad zu deinem vortrainierten Model

    cap = cv2.VideoCapture("test_video.mp4")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = lane_detector.predict(frame)

        # Lanes visualisieren
        for lane in result["lanes"]:
            for x, y in lane:
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        cv2.imshow("Lane Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
