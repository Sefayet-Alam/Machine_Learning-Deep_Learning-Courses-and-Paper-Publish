# Spec: Logout

## Overview
Step 3 wires up the logout flow so authenticated users can end their session cleanly. The route already exists in `app.py` and the nav in `base.html` already conditionally shows the "Sign out" link, so the implementation work is minimal. This step verifies the full round-trip (sign in → see nav → sign out → redirected → session cleared) and updates CLAUDE.md to mark the route as complete.

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`)
- Step 2 — Registration (session is set on register/login; logout clears it)

## Routes
- `GET /logout` — clears session, flashes confirmation, redirects to `/login` — public (no login required; calling it when already logged out is harmless)

## Database changes
No database changes.

## Templates
- **Create:** none
- **Modify:**
  - `templates/base.html` — nav is already correct; no changes needed
  - No other template changes required

## Files to change
- `app.py` — change the `logout` redirect target from `url_for("landing")` to `url_for("login")` so users land on the sign-in page after signing out
- `CLAUDE.md` — update `GET /logout` row from `Stub — Step 3` to `Implemented`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (N/A for this step — no DB writes)
- Passwords hashed with werkzeug (N/A for this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Do NOT add `@login_required` to `/logout` — calling it when already logged out must be safe and silent

## Definition of done
- [ ] Visiting `/logout` while logged in clears the session (subsequent requests to protected routes redirect to login)
- [ ] A "You have been signed out." flash message appears on the login page after logout
- [ ] After logout, the nav shows "Sign in" and "Get started" (not the user name or "Sign out")
- [ ] Visiting `/logout` while already logged out does not raise an error — it silently redirects to `/login`
- [ ] `CLAUDE.md` route table shows `GET /logout` as Implemented
