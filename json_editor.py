import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QFileDialog, QMessageBox, QListWidgetItem, QDialog, QLineEdit, QTextEdit,QInputDialog
)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
import sys

TEMPLATE_JSON = {
    "EPOCHS": [],
    "STYLES": [],
    "OUTFITS": [],
    "OBJECTS": [],
    "LIGHTINGS": [],
    "COLORS": [],
    "LOCATIONS": [],
    "ATMOSPHERE": [],
    "CAMERA_ANGLES": [],
    "POSES": [],
    "EXPRESSIONS": [],
    "HORROR_INTENSITY": {}
}

class EditDialog(QDialog):
    def __init__(self, key, values, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit: {key}")
        self.setStyleSheet("background-color: #333; color: white; font-size: 16px;")
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setText("\n".join(values))
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_values(self):
        return [line.strip() for line in self.text_edit.toPlainText().split("\n") if line.strip()]

class JSONEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prompt JSON Editor")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #222; color: white; font-size: 16px;")

        self.folder = "./JSON_DATA"
        os.makedirs(self.folder, exist_ok=True)

        layout = QVBoxLayout()
        self.json_list = QListWidget()
        self.json_list.itemClicked.connect(self.load_json_keys)
        layout.addWidget(QLabel("Select JSON File:"))
        layout.addWidget(self.json_list)

        self.key_list = QListWidget()
        self.key_list.itemClicked.connect(self.edit_key)
        layout.addWidget(QLabel("Edit Keys:"))
        layout.addWidget(self.key_list)

        button_layout = QHBoxLayout()

        load_button = QPushButton("Reload JSONs")
        load_button.clicked.connect(self.load_json_files)
        button_layout.addWidget(load_button)

        new_button = QPushButton("New JSON")
        new_button.clicked.connect(self.create_new_json)
        button_layout.addWidget(new_button)

        rename_button = QPushButton("Rename JSON")
        rename_button.clicked.connect(self.rename_json)
        button_layout.addWidget(rename_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.current_json_file = None
        self.current_data = {}
        self.load_json_files()

    def load_json_files(self):
        self.json_list.clear()
        for file in os.listdir(self.folder):
            if file.endswith(".json"):
                self.json_list.addItem(file)

    def load_json_keys(self, item):
        filename = item.text()
        self.current_json_file = os.path.join(self.folder, filename)
        try:
            with open(self.current_json_file, "r", encoding="utf-8") as f:
                self.current_data = json.load(f)
            self.key_list.clear()
            for key in self.current_data:
                self.key_list.addItem(key)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load file: {e}")

    def edit_key(self, item):
        key = item.text()
        if isinstance(self.current_data.get(key), list):
            dialog = EditDialog(key, self.current_data[key], self)
            if dialog.exec_():
                self.current_data[key] = dialog.get_values()
                with open(self.current_json_file, "w", encoding="utf-8") as f:
                    json.dump(self.current_data, f, indent=2, ensure_ascii=False)

    def create_new_json(self):
        filename, ok = QInputDialog.getText(self, "New JSON File", "Enter filename (without .json):")
        if ok and filename:
            full_path = os.path.join(self.folder, f"{filename}.json")
            if os.path.exists(full_path):
                QMessageBox.warning(self, "File Exists", "A file with this name already exists.")
                return
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(TEMPLATE_JSON, f, indent=2, ensure_ascii=False)
            self.load_json_files()

    def rename_json(self):
        if not self.current_json_file:
            QMessageBox.warning(self, "No File Selected", "Please select a JSON file first.")
            return
        new_name, ok = QInputDialog.getText(self, "Rename JSON File", "Enter new name (without .json):")
        if ok and new_name:
            new_path = os.path.join(self.folder, f"{new_name}.json")
            if os.path.exists(new_path):
                QMessageBox.warning(self, "File Exists", "A file with this name already exists.")
                return
            os.rename(self.current_json_file, new_path)
            self.load_json_files()
            self.current_json_file = None
            self.key_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = JSONEditor()
    editor.show()
    sys.exit(app.exec_())
