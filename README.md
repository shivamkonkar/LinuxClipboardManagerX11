LinuxClipboardManagerX11

📌 About

LinuxClipboardManagerX11 is a simple yet powerful clipboard manager for Linux, built using Python and PyQt5. It provides clipboard history management with a user-friendly GUI and global hotkey support (Win+V). The project is optimized for X11, ensuring smooth operation with NVIDIA GPUs and better clipboard access.

🚧 Work in Progress 🚧
This project is still under development, and features will be added progressively.

✨ Features

Clipboard history management

Global hotkey support (Win+V) using pynput

PyQt5 GUI for a modern and professional look

Background daemon process for clipboard monitoring

Works on Linux Mint Cinnamon 22.1 “Xia” and other X11-based Linux distributions

📦 Installation

1️⃣ Install dependencies

sudo apt update && sudo apt install xclip -y
pip3 install PyQt5 pynput daemonize

2️⃣ Clone the repository

git clone https://github.com/shivamkonkar/LinuxClipboardManagerX11.git
cd LinuxClipboardManagerX11

3️⃣ Run the Clipboard Manager

python3 main.py

🛠️ Technologies Used

Python 3.12

PyQt5 (for GUI)

pynput (for global hotkeys)

daemonize (for running in the background)

xclip (for clipboard access in X11)

⚠️ Notes on X11 vs Wayland

X11 is chosen for better NVIDIA GPU support, clipboard access, and global hotkeys

Wayland limitations:

Clipboard persistence issues

Strict security restrictions on global hotkeys

Inconsistent NVIDIA driver support

🤝 Contributing

Contributions are welcome! If you'd like to improve the project, feel free to open an issue or submit a pull request.
