#!/usr/bin/env python3
"""PreToolUse hook: block destructive Bash commands against protected files.

Reads the Bash tool-call JSON from stdin and refuses to run a command that
would delete, truncate, overwrite, or move away any of Spendly's critical
files (the SQLite database, env files, migrations).

A command is blocked when EITHER:
  * it uses a destructive verb (rm, unlink, truncate, shred, dd, mv) AND
    references a protected file, OR
  * it truncates/overwrites a protected file via output redirection (`> file`).

Exit codes:
  0  -> allow the command
  2  -> block the command (stderr is fed back to Claude)
"""
import json
import re
import sys

# Files Spendly must never lose. Patterns are matched as substrings/regex
# against the raw command string.
PROTECTED = [
    (r"spendly\.db", "spendly.db (main database)"),
    (r"[\w./-]*\.db\b", "a .db database file"),
    (r"[\w./-]*\.sqlite3?\b", "a SQLite database file"),
    (r"\.env\b", ".env file"),
    (r"migrations/", "migrations/ directory"),
]

# Destructive verbs (matched on word boundaries to avoid false positives).
DANGEROUS = [
    (r"\brm\b", "rm"),
    (r"\bunlink\b", "unlink"),
    (r"\btruncate\b", "truncate"),
    (r"\bshred\b", "shred"),
    (r"\bdd\b", "dd"),
    (r"\bmv\b", "mv"),
]


def find_protected(cmd):
    """Return the human label of the first protected file referenced, or None."""
    for pattern, label in PROTECTED:
        if re.search(pattern, cmd):
            return label
    return None


def find_dangerous_verb(cmd):
    """Return the first destructive verb present, or None."""
    for pattern, name in DANGEROUS:
        if re.search(pattern, cmd):
            return name
    return None


def truncates_protected(cmd):
    """Detect `> protected_file` (single >, i.e. overwrite/truncate)."""
    # Single '>' not preceded by another '>' (so '>>' append is excluded),
    # optionally with '|', followed by an optional quote and a protected path.
    for pattern, label in PROTECTED:
        redirect = re.compile(r"(?<!>)>\|?\s*['\"]?[\w./-]*" + pattern)
        if redirect.search(cmd):
            return label
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # Malformed payload: stay out of the way.

    cmd = data.get("tool_input", {}).get("command", "")
    if not cmd:
        sys.exit(0)

    protected = find_protected(cmd)

    # Case 1: destructive verb + protected file.
    if protected:
        verb = find_dangerous_verb(cmd)
        if verb:
            print(
                f"BLOCKED: '{verb}' would destroy {protected}. "
                "This file is protected — back it up or operate on a copy "
                "instead.",
                file=sys.stderr,
            )
            sys.exit(2)

    # Case 2: output redirection that truncates a protected file.
    truncated = truncates_protected(cmd)
    if truncated:
        print(
            f"BLOCKED: redirection ('>') would overwrite/truncate {truncated}. "
            "This file is protected — append ('>>') to a different file or use "
            "a copy.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
