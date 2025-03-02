#!/bin/bash

# Define script locations
VENV_PATH="$HOME/Documents/clipboard/myenv"  # Use 'myenv' instead of 'venv'
DAEMON_SCRIPT="$HOME/Documents/clipboard/daemon.py"
HOTKEY_SCRIPT="$HOME/Documents/clipboard/hotkey.py"
LOG_DIR="$HOME/.clipboard_manager_logs"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run daemon.py in the background
nohup python3 "$DAEMON_SCRIPT" > "$LOG_DIR/daemon.log" 2>&1 &

# Run hotkey.py in the background
nohup python3 "$HOTKEY_SCRIPT" > "$LOG_DIR/hotkey.log" 2>&1 &

echo "Clipboard Manager started successfully."


