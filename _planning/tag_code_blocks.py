#!/usr/bin/env python3
"""
tag_code_blocks.py — Add language tags to unlabeled fenced code blocks in Snyk user-docs.

Usage:
    python3 _planning/tag_code_blocks.py [--dry-run] [--file path/to/file.md]

Flags:
    --dry-run   Print what would change without modifying files.
    --file      Process a single file instead of all docs/**/*.md files.
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Language inference heuristics (applied in priority order)
# ---------------------------------------------------------------------------

def _count_lines(block: str) -> int:
    return len([l for l in block.split("\n") if l.strip()])


def _is_valid_json(text: str) -> bool:
    """Return True if the text is parseable JSON (object or array)."""
    stripped = text.strip()
    if not (stripped.startswith("{") or stripped.startswith("[")):
        return False
    try:
        json.loads(stripped)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


# Compiled patterns reused across calls
_RE_JSON_START = re.compile(r"^\s*[\[{]")
_RE_SHELL_PROMPT = re.compile(r"^\s*(\$\s|#!)", re.MULTILINE)
_RE_SHELL_SHEBANG = re.compile(r"^#!(\/usr\/bin\/env\s+\w+|\/bin\/\w+)")
_RE_SHELL_COMMANDS = re.compile(
    r"\b(apt(?:-get)?|brew|curl|wget|export|echo|mkdir|"
    r"npm\s|yarn\s|pip\s|pip3\s|docker\s|kubectl\s|helm\s|snyk\s|"
    r"git\s|chmod|chown|rm\s|cp\s|mv\s|ls\s|cat\s|"
    r"source\s|bash\s|sh\s|exec\s|npx\s|"
    r"aws\s|gcloud\s|az\s|terraform\s|ansible\s|"
    r"cd\s+\S)\b"
)
# Shell line-continuation pattern (backslash at end of line)
_RE_SHELL_CONTINUATION = re.compile(r"\\\s*$", re.MULTILINE)
_RE_YAML_KEY_VALUE = re.compile(r"^\s*[\w\-]+:\s", re.MULTILINE)  # any indentation level
_RE_YAML_DASH_LIST = re.compile(r"^\s*-\s+\w", re.MULTILINE)
_RE_YAML_START = re.compile(r"^---\s*$", re.MULTILINE)
# XML tags: require realistic tag names.
# Exclude: ALL_CAPS placeholders like <SNYK_ORG_ID>
# Exclude: all-lowercase-with-underscores like <public_snyk_group_id> (looks like API placeholder)
# Include: camelCase, hyphenated, or mixed names like <groupId>, <artifactId>, <my-element>
_RE_XML_TAG = re.compile(
    r"</?(?!(?:[a-z_]+|[A-Z_]+)>)"  # exclude pure lowercase_underscore or UPPERCASE placeholders
    r"[A-Za-z][A-Za-z0-9\-]*[A-Z][A-Za-z0-9\-]*"  # must have uppercase (camelCase) or hyphen
    r"(?:\s[^>]*)?>|"
    r"</?[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9\-]+(?:\s[^>]*)?>",  # hyphenated names
)
_RE_XML_SELFCLOSE = re.compile(
    r"<[A-Za-z][A-Za-z0-9\-]*[A-Z][A-Za-z0-9\-]*[^>]*/\s*>|"
    r"<[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9\-]+[^>]*/\s*>"
)
# Also detect XML declarations and common XML/HTML structural markers
_RE_XML_DECL = re.compile(r"(<\?xml|<!DOCTYPE|<html[\s>]|<\w+\s+xmlns)")
# Dockerfile: FROM must be followed by an image reference (contains :, /, or AS keyword)
# to avoid matching "FROM users" in SQL queries.
_RE_DOCKERFILE_FROM = re.compile(
    r"^FROM\s+\S+[:/@]|^FROM\s+\S+\s+AS\s+\w|^FROM\s+scratch\b",
    re.MULTILINE | re.IGNORECASE
)
_RE_DOCKERFILE_OTHER = re.compile(
    r"^(RUN|CMD|ENTRYPOINT|COPY|ADD|ENV|EXPOSE|WORKDIR|ARG|LABEL|USER|VOLUME|HEALTHCHECK)\s",
    re.MULTILINE
)
_RE_HCL = re.compile(r'(terraform\s*\{|resource\s+"[^"]+"|variable\s+"[^"]+"|provider\s+"[^"]+"|'
                     r'module\s+"[^"]+"|output\s+"[^"]+"|data\s+"[^"]+")', re.MULTILINE)
_RE_SQL = re.compile(r"\b(SELECT\s+\w|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|CREATE\s+TABLE|"
                     r"DROP\s+TABLE|ALTER\s+TABLE|CREATE\s+INDEX|TRUNCATE\s+TABLE)\b",
                     re.MULTILINE)
# PEM/certificate blocks — exclude from other heuristics
_RE_PEM_BLOCK = re.compile(r"-----BEGIN\s+[\w\s]+-----")
# Rego (OPA policy language) — must check before Go since both use 'package'
_RE_REGO = re.compile(
    r"(^package\s+\w.*\n.*\b(deny|allow|violation|warn)\s*\["   # package + deny/allow rule
    r"|\b(deny|allow|violation)\s*\[msg\]"                       # deny[msg] anywhere
    r"|^import\s+data\."                                          # 'import data.lib' (Rego-specific)
    r"|test_[A-Z][A-Z_]+\s*\{"                                   # test functions like test_MY_RULE {
    r"|\bfuture\.keywords\b)",                                    # future.keywords (Rego-specific)
    re.MULTILINE
)
_RE_GO = re.compile(r'(^package\s+\w|^import\s+"[^"]+"|^func\s+\w)', re.MULTILINE)
_RE_PYTHON = re.compile(r"(^def\s+\w|^class\s+\w|^import\s+\w|^from\s+\w+\s+import|pip\s+install|pip3\s+install)",
                        re.MULTILINE)
_RE_JAVASCRIPT = re.compile(r"(^const\s+\w|^let\s+\w|^var\s+\w|^function\s+\w|\brequire\s*\(|=>\s*\{|"
                            r"module\.exports\s*=|console\.log\()", re.MULTILINE)
_RE_TYPESCRIPT = re.compile(r"(:\s*(string|number|boolean|void|any|never|unknown)\b|"
                            r"\binterface\s+\w|\btype\s+\w+\s*=|\bReadonly<|import\s+type\s+)",
                            re.MULTILINE)

# Patterns that strongly indicate plain text / terminal output / prose
_RE_PLAIN_PROSE = re.compile(
    r"(^[A-Z][a-z].{20,}$)",   # Sentence-like lines
    re.MULTILINE
)
_RE_ERROR_OUTPUT = re.compile(
    r"(Error:|Warning:|INFO\s|DEBUG\s"
    r"|\[\d{4}-\d{2}-\d{2}|HTTP/[12]\."
    r"|\s+at\s+\w+\s*\(|\s+at\s+\w+\."
    r"|Testing\s+\S+\.\.\.|Infrastructure as code issues:"
    r"|\d+\s+vulnerabilit|Severity:\s+\w|Status:\s+\w"
    r"|Apply complete!|Plan:|No changes\.|Outputs:|Resources:\s+\d+"
    r"|\bFAIL:\s+\d+|\bPASS:\s+\d+|Executing\s+\w+\s+test"
    r"|^\-{10,}$)",  # separator lines like ----------
    re.MULTILINE
)
# Snyk CLI unicode symbols (checked separately to avoid regex encoding issues)
_SNYK_OUTPUT_SYMBOLS = ("\u2717 ", "\u2713 ", "\u2718 ", "\u2714 ")  # ✗ ✓ ✘ ✔
# Lines that look like flag/option descriptions (help text)
_RE_HELP_TEXT = re.compile(
    r"(^\s{2,}--?\w[\w\-]+(,\s*-\w)?\s{2,}|"  # --flag   description
    r"^\s{2,}-\w,\s+--\w)",                      # -f, --flag
    re.MULTILINE
)


def infer_language(block: str) -> Optional[str]:
    """
    Infer the language identifier for an unlabeled code block.

    Returns:
        str  — language identifier (e.g., "json", "bash", ...)
        ""   — confident "text" fallback
        None — skip (ambiguous, too short, or plain prose)
    """
    stripped = block.strip()
    if not stripped:
        return None

    # Early exit: PEM/certificate blocks — skip before any other checks
    if _RE_PEM_BLOCK.search(stripped):
        return None  # skip — PEM certificate or key block

    lines = stripped.split("\n")
    non_empty_lines = [l for l in lines if l.strip()]
    n_lines = len(non_empty_lines)

    # Skip very short blocks that are hard to classify (≤ 2 non-empty lines)
    if n_lines <= 2:
        # Allow JSON one-liners that are unambiguous
        if _is_valid_json(stripped):
            return "json"
        # Allow clear shell commands
        if _RE_SHELL_PROMPT.match(stripped) or _RE_SHELL_COMMANDS.search(stripped):
            # Only if it looks like a command, not a sentence
            first = non_empty_lines[0].strip()
            if first.startswith("$") or first.startswith("#!") or len(first) < 80:
                if not re.match(r"^[A-Z][a-z].{15,}$", first):
                    return "bash"
        return None  # too short to be confident

    # --- 1. JSON ---
    if _is_valid_json(stripped):
        return "json"
    # Partial JSON (invalid but clearly JSON-shaped)
    if _RE_JSON_START.match(stripped):
        # Check for enough JSON-like structure
        if stripped.count('"') >= 4 or stripped.count(":") >= 2:
            # Exclude YAML that starts with { but is actually HCL/other
            if not _RE_HCL.search(stripped):
                return "json"

    # --- 2. Dockerfile ---
    # FROM must look like a real image ref (node:18, ubuntu:22.04, ./path, scratch)
    # to avoid matching SQL "FROM users" patterns.
    has_docker_from = bool(_RE_DOCKERFILE_FROM.search(stripped))
    other_docker_cmds = _RE_DOCKERFILE_OTHER.findall(stripped)
    if has_docker_from or len(other_docker_cmds) >= 2:
        return "dockerfile"

    # --- 3. HCL (Terraform) ---
    if _RE_HCL.search(stripped):
        return "hcl"

    # --- 4. SQL ---
    sql_matches = _RE_SQL.findall(stripped)
    # SQL: require at least one keyword in a meaningful context
    if sql_matches and (n_lines >= 3 or len(stripped) > 40):
        return "sql"

    # --- Pre-5 guard: detect CLI help/usage output before checking for shell ---
    # Help-text blocks (flag tables) look like shell but are terminal output — skip them.
    if _RE_HELP_TEXT.search(stripped):
        # Confirm: if *most* non-empty lines are flag descriptions, skip
        help_lines = len(_RE_HELP_TEXT.findall(stripped))
        if help_lines >= max(1, n_lines // 3):
            return None  # skip — looks like CLI help output

    # --- 5. Shell / Bash ---
    if _RE_SHELL_PROMPT.search(stripped):
        return "bash"
    if _RE_SHELL_SHEBANG.match(stripped):
        return "bash"
    shell_hits = len(_RE_SHELL_COMMANDS.findall(stripped))
    if shell_hits >= 2:
        return "bash"
    # Single strong shell command with no prose feel
    if shell_hits == 1 and n_lines <= 6:
        first = non_empty_lines[0].strip()
        if not re.match(r"^[A-Z][a-z].{20,}$", first):
            return "bash"
    # Line-continuation backslash pattern — very common in shell commands
    continuation_lines = len(_RE_SHELL_CONTINUATION.findall(stripped))
    if continuation_lines >= 2:
        # Has multiple continuation lines — almost certainly a shell command
        return "bash"
    if continuation_lines >= 1 and shell_hits >= 1:
        return "bash"
    # Command-like lines with --flags and <placeholder> args (common in Snyk docs)
    flag_lines = len(re.findall(r"--\w[\w\-]+=?", stripped))
    executable_start = re.match(r"^\s*\.?/[\w\-]", stripped)  # starts with ./tool or /usr/bin/...
    if flag_lines >= 2 and executable_start:
        return "bash"

    # --- 6. XML / HTML ---
    # Use strict pattern that requires lowercase in tag name (excludes <PLACEHOLDER> patterns)
    xml_tags = _RE_XML_TAG.findall(stripped) + _RE_XML_SELFCLOSE.findall(stripped)
    has_xml_decl = bool(_RE_XML_DECL.search(stripped))
    if has_xml_decl or len(xml_tags) >= 3:
        return "xml"

    # --- 6.5. Rego (OPA) — must check before Go (both use 'package') ---
    if _RE_REGO.search(stripped):
        return "rego"

    # --- 7. Go ---
    # Exclude Rego-style 'package' that uses deny/allow rules
    if _RE_GO.search(stripped) and not _RE_REGO.search(stripped):
        return "go"

    # --- 8. Python ---
    if _RE_PYTHON.search(stripped):
        return "python"

    # --- 9. TypeScript (before JavaScript — superset) ---
    if _RE_TYPESCRIPT.search(stripped):
        return "typescript"

    # --- 10. JavaScript ---
    if _RE_JAVASCRIPT.search(stripped):
        return "javascript"

    # --- 10.5 Early-exit: error/log/test output (before YAML, since KV patterns can false-match) ---
    if _RE_ERROR_OUTPUT.search(stripped):
        return None  # skip — looks like test/runtime output
    if any(sym in stripped for sym in _SNYK_OUTPUT_SYMBOLS):
        return None  # skip — Snyk CLI output

    # --- 11. YAML ---
    # YAML: has key: value lines, optional leading ---, no braces dominating
    yaml_kv = len(_RE_YAML_KEY_VALUE.findall(stripped))
    yaml_dash = len(_RE_YAML_DASH_LIST.findall(stripped))
    has_yaml_start = bool(_RE_YAML_START.search(stripped))
    brace_chars = stripped.count("{") + stripped.count("}")

    if has_yaml_start:
        return "yaml"
    # Allow YAML with template expressions like ${{ secrets.FOO }} — count only structural braces
    # by subtracting double-brace pairs (Go template / GitHub Actions style)
    double_brace_pairs = len(re.findall(r"\{\{.*?\}\}", stripped))
    structural_braces = brace_chars - (double_brace_pairs * 4)
    if yaml_kv >= 2 and structural_braces < 4:
        return "yaml"
    if yaml_kv >= 1 and yaml_dash >= 1 and structural_braces < 4:
        return "yaml"

    # --- 12. Terminal output / plain prose heuristics → skip ---
    # Mostly prose sentences (complete English sentences with natural language patterns)
    long_prose_lines = len(re.findall(r"^[A-Z][a-z].{25,}$", stripped, re.MULTILINE))
    if long_prose_lines >= n_lines * 0.5:
        return None  # skip — mostly prose
    # Prose with leading spaces or markdown-style text
    indented_prose = len(re.findall(r"^\s{1,4}[A-Z][a-z].{20,}$", stripped, re.MULTILINE))
    if indented_prose >= max(1, n_lines * 0.4):
        return None  # skip — indented prose (e.g., PR template text)

    # File path listings (all lines look like /path/to/file.ext)
    path_lines = len(re.findall(r"^[/\\.][^\s]+\.\w{1,10}$", stripped, re.MULTILINE))
    if path_lines >= max(2, n_lines * 0.6):
        return None  # skip — looks like a directory/file listing

    # --- 13. Default fallback ---
    # Only apply if there's real structure (not all single-word lines)
    avg_line_len = sum(len(l) for l in non_empty_lines) / max(n_lines, 1)
    if avg_line_len < 5:
        return None  # too sparse to be confident

    return "text"


# ---------------------------------------------------------------------------
# Core processing
# ---------------------------------------------------------------------------

# Regex to find the opening fence of a code block.
# Captures: (indent)(fence_chars)(lang_tag)(rest_of_line)
# We use a state machine on lines rather than a single regex to handle nesting.
_FENCE_OPEN_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})(?P<lang>[^\s`~]*)(?P<rest>.*)$")


def process_content(content: str) -> Tuple[str, List[dict]]:
    """
    Scan content for unlabeled fenced code blocks and tag them.

    Returns:
        (new_content, changes)
        changes is a list of dicts with keys: line_no, inferred_lang (or None=skipped)
    """
    lines = content.split("\n")
    changes = []
    result_lines = []
    i = 0

    # State: are we inside a fenced block?
    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_indent = ""
    fence_lang = None
    block_start_line = 0
    block_lines_buf: list[str] = []

    while i < len(lines):
        line = lines[i]
        m = _FENCE_OPEN_RE.match(line)

        if not in_fence:
            if m:
                indent = m.group("indent")
                fence_chars = m.group("fence")
                lang = m.group("lang").strip()
                rest = m.group("rest")

                # Only triple+ backticks matter; tildes too
                char = fence_chars[0]
                length = len(fence_chars)

                in_fence = True
                fence_char = char
                fence_len = length
                fence_indent = indent
                fence_lang = lang
                block_start_line = i
                block_lines_buf = []

                result_lines.append(line)
            else:
                result_lines.append(line)
        else:
            # Check for closing fence: same char, >= same length, optional indent
            if m:
                close_char = m.group("fence")[0]
                close_len = len(m.group("fence"))
                close_lang = m.group("lang").strip()
                # A closing fence: same char, at least same length, no lang tag
                if close_char == fence_char and close_len >= fence_len and not close_lang:
                    # We have a complete block
                    if not fence_lang:
                        # Unlabeled — attempt to infer
                        block_body = "\n".join(block_lines_buf)
                        inferred = infer_language(block_body)
                        changes.append({
                            "line_no": block_start_line + 1,  # 1-indexed
                            "inferred_lang": inferred,
                        })
                        if inferred is not None and inferred != "":
                            # Patch the opening line in result_lines
                            open_idx = len(result_lines) - len(block_lines_buf) - 1
                            old_open = result_lines[open_idx]
                            new_open = fence_indent + fence_char * fence_len + inferred + m.group("rest")  # rest of opening line after fence+lang
                            # Actually reconstruct from stored fence info
                            # Get the original opening line's "rest" (after the fence chars)
                            orig_open = lines[block_start_line]
                            orig_m = _FENCE_OPEN_RE.match(orig_open)
                            orig_rest = orig_m.group("rest") if orig_m else ""
                            new_open = fence_indent + fence_char * fence_len + inferred + orig_rest
                            result_lines[open_idx] = new_open

                    result_lines.append(line)
                    in_fence = False
                    fence_lang = None
                    block_lines_buf = []
                else:
                    block_lines_buf.append(line)
                    result_lines.append(line)
            else:
                block_lines_buf.append(line)
                result_lines.append(line)

        i += 1

    # If file ends while still in a fence (unclosed block), just flush
    # (no change to result_lines since we already appended everything)

    return "\n".join(result_lines), changes


def process_file(filepath: str, dry_run: bool) -> dict:
    """Process a single Markdown file. Returns a stats dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    new_content, changes = process_content(original)

    tagged = [c for c in changes if c["inferred_lang"] is not None and c["inferred_lang"] != ""]
    skipped = [c for c in changes if c["inferred_lang"] is None or c["inferred_lang"] == ""]

    # Count by language
    lang_counts: dict[str, int] = defaultdict(int)
    for c in tagged:
        lang_counts[c["inferred_lang"]] += 1

    if not dry_run and new_content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return {
        "filepath": filepath,
        "total_unlabeled": len(changes),
        "tagged": len(tagged),
        "skipped": len(skipped),
        "lang_counts": dict(lang_counts),
        "modified": new_content != original,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Add language tags to unlabeled fenced code blocks in Markdown files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without modifying files.",
    )
    parser.add_argument(
        "--file",
        metavar="PATH",
        help="Process a single file instead of all docs/**/*.md files.",
    )
    args = parser.parse_args()

    # Resolve file list
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.file:
        if not os.path.isabs(args.file):
            target = os.path.join(os.getcwd(), args.file)
        else:
            target = args.file
        files = [target]
    else:
        docs_dir = os.path.join(repo_root, "docs")
        files = sorted(glob.glob(os.path.join(docs_dir, "**", "*.md"), recursive=True))

    if not files:
        print("No files found.", file=sys.stderr)
        sys.exit(1)

    mode_label = "[DRY RUN] " if args.dry_run else ""
    print(f"{mode_label}Processing {len(files)} file(s)...\n")

    total_unlabeled = 0
    total_tagged = 0
    total_skipped = 0
    total_files_modified = 0
    lang_totals: dict[str, int] = defaultdict(int)
    per_file_results = []

    for filepath in files:
        result = process_file(filepath, dry_run=args.dry_run)
        per_file_results.append(result)
        total_unlabeled += result["total_unlabeled"]
        total_tagged += result["tagged"]
        total_skipped += result["skipped"]
        if result["modified"]:
            total_files_modified += 1
        for lang, count in result["lang_counts"].items():
            lang_totals[lang] += count

    # Per-file detail for files that would change (only if few files or single file)
    if args.file or len(files) <= 5:
        print("=== Per-file detail ===")
        for r in per_file_results:
            if r["total_unlabeled"] > 0:
                rel = os.path.relpath(r["filepath"], repo_root)
                print(f"  {rel}")
                print(f"    unlabeled blocks : {r['total_unlabeled']}")
                print(f"    tagged           : {r['tagged']}")
                print(f"    skipped          : {r['skipped']}")
                if r["lang_counts"]:
                    for lang, cnt in sorted(r["lang_counts"].items()):
                        print(f"      {lang:15s} {cnt}")
                print()

    # Summary
    print("=" * 55)
    print(f"{'DRY RUN — ' if args.dry_run else ''}SUMMARY")
    print("=" * 55)
    print(f"  Files processed          : {len(files)}")
    print(f"  Files {'that would be ' if args.dry_run else ''}modified : {total_files_modified}")
    print(f"  Unlabeled blocks found   : {total_unlabeled}")
    print(f"  Blocks tagged            : {total_tagged}")
    print(f"  Blocks skipped (ambiguous): {total_skipped}")
    print()
    if lang_totals:
        print("  Language breakdown:")
        for lang, cnt in sorted(lang_totals.items(), key=lambda x: -x[1]):
            bar = "#" * min(cnt, 40)
            print(f"    {lang:15s} {cnt:5d}  {bar}")
    print("=" * 55)

    if args.dry_run:
        print("\nRe-run without --dry-run to apply changes.")
    else:
        print(f"\nDone. {total_tagged} blocks tagged across {total_files_modified} files.")


if __name__ == "__main__":
    main()
