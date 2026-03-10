from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _clamp(v: float, lo: float, hi: float) -> float:
    return lo if v < lo else hi if v > hi else v


def clamp_slot_layout_to_image(
    img_w: int, img_h: int, params: Dict[str, Any]
) -> Tuple[int, int]:
    slot_layout = params["slot_layout"]
    roi = slot_layout["slot_roi"]
    w = max(1, min(int(roi["width_px"]), int(img_w)))
    h = max(1, min(int(roi["height_px"]), int(img_h)))
    roi["width_px"] = w
    roi["height_px"] = h

    left_anchors = slot_layout["left_anchors"]
    right_anchors = slot_layout["right_anchors"]
    rows = len(slot_layout["slots_per_row"])
    for r in range(rows):
        left = left_anchors[r]
        right = right_anchors[r]
        xL, yT = int(left["x"]), int(left["y"])
        xR = int(right["x"])
        xL = int(_clamp(xL, 0, max(0, img_w - w)))
        xR = int(_clamp(xR, 0, max(0, img_w - w)))
        yT = int(_clamp(yT, 0, max(0, img_h - h)))
        if xR < xL:
            xR = xL
        left_anchors[r] = {"x": xL, "y": yT}
        right_anchors[r] = {"x": xR, "y": yT}
    return w, h


def generate_grid_rois(
    img_w: int, img_h: int, params: Dict[str, Any]
) -> List[Tuple[int, int, int, int, int, int]]:
    w, h = clamp_slot_layout_to_image(img_w, img_h, params)
    slot_layout = params["slot_layout"]
    cols_per_row = list(slot_layout["slots_per_row"])
    left_anchors = slot_layout["left_anchors"]
    right_anchors = slot_layout["right_anchors"]
    rows = len(cols_per_row)
    rois = []
    for r in range(rows):
        cols = int(cols_per_row[r])
        left = left_anchors[r]
        right = right_anchors[r]
        xL, yT = int(left["x"]), int(left["y"])
        xR = int(right["x"])
        xL = int(_clamp(xL, 0, max(0, img_w - w)))
        xR = int(_clamp(xR, 0, max(0, img_w - w)))
        yT = int(_clamp(yT, 0, max(0, img_h - h)))
        if xR < xL:
            xR = xL
        dx = 0.0 if cols <= 1 else (xR - xL) / (cols - 1)
        for c in range(cols):
            x = int(round(xL + c * dx))
            x = int(_clamp(x, 0, max(0, img_w - w)))
            rois.append((r, c, x, yT, w, h))
    return rois
