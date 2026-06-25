# Implementation Plan: 01 — DB Setup

## Context

This is the foundational step for the Spendly expense tracker. All future features (auth, profile, expense CRUD) depend on a working SQLite data layer. The spec (`db_setup.md`) requires replacing any stub in `database/db.py` with a full implementation providing `get_db()`, `init_db()`, and `seed_db()`, and wiring them into `app.py` startup.

**Current state:** Both `database/db.py` and `app.py` are already fully implemented and satisfy every requirement in the spec. The plan below documents what is in place and what to verify.

---

## Files to Change / Already Changed

| File | Status |
|---|---|
| `database/db.py` | Complete — all three functions implemented |
| `app.py` | Complete — imports and startup calls wired |

---

## Implementation Details

### `database/db.py`

**`get_db()`**
- Opens `spendly.db` relative to the project root via `os.path.join(os.path.dirname(__file__), '..', 'spendly.db')`
- Sets `conn.row_factory = sqlite3.Row` for dict-like row access
- Runs `PRAGMA foreign_keys = ON` on every connection
- Returns the open connection (caller is responsible for closing)

**`init_db()`**
- Calls `get_db()` then `executescript()` with two `CREATE TABLE IF NOT EXISTS` statements
- `users` table: `id` (PK autoincrement), `name` (NOT NULL), `email` (UNIQUE NOT NULL), `password_hash` (NOT NULL), `created_at` (DEFAULT datetime('now'))
- `expenses` table: `id` (PK autoincrement), `user_id` (FK → users.id, NOT NULL), `amount` (REAL NOT NULL), `category` (TEXT NOT NULL), `date` (TEXT NOT NULL), `description` (TEXT nullable), `created_at` (DEFAULT datetime('now'))
- Commits and closes; safe to call repeatedly

**`seed_db()`**
- Guards against duplication: `SELECT COUNT(*) FROM users` — returns early if > 0
- Inserts demo user: name=`Demo User`, email=`demo@spendly.com`, password hashed with `generate_password_hash("demo123")` from `werkzeug.security`
- Inserts 8 sample expenses via `executemany`, all linked to the demo user, covering all 7 categories (Food ×2, Transport, Bills, Health, Entertainment, Shopping, Other), dates in YYYY-MM-DD format spread across June 2026
- All inserts use `?` parameterized placeholders — no string formatting in SQL

### `app.py`

```python
from database.db import get_db, init_db, seed_db

with app.app_context():
    init_db()
    seed_db()
```

Called at module load time, before any request is served. Existing placeholder routes remain unchanged.

---

## Verification

```bash
cd CampusX_Claude_Code/expense-tracker

# 1. Start the app — should create spendly.db with no errors
python app.py

# 2. Verify database was created
ls -la spendly.db

# 3. Inspect schema and data
sqlite3 spendly.db ".tables"
sqlite3 spendly.db "SELECT id, name, email FROM users;"
sqlite3 spendly.db "SELECT id, user_id, category, amount, date FROM expenses;"

# 4. Verify idempotency — run app again, data should not duplicate
python app.py
sqlite3 spendly.db "SELECT COUNT(*) FROM users;"     -- should be 1
sqlite3 spendly.db "SELECT COUNT(*) FROM expenses;"  -- should be 8

# 5. Verify FK enforcement
sqlite3 spendly.db "PRAGMA foreign_keys;"            -- should be 1 after get_db()

# 6. Verify password is hashed (not plaintext)
sqlite3 spendly.db "SELECT password_hash FROM users LIMIT 1;"
```

Expected: app starts cleanly, 1 user, 8 expenses, no duplicates on re-run, FK pragma active, password stored as a bcrypt/werkzeug hash string.

---

## Definition of Done

- [ ] `spendly.db` created on first app startup
- [ ] `users` and `expenses` tables exist with correct schema and constraints
- [ ] Demo user present with hashed password
- [ ] 8 sample expenses across all 7 categories
- [ ] `seed_db()` is idempotent — no duplicates on repeated runs
- [ ] App starts without errors
- [ ] Foreign key enforcement active on every connection
- [ ] All SQL uses `?` parameterized queries
- [ ] Plan file saved to `.claude/plans/01_db_setup.md` in project
