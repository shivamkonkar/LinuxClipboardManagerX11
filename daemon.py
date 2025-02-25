import time
from clipboard import get_clipboard
from database import save_clipboard

def clipboard_listener():
    last_clipboard = ""
    while True:
        current_clipboard = get_clipboard()
        if current_clipboard and current_clipboard != last_clipboard:
            save_clipboard(current_clipboard)
            last_clipboard = current_clipboard
        time.sleep(1)

# Add this check to prevent auto-execution when imported
if __name__ == "__main__":
    clipboard_listener()
