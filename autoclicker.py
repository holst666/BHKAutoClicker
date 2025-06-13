import tkinter as tk
import threading
import keyboard
import pyautogui
import settings
from auto_progress import auto_progress_loop
from auto_click import click_loop
from tkinter import messagebox
from pick_point import pick_point
from auto_level import auto_level_loop
from auto_spell import auto_spell_loop
from fish_detect import detect_fish_loop

VERSION = 0.2

raw_settings = settings.load_settings()

app_state = {
    "running": False,
    "pause_event": threading.Event(),
    "auto_clicking_enabled": settings.getint(raw_settings, "auto_clicking", 1) == 1,
    "auto_click_interval": settings.getfloat(raw_settings, "auto_click_interval", 0.001),
    "auto_click_point": settings.getpoint(raw_settings, "click_point_x", "click_point_y"),
    "auto_level_enabled": settings.getint(raw_settings, "auto_level", 0) == 1,
    "auto_level_interval": settings.getfloat(raw_settings, "auto_level_freq", 10),
    "auto_level_point": settings.getpoint(raw_settings, "level_point_x", "level_point_y"),
    "fish_detect_enabled": settings.getint(raw_settings, "fish_clicking", 0) == 1,
    "auto_cast_enabled": settings.getint(raw_settings, "auto_cast_spells", 0) == 1,
    "auto_cast_interval": settings.getfloat(raw_settings, "auto_cast_freq", 7),
    "auto_progress_enabled": settings.getint(raw_settings, "auto_progress", 0) == 1,
    "debug_mode": settings.getint(raw_settings, "debug", 0) == 1,
    "window_x": settings.getint(raw_settings, "window_x", 0),
    "window_y": settings.getint(raw_settings, "window_y", 0),
    "window_w": settings.getint(raw_settings, "window_w", 800),
    "window_h": settings.getint(raw_settings, "window_h", 600),
}

def gather_settings():
    return {
        "auto_clicking": "1" if auto_click_var.get() else "0",
        "auto_click_interval": str(auto_click_interval.get()),
        "click_point_x": str(app_state["auto_click_point"][0]) if app_state["auto_click_point"] else "",
        "click_point_y": str(app_state["auto_click_point"][1]) if app_state["auto_click_point"] else "",
        "auto_level": "1" if auto_level_var.get() else "0",
        "auto_level_freq": str(auto_level_interval.get()),
        "level_point_x": str(app_state["auto_level_point"][0]) if app_state["auto_level_point"] else "",
        "level_point_y": str(app_state["auto_level_point"][1]) if app_state["auto_level_point"] else "",
        "fish_clicking": "1" if fish_detect_var.get() else "0",
        "auto_cast_spells": "1" if auto_cast_var.get() else "0",
        "auto_cast_freq": str(app_state.get("auto_cast_interval", 7)),
        "auto_progress": "1" if auto_progress_var.get() else "0"
        # add any others you want to save...
    }

def on_close():
    app_state["clicking"] = False
    import settings
    settings.save_settings(gather_settings())
    root.destroy()

def start_all():
    if app_state["running"]:
        return
    app_state["running"] = True

    # Start threads if enabled
    if app_state["auto_clicking_enabled"]:
        threading.Thread(target=click_loop, args=(app_state,), daemon=True).start()
    if app_state["auto_level_enabled"]:
        threading.Thread(target=auto_level_loop, args=(app_state,), daemon=True).start()
    if app_state["auto_cast_enabled"]:
        threading.Thread(target=auto_spell_loop, args=(app_state,), daemon=True).start()
    if app_state["auto_progress_enabled"]:
        threading.Thread(target=auto_progress_loop, args=(app_state, auto_progress_timer_var), daemon=True).start()
    if app_state["fish_detect_enabled"]:
        threading.Thread(target=detect_fish_loop, args=(app_state,), daemon=True).start()

    start_btn.config(text="STOP")


