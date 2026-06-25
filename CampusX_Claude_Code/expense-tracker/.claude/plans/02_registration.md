# Plan: Registration & Sign-In Services (`plans/02_registration.md`)

## Context

Registration (`POST /register`) is fully implemented and working. The login route exists but its POST handler is a stub — it renders the form without authenticating. Logout is a string stub. No `login_required` protection exists for guarded routes. This plan completes the auth layer so users can register, sign in, and sign out, with protected routes enforced.

---

## Files to Change

| File | What changes |
|---|---|
| `database/db.py` | Add `get_user_by_email(email)` |
| `app.py` | Add imports, `login_required` decorator, complete `login` POST, implement `logout` |
| `templates/base.html` | Conditional navbar (logged-in vs guest) |
| `tests/conftest.py` | New — pytest fixtures with isolated temp DB |
| `tests/test_auth.py` | New — full auth test suite |

---

## Step 1 — `database/db.py`: Add `get_user_by_email()`

Add after `register_user()`, before `seed_db()`:

```python
def get_user_by_email(email: str):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()
```

Returns a `sqlite3.Row` (columns accessible by name) or `None`. Matches the open/close pattern of `register_user()`.

---

## Step 2 — `app.py`: Imports

```python
from functools import wraps
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, register_user, get_user_by_email
```

---

## Step 3 — `app.py`: `login_required` Decorator

Place after imports, before any route:

```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access that page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
```

Apply to protected routes by stacking `@login_required` below `@app.route(...)`.

---

## Step 4 — `app.py`: Complete `login` Route

Replace the stub:

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="Email and password are required.")

    user = get_user_by_email(email)

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session.clear()
    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]

    flash("Welcome back, {}!".format(user["name"]), "success")
    return redirect(url_for("landing"))
```

Key decisions:
- Generic error for both "no user" and "wrong password" — prevents user enumeration.
- `session.clear()` before setting keys — prevents session fixation.
- Uses `render_template(..., error=...)` (not flash) — `login.html` already has a `{% if error %}` div.
- Stores `user_name` in session so the navbar can display it without a DB round-trip.

---

## Step 5 — `app.py`: Implement `logout`

Replace the stub:

```python
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("landing"))
```

No `@login_required` — logging out while already logged out should silently redirect.

---

## Step 6 — `templates/base.html`: Conditional Navbar

Replace the `.nav-links` div:

```html
<div class="nav-links">
    {% if session.get("user_id") %}
        <span class="nav-user-name">{{ session.get("user_name", "") }}</span>
        <a href="{{ url_for('logout') }}" class="nav-cta">Sign out</a>
    {% else %}
        <a href="{{ url_for('login') }}">Sign in</a>
        <a href="{{ url_for('register') }}" class="nav-cta">Get started</a>
    {% endif %}
</div>
```

`session` is available in all Jinja2 templates automatically. Also fix any hardcoded `/terms` and `/privacy` footer hrefs to use `url_for('terms')` and `url_for('privacy')`.

---

## Step 7 — Tests

### `tests/conftest.py`

```python
import pytest, tempfile, os
from app import app as flask_app
import database.db as db_module
from database.db import init_db

@pytest.fixture(scope="function")
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    db_module.DB_PATH = db_path
    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test-secret"})
    with flask_app.app_context():
        init_db()
    yield flask_app
    os.unlink(db_path)

@pytest.fixture()
def client(app):
    return app.test_client()
```

Each test gets a fresh isolated SQLite file — no shared state between tests.

### `tests/test_auth.py` — Scenarios to Cover

**Registration (`POST /register`):**
- Valid new user → 302 to `/login`, success flash
- Missing any field → 200, flash "All fields are required."
- Password < 8 chars → 200, flash "Password must be at least 8 characters."
- Passwords mismatch → 200, flash "Passwords do not match."
- Duplicate email → 200, flash "An account with that email already exists."
- Successful registration sets `session["user_id"]`

**Login (`POST /login`):**
- Valid credentials → 302 to `/`, flash "Welcome back, Name!"
- Wrong password → 200, inline error "Invalid email or password."
- Unknown email → 200, inline error "Invalid email or password."
- Empty fields → 200, inline error "Email and password are required."
- Sets `session["user_id"]` and `session["user_name"]` on success
- Login is case-insensitive on email

**Logout (`GET /logout`):**
- Clears `session["user_id"]` after login
- Redirects to `/`
- Gracefully handles logout when not logged in (no error)

**Navbar (integration):**
- Unauthenticated GET `/` → contains "Sign in" link
- Authenticated GET `/` → contains "Sign out", not "Get started"

**`login_required` decorator:**
- `GET /profile` without session → 302 to `/login` with error flash
- `GET /profile` with valid session → not redirected to login

---

## Verification

```bash
# Run full test suite
pytest

# Run just auth tests
pytest tests/test_auth.py -v

# Manual smoke test
python app.py
# Then in browser at http://localhost:5001:
# 1. Visit / — see "Sign in" and "Get started" in nav
# 2. Register a new account — flash success, land on /login
# 3. Log in with those credentials — flash "Welcome back, Name!", land on /
# 4. Navbar shows name + "Sign out"
# 5. Click "Sign out" — flash "You have been signed out."
# 6. Visit /profile while logged out → redirected to /login with error
# 7. Try wrong password on login → inline error (not flash)
# 8. Try duplicate email on register → inline error on form
```
