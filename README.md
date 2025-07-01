# Prompt Creator V2 ✨🎨

A beautiful and powerful desktop app in **PyQt5** that helps you browse, organize, and generate dynamic AI prompts using modular JSON files.

This tool is designed to work with:
- Stable Diffusion
- ComfyUI
- Dynamic Prompts extensions
- OpenAI API (for prompt enhancement using CLIP-based analysis — optional)

---

![preview](./preview.png)

## 🧰 Features

- Browse prompts organized by category (via JSON files)
- Generate random prompts from dropdown selections
- Automatic loading of all `.json` files from `JSON_DATA` folder
- Includes a handy **JSON Editor** to edit or create your own prompt libraries!
- Clean and modern PyQt5 GUI style

---

## 🐍 Installation

### 1. Clone the repo:

```bash
git clone https://github.com/tuo-username/PromptCreatorV2.git
cd PromptCreatorV2
```

### 2. Create a virtual environment:

```bash
python -m venv venv
```

### 3. Activate it:

- **Windows:**

```bash
venv\Scripts\activate
```

- **Linux/Mac:**

```bash
source venv/bin/activate
```

### 4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python prompt_library_app_v2.py
```

To launch the integrated **JSON Editor**, run:

```bash
python json_editor.py
```

---

## 🔐 OpenAI API (optional)

The prompt enhancer uses OpenAI's CLIP via API.

To enable this feature:
1. Get an API Key from [OpenAI](https://platform.openai.com/account/api-keys)
2. Replace the placeholder line in `prompt_library_app_v2.py` with your real key:

```python
openai.api_key = "INSERT_YOUR_API_KEY_HERE"
```

⚠️ **Note**: You need a paid OpenAI account to use this feature.

---

## 📁 Folder Structure

```
PromptCreatorV2/
├── prompt_library_app_v2.py      # Main app
├── json_editor.py                # JSON editor
├── JSON_DATA/                    # All prompt category files (loaded automatically)
│   ├── Resident_Evil.json
│   ├── My_Little_Pony.json
│   └── ...
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## ❤️ Credits

Thanks to:

- **Magnificent Lily** ❤️  
- **My Wonderful cat Dante** 😽  
- **My one and only muse Helly** 😍❤️❤️❤️😍  

---

## ☕ Support My Work

If you enjoy what I do and want to help keep the creative fire burning, feel free to buy me a coffee!  
Every donation helps Dante plan his next mysterious nap... and helps me build even better tools.

[![Ko-Fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/X8X51G4623)

---

## 📦 Powered By

- [OpenAI](https://openai.com/) — For prompt enrichment
- [PyQt5](https://pypi.org/project/PyQt5/) — For the GUI
