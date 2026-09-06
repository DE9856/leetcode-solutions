import re

README_PATH = "README.md"

LANGUAGES = ["Python", "C", "Java"]  # matches the display order in the README

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Find all problem rows in the Problem Log tables: | # | Problem | Difficulty | Language |
pattern = r"\|\s*\d+\s*\|\s*.*?\|\s*(Easy|Medium|Hard)\s*\|\s*(Python|Java|C)\s*\|"
matches = re.findall(pattern, content)

# Count Easy/Medium/Hard per language
counts = {lang: {"Easy": 0, "Medium": 0, "Hard": 0} for lang in LANGUAGES}
for difficulty, lang in matches:
    counts[lang][difficulty] += 1

# Build the Progress section exactly as it appears in the README:
# a heading, a <p align="center"> wrapper, a 5-column table (with Total), then </p>
rows = []
for lang in LANGUAGES:
    e = counts[lang]["Easy"]
    m = counts[lang]["Medium"]
    h = counts[lang]["Hard"]
    total = e + m + h
    rows.append(f"| {lang:<8} | {e:<6} | {m:<8} | {h:<6} | {total:<5} |")

progress_block = (
    "## 📊 Progress\n\n"
    "<p align=\"center\">\n\n"
    "| Language | Easy 🟢 | Medium 🟡 | Hard 🔴 | Total |\n"
    "|----------|--------|----------|--------|-------|\n"
    + "\n".join(rows) + "\n\n"
    "</p>"
)

# Replace everything from "## 📊 Progress" through the closing </p> of that section.
# This matches the real structure of the README (no HTML comment markers needed).
content = re.sub(
    r"## 📊 Progress\n\n<p align=\"center\">[\s\S]*?</p>",
    progress_block,
    content,
    count=1,
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Progress table updated:")
for lang in LANGUAGES:
    e, m, h = counts[lang]["Easy"], counts[lang]["Medium"], counts[lang]["Hard"]
    print(f"  {lang}: Easy={e} Medium={m} Hard={h} Total={e + m + h}")