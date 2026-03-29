import re

with open("README.md", "r") as f:
    content = f.read()

# Find all problem rows
pattern = r"\|\s*\d+\s*\|\s*.*?\|\s*(Easy|Medium|Hard)\s*\|\s*(Python|Java|C)\s*\|"
matches = re.findall(pattern, content)

# Initialize counts
counts = {
    "Python": {"Easy": 0, "Medium": 0, "Hard": 0},
    "Java": {"Easy": 0, "Medium": 0, "Hard": 0},
    "C": {"Easy": 0, "Medium": 0, "Hard": 0},
}

# Count
for difficulty, lang in matches:
    counts[lang][difficulty] += 1

# Build progress table
progress_table = """## 📊 Progress

<!-- START_PROGRESS -->

| Language | Easy | Medium | Hard |
|----------|------|--------|------|
"""

for lang in ["Python", "Java", "C"]:
    e = counts[lang]["Easy"]
    m = counts[lang]["Medium"]
    h = counts[lang]["Hard"]
    progress_table += f"| {lang} | {e} | {m} | {h} |\n"

progress_table += "\n<!-- END_PROGRESS -->"

# Build badges
badge_section = "## 📈 Progress Badges\n\n<!-- START_BADGES -->\n\n"

for lang, emoji in [("Python", "🐍"), ("Java", "☕"), ("C", "⚙️")]:
    e = counts[lang]["Easy"]
    m = counts[lang]["Medium"]
    h = counts[lang]["Hard"]

    badge_section += f"### {emoji} {lang}\n"
    badge_section += f"![Easy](https://img.shields.io/badge/Easy-{e}-brightgreen)\n"
    badge_section += f"![Medium](https://img.shields.io/badge/Medium-{m}-yellow)\n"

    color = "red" if h != 0 else "lightgrey"
    badge_section += f"![Hard](https://img.shields.io/badge/Hard-{h}-{color})\n\n"

badge_section += "<!-- END_BADGES -->"

# Replace sections
content = re.sub(
    r"## 📊 Progress[\s\S]*?<!-- END_PROGRESS -->",
    progress_table,
    content
)

content = re.sub(
    r"## 📈 Progress Badges[\s\S]*?<!-- END_BADGES -->",
    badge_section,
    content
)

with open("README.md", "w") as f:
    f.write(content)
