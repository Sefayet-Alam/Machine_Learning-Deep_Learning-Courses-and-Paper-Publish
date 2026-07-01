#!/usr/bin/env python3
"""PreToolUse hook: enforce Spendly's CLAUDE.md conventions on Write/Edit.

Reads the tool-call JSON from stdin and inspects the content that is about to
be written. It enforces three project rules:

  1. Templates (*.html) must use url_for() — never hardcode internal URLs.
  2. app.py must not contain inline DB logic — that belongs in database/db.py.
  3. requirements.txt must not gain new packages silently (warn, don't block).

Exit codes:
  0  -> allow the tool call
  2  -> block the tool call (stderr is fed back to Claude)
"""
import json
import re
import sys


def get_target(data):
    """Return (file_path, new_content) for the pending Write/Edit."""
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    # Write provides full content; Edit provides the replacement text.
    content = tool_input.get("content")
    if content is None:
        content = tool_input.get("new_string", "")
    return file_path, content or ""


def check_template_urls(content):
    """Block hardcoded internal URLs in href/action attributes."""
    violations = []
    # Match href="/..." or action='/...' where the value starts with a slash.
    pattern = re.compile(r"""(href|action)\s*=\s*["'](/[^"']*)["']""", re.IGNORECASE)
    for match in pattern.finditer(content):
        attr, url = match.group(1), match.group(2)
        # Allow Jinja-generated URLs and anchor-only links.
        if "{{" in url or url == "#":
            continue
        violations.append(f'{attr}="{url}"')
    return violations


def check_inline_db(content):
    """Block inline SQLite/DB logic inside app.py."""
    db_markers = [
        "import sqlite3",
        "sqlite3.connect",
        ".cursor(",
        ".execute(",
        ".executemany(",
        ".executescript(",
        ".commit(",
    ]
    return [marker for marker in db_markers if marker in content]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # Malformed payload: stay out of the way.

    file_path, content = get_target(data)
    if not file_path or not content:
        sys.exit(0)

    # Rule 1: templates must use url_for().
    if file_path.endswith(".html") and "templates/" in file_path:
        bad = check_template_urls(content)
        if bad:
            print(
                "BLOCKED: hardcoded internal URL(s) in template: "
                + ", ".join(bad)
                + "\nUse Jinja's url_for() instead, e.g. "
                "href=\"{{ url_for('login') }}\" (CLAUDE.md: never hardcode URLs).",
                file=sys.stderr,
            )
            sys.exit(2)

    # Rule 2: no inline DB logic in app.py.
    if file_path.endswith("app.py"):
        markers = check_inline_db(content)
        if markers:
            print(
                "BLOCKED: inline DB logic in app.py: "
                + ", ".join(markers)
                + "\nMove queries into database/db.py — routes only fetch data "
                "and render (CLAUDE.md: never put DB logic in route functions).",
                file=sys.stderr,
            )
            sys.exit(2)

    # Rule 3: warn (don't block) on new requirements.txt packages.
    if file_path.endswith("requirements.txt"):
        print(
            "WARNING: requirements.txt is being modified. CLAUDE.md forbids "
            "new pip packages without explicit approval — confirm this change "
            "was requested.",
            file=sys.stderr,
        )
        # Allow, but the warning is surfaced for review.
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
