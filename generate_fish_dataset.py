import cv2
import numpy as np
import os
import pygetwindow as gw
from glob import glob
from tqdm import tqdm
from PIL import Image
import random
import mss

# --- Settings ---
NUM_IMAGES = 1000  # Adjust as needed
TEMPLATE_DIR = "templates/fish_templates"
OUTPUT_DIR = "fish_yolo_dataset"
CLASS_NAME = "fish"
WIN_TITLE = "Clicker Heroes"
IMG_SIZE = (640, 384)  # Target training size, can adjust
OPACITY = 0.9  # 1.0 = fully opaque, 0.8 = 80% opaque (20% transparent)

os.makedirs(f"{OUTPUT_DIR}/images/train", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/labels/train", exist_ok=True)

def grab_screenshot():
    # Find window by title (case-sensitive)
    windows = gw.getWindowsWithTitle("Clicker Heroes")
    if not windows:
        raise RuntimeError('No window found with title "Clicker Heroes"')
    win = windows[0]
    left, top, width, height = win.left, win.top, win.width, win.height

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # Optionally resize to target IMG_SIZE
        return img

# --- Overlay PNG with reduced opacity ---
def overlay_png(bg, overlay, x, y, w, h, angle, opacity=1.0):
    overlay = overlay.resize((w, h), Image.LANCZOS).rotate(angle, expand=True)
    overlay = overlay.convert("RGBA")
    # Reduce opacity
    alpha = overlay.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    overlay.putalpha(alpha)

    # Convert OpenCV BGR to PIL RGB!
    bg_rgb = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    bg_pil = Image.fromarray(bg_rgb)
    ox, oy = overlay.size
    pos = (int(x - ox//2), int(y - oy//2))
    bg_pil.paste(overlay, pos, overlay)
    return np.array(bg_pil), (pos[0], pos[1], ox, oy)

# --- YOLO label helper ---
def save_yolo_label(label_path, box, img_size):
    x, y, w, h = box
    img_w, img_h = img_size
    # Clamp box to image bounds
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(img_w, x + w)
    y2 = min(img_h, y + h)
    # YOLO format: class x_center y_center width height (all normalized)
    xc = ((x1 + x2) / 2) / img_w
    yc = ((y1 + y2) / 2) / img_h
    bw = (x2 - x1) / img_w
    bh = (y2 - y1) / img_h
    with open(label_path, "w") as f:
        f.write(f"0 {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

# --- Main loop ---
templates = [Image.open(path).convert("RGBA") for path in glob(f"{TEMPLATE_DIR}/*.png")]
print(f"Loaded {len(templates)} templates.")

for i in tqdm(range(NUM_IMAGES)):
    # 1. Grab screenshot
    bg = grab_screenshot()
    img_h, img_w = bg.shape[:2]
    # 2. Select random template and augmentations
    tmpl = random.choice(templates)
    scale = random.uniform(0.1, 1.0)
    rot = random.uniform(0, 360)
    tw, th = int(tmpl.width * scale), int(tmpl.height * scale)
    # 3. Random position, ensure inside image
    cx = random.randint(tw//2, img_w - tw//2)
    cy = random.randint(th//2, img_h - th//2)
    # 4. Overlay with reduced opacity
    out_img, bbox = overlay_png(bg, tmpl, cx, cy, tw, th, rot, opacity=OPACITY)
    # 5. Convert from RGB (PIL/NumPy) to BGR (OpenCV) before saving
    out_img_bgr = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
    img_path = f"{OUTPUT_DIR}/images/train/fish_{i:04d}.jpg"
    cv2.imwrite(img_path, out_img_bgr)
    # 6. Save label
    label_path = f"{OUTPUT_DIR}/labels/train/fish_{i:04d}.txt"
    save_yolo_label(label_path, bbox, (img_w, img_h))

print(f"Dataset saved to {OUTPUT_DIR}/images/train and labels/train")
