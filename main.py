import sys
import threading
import os
import signal
from PyQt5.QtWidgets import QApplication
from daemon import clipboard_listener
from hotkey import listen_for_hotkey
from gui import ClipboardUI # Import the PyQt5 window

PID_FILE = "/tmp/clipboard_manager.pid"

def cleanup_and_exit():
    """Remove PID file and exit the application."""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    sys.exit(0)

def run_gui():
    """Start the PyQt5 GUI."""
    app = QApplication(sys.argv)
    window = ClipboardUI()

    # ✅ Ensure PID file is deleted when window is closed
    def close_event():
        cleanup_and_exit()

    window.closeEvent = lambda event: close_event()  # Override close event
    window.show()

    # ✅ Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    print("Starting clipboard manager...")

    # ✅ Create a PID file
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # ✅ Handle termination signals
    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup_and_exit())
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup_and_exit())

    # ✅ Start clipboard listener in a separate thread
    threading.Thread(target=clipboard_listener, daemon=True).start()

    # ✅ Start GUI in the main thread
    run_gui()

    # ✅ Now listen for the hotkey after the GUI starts
    listen_for_hotkey()
