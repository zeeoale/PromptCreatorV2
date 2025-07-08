import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import base64

class PromptHistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prompt History - Dante Archives")
        self.setStyleSheet("background-color: #222; color: white; font-size: 16px;")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Consolas", 11))
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        self.copy_button = QPushButton("Copy Selected Prompt")
        self.clear_button = QPushButton("Clear History")
        self.export_button = QPushButton("Export to HTML")

        for btn in (self.copy_button, self.clear_button, self.export_button):
            btn.setStyleSheet("background-color: #444; color: red; font-weight: bold; padding: 6px;")
            btn.setCursor(Qt.PointingHandCursor)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_history()

        self.copy_button.clicked.connect(self.copy_selected_prompt)
        self.clear_button.clicked.connect(self.clear_history)
        self.export_button.clicked.connect(self.export_to_html)

    def load_history(self):
        if os.path.exists("prompt_history.txt"):
            with open("prompt_history.txt", "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())

    def copy_selected_prompt(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText().strip()
        if selected_text:
            QApplication.clipboard().setText(selected_text)

    def clear_history(self):
        if os.path.exists("prompt_history.txt"):
            with open("prompt_history.txt", "w", encoding="utf-8") as f:
                f.write("")
        self.text_edit.clear()
    from PyQt5.QtWidgets import QFileDialog  # assicurati che sia importato

    def export_to_html(self):
        try:
            with open("prompt_history.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()

            with open("assets/dante_pixel_approve.webp", "rb") as img_file:
                encoded_img = base64.b64encode(img_file.read()).decode("utf-8")

            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Dante Prompt Archive</title>
                <style>
                    body {
                        background-color: #111;
                        color: #f0f0f0;
                        font-family: Consolas, monospace;
                        padding: 20px;
                    }
                    .header {
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        color: #ffae00;
                    }
                    .separator {
                        margin: 20px 0;
                        border-top: 1px dashed #555;
                    }
                    .prompt-block {
                        margin-bottom: 20px;
                    }
                    img {
                        display: block;
                        margin: 20px auto;
                        width: auto;
                        height: 180px;
                    }
                </style>
            </head>
            <body>
                <div class="header">📜 Dante Prompt Archive</div>
                <img src="data:image/webp;base64,%s" alt="Dante Pixel Approves">
                <div class="separator"></div>
            """ % encoded_img

            current_block = ""
            for line in lines:
                if line.strip():
                    current_block += line
                else:
                    if current_block.strip():
                        html_content += f"<div class='prompt-block'><pre>{current_block.strip()}</pre></div>\n"
                        html_content += "<div class='separator'></div>\n"
                        current_block = ""

            if current_block.strip():
                html_content += f"<div class='prompt-block'><pre>{current_block.strip()}</pre></div>\n"

            html_content += "</body></html>"

            # === Finestra per scegliere dove salvare ===
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save HTML File",
                "prompt_history_export.html",
                "HTML Files (*.html);;All Files (*)",
                options=options
            )

            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                QMessageBox.information(self, "Export Complete", f"Prompt history exported to:\n{filename}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"An error occurred while exporting:\n{str(e)}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PromptHistoryWindow()
    viewer.show()
    sys.exit(app.exec_())
