from ultralytics import YOLO
import pygetwindow as gw
import mss
import cv2
import numpy as np

# === SETTINGS ===
MODEL_PATH = "model/progress4.pt"  # Update if needed
WINDOW_TITLE = "Clicker Heroes"
CONF_THRESHOLD = 0.1

# Load model
model = YOLO(MODEL_PATH)

# Find the game window
windows = gw.getWindowsWithTitle(WINDOW_TITLE)
if not windows:
    raise RuntimeError(f'No window found with title "{WINDOW_TITLE}"')
win = windows[0]
left, top, width, height = win.left, win.top, win.width, win.height

# Screenshot the game window
with mss.mss() as sct:
    monitor = {"left": left, "top": top, "width": width, "height": height}
    sct_img = sct.grab(monitor)
    img = np.array(sct_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

# Run YOLO detection
results = model(img)

# Draw results
for box in results[0].boxes:
    conf = float(box.conf.cpu().numpy())
    if conf < CONF_THRESHOLD:
        continue
    x1, y1, x2, y2 = [int(i) for i in box.xyxy[0].cpu().numpy()]
    cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
    cv2.putText(img, f"{conf:.2f}", (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

# Show the result
cv2.imshow("YOLO Detection - Clicker Heroes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
