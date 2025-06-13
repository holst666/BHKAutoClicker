from pynput import mouse

def pick_point(callback=None):
    """Lets user pick a point with the mouse. Calls callback(x, y) with coordinates."""
    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            if callback:
                callback(x, y)
            return False
    listener = mouse.Listener(on_click=on_click)
    listener.start()