def updateVars():
    app_state["auto_clicking_enabled"] = auto_click_var.get()
    try:
        app_state["auto_click_interval"] = float(auto_click_interval.get())
    except Exception:
        app_state["auto_click_interval"] = 0.001

    app_state["auto_level_enabled"] = auto_level_var.get()
    try:
        app_state["auto_level_interval"] = float(auto_level_interval.get())
    except Exception:
        app_state["auto_level_interval"] = 10

    app_state["fish_detect_enabled"] = fish_detect_var.get()
    app_state["auto_cast_enabled"] = auto_cast_var.get()
    try:
        app_state["auto_cast_interval"] = float(auto_cast_interval.get())
    except Exception:
        app_state["auto_cast_interval"] = 7

    app_state["auto_progress_enabled"] = auto_progress_var.get()
    try:
        app_state["auto_progress_timer"] = float(auto_progress_timer_var.get())
    except Exception:
        app_state["auto_progress_timer"] = 5
    


def stop_clicking():
    app_state["running"] = False
    start_btn.config(text="START")

def toggle_clicking():
    if app_state["running"]:
        stop_clicking()
    else:
        start_all()

def pick_auto_click_point():
    def set_point(x, y):
        app_state["auto_click_point"] = (x, y)
        auto_click_point_label.config(text=f"Click point: {x}, {y}")
    pick_point(set_point)

def pick_auto_level_point():
    def set_point(x, y):
        app_state["auto_level_point"] = (x, y)
        auto_level_point_label.config(text=f"Level point: {x}, {y}")
    pick_point(set_point)

def pick_point_and_start():
    # Instantly get current mouse cursor position and use as click point
    x, y = pyautogui.position()
    app_state["auto_click_point"] = (x, y)
    auto_click_point_label.config(text=f"Click point: {x}, {y}")
    start_all()

# ---- LIVE SYNC: Callbacks for all checkboxes ----

def update_auto_click_var(*args):
    app_state["auto_clicking_enabled"] = auto_click_var.get()
def update_auto_level_var(*args):
    app_state["auto_level_enabled"] = auto_level_var.get()
def update_fish_detect_var(*args):
    app_state["fish_detect_enabled"] = fish_detect_var.get()
def update_auto_cast_var(*args):
    app_state["auto_cast_enabled"] = auto_cast_var.get()
def update_auto_progress_var(*args):
    app_state["auto_progress_enabled"] = auto_progress_var.get()

def update_auto_click_interval(event=None):
    try:
        app_state["auto_click_interval"] = float(auto_click_interval.get())
    except Exception:
        app_state["auto_click_interval"] = 0.001

def update_auto_level_interval(event=None):
    try:
        app_state["auto_level_interval"] = float(auto_level_interval.get())
    except Exception:
        app_state["auto_level_interval"] = 10.0

# ---- GUI Setup ----
root = tk.Tk()
root.title("Martins clicker hacks")
root.geometry(f"{app_state['window_w']}x{app_state['window_h']}")
root.resizable(True, True)
if app_state["window_x"] and app_state["window_y"]:
    root.geometry(f"+{app_state['window_x']}+{app_state['window_y']}")

# Header
header_text = "Martins clicker hacks"
header = tk.Label(root, text=header_text, font=("Arial Black", 28), fg="#1976d2")
header.pack(pady=(25, 20))

# Outer frame to center the grid
outer = tk.Frame(root)
outer.pack(expand=True)

# The grid itself
main = tk.Frame(outer)
main.pack()

# Column 1 (left)
col1 = tk.Frame(main)
col1.grid(row=0, column=0, padx=(0,40), sticky="e")

auto_click_var = tk.BooleanVar(value=app_state["auto_clicking_enabled"])
tk.Checkbutton(col1, text="Auto Clicking", font=("Arial", 13), variable=auto_click_var).pack(anchor="w")
tk.Label(col1, text="Interval (sec):", font=("Arial", 10)).pack(anchor="w")
auto_click_interval = tk.Entry(col1, width=10, font=("Arial", 11))
auto_click_interval.insert(0, str(app_state["auto_click_interval"]))
auto_click_interval.pack(pady=(0, 6), anchor="w")

pick_auto_click_btn = tk.Button(col1, text="Pick Auto Click Point", command=pick_auto_click_point)
pick_auto_click_btn.pack(anchor="w")

auto_click_point_str = (
    f"{app_state['auto_click_point'][0]}, {app_state['auto_click_point'][1]}"
    if app_state["auto_click_point"] else "Not set"
)
auto_click_point_label = tk.Label(col1, text=f"Click point: {auto_click_point_str}", font=("Arial", 10), fg="#1976d2")
auto_click_point_label.pack(anchor="w", pady=(2,15))

