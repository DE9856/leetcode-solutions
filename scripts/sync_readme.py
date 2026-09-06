#!/usr/bin/env python3
"""
sync_readme.py

Fully syncs README.md against the actual solution files on disk:

  1. Scans Python/, C/, Java/ for files named "NNNN_slug.ext".
  2. For every problem number found (whether already logged or brand new),
     looks up the OFFICIAL title and difficulty from LeetCode's public API.
     This means new problems get added with correct data automatically,
     and any existing typo in a title/difficulty gets self-healed over time.
  3. Rebuilds each language's Problem Log table, correctly grouped and
     sorted (Easy -> Medium -> Hard, ascending within each block).
  4. Recomputes the Progress table (Easy/Medium/Hard/Total per language).
  5. Writes the result back to README.md.

If a problem number can't be found in LeetCode's data (API unreachable, or
a number that genuinely isn't a real LeetCode problem), it falls back to
whatever was already in the README for that row; if there's nothing to
fall back to (a brand new file with no prior README entry and no
LeetCode match), it's skipped and reported so nothing incorrect gets
silently added.
"""

import re
import os
import sys
import json
import urllib.request
import urllib.error
from collections import defaultdict

README_PATH = "README.md"
LEETCODE_API = "https://leetcode.com/api/problems/all/"

DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2}

SECTION_CONFIG = {
    "PYTHON": {"language": "Python", "folder": "Python", "ext": "py"},
    "C": {"language": "C", "folder": "C", "ext": "c"},
    "JAVA": {"language": "Java", "folder": "Java", "ext": "java"},
}
# Order sections appear in the file
SECTION_ORDER = ["PYTHON", "C", "JAVA"]

