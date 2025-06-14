import time
import pyautogui
import win32gui
from image_detect import detect_object_in_window
from util import resource_path

MODEL_PATH = resource_path("model\progress.pt")
CONFIDENCE = 0.85
WINDOW_TITLE = "Clicker Heroes"


def auto_progress_loop(app_state, timer_var):
    """Run in a thread: scans, waits, presses 'a' if object found."""
    print("[AutoProgress] Thread started.")
    while app_state["running"] and app_state["auto_progress_enabled"]:
        # Only scan every 10 seconds
        for _ in range(10):
            if not app_state["auto_progress_enabled"] or not app_state["running"]:
                print("[AutoProgress] Stopped or disabled.")
                return
            time.sleep(1)
        # Scan for template
        found, confidence, loc = detect_object_in_window(
            window_title=WINDOW_TITLE,
            model_path=MODEL_PATH,
            confidence_threshold=CONFIDENCE
        )
        print(f"[AutoProgress] Detected={found}, Confidence={confidence:.3f}")
        if found:
            try:
                minutes = float(timer_var.get())
            except Exception:
                minutes = 5
            seconds = max(1, int(minutes * 60))
            print(f"[AutoProgress] Found! Waiting {seconds}s, then pressing 'a'.")
            for _ in range(seconds):
                if not app_state["auto_progress_enabled"] or not app_state["running"]:
                    return
                time.sleep(1)
            hwnd = win32gui.FindWindow(None, "Clicker Heroes")
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.2)
            pyautogui.press("a")
            print("[AutoProgress] Pressed 'a'.")
            for _ in range(5):
                if not app_state["auto_progress_enabled"] or not app_state["running"]:
                    return
                time.sleep(1)
    print("[AutoProgress] Thread stopped.")