auto_level_var = tk.BooleanVar(value=app_state["auto_level_enabled"])
tk.Checkbutton(col1, text="Auto Level Click", font=("Arial", 13), variable=auto_level_var).pack(anchor="w")
tk.Label(col1, text="Interval (sec):", font=("Arial", 10)).pack(anchor="w")
auto_level_interval = tk.Entry(col1, width=10, font=("Arial", 11))
auto_level_interval.insert(0, str(app_state["auto_level_interval"]))
auto_level_interval.pack(pady=(0, 6), anchor="w")

pick_auto_level_btn = tk.Button(col1, text="Pick Auto Level Point", command=pick_auto_level_point)
pick_auto_level_btn.pack(anchor="w")

auto_level_point_str = (
    f"{app_state['auto_level_point'][0]}, {app_state['auto_level_point'][1]}"
    if app_state["auto_level_point"] else "Not set"
)
auto_level_point_label = tk.Label(col1, text=f"Level point: {auto_level_point_str}", font=("Arial", 10), fg="#1976d2")
auto_level_point_label.pack(anchor="w")

# Column 2 (right)
col2 = tk.Frame(main)
col2.grid(row=0, column=1, sticky="w")

fish_detect_var = tk.BooleanVar(value=app_state["fish_detect_enabled"])
tk.Checkbutton(col2, text="Fish Clicking", font=("Arial", 13), variable=fish_detect_var).pack(anchor="w", pady=(0, 8))

auto_cast_var = tk.BooleanVar(value=app_state["auto_cast_enabled"])
tk.Checkbutton(col2, text="Auto Cast Spells", font=("Arial", 13), variable=auto_cast_var).pack(anchor="w", pady=(0, 8))

# Big Start button, centered under grid
start_btn = tk.Button(root, text="START", font=("Arial Black", 20), bg="#1976d2", fg="white",
                      width=22, height=2, command=toggle_clicking, relief="flat")
start_btn.pack(pady=(30, 10))

auto_progress_var = tk.BooleanVar(value=app_state["auto_progress_enabled"])
tk.Checkbutton(col2, text="Auto Progress", font=("Arial", 13), variable=auto_progress_var).pack(anchor="w", pady=(0, 8))
tk.Label(col2, text="Auto Progress Timer (min):", font=("Arial", 10)).pack(anchor="w")
auto_progress_timer_var = tk.Entry(col2, width=10, font=("Arial", 11))
auto_progress_timer_var.insert(0, str(app_state.get("auto_progress_timer", 5)))
auto_progress_timer_var.pack(pady=(0, 8), anchor="w")



# Shortcut info
shortcut_frame = tk.Frame(root)
shortcut_frame.pack(pady=(0,12))
tk.Label(shortcut_frame, text="F6: Start/Stop", font=("Arial", 11, "bold"), fg="#1976d2").pack(side="left", padx=14)
tk.Label(shortcut_frame, text="F7: Pick Auto Click Point & Start", font=("Arial", 11, "bold"), fg="#1976d2").pack(side="left", padx=14)

# Version
version_label = tk.Label(root, text=VERSION, font=("Arial", 10), fg="#1976d2")
version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

# --- Live Sync: Attach variable traces and entry <FocusOut> events ---
auto_click_var.trace_add("write", update_auto_click_var)
auto_level_var.trace_add("write", update_auto_level_var)
fish_detect_var.trace_add("write", update_fish_detect_var)
auto_cast_var.trace_add("write", update_auto_cast_var)
auto_progress_var.trace_add("write", update_auto_progress_var)

auto_click_interval.bind("<FocusOut>", update_auto_click_interval)
auto_level_interval.bind("<FocusOut>", update_auto_level_interval)

# --- Keyboard shortcuts ---
keyboard.add_hotkey('F6', toggle_clicking)
keyboard.add_hotkey('F7', pick_point_and_start)

# Save window geometry and settings on close
def on_close_with_window_save():
    # Save window position and size to settings
    x = root.winfo_x()
    y = root.winfo_y()
    w = root.winfo_width()
    h = root.winfo_height()
    s = gather_settings()
    s.update({
        "window_x": str(x),
        "window_y": str(y),
        "window_w": str(w),
        "window_h": str(h),
    })
    import settings
    settings.save_settings(s)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close_with_window_save)

root.mainloop()
