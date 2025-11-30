import numpy as np
import torch
from unittest import TestCase
from unittest.mock import patch, MagicMock
from perception.depth_estimator import DepthPerception


class TestDepthPerception(TestCase):

    @patch("perception.depth_estimator.torch.hub.load")
    def test_depth_output(self, mock_midas_load):
        """
        Testet, ob DepthPerception korrekt ein dict mit depth_map, objects, lanes zurückgibt.
        MiDaS wird gemockt, damit der Test offline und schnell läuft.
        """

        # Fake MiDaS model
        fake_model = MagicMock()
        fake_model.forward = lambda x: torch.randn(256, 256)  # fake depth tensor

        mock_midas_load.return_value = fake_model

        # Depth model
        dp = DepthPerception(model_type="MiDaS_small")

        # Transform mock (korrekt: gibt torch.Tensor zurück!)
        dp.transform = lambda x: torch.randn(1, 3, 256, 256)

        # Dummy input frame
        dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        # Run prediction
        result = dp.predict(dummy_frame)

        # Assertions
        assert isinstance(result, dict)
        assert "depth_map" in result
        assert "lanes" in result
        assert "objects" in result

        assert result["lanes"] == []
        assert result["objects"] == []

        depth_map = result["depth_map"]
        assert isinstance(depth_map, np.ndarray)
        assert depth_map.shape == dummy_frame.shape[:2]
        assert np.all(np.isfinite(depth_map))
