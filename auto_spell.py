import pyautogui
import win32gui
import time

def auto_spell_loop(app_state):
    """Thread: cast spells every N seconds."""
    print("[AutoSpell] Thread started.")
    spell_keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    while app_state["running"] and app_state["auto_cast_enabled"]:
        hwnd = win32gui.FindWindow(None, "Clicker Heroes")
        if hwnd:
            try:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.1)
                for k in spell_keys:
                    pyautogui.press(k)
                print("[AutoSpell] Spells cast!")
            except Exception as e:
                print("[AutoSpell] Could not set focus or cast:", e)
        else:
            print("[AutoSpell] Game window not found.")

        interval = app_state.get("auto_cast_interval", 7)
        for _ in range(int(interval)):
            if not app_state["auto_cast_enabled"] or not app_state["running"]:
                print("[AutoSpell] Stopped.")
                return
            time.sleep(1)
    print("[AutoSpell] Thread stopped.")
