import time
import pyautogui

def click_loop(app_state):
    print("[AutoClick] Thread started.")
    while app_state["running"] and app_state["auto_clicking_enabled"]:
        if app_state.get("auto_click_point") is not None:
            if not app_state["pause_event"].is_set():
                x, y = app_state["auto_click_point"]
                pyautogui.click(x, y)
        time.sleep(app_state.get("auto_click_interval", 0.001))
    print("[AutoClick] Thread stopped.")