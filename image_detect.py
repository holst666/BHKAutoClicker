import cv2
import numpy as np
import mss
import win32gui
import os

def detect_object_in_window(
    window_title,
    template_path,
    confidence_threshold=0.98,
    debug_save_path=None
):
    """Returns (found: bool, confidence: float, location: tuple or None)"""
    if not os.path.exists(template_path):
        print(f"[Detect] Template '{template_path}' not found!")
        return False, 0.0, None
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"[Detect] Could not read template: {template_path}")
        return False, 0.0, None
    if template.shape[2] == 4:
        template_bgr = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        mask = template[:, :, 3]
        mask_bin = (mask > 250).astype(np.uint8) * 255
    else:
        template_bgr = template
        mask_bin = None
    th, tw = template_bgr.shape[:2]
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"[Detect] Game window '{window_title}' not found!")
        return False, 0.0, None
    l, t, r, b = win32gui.GetWindowRect(hwnd)
    with mss.mss() as sct:
        monitor = {"top": t, "left": l, "width": r - l, "height": b - t}
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)[..., :3]
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    result = cv2.matchTemplate(img, template_bgr, cv2.TM_CCORR_NORMED, mask=mask_bin)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    found = max_val > confidence_threshold
    if debug_save_path:
        img_copy = img.copy()
        if found:
            cv2.rectangle(img_copy, max_loc, (max_loc[0] + tw, max_loc[1] + th), (0,0,255), 2)
        cv2.imwrite(debug_save_path, img_copy)
    return found, max_val, max_loc if found else None