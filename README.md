# Clipboard Manager for Linux

A simple clipboard manager for Linux that runs in the background, supports hotkeys, and logs clipboard history.

## Features
- Runs as a background daemon
- Listens for a hotkey (`Win + Alt` by default) to manage clipboard history
- Logs clipboard data for easy retrieval
- Uses Python with a virtual environment
- Automatically starts at system boot using `systemd`

## Installation

### 1️⃣ Clone the Repository
```bash
cd ~/Documents
git clone <your-repo-url> clipboard
cd clipboard
```

### 2️⃣ Set Up the Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Make the Scripts Executable
```bash
chmod +x start_clipboard_manager.sh
touch ~/.clipboard_manager_logs/debug.log
```

### 4️⃣ Configure Systemd to Run at Startup

Create a `systemd` service:
```bash
sudo nano /etc/systemd/system/clipboard.service
```

Add the following content:
```ini
[Unit]
Description=Clipboard Manager Startup
After=network.target

[Service]
User=shivam
WorkingDirectory=/home/shivam/Documents/clipboard
ExecStart=/bin/bash /home/shivam/Documents/clipboard/start_clipboard_manager.sh
Restart=always
RestartSec=5s
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/shivam/.Xauthority"

[Install]
WantedBy=default.target
```

### 5️⃣ Enable & Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable clipboard.service
sudo systemctl start clipboard.service
```

## Usage
The clipboard manager will run automatically at startup. You can manually start or stop it using:
```bash
systemctl start clipboard.service
systemctl stop clipboard.service
systemctl restart clipboard.service
systemctl status clipboard.service
```

## Debugging
If the service is not working, check logs:
```bash
tail -f ~/.clipboard_manager_logs/debug.log
journalctl -u clipboard.service --no-pager --lines=50
```

## Uninstallation
To remove the clipboard manager:
```bash
sudo systemctl stop clipboard.service
sudo systemctl disable clipboard.service
sudo rm /etc/systemd/system/clipboard.service
rm -rf ~/Documents/clipboard ~/.clipboard_manager_logs
```

## License
MIT License

