#!/usr/bin/env python3
"""
validate_readme.py

Thorough validator for a LeetCode-solutions README + repo layout.

Checks performed:
  1. Ordering       - within each (section, language), difficulties appear
                       grouped Easy -> Medium -> Hard, and problem numbers
                       strictly ascend within each difficulty block.
  2. Duplicates     - no problem number repeated within a
                       (section, language, difficulty) group.
  3. Section/Lang   - a row's "Language" column must match the language
     consistency      implied by its section header (**PYTHON** -> Python,
                       **C** -> C, **JAVA** -> Java).
  4. Malformed rows - any "|"-prefixed line inside the Problem Log that
                       isn't a valid header/separator/data row is flagged,
                       so silent typos (missing pipe, stray column) surface.
  5. Difficulty     - stated difficulty must match LeetCode's own
     accuracy          difficulty for that problem number (via LeetCode's
                       public problem-list API).
  6. Title accuracy - stated title must closely match LeetCode's own
                       title for that problem number (catches typos like
                       "Paranthesis" vs "Parentheses"). Uses fuzzy
                       matching so trivial punctuation/case differences
                       don't trip it.
  7. Progress table - the Easy/Medium/Hard/Total numbers in the
     accuracy          "## Progress" summary table must match what's
                       actually counted in the Problem Log tables.
  8. File existence - every logged problem must have a matching solution
                       file on disk (e.g. "0014_longest_common_prefix.py"
                       for Python problem 14), based on the repo's
                       "NNNN_slug.ext" naming convention.
  9. Orphan files   - solution files on disk that aren't referenced by
                       any row in the Problem Log are flagged (soft
                       warning, not a hard failure).

Exits non-zero if any hard check (1-8) fails, so it can gate CI.
Orphan files (9) are reported as warnings only and do not fail the build.
"""

import re
import sys
import json
import os
import difflib
import urllib.request
import urllib.error
from collections import defaultdict

README_PATH = "README.md"
LEETCODE_API = "https://leetcode.com/api/problems/all/"

VALID_DIFFICULTIES = ("Easy", "Medium", "Hard")
DIFFICULTY_ORDER = {d: i for i, d in enumerate(VALID_DIFFICULTIES)}

# Section header -> expected "Language" column value and folder/extension.
SECTION_CONFIG = {
    "PYTHON": {"language": "Python", "folder": "Python", "ext": "py"},
    "C": {"language": "C", "folder": "C", "ext": "c"},
    "JAVA": {"language": "Java", "folder": "Java", "ext": "java"},
}

TITLE_MATCH_THRESHOLD = 0.90  # below this, flag as a likely typo/mismatch

SECTION_HEADER_RE = re.compile(r"^\*\*([A-Za-z0-9+#]+)\*\*\s*$")
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(Easy|Medium|Hard)\s*\|\s*([A-Za-z0-9+#]+)\s*\|\s*$"
)
TABLE_HEADER_RE = re.compile(r"^\|\s*#\s*\|")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s\-|:]+\|$")

PROBLEM_LOG_HEADING_RE = re.compile(r"Problem Log")
PROGRESS_HEADING_RE = re.compile(r"^##.*\bProgress\b")
NEXT_H2_RE = re.compile(r"^##\s")

# Progress table rows: | Python | 35 | 27 | 5 | 67 |  (emoji-decorated header is fine, data rows are plain)
PROGRESS_ROW_RE = re.compile(
    r"^\|\s*([A-Za-z0-9+#]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*$"
)

FILE_NUMBER_RE = re.compile(r"^(\d+)_.+\.([A-Za-z0-9]+)$")


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def slice_section(lines, start_pattern, end_pattern=None):
    """Return (start_idx, end_idx, lines_in_range) for the block starting at
    the first line matching start_pattern, up to (but excluding) the next
    line matching end_pattern (or another '## ' heading if end_pattern is None)."""
    start_idx = None
    for i, line in enumerate(lines):
        if start_pattern.search(line):
            start_idx = i
            break
    if start_idx is None:
        return None, None, []

    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if end_pattern and end_pattern.search(lines[i]):
            end_idx = i
            break
        if not end_pattern and NEXT_H2_RE.match(lines[i]):
            end_idx = i
            break
    return start_idx, end_idx, lines[start_idx:end_idx]


