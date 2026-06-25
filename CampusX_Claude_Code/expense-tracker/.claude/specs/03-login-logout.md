# Spec: Login and Logout

## Overview
Step 3 completes the authentication round-trip for Spendly. The `POST /login` route and `GET /logout` stub both exist in `app.py` but are not fully correct: login lacks session hardening and redirect-after-login to a dashboard, and logout redirects to the landing page rather than the login page. This step fixes both routes, verifies the nav responds correctly to session state, and marks them complete in `CLAUDE.md`. After this step users can sign in, see a personalised nav, and sign out cleanly.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`, `get_user_by_email()`)
- Step 02 — Registration (produces rows in `users` for login to find)

## Routes
- `GET /login` — render login form — public (already exists; no structural change needed)
- `POST /login` — validate credentials, set session, redirect to `GET /` — public (already exists; redirect target confirmed as landing for now)
- `GET /logout` — clear session, flash message, redirect to `url_for("login")` — public (currently redirects to landing — fix the redirect target)

## Database changes
No new tables or columns. `get_user_by_email()` already exists in `database/db.py` and covers all lookup needs.

## Templates
- **Modify:** `templates/base.html`
  - Verify nav conditionally shows `Sign in` / `Get started` when no session, and user name + `Sign out` when `session.user_name` is set — fix if not already working
- **Create:** none

## Files to change
- `app.py`
  - `logout()` — change `url_for("landing")` to `url_for("login")`
  - `login()` POST branch — ensure `session.clear()` is called before setting new session keys (already done; confirm no regression)
- `CLAUDE.md` — update `GET /login` and `GET /logout` rows from current status to `Implemented`

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with werkzeug — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Do NOT add `@login_required` to `/logout` — calling it when already logged out must be safe (session.clear() on an empty session is a no-op)
- `session.clear()` must be called before setting new keys in `/login` POST to prevent session fixation
- Flash messages use the `"success"` category on success and `"error"` on failure

## Definition of done
- [ ] `GET /login` renders the login form without errors when not logged in
- [ ] Submitting valid credentials (e.g. `demo@spendly.com` / `demo123`) sets `session["user_id"]` and `session["user_name"]` and redirects to `/`
- [ ] Submitting an unknown email or wrong password re-renders the form with "Invalid email or password." error — no session is set
- [ ] Submitting with empty email or password re-renders the form with a validation error
- [ ] After login, `base.html` nav shows the user's name and a "Sign out" link
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/login` with "You have been signed out." flash
- [ ] After logout, the nav shows "Sign in" and "Get started" — user name and "Sign out" are gone
- [ ] Visiting `/logout` while already logged out does not raise an error — redirects silently to `/login`
- [ ] `CLAUDE.md` route table shows `GET /login` and `GET /logout` as `Implemented`
