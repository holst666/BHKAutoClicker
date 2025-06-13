import time
import pyautogui
import win32gui
from image_detect import detect_object_in_window

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
            window_title="Clicker Heroes",
            template_path="templates/progress_stopped.png",
            confidence_threshold=0.98,
            debug_save_path="auto_progress_debug.png"
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