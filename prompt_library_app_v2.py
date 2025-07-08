import sys
import os
import json
import random
import openai
import warnings
from datetime import datetime
import string
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QComboBox, QCheckBox, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup, QLineEdit
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QMovie
from prompt_history import PromptHistoryWindow
import requests

warnings.filterwarnings("ignore", category=DeprecationWarning)

class PromptConfigWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Prompt Settings")
        self.setGeometry(200, 200, 600, 200)
        self.setStyleSheet("background-color: #222; color: white; font-size: 16px;")

        self.parent = parent

        layout = QVBoxLayout()

        self.system_prompt_edit = QTextEdit(self)
        self.system_prompt_edit.setPlaceholderText("System Prompt")
        self.system_prompt_edit.setText(self.parent.system_prompt)
        layout.addWidget(QLabel("System Prompt:"))
        layout.addWidget(self.system_prompt_edit)

        self.user_prompt_edit = QTextEdit(self)
        self.user_prompt_edit.setPlaceholderText("User Prompt Template (use {prompt} as placeholder)")
        self.user_prompt_edit.setText(self.parent.user_prompt_template)
        layout.addWidget(QLabel("User Prompt Template:"))
        layout.addWidget(self.user_prompt_edit)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_prompts)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_prompts(self):
        self.parent.system_prompt = self.system_prompt_edit.toPlainText()
        self.parent.user_prompt_template = self.user_prompt_edit.toPlainText()
        self.close()

class PromptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("traumakom Prompt Generator v1.1.0")
        self.setWindowIcon(QIcon("assets/firma_trauma_logo.ico"))
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #222; color: white; font-size: 16px;")

        self.openai_api_key = ""
        self.system_prompt = "You are an expert at enhancing visual descriptions for image generation."
        self.user_prompt_template = "Enhance this prompt with detailed and imaginative language: {prompt}"
        self.load_openai_key()

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("assets/logo_prompt_generator.png").scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label)

        world_label = QLabel("Choose World")
        version_selector_layout = QHBoxLayout()
        self.version_selector = QComboBox()
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon("assets/refresh_icon.png"))
        self.refresh_button.setIconSize(QSize(24, 24))
        self.refresh_button.setFixedSize(32, 32)
        self.refresh_button.clicked.connect(self.refresh_json_files)
        version_selector_layout.addWidget(self.version_selector)
        version_selector_layout.addWidget(self.refresh_button)

        self.json_folder = "JSON_DATA"
        self.available_versions = [f[:-5] for f in os.listdir(self.json_folder) if f.endswith(".json")]
        self.version_selector.addItems(self.available_versions)
        self.version_selector.currentIndexChanged.connect(self.update_intensity_combo)

        left_layout.addWidget(world_label)
        left_layout.addLayout(version_selector_layout)

        self.intensity_label = QLabel("Horror/Magic Intensity:")
        self.intensity_combo = QComboBox()
        self.intensity_combo.addItem("None")
        left_layout.addWidget(self.intensity_label)
        left_layout.addWidget(self.intensity_combo)

        self.engine_label = QLabel("Prompt Engine:")
        self.radio_openai = QRadioButton("OpenAI")
        self.radio_ollama = QRadioButton("Ollama")
        self.radio_none = QRadioButton("No AI Enhance")
        self.radio_openai.setChecked(True)

        self.engine_group = QButtonGroup()
        self.engine_group.addButton(self.radio_openai)
        self.engine_group.addButton(self.radio_ollama)
        self.engine_group.addButton(self.radio_none)

        left_layout.addWidget(self.engine_label)
        left_layout.addWidget(self.radio_openai)
        left_layout.addWidget(self.radio_ollama)
        left_layout.addWidget(self.radio_none)

        self.generate_button = QPushButton()
        self.generate_button.setIcon(QIcon("assets/genera.png"))
        self.generate_button.setFixedHeight(105)
        self.generate_button.setIconSize(QSize(300, 207))
        self.generate_button.setStyleSheet("QPushButton { border-radius: 10px; background-color: rgba(255, 255, 255, 10); } QPushButton:hover { background-color: rgba(255, 50, 50, 50); } QPushButton:pressed { background-color: rgba(100, 0, 0, 100); }")
        self.generate_button.clicked.connect(self.generate_prompt)
        left_layout.addWidget(self.generate_button)

        self.history_button = QPushButton()
        self.history_button.setFixedHeight(50)
        self.history_button.setIcon(QIcon("assets/prompt_history.png"))
        self.history_button.setIconSize(QSize(300, 207))
        self.history_button.setFixedHeight(109)
        self.history_button.setStyleSheet(self.generate_button.styleSheet())
        self.history_button.clicked.connect(self.open_prompt_history)
        left_layout.addWidget(self.history_button)

        self.prompt_config_button = QPushButton()
        self.prompt_config_button.setIcon(QIcon("assets/prompt_setting.png"))
        self.prompt_config_button.setIconSize(QSize(300, 207))
        self.prompt_config_button.setFixedHeight(100)
        self.prompt_config_button.clicked.connect(self.open_prompt_config)
        left_layout.addWidget(self.prompt_config_button)

        self.summon_button = QPushButton()
        self.summon_button.setIcon(QIcon("assets/summon_dante.png"))
        self.summon_button.setIconSize(QSize(300, 207))
        self.summon_button.setFixedHeight(50)
        self.summon_button.setStyleSheet(self.generate_button.styleSheet())
        self.summon_button.clicked.connect(self.show_summon_dante)
        left_layout.addWidget(self.summon_button)

        left_layout.addStretch()

        self.output_label = QLabel("Generated Prompt")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #111; color: white; font-size: 16px;")

        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon("assets/copia.png"))
        self.copy_button.setIconSize(QSize(100, 100))
        self.copy_button.setStyleSheet(self.generate_button.styleSheet())
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        right_layout.addWidget(self.output_label)
        right_layout.addWidget(self.output)
        right_layout.addWidget(self.copy_button)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 5)
        self.setLayout(main_layout)

    def load_openai_key(self):
        try:
            with open("openai_key.txt", "r", encoding="utf-8") as f:
                self.openai_api_key = f.read().strip()
                openai.api_key = self.openai_api_key
        except FileNotFoundError:
            self.openai_api_key = ""
            openai.api_key = ""

    def refresh_json_files(self):
        self.version_selector.clear()
        self.available_versions = [f[:-5] for f in os.listdir(self.json_folder) if f.endswith(".json")]
        self.version_selector.addItems(self.available_versions)
        self.update_intensity_combo()

    def load_data(self, version):
        path = os.path.join(self.json_folder, f"{version}.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_intensity_combo(self):
        version = self.version_selector.currentText()
        if not version:
            return
        try:
            data = self.load_data(version)
            self.intensity_combo.clear()
            self.intensity_combo.addItem("None")
            if "HORROR_INTENSITY" in data and isinstance(data["HORROR_INTENSITY"], dict):
                self.intensity_combo.addItems(data["HORROR_INTENSITY"].keys())
        except FileNotFoundError:
            print(f"⚠️ JSON file not found for version: {version}")
        except Exception as e:
            print(f"❌ Error updating intensity combo: {e}")

    def generate_prompt(self):
        version = self.version_selector.currentText()
        data = self.load_data(version)

        try:
            if "ANIMALS" in data:
                epoca = random.choice(data.get("ANIMALS", [""]))
                outfit = random.choice(data.get("OUTFITS", [""]))
                luce = random.choice(data.get("LIGHTING", [""]))
                sfondo = random.choice(data.get("BACKGROUNDS", [""]))
                oggetto = random.choice(data.get("OBJECTS", [""]))
                posa = random.choice(data.get("POSES", [""]))
                espressione = random.choice(data.get("EXPRESSIONS", [""]))
                angolazione = random.choice(data.get("CAMERA_ANGLES", [""]))
                atmosfera = random.choice(data.get("ATMOSPHERES", [""]))
                accessorio = random.choice(data.get("ACCESSORIES", [""]))
                base_prompt = (
                    f"{epoca}, wearing {outfit}, {luce}, set in {sfondo}, "
                    f"with {oggetto}, {posa}, {espressione}, {angolazione}, {atmosfera}, {accessorio}.")
            else:
                epoca = random.choice(data.get("EPOCHS", [""]))
                outfit = random.choice(data.get("OUTFITS", [""]))
                luce = random.choice(data.get("LIGHTING", [""]))
                sfondo = random.choice(data.get("BACKGROUNDS", [""]))
                oggetto = random.choice(data.get("OBJECTS", [""]))
                posa = random.choice(data.get("POSES", [""]))
                espressione = random.choice(data.get("EXPRESSIONS", [""]))
                angolazione = random.choice(data.get("CAMERA_ANGLES", [""]))
                atmosfera = random.choice(data.get("ATMOSPHERES", [""]))
                accessorio = random.choice(data.get("ACCESSORIES", [""]))
                base_prompt = (
                    f"A beautiful woman from the {epoca} era, wearing {outfit}, {luce}, set in {sfondo}, "
                    f"with {oggetto}, {posa}, {espressione}, {angolazione}, {atmosfera}, {accessorio}."
                )

            intensita = self.intensity_combo.currentText()
            horror_descr = data.get("HORROR_INTENSITY", {}).get(intensita, "")
            if intensita != "None":
                base_prompt += f" {horror_descr}"

        except Exception as e:
            self.output.setText(f"❌ Error loading JSON content: {e}")
            return

        try:
            if self.radio_openai.isChecked():
                if not self.openai_api_key:
                    prompt = "⚠️ OpenAI key not found. Please add your key in 'openai_key.txt'."
                else:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": self.user_prompt_template.format(prompt=base_prompt)}
                        ]
                    )
                    prompt = response['choices'][0]['message']['content'].strip()
            elif self.radio_ollama.isChecked():
                self.output.setText("🕯️ Invoking Ollama... please wait.")
                QApplication.processEvents()
                try:
                    res = requests.post("http://localhost:11434/api/generate", json={"model": "mistral", "prompt": base_prompt})
                    lines = res.text.splitlines()
                    max_chars = 1000  # o 500 se vuoi un po' più lungo
                    prompt = "".join([json.loads(line)["response"] for line in lines if line.strip() and "response" in json.loads(line)])
                    prompt = prompt.strip()
                    if len(prompt) > max_chars:
                        prompt = prompt[:max_chars].rsplit(".", 1)[0] + "."
                except Exception as e:
                    prompt = f"Ollama Engine Error: {e}"
            else:
                prompt = f"{base_prompt}"

        except Exception as e:
            prompt = f"Prompt Engine Error: {e}"

        self.output.setText(prompt)

        def generate_id(length=8):
            chars = string.ascii_uppercase + string.digits
            return '-'.join(''.join(random.choices(chars, k=4)) for _ in range(2))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry_id = generate_id()
        with open("prompt_history.txt", "a", encoding="utf-8") as f:
            f.write(f"[ID: {entry_id} | {timestamp}]\n{prompt.strip()}\n\n------------------------\n\n")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output.toPlainText())

    def open_prompt_history(self):
        self.history_window = PromptHistoryWindow()
        self.history_window.show()

    def open_prompt_config(self):
        self.prompt_config_window = PromptConfigWindow(self)
        self.prompt_config_window.show()

    def show_summon_dante(self):
        self.summon_window = SummonDanteWindow()
        self.summon_window.show()

class SummonDanteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Summon Dante")
        self.setGeometry(500, 500, 600, 600)
        self.setStyleSheet("background-color: black;")

        self.label = QLabel(self)
        self.movie = QMovie("assets/Dante_Dance.gif")
        self.movie.setScaledSize(QSize(400, 712))
        self.label.setMovie(self.movie)
        self.label.setAlignment(Qt.AlignCenter)
        self.movie.start()

        self.player = QMediaPlayer()
        media = QMediaContent(QUrl.fromLocalFile(os.path.abspath("assets/Dante_il_Pirata_Maledetto_48kbps.mp3")))
        self.player.setMedia(media)
        self.player.setVolume(50)
        self.player.play()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.player.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptApp()
    window.show()
    sys.exit(app.exec_())
