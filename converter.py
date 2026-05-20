from pathlib import Path
import html
import re

input_path = Path("2PDF_zh-TW.md")
output_path = Path("resume_zh-TW.html")

lines = input_path.read_text(encoding="utf-8").splitlines()

html_lines = []
in_ul = False

def parse_inline(text):

    # 先處理 markdown link
    pattern_md = r"\[([^\]]+)\]\(([^)]+)\)"

    def replace_md(match):
        link_text = match.group(1)
        link_url = match.group(2)

        return (
            f'<a href="{html.escape(link_url, quote=True)}" '
            f'target="_blank">'
            f'{html.escape(link_text)}</a>'
        )

    text = re.sub(pattern_md, replace_md, text)

    # 再處理：
    # Linkedin:(https://xxx)
    pattern_simple = r'([A-Za-z0-9_+\- ]+):\((https?://[^)]+)\)'

    def replace_simple(match):
        label = match.group(1).strip()
        url = match.group(2).strip()

        return (
            f'{html.escape(label)}: '
            f'<a href="{html.escape(url, quote=True)}" '
            f'target="_blank">'
            f'{html.escape(url)}</a>'
        )

    text = re.sub(pattern_simple, replace_simple, text)

    return text

def close_ul():
    global in_ul
    if in_ul:
        html_lines.append("</ul>")
        in_ul = False

for line in lines:
    line = line.strip()

    if line == "":
        close_ul()
        html_lines.append("")
        continue
    
    if line == "---":
        close_ul()
        html_lines.append("")
        continue

    if line.startswith("# "):
        close_ul()
        html_lines.append(f"<h1>{parse_inline(line[2:].strip())}</h1>")

    elif line.startswith("## "):
        close_ul()
        html_lines.append(f"<h2>{parse_inline(line[3:].strip())}</h2>")

    elif line.startswith("### "):
        close_ul()
        html_lines.append(f"<h3>{parse_inline(line[4:].strip())}</h3>")

    elif line.startswith("- "):
        if not in_ul:
            html_lines.append("<ul>")
            in_ul = True

        html_lines.append(f"  <li>{parse_inline(line[2:].strip())}</li>")

    else:
        close_ul()
        html_lines.append(f"<p>{parse_inline(line)}</p>")

close_ul()

html_content = "\n".join(html_lines)

template = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <title>Resume</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="resume">
{html_content}
  </main>
</body>
</html>
"""

output_path.write_text(template, encoding="utf-8")

print(f"轉換完成：{output_path}")