import cv2
import os

img_dir = "progress_yolo_dataset/images/train"
lbl_dir = "progress_yolo_dataset/labels/train"

for fname in os.listdir(img_dir):
    if fname.endswith('.png') or fname.endswith('.jpg'):
        img_path = os.path.join(img_dir, fname)
        lbl_path = os.path.join(lbl_dir, os.path.splitext(fname)[0] + ".txt")
        img = cv2.imread(img_path)
        h, w = img.shape[:2]
        if os.path.exists(lbl_path):
            with open(lbl_path) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        cls, xc, yc, bw, bh = map(float, parts)
                        x1 = int((xc - bw / 2) * w)
                        y1 = int((yc - bh / 2) * h)
                        x2 = int((xc + bw / 2) * w)
                        y2 = int((yc + bh / 2) * h)
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.imshow("Label check", img)
            cv2.waitKey(0)
cv2.destroyAllWindows()