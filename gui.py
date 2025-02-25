from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget
from PyQt5.QtCore import Qt
import sqlite3
import sys

class ClipboardHistory(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Remove window border
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowTitle("Clipboard History")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        self.load_history()

        self.setLayout(layout)

    def load_history(self):
        conn = sqlite3.connect("clipboard.db")
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM history ORDER BY timestamp DESC LIMIT 10")
        
        for row in cursor.fetchall():
            self.history_list.addItem(row[0])

        conn.close()

    # ✅ Allow ESC key to close the window
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window on ESC key press
        else:
            super().keyPressEvent(event)

# ✅ Fix QApplication issue and avoid segmentation faults
def show_history():
    app = QApplication.instance()  # Check if an instance already exists
    if not app:  
        app = QApplication(sys.argv)

    window = ClipboardHistory()
    window.show()
    
    # ✅ Use `exec_()` only if the application is not running
    if not QApplication.instance().exec():
        sys.exit(app.exec_())
