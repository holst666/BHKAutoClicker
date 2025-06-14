import os
from glob import glob
from PIL import Image

# === SETTINGS: Icon bounding box in pixels (double check these are up to date!) ===
OUTPUT_DIR = "progress_yolo_dataset"
BOX_X = 2395    # left
BOX_Y = 390     # top
BOX_W = 66      # width
BOX_H = 63      # height

os.makedirs(f"{OUTPUT_DIR}/labels/train", exist_ok=True)

image_paths = glob(f"{OUTPUT_DIR}/images/train/*.jpg") + glob(f"{OUTPUT_DIR}/images/train/*.png")
print(f"Found {len(image_paths)} images.")

for img_path in image_paths:
    with Image.open(img_path) as img:
        img_w, img_h = img.size
    print("image width: " + str(img_w))
    print("image height: " + str(img_h))
    print("box x: " + str(BOX_X))
    print("box w: " + str(BOX_W))
    xc = (BOX_X + BOX_X + BOX_W) / 2 / img_w
    yc = (BOX_Y + BOX_Y + BOX_H) / 2 / img_h
    bw = BOX_W / img_w
    bh = BOX_H / img_h

    label_line = f"0 {xc:.4f} {yc:.4f} {bw:.4f} {bh:.4f}\n"
    label_path = os.path.join(
        OUTPUT_DIR,
        "labels/train",
        os.path.splitext(os.path.basename(img_path))[0] + ".txt"
    )
    with open(label_path, "w") as f:
        f.write(label_line)

    print(f"Labeled {img_path} → {label_path} | {label_line.strip()}")

print("Auto-labeling done!")