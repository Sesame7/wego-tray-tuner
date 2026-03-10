from __future__ import annotations

from typing import Any, Dict

import numpy as np

from detect.base import Detector
from detect.wego_tray import WegoTrayDetector


def create_runtime_detector(params: Dict[str, Any]) -> Detector:
    return WegoTrayDetector(
        params=params,
        generate_overlay=True,
        input_pixel_format="bgr8",
    )


def run_detector(detector_instance: Detector, img_bgr: np.ndarray) -> Dict[str, Any]:
    ok, message, overlay_bgr, result_code = detector_instance.detect(img_bgr)
    if overlay_bgr is None:
        overlay_bgr = img_bgr.copy()
    return {
        "ok": bool(ok),
        "message": str(message),
        "result_code": str(result_code or ("OK" if ok else "NG")),
        "overlay_bgr": overlay_bgr,
    }
