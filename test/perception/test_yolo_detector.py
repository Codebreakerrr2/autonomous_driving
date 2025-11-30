from unittest import TestCase
import pytest
import numpy as np

from perception.yolo_detector import YoloPerception


class TestYoloPerception(TestCase):
    def test_predict(self):
        # Dummy-Bild erstellen (RGB 640x480)
        dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        # YOLO Modell initialisieren
        yolo = YoloPerception(conf_threshold=0.3)

        # Prediction auf Dummy-Bild
        output = yolo.predict(dummy_frame)

        # Überprüfen, dass Output das erwartete Format hat
        assert isinstance(output, dict)
        assert "objects" in output
        assert "lanes" in output
        assert "depth_map" in output

        # Objekte sollten Liste sein
        assert isinstance(output["objects"], list)
        for obj in output["objects"]:
            assert "bbox" in obj
            assert "class" in obj
            assert "confidence" in obj
            x1, y1, x2, y2 = obj["bbox"]
            assert 0 <= x1 <= 640
            assert 0 <= x2 <= 640
            assert 0 <= y1 <= 480
            assert 0 <= y2 <= 480
            assert 0.0 <= obj["confidence"] <= 1.0

        # Lanes sollten leer sein
        assert output["lanes"] == []

        # Depth Map sollte None sein
        assert output["depth_map"] is None

        print("YOLO Perception Test passed!")
