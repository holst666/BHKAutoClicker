import os
import time
import mss
import pygetwindow as gw
import numpy as np
import cv2
import re

# --- SETTINGS ---
IMAGE_DIR = "progress_yolo_dataset/images/train"
IMAGE_PREFIX = "icon"   # <--- set your preferred prefix here!
WIN_TITLE = "Clicker Heroes"
NUM_IMAGES = 50         # <--- number of screenshots to take
INTERVAL = 5            # seconds between screenshots

os.makedirs(IMAGE_DIR, exist_ok=True)

def next_image_index(folder, prefix):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png')) and f.startswith(prefix + "_")]
    numbers = []
    for f in files:
        m = re.search(rf'{re.escape(prefix)}_(\d+)', f)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers, default=-1) + 1

def grab_screenshot():
    windows = gw.getWindowsWithTitle(WIN_TITLE)
    if not windows:
        raise RuntimeError(f'No window found with title "{WIN_TITLE}"')
    win = windows[0]
    left, top, width, height = win.left, win.top, win.width, win.height

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

start_idx = next_image_index(IMAGE_DIR, IMAGE_PREFIX)

for i in range(NUM_IMAGES):
    try:
        img = grab_screenshot()
        img_path = os.path.join(IMAGE_DIR, f"{IMAGE_PREFIX}_{start_idx + i:04d}.jpg")
        cv2.imwrite(img_path, img)
        print(f"Saved {img_path}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(INTERVAL)

print(f"Done! {NUM_IMAGES} screenshots saved to {IMAGE_DIR}")
