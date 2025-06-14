import os
from glob import glob

# --- SETTINGS ---
IMAGE_DIR = "progress_yolo_dataset/images/train"     # folder with your images
LABEL_DIR = "progress_yolo_dataset/labels/train"     # where YOLO expects labels

# Make sure label directory exists
os.makedirs(LABEL_DIR, exist_ok=True)

# Find all image files (jpg/png)
img_files = glob(os.path.join(IMAGE_DIR, "*.jpg")) + glob(os.path.join(IMAGE_DIR, "*.png"))
print(f"Found {len(img_files)} images.")

count = 0
for img_path in img_files:
    base = os.path.splitext(os.path.basename(img_path))[0]
    label_path = os.path.join(LABEL_DIR, base + ".txt")
    # Only create label if it does not exist or is empty
    if not os.path.exists(label_path) or os.stat(label_path).st_size == 0:
        with open(label_path, "w") as f:
            pass  # Write nothing: leave file empty
        print(f"Created empty label: {label_path}")
        count += 1
    else:
        print(f"Label already exists: {label_path}")

print(f"Done! {count} empty label files created.")