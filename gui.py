import os
import sys
import threading
import subprocess
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget,
    QPushButton, QListWidgetItem, QFrame
)
from PyQt5.QtCore import Qt, QSize

PID_FILE = "/tmp/clipboard_manager.pid"
DB_FILE = "clipboard.db"

class ClipboardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.init_ui()
        self.apply_styles()

    def setup_window(self):
        self.setWindowTitle("Clipboard Manager")
        self.setGeometry(100, 100, 380, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)

    def init_ui(self):
        layout = QVBoxLayout()
        self.clipboard_list = self.create_clipboard_list()
        layout.addWidget(self.clipboard_list)
        layout.addWidget(self.create_divider())
        clear_btn = self.create_button("Clear all", "clearBtn", (80, 30), self.clear_clipboard)
        layout.addWidget(clear_btn)
        self.setLayout(layout)
        self.load_history()

        if self.clipboard_list.count() > 0:
            self.clipboard_list.setCurrentRow(0)

    def create_button(self, text, object_name, size, callback=None):
        btn = QPushButton(text)
        btn.setObjectName(object_name)
        btn.setFixedSize(*size)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def create_clipboard_list(self):
        clipboard_list = QListWidget()
        clipboard_list.setObjectName("clipboardList")
        clipboard_list.itemClicked.connect(self.item_clicked)
        return clipboard_list

    def create_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def clear_clipboard(self):
        self.clipboard_list.clear()
        if os.path.exists(DB_FILE):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            conn.commit()
            conn.close()

    def load_history(self):
        if not os.path.exists(DB_FILE):
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM history ORDER BY timestamp DESC LIMIT 10")
        for row in cursor.fetchall():
            self.add_clipboard_item(row[0])
        conn.close()

    def add_clipboard_item(self, text):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignLeft)
        item.setSizeHint(QSize(340, 50))
        self.clipboard_list.addItem(item)

    def item_clicked(self, item):
        self.paste_content(item.text())

    def paste_content(self, text):
        if not all(map(self.is_tool_installed, ["xclip", "xdotool"])):
            print("Required dependencies (xclip, xdotool) are missing.")
            return
        
        self.hide()
        threading.Thread(target=self.paste_using_xdotool, args=(text,), daemon=True).start()
        self.cleanup_and_exit()

    def paste_using_xdotool(self, text):
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
            subprocess.run(["xdotool", "key", "--clearmodifiers", "ctrl+v"], check=True)
            print("Pasted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error while pasting: {e}")

    @staticmethod
    def is_tool_installed(tool):
        return subprocess.run(["which", tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0

    def keyPressEvent(self, event):
        key_actions = {
            Qt.Key_Return: self.paste_selected,
            Qt.Key_Enter: self.paste_selected,
            Qt.Key_Escape: self.cleanup_and_exit,
        }
        
        if event.key() in key_actions:
            key_actions[event.key()]()
        elif event.key() in (Qt.Key_Up, Qt.Key_Down):
            self.navigate_list(-1 if event.key() == Qt.Key_Up else 1)

    def navigate_list(self, direction):
        current_row = self.clipboard_list.currentRow()
        new_row = current_row + direction
        if 0 <= new_row < self.clipboard_list.count():
            self.clipboard_list.setCurrentRow(new_row)

    def paste_selected(self):
        selected_item = self.clipboard_list.currentItem()
        if selected_item:
            self.paste_content(selected_item.text())

    def focusOutEvent(self, event):
        self.cleanup_and_exit()
        super().focusOutEvent(event)

    def closeEvent(self, event):
        self.cleanup_and_exit()
        event.accept()

    def cleanup_and_exit(self):
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        QApplication.instance().quit()
        sys.exit(0)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #202124; color: #E8EAED; font-size: 14px; border-radius: 8px; }
            QPushButton { background-color: #303134; border-radius: 6px; padding: 8px; font-size: 16px; color: white; border: none; }
            QPushButton:hover { background-color: #3C4043; }
            QPushButton:pressed { background-color: #5F6368; }
            #clipboardList { background-color: #292A2D; border: none; padding: 6px; border-radius: 8px; }
            QListWidget::item { padding: 10px; border-radius: 6px; margin: 4px; background-color: #303134; font-size: 14px; }
            QListWidget::item:hover { background-color: #474A4F; }
            QListWidget::item:selected { border: 2px solid #4285F4; background-color: #3C4043; }
            #clearBtn { background-color: #303134; color: white; font-weight: bold; padding: 6px; border: 2px solid #4285F4;}
            #clearBtn:hover { background-color: #3C4043; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardUI()
    window.show()
    sys.exit(app.exec_())




