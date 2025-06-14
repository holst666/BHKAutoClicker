import mss
import pygetwindow as gw
import numpy as np
import cv2
from ultralytics import YOLO

def detect_object_in_window(
    window_title,
    model_path,
    confidence_threshold=0.8
):
    """
    Returns (found: bool, confidence: float, bbox: (x1, y1, x2, y2) or None)
    """
    # Load YOLO model
    model = YOLO(model_path)
    
    # Find window and grab screenshot
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"[Detect] Game window '{window_title}' not found!")
        return False, 0.0, None
    win = windows[0]
    left, top, width, height = win.left, win.top, win.width, win.height

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Run YOLO inference
    results = model(img)
    boxes = results[0].boxes
    if boxes is not None and len(boxes) > 0:
        confs = boxes.conf.cpu().numpy()
        best_idx = int(np.argmax(confs))
        best_conf = confs[best_idx]
        if best_conf >= confidence_threshold:
            box = boxes.xyxy[best_idx].cpu().numpy()
            return True, float(best_conf), tuple(map(int, box))
        else:
            return False, float(best_conf), None
    else:
        return False, 0.0, None