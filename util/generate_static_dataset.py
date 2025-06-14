import cv2
import numpy as np
import os
import pygetwindow as gw
from glob import glob
from tqdm import tqdm
from PIL import Image
import mss

# --- Settings ---
NUM_IMAGES = 500
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "progress_yolo_dataset"
CLASS_NAME = "progress"
WIN_TITLE = "Clicker Heroes"
IMG_SIZE = (640, 384)  # Target training size

# ----> SET THESE TO YOUR ICON'S LOCATION AND SIZE IN SCREENSHOT <----
ICON_CENTER_X = 100    # <-- CHANGE ME (x coord in 640x384 image)
ICON_CENTER_Y = 100    # <-- CHANGE ME (y coord in 640x384 image)
ICON_SIZE = (32, 32)   # <-- CHANGE ME (width, height in pixels)
# ---------------------------------------------------------------
#2393 x 390   + 2462 x 453
os.makedirs(f"{OUTPUT_DIR}/images/train", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/labels/train", exist_ok=True)

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

def overlay_png(bg, overlay, cx, cy, w, h, opacity=1.0):
    overlay = overlay.resize((w, h), Image.LANCZOS)
    overlay = overlay.convert("RGBA")
    alpha = overlay.split()[3].point(lambda p: int(p * opacity))
    overlay.putalpha(alpha)

    bg_rgb = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    bg_pil = Image.fromarray(bg_rgb)
    ox, oy = overlay.size
    pos = (int(cx - ox // 2), int(cy - oy // 2))
    bg_pil.paste(overlay, pos, overlay)
    return np.array(bg_pil), (pos[0], pos[1], ox, oy)

def save_yolo_label(label_path, box, img_size):
    x, y, w, h = box
    img_w, img_h = img_size
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(img_w, x + w)
    y2 = min(img_h, y + h)
    xc = ((x1 + x2) / 2) / img_w
    yc = ((y1 + y2) / 2) / img_h
    bw = (x2 - x1) / img_w
    bh = (y2 - y1) / img_h
    with open(label_path, "w") as f:
        f.write(f"0 {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

templates = [Image.open(path).convert("RGBA") for path in glob(f"{TEMPLATE_DIR}/*.png")]
print(f"Loaded {len(templates)} templates.")

for i in tqdm(range(NUM_IMAGES)):
    bg = grab_screenshot()
    img_h, img_w = bg.shape[:2]
    tmpl = random.choice(templates)  # If you have multiple icon PNGs
    tw, th = ICON_SIZE
    cx, cy = ICON_CENTER_X, ICON_CENTER_Y

    out_img, bbox = overlay_png(bg, tmpl, cx, cy, tw, th, opacity=OPACITY)
    out_img_bgr = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
    img_path = f"{OUTPUT_DIR}/images/train/progress_{i:04d}.jpg"
    cv2.imwrite(img_path, out_img_bgr)
    label_path = f"{OUTPUT_DIR}/labels/train/progress_{i:04d}.txt"
    save_yolo_label(label_path, bbox, (img_w, img_h))

print(f"Dataset saved to {OUTPUT_DIR}/images/train and labels/train")
