# Spec: Profile Page Design

## Overview
Step 4 replaces the `GET /profile` stub with a real page that shows the logged-in user's account details and a high-level summary of their spending. The page displays name, email, and member-since date pulled from the `users` table, alongside aggregate stats (total expenses logged and total amount spent) derived from the `expenses` table. This gives users a personal home base inside the app and sets up the data access patterns that expense listing and editing steps will reuse.

## Depends on
- Step 01 — Database setup (`users` and `expenses` tables, `get_db()`)
- Step 02 — Registration (creates user rows)
- Step 03 — Login and Logout (session carries `user_id`; `@login_required` guard already on this route)

## Routes
- `GET /profile` — render profile page with user info and expense summary — logged-in only (stub already exists with `@login_required`; upgrade it)

## Database changes
No new tables or columns. Two new read-only helpers must be added to `database/db.py`:

- `get_user_by_id(user_id)` — returns the matching row from `users` (id, name, email, created_at). Used to display account details.
- `get_expense_summary(user_id)` — returns a dict with:
  - `total_count` — number of expense rows for this user
  - `total_amount` — sum of `amount` for this user (0.0 if no expenses)
  - `category_breakdown` — list of `(category, count, total)` tuples, ordered by total descending

## Templates
- **Create:** `templates/profile.html`
  - Extends `base.html`
  - Sections: account info card (name, email, member since), spending summary card (total count, total amount), category breakdown table
  - Page-specific styles live in `static/css/profile.css` (linked via `{% block head %}`)
- **Modify:** `templates/base.html`
  - Add a "Profile" nav link inside the `{% if session.get("user_id") %}` block, before "Sign out"

## Files to change
- `app.py` — replace stub body in `profile()` with calls to `get_user_by_id()` and `get_expense_summary()`, then render `profile.html`
- `database/db.py` — add `get_user_by_id()` and `get_expense_summary()`
- `templates/base.html` — add Profile nav link for authenticated users

## Files to create
- `templates/profile.html` — profile page template
- `static/css/profile.css` — page-specific styles

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with werkzeug (no password handling on this page — rule is N/A but must not expose `password_hash` to the template)
- Use CSS variables — never hardcode hex values in `profile.css`
- All templates extend `base.html`
- `get_expense_summary()` must use `COALESCE(SUM(amount), 0)` so total is 0.0 when no expenses exist, not NULL
- The route must call `abort(404)` if `get_user_by_id()` returns `None` (defensive; should never happen for a valid session)
- Format `created_at` as a human-readable date in the template using Jinja's `strptime`/slice — do not add Python `datetime` parsing to the route function
- Do not expose raw `password_hash` or `id` values in the template context

## Definition of done
- [ ] `GET /profile` while logged in renders the profile page without errors
- [ ] Profile page shows the correct name and email for the logged-in user
- [ ] Profile page shows the correct "Member since" date derived from `created_at`
- [ ] Profile page shows total number of expenses and total amount spent for the logged-in user
- [ ] Category breakdown is present and lists each category with count and total
- [ ] Profile page for the demo user (`demo@spendly.com`) shows 8 expenses matching the seeded data
- [ ] Visiting `GET /profile` while logged out redirects to `/login` with a flash message
- [ ] Nav shows a "Profile" link when logged in; link is absent when logged out
- [ ] Page uses only CSS variables — no hardcoded colour values in `profile.css`
