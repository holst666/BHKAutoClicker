import cv2
import numpy as np
import os
import pygetwindow as gw
from glob import glob
from tqdm import tqdm
from PIL import Image
import random
import mss
import re

# --- User options here ---
useFile = True    # Set to True to use file instead of screenshot
filePath = "templates/background/screenshot2.png"  # The image file to use if useFile is True

# --- Settings ---
NUM_IMAGES = 100  # Images to generate in this run
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "progress_yolo_dataset"
CLASS_NAME = "progress"
WIN_TITLE = "Clicker Heroes"
# IMG_SIZE = (2560, 1440)  # Optionally resize to match training
OPACITY = 1  # 1.0 = fully opaque
MIN_SIZE = 1.0
MAX_SIZE = 1.0

os.makedirs(f"{OUTPUT_DIR}/images/train", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/labels/train", exist_ok=True)

def grab_background():
    if useFile:
        print(f"Using file: {filePath}")
        img = cv2.imread(filePath)
        if img is None:
            raise FileNotFoundError(f"Could not read image file: {filePath}")
        return img
    else:
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
            #img = cv2.resize(img, IMG_SIZE)
            return img

def overlay_png(bg, overlay, x, y, w, h, opacity=1.0):
    overlay = overlay.resize((w, h), Image.LANCZOS)
    overlay = overlay.convert("RGBA")
    alpha = overlay.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    overlay.putalpha(alpha)
    bg_rgb = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    bg_pil = Image.fromarray(bg_rgb)
    ox, oy = overlay.size
    pos = (int(x - ox // 2), int(y - oy // 2))
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

def next_image_index(folder):
    files = glob(os.path.join(folder, "icon_*.jpg")) + glob(os.path.join(folder, "icon_*.png"))
    numbers = []
    for f in files:
        m = re.search(r'icon_(\d{4})', f)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers, default=-1) + 1

templates = [Image.open(path).convert("RGBA") for path in glob(f"{TEMPLATE_DIR}/*.png")]
print(f"Loaded {len(templates)} templates.")

start_idx = next_image_index(f"{OUTPUT_DIR}/images/train")
print(f"Starting at image index: {start_idx}")

for i in tqdm(range(NUM_IMAGES)):
    bg = grab_background()
    img_h, img_w = bg.shape[:2]
    tmpl = random.choice(templates)
    scale = random.uniform(MIN_SIZE, MAX_SIZE)
    tw, th = int(tmpl.width * scale), int(tmpl.height * scale)
    cx = random.randint(tw // 2, img_w - tw // 2)
    cy = random.randint(th // 2, img_h - th // 2)
    out_img, bbox = overlay_png(bg, tmpl, cx, cy, tw, th, opacity=OPACITY)
    out_img_bgr = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
    img_num = start_idx + i
    img_path = f"{OUTPUT_DIR}/images/train/icon_{img_num:04d}.jpg"
    cv2.imwrite(img_path, out_img_bgr)
    label_path = f"{OUTPUT_DIR}/labels/train/icon_{img_num:04d}.txt"
    save_yolo_label(label_path, bbox, (img_w, img_h))

print(f"Dataset saved to {OUTPUT_DIR}/images/train and labels/train")
