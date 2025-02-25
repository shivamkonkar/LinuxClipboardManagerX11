from pynput import keyboard
import subprocess
import os

PID_FILE = "/tmp/clipboard_manager.pid"

def is_already_running():
    """Check if the clipboard manager is already running using a PID file."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
        if pid and os.path.exists(f"/proc/{pid}"):  # Check if process is still active
            return True
    return False

def on_activate():
    print("Win + V pressed! Launching clipboard manager...")
    
    if is_already_running():
        print("Clipboard manager already running.")
        return
    
    # Run main.py in a separate process and store its PID
    process = subprocess.Popen(["python3", "main.py"])
    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

def listen_for_hotkey():
    print("Listening for Win + V...")
    with keyboard.GlobalHotKeys({'<cmd>+v': on_activate}) as hotkey:
        hotkey.join()

if __name__ == "__main__":
    listen_for_hotkey()


