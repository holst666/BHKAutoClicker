import time
import pyautogui

def auto_level_loop(app_state):
    print("[AutoLevel] Thread started.")
    while app_state["running"] and app_state["auto_level_enabled"]:
        interval = app_state.get("auto_level_interval", 10.0)
        point = app_state.get("auto_level_point")
        if point is None:
            print("[AutoLevel] No point set, skipping.")
            time.sleep(1)
            continue

        # Wait for the interval
        for _ in range(int(interval * 10)):
            if not app_state["running"] or not app_state["auto_level_enabled"]:
                print("[AutoLevel] Stopped early.")
                return
            time.sleep(0.1)

        # Pause auto clicking (via event)
        app_state["pause_event"].set()
        print("[AutoLevel] Paused auto clicking.")

        # Click at the auto level point
        x, y = point
        pyautogui.click(x, y)
        print(f"[AutoLevel] Clicked at ({x},{y})")

        # Short delay to ensure click is delivered
        time.sleep(0.2)

        # Resume auto clicking
        app_state["pause_event"].clear()
        print("[AutoLevel] Resumed auto clicking.")

    print("[AutoLevel] Thread stopped.")
