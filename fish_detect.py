import time
import mss
import pygetwindow as gw
import pyautogui
import numpy as np
import cv2
from util import resource_path
from ultralytics import YOLO

YOLO_MODEL_PATH = resource_path("best.pt")
WINDOW_TITLE = "Clicker Heroes"
DETECTION_INTERVAL = 10  # seconds
CONFIDENCE_THRESHOLD = 0.8
FISH_COUNTER = 0

# Load YOLO model
model = YOLO(YOLO_MODEL_PATH)
model.to('cpu')  # Force CPU (works with torch>=2)

def detect_fish_loop(app_state):
    global FISH_COUNTER
    FISH_COUNTER = 0
    while app_state["running"] and app_state["fish_detect_enabled"]:
        print("Starting detect fish loop")
        detect_fish_and_click(app_state)
        time.sleep(10)

def get_window_bbox():
    windows = gw.getWindowsWithTitle(WINDOW_TITLE)
    if not windows:
        raise RuntimeError(f'No window found with title "{WINDOW_TITLE}"')
    win = windows[0]
    return win.left, win.top, win.width, win.height

def grab_window_screenshot(left, top, width, height):
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def detect_fish_and_click(app_state):
    global FISH_COUNTER
    left, top, width, height = get_window_bbox()
    img = grab_window_screenshot(left, top, width, height)
    results = model(img)
    boxes = results[0].boxes
    if boxes is not None and len(boxes) > 0:
        # Get confidences
        confs = boxes.conf.cpu().numpy()
        best_idx = int(np.argmax(confs))
        best_conf = confs[best_idx]
        box = boxes.xyxy[best_idx].cpu().numpy()
        # Box: [x1, y1, x2, y2] (relative to window)
        fish_cx = int((box[0] + box[2]) / 2) + left
        fish_cy = int((box[1] + box[3]) / 2) + top
        if best_conf >= CONFIDENCE_THRESHOLD:
            while app_state["running"] and app_state["pause_event"].is_set():
                time.sleep(0.01)
            
            if app_state["running"] and not app_state["pause_event"].is_set():
                app_state["pause_event"].set()
                time.sleep(0.1)
                print(f"Fish detected at: ({fish_cx}, {fish_cy}) with confidence {best_conf:.2f}. Clicking.")
                pyautogui.moveTo(fish_cx, fish_cy, duration=0.1)
                pyautogui.click()
                FISH_COUNTER += 1
                print("Clicked " + str(FISH_COUNTER) + " this session")
                app_state["pause_event"].clear()
            else:
                print("Auto clicker was stopped")
        else:
            print(f"Fish detected but confidence too low ({best_conf:.2f} < {CONFIDENCE_THRESHOLD}). Not clicking.")
    else:
        print("No fish detected.")