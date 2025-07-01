import sys
import os
import json
import random
import openai
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QComboBox, QCheckBox, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize


openai.api_key = "INSERT_YOUR_API_KEY_HERE"

class PromptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRAUMA Prompt Generator")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #222; color: white; font-size: 16px;")
        
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # === Logo ===
        logo_label = QLabel()
        pixmap = QPixmap("logo_prompt_generator.png").scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label)

        # === Selettore mondo ===
        world_label = QLabel("Scegli il Mondo")
        self.version_selector = QComboBox()
        

# Carica dinamicamente i file JSON nella cartella JSON_DATA
        self.json_folder = "JSON_DATA"
        self.available_versions = [f[:-5] for f in os.listdir(self.json_folder) if f.endswith(".json")]
        self.version_selector.addItems(self.available_versions)
        self.version_selector.currentIndexChanged.connect(self.update_intensity_combo)
        left_layout.addWidget(world_label)
        left_layout.addWidget(self.version_selector)

        # === Intensità Horror/Magia ===
        self.intensity_label = QLabel("Horror/Magic Intensity:")
        self.intensity_combo = QComboBox()
        self.intensity_combo.addItem("None")
        left_layout.addWidget(self.intensity_label)
        left_layout.addWidget(self.intensity_combo)

        # === Checkbox GPT ===
        self.use_gpt = QCheckBox("Enhance prompt using OpenAI")
        self.use_gpt.setChecked(True)
        left_layout.addWidget(self.use_gpt)

        # Pulsanti
        button_layout = QHBoxLayout()
        
        # === Pulsanti personalizzati ===
        self.generate_button = QPushButton()
        self.generate_button.setIcon(QIcon("genera.png"))
        self.generate_button.setIconSize(QSize(300, 207))
        self.generate_button.setStyleSheet("""
    QPushButton {
        border: 2px solid #ff0000;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 10);
    }
    QPushButton:hover {
        background-color: rgba(255, 50, 50, 50);
    }
    QPushButton:pressed {
        background-color: rgba(100, 0, 0, 100);
    }
""")
        self.generate_button.clicked.connect(self.generate_prompt)
        button_layout.addWidget(self.generate_button)
        
        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon("copia.png"))
        self.copy_button.setIconSize(QSize(150, 150))
        self.generate_button.setStyleSheet("""
    QPushButton {
        border: 2px solid #ff0000;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 10);
    }
    QPushButton:hover {
        background-color: rgba(255, 50, 50, 50);
    }
    QPushButton:pressed {
        background-color: rgba(100, 0, 0, 100);
    }
""")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)

        left_layout.addSpacing(20)
        left_layout.addWidget(self.generate_button)
        left_layout.addWidget(self.copy_button)
        left_layout.addStretch()

        # === Output Prompt ===
        self.output_label = QLabel("Prompt Generato")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #111; color: white; font-size: 16px;")

        right_layout.addWidget(self.output_label)
        right_layout.addWidget(self.output)

        # Eventi
        self.generate_button.clicked.connect(self.generate_prompt)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Unione layout
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 5)
        self.setLayout(main_layout)

    def load_data(self, version):
        path = os.path.join(self.json_folder, f"{version}.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
        path = files.get(version)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_intensity_combo(self):
        version = self.version_selector.currentText()
        data = self.load_data(version)
        self.intensity_combo.clear()
        self.intensity_combo.addItem("None")
        if "HORROR_INTENSITY" in data and isinstance(data["HORROR_INTENSITY"], dict):
            self.intensity_combo.addItems(data["HORROR_INTENSITY"].keys())

    def generate_prompt(self):
        version = self.version_selector.currentText()
        data = self.load_data(version)

        epoca = random.choice(data["EPOCHS"])
        outfit = random.choice(data["OUTFITS"])
        luce = random.choice(data["LIGHTING"])
        sfondo = random.choice(data["BACKGROUNDS"])
        oggetto = random.choice(data["OBJECTS"])
        posa = random.choice(data.get("POSES", [""]))
        espressione = random.choice(data.get("EXPRESSIONS", [""]))
        angolazione = random.choice(data.get("CAMERA_ANGLES", [""]))
        atmosfera = random.choice(data.get("ATMOSPHERES", [""]))
        accessorio = random.choice(data.get("ACCESSORIES", [""]))
        intensita = self.intensity_combo.currentText()
        horror_descr = data.get("HORROR_INTENSITY", {}).get(intensita, "")

        base_prompt = (
            f"A beautiful woman from the {epoca} era, wearing {outfit}, {luce}, set in {sfondo}, "
            f"with {oggetto}, {posa}, {espressione}, {angolazione}, {atmosfera}, {accessorio}."
        )

        if intensita != "None":
            base_prompt += f" {horror_descr}"

        if self.use_gpt.isChecked():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert at enhancing visual descriptions for image generation."},
                        {"role": "user", "content": f"Enhance this prompt with detailed and imaginative language: {base_prompt}"}
                    ]
                )
                prompt = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                prompt = f"OpenAI Error: {e}"
        else:
            prompt = base_prompt

        self.output.setText(prompt)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptApp()
    window.show()
    sys.exit(app.exec_())
