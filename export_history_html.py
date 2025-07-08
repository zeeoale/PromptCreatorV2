import os
from datetime import datetime

def export_history_to_html(txt_path="prompt_history.txt", output_path="prompt_history_export.html"):
    if not os.path.exists(txt_path):
        print("History file not found.")
        return

    with open(txt_path, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    entries = raw.split("\n\n")
    html_blocks = []

    for entry in entries:
        if entry.strip():
            html_blocks.append(f'<div class="prompt">{entry.replace(chr(10), "<br>")}</div>')

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dante Archives - Prompt History</title>
    <style>
        body {{
            background-color: #111;
            color: #f0f0f0;
            font-family: 'Courier New', monospace;
            padding: 30px;
        }}
        h1 {{
            text-align: center;
            color: #ff4444;
        }}
        .prompt {{
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #444;
        }}
        .footer {{
            margin-top: 50px;
            text-align: center;
            color: #888;
        }}
        .footer img {{
            width: 200px;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>Dante Archives - Prompt History</h1>
    {"".join(html_blocks)}
    <div class="footer">
        <p><em>Approved by the All-Seeing Eye of Dante™</em></p>
        <img src="assets/dante_pixel_approve.webp" alt="Dante Approves">
    </div>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Prompt history exported to: {output_path}")

if __name__ == "__main__":
    export_history_to_html()
