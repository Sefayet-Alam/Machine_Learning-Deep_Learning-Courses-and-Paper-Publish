# Plan: Registration (Step 02)

## Context

Registration is the first authenticated entry point in Spendly. `POST /register` validates user input, hashes the password, and inserts a row into the `users` table. On success the user is redirected to `/login`. This step is already fully implemented — this plan documents the implementation and provides a verification checklist.

---

## Status: Implemented

All items from the spec definition of done are complete. No code changes are required.

---

## Files Changed

| File | Change |
|---|---|
| `database/db.py` | Added `register_user(name, email, password)` — hashes password with `werkzeug`, inserts into `users`, returns new `id`, raises `sqlite3.IntegrityError` on duplicate email |
| `app.py` | `register()` upgraded to handle `GET` (render form) and `POST` (validate, insert, redirect to `/login`) |
| `templates/register.html` | Form wired with `action="{{ url_for('register') }}"`, `method="post"`, `name` attributes on all inputs, flash message block |

---

## Validation Rules Implemented (`app.py`)

1. All fields non-empty → flash "All fields are required."
2. Password ≥ 8 characters → flash "Password must be at least 8 characters."
3. Passwords match → flash "Passwords do not match."
4. Email unique → catch `sqlite3.IntegrityError` → flash "An account with that email already exists."
5. On success → flash success, redirect to `url_for("login")`
6. On any failure → re-render form with `name` and `email` pre-filled

---

## Verification

```bash
# Start the app
python app.py

# Open http://localhost:5001/register and verify:
# 1. GET /register renders form with no errors
# 2. Submit all valid fields → redirected to /login with success flash
# 3. Submit mismatched passwords → form re-renders with error, no DB insert
# 4. Submit already-registered email → form re-renders with "already exists" error
# 5. Submit with any empty field → form re-renders with "All fields are required."
# 6. Inspect spendly.db → password_hash column contains a hash, not plaintext:
sqlite3 spendly.db "SELECT email, password_hash FROM users LIMIT 5;"
```

---

## Definition of Done

- [x] `GET /register` renders the registration form without errors
- [x] Submitting valid fields creates a new user and redirects to `/login`
- [x] Mismatched passwords re-renders form with error, no DB insert
- [x] Already-registered email re-renders form with error
- [x] Any empty field re-renders form with validation error
- [x] Password is stored as a hash — never plaintext
- [x] No duplicate user is created on repeated valid submissions with the same email