def parse_problem_rows(lines):
    """Parses all problem rows across the whole file, tagging each with its
    section (PYTHON/C/JAVA) based on the nearest preceding bold header."""
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
    errors = []
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["section"], row["language"])].append(row)

    for (section, language), group_rows in grouped.items():
        last_number_by_difficulty = {}
        seen_numbers_by_difficulty = defaultdict(set)
        last_difficulty_rank = -1

        for row in group_rows:
            diff = row["difficulty"]
            rank = DIFFICULTY_ORDER[diff]

            if rank < last_difficulty_rank:
                errors.append(
                    f"[Line {row['line_no']}] {section}/{language}: '{diff}' row "
                    f"for #{row['number']} appears after a "
                    f"'{VALID_DIFFICULTIES[last_difficulty_rank]}' row — difficulty "
                    f"blocks must be grouped Easy -> Medium -> Hard."
                )
            last_difficulty_rank = max(last_difficulty_rank, rank)

            if diff in last_number_by_difficulty and row["number"] <= last_number_by_difficulty[diff]:
                errors.append(
                    f"[Line {row['line_no']}] {section}/{language}/{diff}: "
                    f"#{row['number']} is not greater than the previous entry "
                    f"(#{last_number_by_difficulty[diff]}) in this block."
                )
            last_number_by_difficulty[diff] = row["number"]

            if row["number"] in seen_numbers_by_difficulty[diff]:
                errors.append(
                    f"[Line {row['line_no']}] {section}/{language}/{diff}: "
                    f"#{row['number']} is listed more than once."
                )
            seen_numbers_by_difficulty[diff].add(row["number"])

    return errors


def check_section_language_consistency(rows):
    errors = []
    for row in rows:
        expected = SECTION_CONFIG.get(row["section"], {}).get("language")
        if expected and row["language"] != expected:
            errors.append(
                f"[Line {row['line_no']}] Row is under **{row['section']}** but its "
                f"Language column says '{row['language']}' (expected '{expected}')."
            )
    return errors


def check_malformed_rows(lines):
    """Flags '|'-prefixed lines inside the Problem Log that aren't a
    recognized header, separator, or valid data row."""
    errors = []
    start, end, _ = slice_section(lines, PROBLEM_LOG_HEADING_RE)
    if start is None:
        return errors

    for i in range(start, end):
        line = lines[i].rstrip("\n")
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if TABLE_HEADER_RE.match(line) or TABLE_SEPARATOR_RE.match(line):
            continue
        if ROW_RE.match(line):
            continue
        errors.append(
            f"[Line {i + 1}] Malformed table row (doesn't match the expected "
            f"'| # | Problem | Difficulty | Language |' format): {stripped!r}"
        )
    return errors


def check_progress_table(lines, rows):
    """Cross-checks the '## Progress' summary table against counts derived
    from the actual Problem Log rows."""
    errors = []
    start, end, _ = slice_section(lines, PROGRESS_HEADING_RE, end_pattern=NEXT_H2_RE)
    if start is None:
        return errors  # no progress table found; nothing to check

    declared = {}
    for i in range(start, end):
        m = PROGRESS_ROW_RE.match(lines[i].rstrip("\n"))
        if m:
            lang, easy, medium, hard, total = m.groups()
            declared[lang] = {
                "easy": int(easy),
                "medium": int(medium),
                "hard": int(hard),
                "total": int(total),
                "line_no": i + 1,
            }

    actual_counts = defaultdict(lambda: defaultdict(int))
    for row in rows:
        actual_counts[row["language"]][row["difficulty"].lower()] += 1

    for lang, decl in declared.items():
        actual = actual_counts.get(lang, {"easy": 0, "medium": 0, "hard": 0})
        for level in ("easy", "medium", "hard"):
            if decl[level] != actual.get(level, 0):
                errors.append(
                    f"[Line {decl['line_no']}] Progress table says {lang} has "
                    f"{decl[level]} {level.title()} problems, but the Problem Log "
                    f"actually lists {actual.get(level, 0)}."
                )
        declared_sum = decl["easy"] + decl["medium"] + decl["hard"]
        if decl["total"] != declared_sum:
            errors.append(
                f"[Line {decl['line_no']}] Progress table's {lang} Total "
                f"({decl['total']}) doesn't equal Easy+Medium+Hard ({declared_sum})."
            )

    logged_languages = set(actual_counts.keys())
    declared_languages = set(declared.keys())
    for missing_lang in logged_languages - declared_languages:
        errors.append(
            f"Problem Log has entries for language '{missing_lang}' but the "
            f"Progress table has no row for it."
        )

    return errors


