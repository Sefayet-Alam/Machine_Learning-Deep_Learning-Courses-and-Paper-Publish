# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
venv/bin/python app.py        # runs on http://localhost:5001 with debug=True
```

Always use the project venv (`venv/`) — the system Python does not have Flask installed.

## Running tests

```bash
venv/bin/pytest               # all tests
venv/bin/pytest tests/test_foo.py::test_name  # single test
```

## Architecture

This is a **Flask + SQLite** expense tracker built as a step-by-step student project. The app is intentionally incomplete — many routes and the entire database layer are stubs that students implement one step at a time.

### Request flow

```
browser → app.py (route) → render_template(*.html) → templates/ + static/
```

`app.py` is the only Python entry point. There is no blueprint or application factory — all routes live in a single file.

### Database layer (`database/db.py`)

The file is a placeholder. Students implement three functions:
- `get_db()` — SQLite connection with `row_factory` and foreign keys enabled
- `init_db()` — `CREATE TABLE IF NOT EXISTS` for all tables
- `seed_db()` — sample data for development

### Templates

All templates extend `templates/base.html`, which provides the navbar, footer, and block slots (`title`, `head`, `content`, `scripts`).

- `landing.html` loads `static/css/landing.css` via `{% block head %}` — this file overrides hero styles from `style.css` and is only active on the landing page.
- Page-specific JS goes in `{% block scripts %}` rather than `static/js/main.js`.

### CSS conventions

`static/css/style.css` defines all CSS custom properties (`--ink`, `--accent`, `--paper`, `--font-display`, `--radius-*`, etc.) used across every page. Page-specific overrides go in separate CSS files (e.g. `landing.css`) loaded only by the relevant template.

### Git / .gitignore

The parent repo's `.gitignore` only tracks `.py`, `.md`, `.ipynb`, `.csv`, `.json`, `.xlsx` files. **HTML, CSS, and JS files are not committed.** Only `app.py` (and other `.py` files) are version-controlled. Keep this in mind when committing — stage by filename, not `git add -A`.

### Placeholder routes

Routes marked "coming in Step N" in `app.py` are not yet implemented. Do not remove the stubs; students fill them in as they progress through the curriculum.
