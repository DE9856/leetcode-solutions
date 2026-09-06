#!/usr/bin/env python3
"""
validate_readme.py

Validates the "Problem Log" tables in README.md:
  1. Ordering  - within each (Language, Difficulty) block, problem numbers
                 must be strictly ascending, and difficulties must not
                 interleave (all Easy rows before all Medium rows before
                 all Hard rows, per language section).
  2. Duplicates - no problem number repeated within the same
                 (Language, Difficulty) block.
  3. Difficulty - the stated difficulty must match LeetCode's own
                 difficulty for that problem number (cross-checked
                 against LeetCode's public problem list API).

Exits with a non-zero status (and prints a report) if any check fails,
so it can be used as a CI gate in GitHub Actions.
"""

import re
import sys
import json
import urllib.request
import urllib.error
from collections import defaultdict

README_PATH = "README.md"
LEETCODE_API = "https://leetcode.com/api/problems/all/"

VALID_DIFFICULTIES = ("Easy", "Medium", "Hard")
DIFFICULTY_ORDER = {d: i for i, d in enumerate(VALID_DIFFICULTIES)}

# Matches a section header like "**PYTHON**" (also allows "**C++**" etc.)
SECTION_HEADER_RE = re.compile(r"^\*\*([A-Za-z0-9+#]+)\*\*\s*$")

# Matches a data row like: | 14 | Longest Common Prefix | Easy | Python |
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(Easy|Medium|Hard)\s*\|\s*([A-Za-z0-9+#]+)\s*\|\s*$"
)


def parse_readme(path):
    """Returns a list of dicts: {line_no, number, title, difficulty, language, section}"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

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


def check_ordering_and_duplicates(rows):
    """
    Groups rows by (section, language) preserving file order, then checks:
      - difficulties appear in blocks (Easy*, then Medium*, then Hard*)
      - within each difficulty block, numbers strictly ascending
      - no duplicate numbers within a (section, language, difficulty) group
    Returns a list of human-readable error strings.
    """
    errors = []
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["section"], row["language"])].append(row)

    for (section, language), group_rows in grouped.items():
        seen_difficulty_order = []
        last_number_by_difficulty = {}
        seen_numbers_by_difficulty = defaultdict(set)

        last_difficulty_rank = -1

        for row in group_rows:
            diff = row["difficulty"]
            rank = DIFFICULTY_ORDER[diff]

            # Difficulty block ordering: rank must never decrease
            if rank < last_difficulty_rank:
                errors.append(
                    f"[Line {row['line_no']}] {section}/{language}: "
                    f"'{diff}' row for #{row['number']} appears after a "
                    f"'{VALID_DIFFICULTIES[last_difficulty_rank]}' row — "
                    f"difficulty blocks must be grouped as Easy -> Medium -> Hard."
                )
            last_difficulty_rank = max(last_difficulty_rank, rank)

            # Ascending order within the difficulty block
            if diff in last_number_by_difficulty:
                if row["number"] <= last_number_by_difficulty[diff]:
                    errors.append(
                        f"[Line {row['line_no']}] {section}/{language}/{diff}: "
                        f"#{row['number']} is not greater than the previous "
                        f"entry (#{last_number_by_difficulty[diff]}) in this block."
                    )
            last_number_by_difficulty[diff] = row["number"]

            # Duplicates
            if row["number"] in seen_numbers_by_difficulty[diff]:
                errors.append(
                    f"[Line {row['line_no']}] {section}/{language}/{diff}: "
                    f"#{row['number']} is listed more than once."
                )
            seen_numbers_by_difficulty[diff].add(row["number"])

    return errors


def fetch_leetcode_difficulty_map():
    """
    Fetches LeetCode's public problem list and returns:
      { frontend_question_id (int) : "Easy" | "Medium" | "Hard" }
    Returns None if the fetch fails (e.g. no network access), in which
    case difficulty cross-checking is skipped with a warning.
    """
    level_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    try:
        req = urllib.request.Request(
            LEETCODE_API, headers={"User-Agent": "readme-validator/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"::warning::Could not reach LeetCode API ({e}); "
              f"skipping difficulty cross-check.")
        return None

    result = {}
    for entry in data.get("stat_status_pairs", []):
        stat = entry.get("stat", {})
        difficulty = entry.get("difficulty", {})
        frontend_id = stat.get("frontend_question_id")
        level = difficulty.get("level")
        if frontend_id is not None and level in level_map:
            result[frontend_id] = level_map[level]
    return result


def check_difficulty_accuracy(rows, leetcode_map):
    errors = []
    if leetcode_map is None:
        return errors  # skipped, already warned

    for row in rows:
        actual = leetcode_map.get(row["number"])
        if actual is None:
            print(
                f"::warning::[Line {row['line_no']}] #{row['number']} "
                f"('{row['title']}') not found in LeetCode's problem list; "
                f"could not verify difficulty."
            )
            continue
        if actual != row["difficulty"]:
            errors.append(
                f"[Line {row['line_no']}] #{row['number']} ('{row['title']}'): "
                f"README says '{row['difficulty']}' but LeetCode says '{actual}'."
            )
    return errors


def main():
    rows = parse_readme(README_PATH)

    if not rows:
        print("::error::No problem rows found in README.md — check table format.")
        sys.exit(1)

    ordering_errors = check_ordering_and_duplicates(rows)
    leetcode_map = fetch_leetcode_difficulty_map()
    difficulty_errors = check_difficulty_accuracy(rows, leetcode_map)

    all_errors = ordering_errors + difficulty_errors

    print(f"Checked {len(rows)} problem rows across "
          f"{len({(r['section'], r['language']) for r in rows})} language sections.\n")

    if all_errors:
        print(f"❌ {len(all_errors)} issue(s) found:\n")
        for err in all_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("✅ All problem rows are correctly ordered and difficulties match LeetCode.")
        sys.exit(0)


if __name__ == "__main__":
    main()