def fetch_leetcode_data():
    """Returns { frontend_question_id: {"difficulty": str, "title": str} }
    or None if the API can't be reached."""
    level_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    try:
        req = urllib.request.Request(LEETCODE_API, headers={"User-Agent": "readme-validator/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"::warning::Could not reach LeetCode API ({e}); skipping "
              f"difficulty and title cross-checks.")
        return None

    result = {}
    for entry in data.get("stat_status_pairs", []):
        stat = entry.get("stat", {})
        difficulty = entry.get("difficulty", {})
        frontend_id = stat.get("frontend_question_id")
        level = difficulty.get("level")
        title = stat.get("question__title")
        if frontend_id is not None and level in level_map:
            result[frontend_id] = {"difficulty": level_map[level], "title": title}
    return result


def normalize_title(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


def check_difficulty_and_title_accuracy(rows, leetcode_map):
    errors = []
    if leetcode_map is None:
        return errors

    for row in rows:
        info = leetcode_map.get(row["number"])
        if info is None:
            print(
                f"::warning::[Line {row['line_no']}] #{row['number']} "
                f"('{row['title']}') not found in LeetCode's problem list; "
                f"could not verify difficulty or title."
            )
            continue

        if info["difficulty"] != row["difficulty"]:
            errors.append(
                f"[Line {row['line_no']}] #{row['number']} ('{row['title']}'): "
                f"README says '{row['difficulty']}' but LeetCode says "
                f"'{info['difficulty']}'."
            )

        if info["title"]:
            a, b = normalize_title(row["title"]), normalize_title(info["title"])
            ratio = difflib.SequenceMatcher(None, a, b).ratio()
            if ratio < TITLE_MATCH_THRESHOLD:
                errors.append(
                    f"[Line {row['line_no']}] #{row['number']}: README title "
                    f"'{row['title']}' doesn't closely match LeetCode's title "
                    f"'{info['title']}' (similarity {ratio:.2f}) — check for a typo."
                )

    return errors


def check_files(rows):
    """Checks that every logged row has a matching solution file on disk,
    and separately collects orphan files (on disk, not logged)."""
    errors = []
    warnings = []

    rows_by_language = defaultdict(set)
    for row in rows:
        rows_by_language[row["language"]].add(row["number"])

    for section, config in SECTION_CONFIG.items():
        folder = config["folder"]
        expected_ext = config["ext"]
        language = config["language"]

        if not os.path.isdir(folder):
            warnings.append(f"Folder '{folder}/' not found; skipping file checks for {language}.")
            continue

        on_disk = {}  # number -> filename
        for fname in os.listdir(folder):
            m = FILE_NUMBER_RE.match(fname)
            if not m:
                continue
            number, ext = m.groups()
            if ext.lower() != expected_ext:
                continue
            on_disk[int(number)] = fname

        logged_numbers = rows_by_language.get(language, set())

        # Missing files: logged in README but no file on disk
        for number in sorted(logged_numbers):
            if number not in on_disk:
                errors.append(
                    f"{language}: README logs problem #{number} but no matching "
                    f"'{number:04d}_*.{expected_ext}' file was found in '{folder}/'."
                )

        # Orphan files: on disk but not logged in README
        for number, fname in sorted(on_disk.items()):
            if number not in logged_numbers:
                warnings.append(
                    f"{language}: file '{folder}/{fname}' exists but problem #{number} "
                    f"is not listed in the README's {language} table."
                )

    return errors, warnings


def main():
    if not os.path.isfile(README_PATH):
        print(f"::error::{README_PATH} not found.")
        sys.exit(1)

    lines = read_lines(README_PATH)
    rows = parse_problem_rows(lines)

    if not rows:
        print("::error::No problem rows found in README.md — check table format.")
        sys.exit(1)

    all_errors = []
    all_warnings = []

    all_errors += check_ordering_and_duplicates(rows)
    all_errors += check_section_language_consistency(rows)
    all_errors += check_malformed_rows(lines)
    all_errors += check_progress_table(lines, rows)

    leetcode_map = fetch_leetcode_data()
    all_errors += check_difficulty_and_title_accuracy(rows, leetcode_map)

    file_errors, file_warnings = check_files(rows)
    all_errors += file_errors
    all_warnings += file_warnings

    n_sections = len({(r["section"], r["language"]) for r in rows})
    print(f"Checked {len(rows)} problem rows across {n_sections} language sections.\n")

    if all_warnings:
        print(f"⚠️  {len(all_warnings)} warning(s) (non-blocking):\n")
        for w in all_warnings:
            print(f" - {w}")
        print()

    if all_errors:
        print(f"❌ {len(all_errors)} issue(s) found:\n")
        for err in all_errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("✅ All checks passed: ordering, duplicates, section/language "
              "consistency, table formatting, progress-table accuracy, "
              "LeetCode difficulty/title accuracy, and solution-file existence.")
        sys.exit(0)


if __name__ == "__main__":
    main()