SECTION_HEADER_RE = re.compile(r"^\*\*([A-Za-z0-9+#]+)\*\*\s*$")
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(Easy|Medium|Hard)\s*\|\s*([A-Za-z0-9+#]+)\s*\|\s*$"
)
FILE_NUMBER_RE = re.compile(r"^(\d+)_.+\.([A-Za-z0-9]+)$")


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def parse_problem_rows(lines):
    rows = []
    current_section = None
    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")
        header_match = SECTION_HEADER_RE.match(line.strip())
        if header_match:
            current_section = header_match.group(1)
            continue
        row_match = ROW_RE.match(line)
        if row_match:
            number, title, difficulty, language = row_match.groups()
            rows.append(
                {
                    "line_no": i,
                    "number": int(number),
                    "title": title,
                    "difficulty": difficulty,
                    "language": language,
                    "section": current_section,
                }
            )
    return rows


def scan_folder_numbers(folder, ext):
    numbers = set()
    if not os.path.isdir(folder):
        return numbers
    for fname in os.listdir(folder):
        m = FILE_NUMBER_RE.match(fname)
        if m and m.group(2).lower() == ext:
            numbers.add(int(m.group(1)))
    return numbers


def fetch_leetcode_data():
    """Returns { frontend_question_id: {"difficulty": str, "title": str} }
    or None if the API can't be reached."""
    level_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    try:
        req = urllib.request.Request(LEETCODE_API, headers={"User-Agent": "readme-sync/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"::warning::Could not reach LeetCode API ({e}).")
        return None

    result = {}
    for entry in data.get("stat_status_pairs", []):
        stat = entry.get("stat", {})
        difficulty = entry.get("difficulty", {})
        frontend_id = stat.get("frontend_question_id")
        level = difficulty.get("level")
        title = stat.get("question__title")
        if frontend_id is not None and level in level_map and title:
            result[frontend_id] = {"difficulty": level_map[level], "title": title}
    return result


def build_section_block(section, lang_rows):
    """lang_rows: {number: {"title":..., "difficulty":...}} -> full section text block"""
    language = SECTION_CONFIG[section]["language"]
    items = sorted(
        lang_rows.items(),
        key=lambda kv: (DIFFICULTY_ORDER[kv[1]["difficulty"]], kv[0]),
    )
    lines_out = [f"**{section}**", "| # | Problem | Difficulty | Language |", "|---|---------|------------|----------|"]
    for number, info in items:
        lines_out.append(f"| {number} | {info['title']} | {info['difficulty']} | {language} |")
    return "\n".join(lines_out) + "\n"


def replace_section_in_content(content, section, new_block):
    pattern = re.compile(rf"^\*\*{re.escape(section)}\*\*\n(?:\|.*\n)+", re.MULTILINE)
    if pattern.search(content):
        return pattern.sub(new_block, content, count=1)
    else:
        print(f"::warning::Could not locate **{section}** section in README; skipping update for it.")
        return content


def build_progress_block(counts):
    rows = []
    for lang in ["Python", "C", "Java"]:
        c = counts.get(lang, {"Easy": 0, "Medium": 0, "Hard": 0})
        e, m, h = c["Easy"], c["Medium"], c["Hard"]
        total = e + m + h
        rows.append(f"| {lang:<8} | {e:<6} | {m:<8} | {h:<6} | {total:<5} |")
    return (
        "## 📊 Progress\n\n"
        "<p align=\"center\">\n\n"
        "| Language | Easy 🟢 | Medium 🟡 | Hard 🔴 | Total |\n"
        "|----------|--------|----------|--------|-------|\n"
        + "\n".join(rows) + "\n\n"
        "</p>"
    )


def main():
    if not os.path.isfile(README_PATH):
        print(f"::error::{README_PATH} not found.")
        sys.exit(1)

    lines = read_lines(README_PATH)
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    existing_rows = parse_problem_rows(lines)
    existing_by_lang = defaultdict(dict)
    for r in existing_rows:
        existing_by_lang[r["language"]][r["number"]] = {
            "title": r["title"],
            "difficulty": r["difficulty"],
        }

    leetcode_map = fetch_leetcode_data()

    added, refreshed, unresolved = [], [], []
    counts = {}

    for section in SECTION_ORDER:
        config = SECTION_CONFIG[section]
        language = config["language"]
        folder = config["folder"]
        ext = config["ext"]

        disk_numbers = scan_folder_numbers(folder, ext)
        logged_numbers = set(existing_by_lang.get(language, {}).keys())
        all_numbers = disk_numbers | logged_numbers

        lang_rows = {}
        for number in all_numbers:
            info = leetcode_map.get(number) if leetcode_map else None
            existing = existing_by_lang.get(language, {}).get(number)

            if info:
                lang_rows[number] = {"title": info["title"], "difficulty": info["difficulty"]}
                if not existing:
                    added.append((language, number, info["title"], info["difficulty"]))
                elif existing["title"] != info["title"] or existing["difficulty"] != info["difficulty"]:
                    refreshed.append((language, number, existing, info))
            elif existing:
                lang_rows[number] = existing  # keep what's already there, can't verify right now
            else:
                unresolved.append((language, number))
                continue  # brand new file, no LeetCode data, no prior entry -> skip

        counts[language] = {"Easy": 0, "Medium": 0, "Hard": 0}
        for info in lang_rows.values():
            counts[language][info["difficulty"]] += 1

        new_block = build_section_block(section, lang_rows)
        content = replace_section_in_content(content, section, new_block)

    progress_block = build_progress_block(counts)
    content = re.sub(
        r"## 📊 Progress\n\n<p align=\"center\">[\s\S]*?</p>",
        progress_block,
        content,
        count=1,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    if added:
        print(f"Added {len(added)} new row(s):")
        for lang, number, title, difficulty in added:
            print(f"  + [{lang}] #{number} {title} ({difficulty})")
    if refreshed:
        print(f"Refreshed {len(refreshed)} row(s) with corrected LeetCode data:")
        for lang, number, old, new in refreshed:
            print(f"  ~ [{lang}] #{number}: '{old['title']}'/{old['difficulty']} -> "
                  f"'{new['title']}'/{new['difficulty']}")
    if unresolved:
        print(f"::warning::{len(unresolved)} file(s) found on disk with no README entry "
              f"and no LeetCode match; left unlisted: "
              + ", ".join(f"{lang} #{n}" for lang, n in unresolved))
    if not added and not refreshed and not unresolved:
        print("No new problems found; README already in sync.")

    print("\nProgress table:")
    for lang, c in counts.items():
        total = c["Easy"] + c["Medium"] + c["Hard"]
        print(f"  {lang}: Easy={c['Easy']} Medium={c['Medium']} Hard={c['Hard']} Total={total}")


if __name__ == "__main__":
    main()